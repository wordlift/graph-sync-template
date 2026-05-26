from __future__ import annotations

import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


OLD_PACKAGE = "acme_kg"
SEED_FILES = (
    "exports.toml.j2",
    "mappings/default.yarrrml.j2",
    "templates/20_organization.ttl.j2",
    "templates/20_website.ttl.j2",
    "templates/40_organization_postal_address.ttl.j2",
)


@dataclass(frozen=True)
class ProjectNames:
    distribution_name: str
    runtime_package: str


def load_context(context_path: Path) -> dict[str, object]:
    raw_context = context_path.read_text(encoding="utf-8")
    context_path.unlink(missing_ok=True)
    return json.loads(raw_context)


def context_string(context: dict[str, object], key: str) -> str:
    value = context.get(key, "")
    if not isinstance(value, str):
        raise SystemExit(f"Invalid Copier context value for {key}: expected string")
    return value


def context_bool(context: dict[str, object], key: str) -> bool:
    value = context.get(key)
    if not isinstance(value, bool):
        raise SystemExit(f"Invalid Copier context value for {key}: expected boolean")
    return value


def context_profiles(context: dict[str, object]) -> list[str]:
    value = context.get("profiles")
    if not isinstance(value, list) or not value:
        raise SystemExit("Invalid Copier context value for profiles: expected non-empty list")
    if not all(isinstance(profile, str) and profile for profile in value):
        raise SystemExit("Invalid Copier context value for profiles: expected string names")
    return value


def clean_api_key(raw_api_key: str) -> str:
    api_key = raw_api_key.strip()
    if not api_key:
        raise SystemExit("WordLift API key is required.")
    if "\n" in api_key or "\r" in api_key:
        raise SystemExit(
            "WordLift API key must be a single line. Please check the key and run generation again."
        )
    return api_key


def scaffold_profiles(profiles: list[str]) -> None:
    default_profile_dir = Path("profiles/default")

    for profile in profiles:
        profile_dir = Path("profiles") / profile
        (profile_dir / "mappings").mkdir(parents=True, exist_ok=True)
        (profile_dir / "templates").mkdir(parents=True, exist_ok=True)
        (profile_dir / "postprocessors").mkdir(parents=True, exist_ok=True)

        if profile == "default":
            continue

        for rel_path in SEED_FILES:
            src = default_profile_dir / rel_path
            dst = profile_dir / rel_path
            if dst.exists():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def write_env(api_key: str, sheets_service_account: str) -> None:
    escaped_service_account = sheets_service_account.replace("\n", "\\n")
    content = [
        f"WORDLIFT_API_KEY={api_key}",
        f"SHEETS_SERVICE_ACCOUNT={escaped_service_account}",
        "YOUTUBE_API_KEY=",
        "",
    ]
    Path(".env").write_text("\n".join(content), encoding="utf-8")


def normalize_slug(raw: str) -> str:
    normalized = re.sub(r"[^a-z0-9._-]+", "-", raw.lower())
    normalized = re.sub(r"[-_.]+", "-", normalized).strip("-")
    return normalized


def distribution_name_from_slug(raw: str) -> str:
    slug = normalize_slug(raw)
    if not slug:
        slug = "project"
    if slug.startswith("graph-sync-"):
        return slug
    return f"graph-sync-{slug}"


def runtime_package_from_distribution_name(distribution_name: str) -> str:
    package_name = distribution_name.replace("-", "_")
    package_name = re.sub(r"[^a-z0-9_]+", "_", package_name.lower()).strip("_")
    if not package_name:
        package_name = "graph_sync_project"
    if package_name[0].isdigit():
        package_name = f"pkg_{package_name}"
    return package_name


def project_names_from_slug(raw: str) -> ProjectNames:
    distribution_name = distribution_name_from_slug(raw)
    return ProjectNames(
        distribution_name=distribution_name,
        runtime_package=runtime_package_from_distribution_name(distribution_name),
    )


def update_project_name(distribution_name: str) -> None:
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        return

    pyproject_content = pyproject_path.read_text(encoding="utf-8")
    pyproject_content = re.sub(
        r'(?m)^name\s*=\s*"[^"]*"\s*$',
        f'name = "{distribution_name}"',
        pyproject_content,
        count=1,
    )
    pyproject_path.write_text(pyproject_content, encoding="utf-8")


def slug_from_account_url(account_url: str) -> str:
    parsed = urlparse(account_url)
    host = parsed.netloc or ""
    if host.startswith("www."):
        host = host[4:]
    source = f"{host}{parsed.path}" if host else account_url
    return normalize_slug(source)


