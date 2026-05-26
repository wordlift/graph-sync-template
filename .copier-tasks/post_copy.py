from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


FALLBACK_PACKAGE = "acme_graph_sync"
OLD_PACKAGE = "acme_kg"
SEED_FILES = (
    "exports.toml.j2",
    "mappings/default.yarrrml.j2",
    "templates/20_organization.ttl.j2",
    "templates/20_website.ttl.j2",
    "templates/40_organization_postal_address.ttl.j2",
)


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


def normalize_project_name(raw: str) -> str:
    normalized = re.sub(r"[^a-z0-9._-]+", "-", raw.lower())
    normalized = re.sub(r"[-_.]+", "-", normalized).strip("-")
    if not normalized:
        normalized = "graph-sync-project"
    if normalized[0].isdigit():
        normalized = f"proj-{normalized}"
    return normalized


def update_project_name() -> None:
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        return

    project_dir_name = Path.cwd().name
    pyproject_content = pyproject_path.read_text(encoding="utf-8")
    pyproject_content = re.sub(
        r'(?m)^name\s*=\s*"[^"]*"\s*$',
        f'name = "{normalize_project_name(project_dir_name)}"',
        pyproject_content,
        count=1,
    )
    pyproject_path.write_text(pyproject_content, encoding="utf-8")


def package_from_dataset_uri(dataset_uri: str) -> str:
    path = urlparse(dataset_uri).path
    parts = [p for p in re.split(r"[^a-zA-Z0-9]+", path.lower()) if p]
    base = "_".join(parts) if parts else "wordlift"
    if base[0].isdigit():
        base = f"pkg_{base}"
    return f"{base}_graph_sync"


def derive_runtime_package(api_key: str, validate_api_key: bool) -> str:
    if not validate_api_key:
        return FALLBACK_PACKAGE

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
                dataset_uri = str(payload.get("datasetUri", "")).strip()
                if not dataset_uri:
                    print(
                        "WordLift API key validation succeeded but datasetUri is missing in response.",
                        file=sys.stderr,
                    )
                    raise SystemExit(1)
                return package_from_dataset_uri(dataset_uri)

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
        return FALLBACK_PACKAGE
    except ValueError as exc:
        print(
            "WordLift API key validation failed before the request. "
            "Please check the key and run generation again.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc
    except Exception as exc:
        print(f"Warning: unexpected error during API key validation: {exc}", file=sys.stderr)
        return FALLBACK_PACKAGE


def rename_runtime_package(new_package: str) -> None:
    if new_package == OLD_PACKAGE:
        return

    old_dir = Path("src") / OLD_PACKAGE
    new_dir = Path("src") / new_package
    if old_dir.exists():
        if new_dir.exists():
            raise SystemExit(f"Cannot rename package: destination already exists: {new_dir}")
        shutil.move(str(old_dir), str(new_dir))

    suffixes = {".py", ".md", ".toml", ".yml", ".j2"}
    for file_path in Path(".").rglob("*"):
        if not file_path.is_file() or file_path.suffix not in suffixes:
            continue
        content = file_path.read_text(encoding="utf-8")
        if OLD_PACKAGE not in content:
            continue
        file_path.write_text(content.replace(OLD_PACKAGE, new_package), encoding="utf-8")


def cleanup_copier_answers() -> None:
    Path(".copier-answers.yml").unlink(missing_ok=True)


def main(argv: list[str]) -> int:
    context_path = Path(argv[1]) if len(argv) > 1 else Path(".copier-tasks/context.json")
    helper_dir = context_path.parent
    package_name = FALLBACK_PACKAGE

    try:
        context = load_context(context_path)
        api_key = clean_api_key(context_string(context, "api_key"))
        scaffold_profiles(context_profiles(context))
        write_env(
            api_key,
            context_string(context, "sheets_service_account"),
        )
        update_project_name()
        package_name = derive_runtime_package(
            api_key,
            context_bool(context, "validate_api_key"),
        )
        rename_runtime_package(package_name)
        cleanup_copier_answers()
    finally:
        shutil.rmtree(helper_dir, ignore_errors=True)

    print(f"Graph Sync project post-copy setup completed. Runtime package: {package_name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
