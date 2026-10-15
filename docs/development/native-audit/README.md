# Native dependency audit

Audit date: 2026-10-15. Scope: [issue #1](https://github.com/daniel-kindl/sonumio/issues/1).
No package was installed in a project. No native code was executed.

## Issue status

| Acceptance criterion | Result |
| --- | --- |
| Every native file listed with its license | PARTIAL. All native library files are listed with module license evidence. Linked-component licenses remain unresolved. |
| Redistribution decision recorded | Recorded in ADR 0006. GPL binary terms selected, MIT source retained. |
| Linux strategy decided | System libVLC selected. |
| Avalonia 12 compatibility confirmed or alternative chosen | Tagged upstream source confirms support. Runtime checks remain for integration. |
| Licensing and dependency guides updated | Updated in the same change. |

Issue #1 remains incomplete until the per-file license review covers linked components.
The inventory must not be described as a complete redistribution clearance.

## Candidates and inventory

[native-files.tsv](native-files.tsv) lists all 1,574 native library files in the two candidate NuGet archives.
Each row records the package, version, package hash, path, size, file hash, module license, and evidence.
Windows import libraries are included. All package architectures are included, even architectures outside the Sonumio targets.

| Candidate | Native files | LGPL module declarations or library identity | GPL module declarations |
| --- | ---: | ---: | ---: |
| [VideoLAN.LibVLC.Windows 3.0.24](https://www.nuget.org/packages/VideoLAN.LibVLC.Windows/3.0.24) | 968 | 956 | 12 |
| [VideoLAN.LibVLC.Mac 3.1.3.2](https://www.nuget.org/packages/VideoLAN.LibVLC.Mac/3.1.3.2) | 606 | 598 | 8 |

The Windows count includes 956 DLLs and 12 import libraries. The macOS count includes 606 dylibs.
Both packages contain VLC version string `3.0.24-rc1-0-g6de05adcba` in their core libraries.
The macOS NuGet version is not the VLC engine version. Its archive contains separate `osx-x64` and `osx-arm64` trees.

Archive SHA-256 values:

```text
VideoLAN.LibVLC.Windows 3.0.24
3da3f37ee2b2b10e5c788d830a3b513658c36521ea1b0f966ed86eb69f41ef3c
VideoLAN.LibVLC.Mac 3.1.3.2
b83faf0e4866a5d8c53e998aec4caafc38d0e8aff9390a2a02d49af4d9757715
```

## License evidence and limits

For 1,557 DLLs and dylibs, the inventory reads the embedded module license declaration.
The [VLC module export definitions](https://github.com/videolan/vlc/blob/3.0.24/include/vlc_plugin.h) define these declarations and export them through `vlc_entry_license`.
The declarations name LGPL-2.1-or-later or GPL-2.0-or-later.
For the five `libvlc` API libraries and 12 import libraries, the evidence is library identity and [VLC COPYING.LIB](https://github.com/videolan/vlc/blob/3.0.24/COPYING.LIB).

These are module licenses, not a complete license expression for every statically linked component.
VLC supplies a default LGPL module declaration when a module does not override it.
An embedded declaration therefore cannot establish the license of every source file or linked dependency.
Every inventory row explicitly records that linked components are not cleared.
Neither archive contains a `COPYING`, `LICENSE`, or third-party notice file.
The package-level LGPL expression is insufficient evidence for the complete payload.

The archives also contain headers, Lua bytecode, Java archives, HRTF data, and web assets.
Those files are outside the native-library table. Their licenses still need inclusion if a release copies them.
Their omission from this table does not authorize their redistribution.

## GPL modules in the nominal LGPL packages

These files contain an explicit GPL-2.0-or-later module declaration:

| Package | Relative plugin path | Architectures |
| --- | --- | --- |
| Windows | `lua/liblua_plugin.dll` | x64, x86, arm64 |
| Windows | `audio_filter/libdolby_surround_decoder_plugin.dll` | x64, x86, arm64 |
| Windows | `audio_filter/libheadphone_channel_mixer_plugin.dll` | x64, x86, arm64 |
| Windows | `codec/libx26410b_plugin.dll` | x64, x86, arm64 |
| macOS | `liblua_plugin.dylib` | x64, arm64 |
| macOS | `libdolby_surround_decoder_plugin.dylib` | x64, arm64 |
| macOS | `libheadphone_channel_mixer_plugin.dylib` | x64, arm64 |
| macOS | `libsyslog_plugin.dylib` | x64, arm64 |

The upstream [Windows packaging script](https://code.videolan.org/videolan/libvlc-nuget/-/blob/bff3a598ac3d67f2cc5bfdc39293792890ebe292/package-nuget-win.sh)
and [macOS packaging script](https://code.videolan.org/videolan/libvlc-nuget/-/blob/bff3a598ac3d67f2cc5bfdc39293792890ebe292/package-nuget-mac.sh)
remove a named set of GPL plugins before packing the LGPL variants.
Their lists do not remove all modules found above. The inspected revision documents the packaging method, not proven provenance for every package byte.
Deleting only these 20 files would not establish a complete LGPL-only dependency set.
No LGPL-only release allowlist is approved by this audit.

## Managed packages and Avalonia 12

The candidates are [LibVLCSharp 3.10.2](https://www.nuget.org/packages/LibVLCSharp/3.10.2)
and [LibVLCSharp.Avalonia 3.10.2](https://www.nuget.org/packages/LibVLCSharp.Avalonia/3.10.2).
Both declare LGPL-2.1-or-later. The Avalonia package depends on Avalonia `>= 11.3.13` and LibVLCSharp `>= 3.10.2`.
An open dependency range alone does not prove Avalonia 12 support.
The tagged [NEWS](https://github.com/videolan/libvlcsharp/blob/3.10.2/NEWS) explicitly records Avalonia 12 compatibility in 3.9.7.
The tagged [VideoView implementation](https://github.com/videolan/libvlcsharp/blob/3.10.2/src/LibVLCSharp.Avalonia/VideoView.cs) handles Avalonia major versions 12 and later.
This confirms upstream source support for Avalonia 12. No alternative is selected on compatibility grounds.
No Sonumio runtime or rendering check was performed on any platform.

The official control depends on both Avalonia and LibVLCSharp. The current repository boundaries do not permit either project to reference both.
The integration issue must resolve that placement with an ADR before adding the control. This audit changes no architecture rules.
The control also uses an [overlay window](https://github.com/videolan/libvlcsharp/blob/3.10.2/src/LibVLCSharp.Avalonia/README.md).
Focus, overlays, and native window behavior require validation during UI integration.

## Decision and release requirements

[ADR 0006](../../decisions/0006-licensing-mit-with-lgpl-libvlc.md) selects GPL-3.0-or-later terms for combined Sonumio binary releases that include these native plugins.
Application source remains MIT. Individual third-party components retain their licenses.
This conservative distribution policy does not assert that all aggregation creates a GPL derivative work.
GPL-3.0-or-later is a project choice, not the license declared by each module.
It accommodates the observed GPL-2.0-or-later declarations through their later-version option.
It does not establish compatibility with every linked dependency.

Linux uses distribution-provided libVLC and plugins. Sonumio does not bundle Linux native files.
Flatpak and other bundles are deferred. Each would need an inventory for its actual runtime contents.

Before a binary release, the release owner must:

1. Fix the exact platform payload and generate its inventory.
2. Identify all linked components and resolve their licenses against the matching build sources.
3. Include the licenses for copied headers, scripts, data, Java archives, and other auxiliary files.
4. Collect matching source, patches, dependency sources, and build material for the shipped libraries.
5. Select and implement a source-delivery method that satisfies the applicable license sections.
6. Include the notices and license texts described in [licensing.md](../licensing.md).
7. Check codec patent requirements for the intended distribution territories.

Until those requirements are met, these archives are candidates, not approved release payloads.
The per-file module inventory is complete. A full source-level audit of linked components remains open.

## Reproduction

Download the exact packages from NuGet. Do not execute their contents.

```bash
mkdir -p /tmp/sonumio-native-audit
curl -fL https://api.nuget.org/v3-flatcontainer/videolan.libvlc.windows/3.0.24/videolan.libvlc.windows.3.0.24.nupkg -o /tmp/sonumio-native-audit/windows.nupkg
curl -fL https://api.nuget.org/v3-flatcontainer/videolan.libvlc.mac/3.1.3.2/videolan.libvlc.mac.3.1.3.2.nupkg -o /tmp/sonumio-native-audit/mac.nupkg
python3 docs/development/native-audit/inventory.py /tmp/sonumio-native-audit > /tmp/sonumio-native-files.tsv
diff -u docs/development/native-audit/native-files.tsv /tmp/sonumio-native-files.tsv
```

The generator uses Python's standard library. It fails if a native file has no recognized license evidence.
Compare both package hashes with the values above. The TSV comparison also checks every recorded file hash.
This procedure checks reproducibility of the module inventory. It does not replace source-level license review.

## Verification record

The regenerated TSV matches the committed inventory byte for byte.
All local Markdown file links resolve. `git diff --check` passes.
`./eng/verify.sh` stops at prerequisites because SDK 10.0.402 is missing. Only SDK 10.0.401 is installed.
No SDK pin or verification rule was changed. All subsequent verification steps are NOT RUN.
Windows and macOS verification are NOT RUN. Native execution and playback checks are NOT RUN on every platform.
