from pathlib import Path
import shutil
import subprocess


def test_template_smoke_script_passes() -> None:
    script = Path("scripts/smoke_render_template.sh")
    assert script.exists()

    copier_bin = shutil.which("copier")
    assert copier_bin is not None, "copier must be installed to run template smoke test"

    subprocess.run([str(script)], check=True)