def slug_from_dataset_uri(dataset_uri: str) -> str:
    path = urlparse(dataset_uri).path
    slug = normalize_slug(path)
    if slug:
        return slug
    return normalize_slug(dataset_uri)


def project_names_from_account_payload(
    payload: dict[str, object],
    fallback_project_dir: str,
) -> ProjectNames:
    account_url = str(payload.get("url", "")).strip()
    if account_url:
        return project_names_from_slug(slug_from_account_url(account_url))

    dataset_uri = str(payload.get("datasetUri", "")).strip()
    if dataset_uri:
        return project_names_from_slug(slug_from_dataset_uri(dataset_uri))

    print(
        "WordLift API key validation succeeded but account url and datasetUri are missing in response.",
        file=sys.stderr,
    )
    return project_names_from_slug(fallback_project_dir)


def derive_project_names(
    api_key: str,
    validate_api_key: bool,
    fallback_project_dir: str,
) -> ProjectNames:
    if not validate_api_key:
        return project_names_from_slug(fallback_project_dir)

    request = Request(
        "https://api.wordlift.io/accounts/me",
        headers={
            "Authorization": f"Key {api_key}",
            "Accept": "application/vnd.wordlift.account-info.v2+json",
            "User-Agent": "wordlift-key-check/1.0",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=10) as response:
            if 200 <= response.status < 300:
                payload = json.loads(response.read().decode("utf-8"))
                return project_names_from_account_payload(payload, fallback_project_dir)

            print(
                f"Unexpected response while validating WordLift API key: HTTP {response.status}",
                file=sys.stderr,
            )
            raise SystemExit(1)
    except HTTPError as exc:
        if exc.code in (401, 403):
            print(
                "WordLift API key validation failed (unauthorized). "
                "Please check the key and run generation again.",
                file=sys.stderr,
            )
        else:
            body = exc.read().decode("utf-8", errors="replace")[:300]
            print(
                f"WordLift API key validation failed: HTTP {exc.code}. {body}",
                file=sys.stderr,
            )
        raise SystemExit(1)
    except URLError as exc:
        print(
            f"Warning: could not validate WordLift API key due to network/API error: {exc}",
            file=sys.stderr,
        )
        return project_names_from_slug(fallback_project_dir)
    except ValueError as exc:
        print(
            "WordLift API key validation failed before the request. "
            "Please check the key and run generation again.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Warning: unexpected error during API key validation: {exc}", file=sys.stderr)
        return project_names_from_slug(fallback_project_dir)


def rename_runtime_package(project_names: ProjectNames) -> None:
    new_package = project_names.runtime_package
    replacements = {
        OLD_PACKAGE: new_package,
        "__GRAPH_SYNC_PROJECT_PACKAGE__": project_names.distribution_name,
    }

    old_dir = Path("src") / OLD_PACKAGE
    new_dir = Path("src") / new_package
    if old_dir.exists() and new_package != OLD_PACKAGE:
        if new_dir.exists():
            raise SystemExit(f"Cannot rename package: destination already exists: {new_dir}")
        shutil.move(str(old_dir), str(new_dir))

    suffixes = {".py", ".md", ".toml", ".yml", ".j2"}
    for file_path in Path(".").rglob("*"):
        if not file_path.is_file() or file_path.suffix not in suffixes:
            continue
        content = file_path.read_text(encoding="utf-8")
        updated_content = content
        for old_value, new_value in replacements.items():
            updated_content = updated_content.replace(old_value, new_value)
        if updated_content == content:
            continue
        file_path.write_text(updated_content, encoding="utf-8")


def cleanup_copier_answers() -> None:
    Path(".copier-answers.yml").unlink(missing_ok=True)


def main(argv: list[str]) -> int:
    context_path = Path(argv[1]) if len(argv) > 1 else Path(".copier-tasks/context.json")
    helper_dir = context_path.parent
    project_names = project_names_from_slug(Path.cwd().name)

    try:
        context = load_context(context_path)
        api_key = clean_api_key(context_string(context, "api_key"))
        scaffold_profiles(context_profiles(context))
        write_env(
            api_key,
            context_string(context, "sheets_service_account"),
        )
        project_names = derive_project_names(
            api_key,
            context_bool(context, "validate_api_key"),
            Path.cwd().name,
        )
        update_project_name(project_names.distribution_name)
        rename_runtime_package(project_names)
        cleanup_copier_answers()
    finally:
        shutil.rmtree(helper_dir, ignore_errors=True)

    print("Graph Sync project post-copy setup completed.")
    print(f"Project package: {project_names.distribution_name}")
    print(f"Runtime module: {project_names.runtime_package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
