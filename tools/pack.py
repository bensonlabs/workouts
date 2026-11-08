#!/usr/bin/env python3
"""Pack the workout plans exactly as bensonlabs.org serves them.

    python3 tools/pack.py                    # write and check dist/projects/workouts/
    python3 tools/pack.py --version v1.2.0   # also write dist/workouts-v1.2.0.tar.gz + .sha256

The blog (bensonlabs/blog) downloads the release, checks its sha256, unpacks it into
/projects/workouts/ and wraps both pages in the site header.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import shutil
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUT = DIST / "projects" / "workouts"
# Plan in this repo -> its path under /projects/workouts/ on the site.
PAGES = {"justin/index.html": "index.html", "cl/index.html": "cl/index.html"}


def valid_version(version: str) -> bool:
    parts = version[1:].split(".")
    return version.startswith("v") and len(parts) == 3 and all(part.isdigit() for part in parts)


def problems(text: str) -> list[str]:
    found = []
    if text.startswith("---"):
        found.append("starts with front matter; plans are standalone HTML pages")
    lowered = text.lower()
    for tag in ("<head", "</head>", "<body", "</body>"):
        if tag not in lowered:
            found.append(f"has no {tag}")
    return found


def write_release(version: str) -> Path:
    """Reproducible: sorted entries, fixed times and modes, so the same plans give the same sha256."""
    name = f"workouts-{version}.tar.gz"
    files = sorted((p for p in OUT.rglob("*") if p.is_file()), key=lambda p: p.relative_to(OUT).as_posix())
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for path in files:
            info = tarfile.TarInfo(path.relative_to(OUT).as_posix())
            info.size = path.stat().st_size
            info.mode = 0o644
            info.mtime = 0
            with path.open("rb") as handle:
                tar.addfile(info, handle)
    archive = DIST / name
    with archive.open("wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(buffer.getvalue())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (DIST / f"{name}.sha256").write_text(f"{digest}  {name}\n", encoding="utf-8", newline="\n")
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description="Pack the workout plans for bensonlabs.org.")
    parser.add_argument("--version", help="release version such as v1.2.0; also writes the release file")
    args = parser.parse_args()
    if args.version and not valid_version(args.version):
        sys.exit(f"--version must look like v1.2.0, not {args.version!r}")

    if DIST.exists():
        shutil.rmtree(DIST)
    errors = []
    for source, published in PAGES.items():
        text = (ROOT / source).read_text(encoding="utf-8")
        errors += [f"{source}: {problem}" for problem in problems(text)]
        dest = OUT / published
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, dest)
    if errors:
        sys.exit("Pack FAILED:\n" + "\n".join(f"  - {error}" for error in errors))
    print(f"Packed {len(PAGES)} plans in dist/projects/workouts/")
    if args.version:
        archive = write_release(args.version)
        print((DIST / f"{archive.name}.sha256").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
