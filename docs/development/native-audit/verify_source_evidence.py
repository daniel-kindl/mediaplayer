#!/usr/bin/env python3
"""Check component source hashes and retained license evidence without extraction."""

import argparse
import hashlib
import json
from pathlib import Path
import tarfile
import zipfile


def main():
    """Check downloaded source inputs against the reviewed catalog."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive_directory", type=Path)
    parser.add_argument("--catalog", type=Path,
                        default=Path(__file__).with_name("component-licenses.json"))
    arguments = parser.parse_args()
    catalog = json.loads(arguments.catalog.read_text())
    checked = 0
    for component in catalog["components"]:
        source = arguments.archive_directory / component["archive"]
        if hashlib.sha512(source.read_bytes()).hexdigest() != component["sha512"]:
            raise ValueError("Source SHA-512 mismatch for " + component["component"])
        if zipfile.is_zipfile(source):
            with zipfile.ZipFile(source) as archive:
                members = {name: archive.read(name) for name in archive.namelist()
                           if not name.endswith("/")}
        elif tarfile.is_tarfile(source):
            with tarfile.open(source) as archive:
                # Read only evidence files. Do not extract paths from the source archive.
                wanted = [item["path"] for item in component["license_evidence"]]
                members = {}
                for member in archive.getmembers():
                    if member.isfile() and any(
                        member.name == name or member.name.endswith("/" + name)
                        for name in wanted
                    ):
                        members[member.name] = archive.extractfile(member).read()
        else:
            members = {source.name: source.read_bytes()}
        for evidence in component["license_evidence"]:
            name = evidence["path"]
            matches = [data for path, data in members.items()
                       if path == name or path.endswith("/" + name)]
            if not any(hashlib.sha256(data).hexdigest() == evidence["sha256"]
                       for data in matches):
                raise ValueError("License evidence mismatch for "
                                 + component["component"] + ": " + name)
            checked += 1
    supplemental = [item for component in catalog["components"]
                    for item in component.get("supplemental_source_inputs", [])]
    supplemental.extend(item for runtime in catalog.get("supplemental_runtime_sources", [])
                        for item in runtime["inputs"])
    for item in supplemental:
        data = (arguments.archive_directory / "supplemental" / item["sha256"]).read_bytes()
        if (hashlib.sha256(data).hexdigest() != item["sha256"]
                or hashlib.sha512(data).hexdigest() != item["sha512"]):
            raise ValueError("Supplemental source hash mismatch for " + item["path"])
    print("Verified source inputs for " + str(len(catalog["components"]))
          + " component records, " + str(checked) + " license evidence files, and "
          + str(len(supplemental)) + " supplemental source files.")


if __name__ == "__main__":
    main()
