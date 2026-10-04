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

ROUTES = ["/", "/add", "/calendar", "/account", "/register", "/login", "/account/details"]

TEST = r'''
import sys
from pathlib import Path
sys.path.insert(0, ".")
from app import app
client = app.test_client()
routes = [r for r in sys.argv[1:]]
source = Path("app.py").read_text()
if "init_db_command" in source:
    result = app.test_cli_runner().invoke(args=["init-db"])
    assert "Database created." in result.output, result.output
HX = {"HX-Request": "true"}
if 'route("/register"' in source:
    form = {"email": "sam@school.com", "password": "short", "confirm": "short"}
    assert b"at least 8" in client.post("/register", data=form, headers=HX).data
    form = {"email": "Sam@School.com ", "password": "password1", "confirm": "password1"}
    response = client.post("/register", data=form, headers=HX)
    assert response.status_code == 200, response.status_code
    form = {"email": "sam@school.com", "password": "password1", "confirm": "password1"}
    if 'route("/logout"' in source:
        client.post("/logout", headers=HX)
    assert b"already registered" in client.post("/register", data=form, headers=HX).data
if 'route("/login"' in source:
    bad = client.post("/login", data={"email": "sam@school.com", "password": "wrong"}, headers=HX)
    assert b"Incorrect" in bad.data
    good = client.post("/login", data={"email": "sam@school.com", "password": "password1"}, headers=HX)
    assert good.headers.get("HX-Push-Url") == "/", good.headers
    page = client.get("/", headers=HX).data
    if b"current_user.is_authenticated" in Path("templates/nav.html").read_bytes():
        assert b"Logout" in page and b"Register" not in page, "menu not showing logged-in links"
        client.post("/logout", headers=HX)
        page = client.get("/", headers=HX).data
        assert b"Register" in page and b"Logout" not in page, "menu not showing logged-out links"
if 'route("/account/details"' in source:
    client.post("/login", data={"email": "sam@school.com", "password": "password1"}, headers=HX)
    page = client.get("/account/details", headers=HX).data
    assert b"first_name" in page, "set details form missing"
    if 'request.method == "GET"' in source.split('def set_details')[1].split('@app.route')[0]:
        bad = client.post("/account/details", data={"first_name": "", "last_name": "Lee"}, headers=HX)
        assert b"first and last name" in bad.data
        good = client.post("/account/details", data={"first_name": "Sam", "last_name": "Lee"}, headers=HX)
        assert b"Sam" in good.data and b"Lee" in good.data, "names not saved"
        assert b"Sam" in client.get("/account", headers=HX).data
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
            routes = [r for r in ROUTES if r == "/" or f'route("{r}"' in app_text]
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
