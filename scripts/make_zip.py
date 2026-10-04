"""Build the student download: StudyM8's code at the end of each lesson.

Each lesson's code lives in docs/examples/<section>/<lesson>/stepNN/<path>,
where a step folder only holds the files that changed in that step
(for example step02/templates/base.html). For every lesson, the zip gets
the latest version of each file, carried forward from earlier lessons, so
every folder is a checkpoint of the whole app at the end of that lesson:

    studym8/shell/05_htmx_links/templates/base.html

Files listed in REMOVED are deleted from the checkpoints from that lesson
on, because the lesson tells students to delete them.

Run from the repo root: python scripts/make_zip.py
"""

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "docs" / "examples"
ZIP_PATH = ROOT / "docs" / "downloads" / "studym8_checkpoints.zip"

# Lessons in the order they are built. Each starts from the end of the one before.
CHECKPOINTS = [
    "shell/01_first_flask_app",
    "shell/02_html_templates",
    "shell/03_page_shell",
    "shell/04_pico",
    "shell/05_htmx_links",
    "shell/06_page_titles",
    "shell/07_active_link",
]

# Files a lesson tells students to delete.
REMOVED = {
    "shell/03_page_shell": ["templates/index.html"],
}


def checkpoints():
    """Yield (lesson, {path: file}) for each lesson, carrying files forward."""
    files = {}
    for lesson in CHECKPOINTS:
        folder = EXAMPLES / lesson
        if not folder.exists():
            print(f"WARNING: missing {folder}")
            continue
        for step in sorted(p for p in folder.iterdir() if p.is_dir() and p.name.startswith("step")):
            for source in sorted(step.rglob("*")):
                if source.is_file():
                    files[source.relative_to(step).as_posix()] = source
        for path in REMOVED.get(lesson, []):
            files.pop(path, None)
        yield lesson, dict(files)


def main():
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for lesson, files in checkpoints():
            for path, source in sorted(files.items()):
                archive.write(source, f"studym8/{lesson}/{path}")
                count += 1
    print(f"Wrote {count} file(s) to {ZIP_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
