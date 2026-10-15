#!/usr/bin/env python3
"""Compare candidate native files with checksum-pinned upstream releases."""

import argparse
import csv
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


PACKAGES = {
    "windows.nupkg": "3da3f37ee2b2b10e5c788d830a3b513658c36521ea1b0f966ed86eb69f41ef3c",
    "mac.nupkg": "b83faf0e4866a5d8c53e998aec4caafc38d0e8aff9390a2a02d49af4d9757715",
}
RELEASES = (
    ("windows.nupkg", "build/x64/", "vlc-3.0.24-win64.7z",
     "1ed59c09152e78aff84663fa76efab26057716576db74332858810e5ef54ae1f"),
    ("windows.nupkg", "build/x86/", "vlc-3.0.24-win32.7z",
     "80b61c03a5c7c4d4b44a79a2db34eda244ad6b09f1e0f44fcf6183f4c10e9966"),
    ("windows.nupkg", "build/arm64/", "vlc-3.0.24-winarm64.7z",
     "4c448ca4995bafc4954a4c929bc7dad756eb0a234afc9d58946ad05b8fe51389"),
    ("mac.nupkg", "build/macos/osx-x64/", "vlc-3.0.24-intel64.dmg",
     "1ef6c903e2dc026d4e58ddf7b2a9ed0eb6f8caf80a9a9f46f96490340b962707"),
    ("mac.nupkg", "build/macos/osx-arm64/", "vlc-3.0.24-arm64.dmg",
     "64a89d93cdd30b0e97131743e246373db82d6826ea882d265d46d74b136da2b7"),
)
NATIVE_SUFFIXES = (".dll", ".dylib", ".lib", ".a", ".so", ".exe")


def checked_file(path, expected):
    """Reject an input that differs from the audited archive."""
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("SHA-256 mismatch for " + path.name)


def main():
    """Emit provenance TSV only after every candidate native file matches."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package_directory", type=Path)
    parser.add_argument("release_directory", type=Path)
    arguments = parser.parse_args()
    for filename, expected in PACKAGES.items():
        checked_file(arguments.package_directory / filename, expected)
    for _, _, filename, expected in RELEASES:
        checked_file(arguments.release_directory / filename, expected)

    rows = []
    compared = set()
    for package, prefix, filename, release_hash in RELEASES:
        with tempfile.TemporaryDirectory(prefix="sonumio-provenance-") as temporary:
            output = Path(temporary)
            subprocess.run(
                ["7z", "x", "-y", "-sns-", "-o" + temporary,
                 str((arguments.release_directory / filename).resolve())],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            upstream = {}
            for path in sorted(output.rglob("*")):
                if path.is_file() and path.name.endswith(NATIVE_SUFFIXES):
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    upstream.setdefault(digest, []).append(path.relative_to(output).as_posix())
            with zipfile.ZipFile(arguments.package_directory / package) as archive:
                for name in sorted(archive.namelist()):
                    if not name.startswith(prefix) or not name.endswith(NATIVE_SUFFIXES):
                        continue
                    digest = hashlib.sha256(archive.read(name)).hexdigest()
                    if digest not in upstream:
                        raise ValueError("No identical upstream native file for " + name)
                    compared.add((package, name))
                    rows.append((package, name, digest, filename, release_hash,
                                 " | ".join(upstream[digest])))

    for package in PACKAGES:
        with zipfile.ZipFile(arguments.package_directory / package) as archive:
            expected = {(package, name) for name in archive.namelist()
                        if name.endswith(NATIVE_SUFFIXES)}
            if not expected.issubset(compared):
                raise ValueError("Unmapped native file in " + package)
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("package_archive", "nuget_path", "file_sha256", "upstream_archive",
                     "upstream_archive_sha256", "identical_upstream_paths"))
    writer.writerows(rows)


if __name__ == "__main__":
    main()
