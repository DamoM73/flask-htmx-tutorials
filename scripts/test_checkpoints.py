"""Run every checkpoint in the student zip and check its pages load.

For each lesson checkpoint, the files are copied to a temporary folder and
the app is loaded with Flask's test client in a separate Python process.
Each route is requested twice: once as a normal browser request and once
as an HTMX request (with the HX-Request header). The script reports PASS
or FAIL for each checkpoint, with the end of the traceback for a failure.

Needs Flask (and, for later lessons, Flask-Login, Plotly and pandas).
Run from the repo root: python scripts/test_checkpoints.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_zip import checkpoints  # noqa: E402

ROUTES = ["/", "/add", "/calendar", "/account"]

TEST = r'''
import sys
from pathlib import Path
sys.path.insert(0, ".")
from app import app
client = app.test_client()
routes = [r for r in sys.argv[1:]]
for route in routes:
    full = client.get(route)
    assert full.status_code == 200, f"{route} returned {full.status_code}"
    if Path("templates/fragment.html").exists() or "render_page" in Path("app.py").read_text():
        part = client.get(route, headers={"HX-Request": "true"})
        assert part.status_code == 200, f"{route} (HTMX) returned {part.status_code}"
        assert b"<!doctype html>" not in part.data, f"{route} (HTMX) sent a whole page"
print("ok", len(routes), "route(s)")
'''


def main():
    failed = 0
    for lesson, files in checkpoints():
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for path, source in files.items():
                target = folder / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            app_text = (folder / "app.py").read_text()
            routes = [r for r in ROUTES if r == "/" or f'route("{r}")' in app_text]
            result = subprocess.run([sys.executable, "-c", TEST, *routes], cwd=folder,
                                    capture_output=True, text=True)
            if result.returncode == 0:
                print(f"PASS {lesson}: {result.stdout.strip()}")
            else:
                failed += 1
                print(f"FAIL {lesson}")
                print("\n".join(result.stderr.strip().splitlines()[-6:]))
    print(f"{failed} checkpoint(s) failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
