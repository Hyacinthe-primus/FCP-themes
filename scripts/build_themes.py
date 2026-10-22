#!/usr/bin/env python3
"""Validate the themes and generate everything derived from them.

    python scripts/build_themes.py              validate, then rebuild themes.json,
                                                the .fctheme archives and the README gallery
    python scripts/build_themes.py --check      validate only, write nothing
    python scripts/build_themes.py --pack NAME  build themes/NAME.fctheme only (to test a theme locally)

Only the standard library is used. The CI workflow runs this on every push to main.
"""
import argparse
import configparser
import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = ROOT / "themes"
INDEX_FILE = ROOT / "themes.json"
README_FILE = ROOT / "README.md"

REPO_URL = "https://github.com/Hyacinthe-primus/fcp-themes"
ID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, REPO_URL)

TEMPLATE = "theme_template"
STYLE_SUFFIXES = {".qss", ".css"}
REQUIRED_FILES = {
    "style.qss", "advanced_conversions.qss", "advanced_group.qss", "contact_links.css",
    "dashboard.qss", "lang_scroll.qss", "scrollbar.qss", "settings.qss",
    "templates.qss", "terms.qss", "terms_html.css",
}
REQUIRED_FIELDS = ("name", "author", "description", "kind")
KINDS = {"dark", "light"}
FOLDER_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
GALLERY_START = "<!-- themes:start -->"
GALLERY_END = "<!-- themes:end -->"


def is_style_file(path):
    return path.is_file() and path.suffix.lower() in STYLE_SUFFIXES


def discover():
    return sorted(
        p for p in THEMES_DIR.iterdir()
        if p.is_dir() and p.name != TEMPLATE and not p.name.startswith(".")
    )


def read_metadata(folder):
    parser = configparser.ConfigParser(interpolation=None)
    parser.read(folder / "metadata.ini", encoding="utf-8-sig")
    if not parser.has_section("theme"):
        return {}
    return {k: v.strip() for k, v in parser["theme"].items()}


def find_screenshot(folder):
    wanted = {f"{folder.name}.png".lower(), f"{folder.name}_preview.png".lower()}
    for p in sorted(folder.iterdir()):
        if p.name.lower() in wanted:
            return p.name
    return None


def widget_files(folder):
    return sorted(p.name for p in folder.iterdir() if is_style_file(p))


