# Audit evidence

These records were collected on 2026-10-15. They supplement the [audit](../README.md).
Native files were read as data. No downloaded binary or source build script was executed.

## Exact native provenance

[upstream-native-files.tsv](upstream-native-files.tsv) maps all 1,574 candidate native and linker files to identical files in official VLC archives.
[upstream-releases.json](upstream-releases.json) records archive URLs, SHA-256 values, package paths, and match counts.
All five archive hashes match the checksums published beside the official downloads.
No OpenPGP signature check was performed.

| Platform tree | Files matched | Official archive |
| --- | ---: | --- |
| Windows x64 | 327 | `vlc-3.0.24-win64.7z` |
| Windows x86 | 327 | `vlc-3.0.24-win32.7z` |
| Windows ARM64 | 314 | `vlc-3.0.24-winarm64.7z` |
| macOS x64 | 306 | `vlc-3.0.24-intel64.dmg` |
| macOS ARM64 | 300 | `vlc-3.0.24-arm64.dmg` |

The Windows `.lib` entries consist of six import archives and six GNU linker scripts.
They remain in the inventory because they are part of the candidate native development payload.
The runtime payload consists of 956 Windows DLLs and 606 macOS dylibs.

## Retrieved build records

[upstream-build-receipts.json](upstream-build-receipts.json) contains factual excerpts from five public upstream job logs.
Each record has the job URL, complete trace hash, source archive SHA-512 receipts, configuration lines, package selections, and FFmpeg license summaries.
The original public trace contains additional patch progress and build output. Line references permit inspection of that original record.
The excerpts omit runner artifact-upload fields. Full job logs are not copied into this repository.

| Platform | Job | Relationship to the candidate |
| --- | --- | --- |
| Windows x86 | [2841096](https://code.videolan.org/videolan/vlc/-/jobs/2841096) | Release build of the embedded source revision. Original output artifact expired. |
| Windows x64 | [2841097](https://code.videolan.org/videolan/vlc/-/jobs/2841097) | Release build of the embedded source revision. Original output artifact expired. |
| Windows ARM64 | [2841098](https://code.videolan.org/videolan/vlc/-/jobs/2841098) | Release build of the embedded source revision. Original output artifact expired. |
| macOS x64 | [2841088](https://code.videolan.org/videolan/vlc/-/jobs/2841088) | Same source revision. CI configuration differs from the published release. |
| macOS ARM64 | [2841089](https://code.videolan.org/videolan/vlc/-/jobs/2841089) | Same source revision. CI build path differs from the published release. |

All five logs identify the full source commit `6de05adcbaf2e8b85fe86aad4169393098628119`.
The matching Windows release jobs belong to [pipeline 741289](https://code.videolan.org/videolan/vlc/-/pipelines/741289).
The earlier pipeline named `3.0.24` used a different commit. A release name alone cannot identify the build inputs.

The main FFmpeg builds report `LGPL version 2.1 or later` and enable libgsm, OpenJPEG, and LAME.
Their configure commands do not enable GPL or nonfree mode.
A separate postproc build reports `GPL version 2 or later`. Its summary does not describe the main avcodec build.
These are facts about the recorded jobs. They do not prove the exact inputs of the published candidate binaries.

## Conditional module source map

[module-component-candidates.tsv](module-component-candidates.tsv) covers all 339 module source groups and their 1,552 plugin binaries.
The remaining ten runtime libraries are the five libVLC API libraries and five libvlccore libraries.
The map follows Automake source assignments, recursive internal `.la` libraries, external include references, and contrib dependency recipes.
It preserves a union of conditional branches. It does not evaluate a platform build configuration.
A listed component is a source candidate, not proof that it occurs in each corresponding binary.
The recorded source license expressions come from explicit source-header grants.
They do not describe all external library code inside the binary.
The FluidSynth module includes both the `fluid` and `fluidlite` conditional source candidates.
The retrieved Windows job selections name FluidLite. Its pinned source grant is recorded separately in the catalog.

[The component catalog](../component-licenses.json) supplies independently inspected source license records, source URLs, source hashes, and license-evidence hashes.
GnuTLS bundled dependencies have separate records that refer to the parent GnuTLS source archive.
The bundled libtasn1 version is 4.20.0. The standalone contrib libtasn1 recipe version 4.21.0 does not identify that bundled source.

## Reproduce native provenance

This check requires Python 3 and `7z`.
Download the two candidate NuGet archives as described in [the audit](../README.md#reproduction).
Download the five official archives from the URLs in `upstream-releases.json` into one release directory.
Then run:

```bash
python3 docs/development/native-audit/verify_provenance.py /tmp/sonumio-native-audit /tmp/sonumio-release-archives > /tmp/sonumio-upstream-native-files.tsv
diff -u docs/development/native-audit/evidence/upstream-native-files.tsv /tmp/sonumio-upstream-native-files.tsv
```

The helper checks pinned hashes before extraction. It extracts into temporary directories and compares every candidate native file by hash.
It emits a complete TSV only after all files match. A missing file or changed input fails the check.
Archive hash verification and byte identity establish the native release provenance, not the component license closure.

## Reproduce source evidence

Download each component's `archive` into one cache directory using its `source_url` from `component-licenses.json`.
The catalog records source hashes and archive-member hashes. License evidence paths identify members within the source input.
Save each supplemental input from its `source_url` under `supplemental/<sha256>` in the same cache directory.
The helper checks those separate files as well as the archive members. It does not extract or execute source code:

```bash
python3 docs/development/native-audit/verify_source_evidence.py /tmp/sonumio-component-sources
```

For recipe-pinned releases, the recorded SHA-512 was checked against VLC's contrib checksum file.
For Git-commit archives, the catalog identifies the pinned commit and the measured archive hash.
A matching source hash does not prove that a binary used that source input.

## Reproduce the conditional source map

Extract the checksum-pinned VLC source archive identified in [the source review](../linked-component-review.md#source-identity).
Then run:

```bash
python3 docs/development/native-audit/map_module_sources.py /tmp/vlc-3.0.24 > /tmp/sonumio-module-component-candidates.tsv
diff -u docs/development/native-audit/evidence/module-component-candidates.tsv /tmp/sonumio-module-component-candidates.tsv
```

The helper reads `native-files.tsv` beside the script by default. It does not execute Automake or downloaded source code.
Its fixed library and header mappings identify candidates. They do not replace configuration-specific link records or manual source review.

## Outstanding upstream evidence

The original Windows job artifact routes return 404. The release job hashes describe containers with symbols, which differ from the later published containers.
No retrieved output manifest connects those original jobs to the published individual native file hashes.
The retrieved macOS CI jobs use different build paths and host settings from the published macOS binaries.
Their dependency manifests therefore cannot serve as exact release receipts.
The [upstream request draft](../upstream-records-request.md) asks for those specific missing records.
It has not been sent.
