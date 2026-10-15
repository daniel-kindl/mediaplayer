#!/usr/bin/env python3
"""Inventory native files without loading or executing package contents."""

import csv
import hashlib
from pathlib import Path
import re
import sys
import zipfile


PACKAGES = (
    ("VideoLAN.LibVLC.Windows", "3.0.24", "windows.nupkg"),
    ("VideoLAN.LibVLC.Mac", "3.1.3.2", "mac.nupkg"),
)
DECLARATIONS = {
    b"GNU Lesser General Public License, version 2.1 or later.": "LGPL-2.1-or-later",
    b"GNU General Public License, version 2 or later.": "GPL-2.0-or-later",
}


def main():
    """Write TSV data from the two downloaded candidate packages."""
    package_directory = Path(sys.argv[1])
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("package", "version", "package_sha256", "path", "bytes",
                     "file_sha256", "module_license", "evidence", "linked_components"))
    for package, version, filename in PACKAGES:
        archive_path = package_directory / filename
        package_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        with zipfile.ZipFile(archive_path) as archive:
            for name in sorted(archive.namelist()):
                if not name.endswith((".dll", ".dylib", ".lib", ".a", ".so", ".exe")):
                    continue
                data = archive.read(name)
                declarations = set(re.findall(
                    rb"Licensed under the terms of the ([^\x00\r\n]+)", data))
                licenses = {DECLARATIONS[item] for item in declarations}
                evidence = "embedded-module-declaration"
                if not licenses:
                    if Path(name).name not in (
                        "libvlc.dll", "libvlc.dylib", "libvlc.lib", "libvlccore.lib",
                        "vlc.lib", "vlccore.lib",
                    ):
                        raise ValueError("No license evidence for " + name)
                    licenses = {"LGPL-2.1-or-later"}
                    evidence = "VLC-3.0.24-COPYING.LIB-and-library-identity"
                writer.writerow((package, version, package_hash, name, len(data),
                                 hashlib.sha256(data).hexdigest(),
                                 " AND ".join(sorted(licenses)), evidence,
                                 "NOT-CLEARED-see-README"))


if __name__ == "__main__":
    main()