def has_balanced_braces(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return text.count("{") == text.count("}")


def validate(folder):
    errors, warnings = [], []
    name = folder.name

    if not FOLDER_NAME.match(name):
        errors.append(f"{name}: folder name may only use letters, digits, _ and -")

    meta_file = folder / "metadata.ini"
    if not meta_file.is_file():
        return [f"{name}: metadata.ini is missing"], warnings
    meta = read_metadata(folder)
    if not meta:
        return [f"{name}: metadata.ini needs a [theme] section"], warnings

    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            errors.append(f"{name}: metadata.ini has no '{field}'")
    if meta.get("name") == "My Theme" or meta.get("author") == "Your name":
        errors.append(f"{name}: metadata.ini still has the {TEMPLATE} placeholders")
    if meta.get("kind") and meta["kind"].lower() not in KINDS:
        errors.append(f"{name}: kind must be 'dark' or 'light', got '{meta['kind']}'")
    if meta.get("name") and meta["name"].replace(" ", "_") != name:
        warnings.append(f"{name}: folder name usually matches the theme name ('{meta['name'].replace(' ', '_')}')")

    present = set(widget_files(folder))
    for missing in sorted(REQUIRED_FILES - present):
        errors.append(f"{name}: {missing} is missing (copy it from themes/{TEMPLATE})")
    for file in sorted(present):
        text = (folder / file).read_text(encoding="utf-8", errors="replace")
        if not has_balanced_braces(text):
            errors.append(f"{name}: {file} has unbalanced braces")

    preview = meta.get("preview")
    if preview and not (folder / preview).is_file():
        errors.append(f"{name}: preview file '{preview}' not found")
    if find_screenshot(folder) is None:
        errors.append(f"{name}: add a screenshot named {name}.png")

    return errors, warnings


def first_commit_date(path):
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
    except (OSError, subprocess.CalledProcessError):
        out = []
    if out:
        when = dt.datetime.fromisoformat(out[-1]).astimezone(dt.timezone.utc)
    else:
        when = dt.datetime.now(dt.timezone.utc)
    return when.replace(tzinfo=None).isoformat()


def load_index():
    try:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def build_index(folders, previous):
    known = {}
    for entry in previous.values():
        image = entry.get("image")
        if image:
            known[Path(image).parent.name] = entry

    entries = []
    for folder in folders:
        meta = read_metadata(folder)
        old = known.get(folder.name, {})
        entries.append({
            "id": old.get("id") or str(uuid.uuid5(ID_NAMESPACE, folder.name)),
            "name": meta["name"],
            "description": meta["description"],
            "image": f"themes/{folder.name}/{find_screenshot(folder)}",
            "author": meta["author"],
            "publish_date": old.get("publish_date") or first_commit_date(folder / "metadata.ini"),
            "widgets": widget_files(folder),
        })
    entries.sort(key=lambda e: (e["publish_date"], e["name"].lower()))
    return {e["id"]: e for e in entries}


def read_archive(path):
    try:
        with zipfile.ZipFile(path) as z:
            return {i.filename: z.read(i) for i in z.infolist() if not i.is_dir()}
    except (OSError, zipfile.BadZipFile):
        return None


def write_archive(folder):
    meta = read_metadata(folder)
    names = set(widget_files(folder)) | {"metadata.ini"}
    if meta.get("preview"):
        names.add(meta["preview"])
    members = {f"{folder.name}/{n}": (folder / n).read_bytes() for n in sorted(names)}
    target = THEMES_DIR / f"{folder.name}.fctheme"
    if read_archive(target) == members:
        return False
    with zipfile.ZipFile(target, "w") as z:
        z.writestr(zipfile.ZipInfo(f"{folder.name}/", date_time=(2020, 1, 1, 0, 0, 0)), b"")
        for name, data in members.items():
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return True


def remove_orphan_archives(folders):
    names = {f.name for f in folders}
    removed = []
    for archive in THEMES_DIR.glob("*.fctheme"):
        if archive.stem not in names:
            archive.unlink()
            removed.append(archive.name)
    return removed


def render_gallery(index):
    blocks = []
    for entry in sorted(index.values(), key=lambda e: e["name"].lower()):
        folder = Path(entry["image"]).parent.name
        blocks.append(
            f"### [{folder}.fctheme](themes/{folder}.fctheme)\n\n"
            f"![{entry['name']}]({entry['image']})"
        )
    return "\n\n".join(blocks)


def update_readme(index):
    if not README_FILE.is_file():
        return False
    text = README_FILE.read_text(encoding="utf-8")
    start, end = text.find(GALLERY_START), text.find(GALLERY_END)
    if start == -1 or end == -1 or end < start:
        return False
    new = text[: start + len(GALLERY_START)] + "\n" + render_gallery(index) + "\n" + text[end:]
    if new == text:
        return False
    README_FILE.write_text(new, encoding="utf-8")
    return True


def write_index(index):
    text = json.dumps(index, indent=4, ensure_ascii=False) + "\n"
    if INDEX_FILE.is_file() and INDEX_FILE.read_text(encoding="utf-8") == text:
        return False
    INDEX_FILE.write_text(text, encoding="utf-8")
    return True


def report(errors, warnings):
    on_ci = os.environ.get("GITHUB_ACTIONS") == "true"
    for msg in warnings:
        print(f"::warning::{msg}" if on_ci else f"warning: {msg}")
    for msg in errors:
        print(f"::error::{msg}" if on_ci else f"error: {msg}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--pack", metavar="NAME", help="build themes/NAME.fctheme only")
    args = ap.parse_args()

    folders = discover()
    if args.pack:
        folders = [f for f in folders if f.name == args.pack]
        if not folders:
            print(f"error: no theme folder named '{args.pack}' in themes/")
            return 1

    errors, warnings = [], []
    for folder in folders:
        e, w = validate(folder)
        errors += e
        warnings += w

    if not args.pack:
        names = {}
        for folder in folders:
            key = read_metadata(folder).get("name", "").lower()
            if key and key in names:
                errors.append(f"themes '{names[key]}' and '{folder.name}' share the same name")
            names[key] = folder.name

    report(errors, warnings)
    if errors:
        return 1
    if args.check:
        print(f"{len(folders)} theme(s) valid")
        return 0

    if args.pack:
        write_archive(folders[0])
        print(f"built themes/{args.pack}.fctheme")
        return 0

    rebuilt = [f.name for f in folders if write_archive(f)]
    removed = remove_orphan_archives(folders)
    index = build_index(folders, load_index())
    if write_index(index):
        print("themes.json updated")
    if update_readme(index):
        print("README gallery updated")
    if rebuilt:
        print("archives rebuilt: " + ", ".join(rebuilt))
    if removed:
        print("archives removed: " + ", ".join(removed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
