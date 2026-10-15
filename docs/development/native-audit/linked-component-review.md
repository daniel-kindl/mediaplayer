# Linked component source review

Reviewed on 2026-10-15. The review used static archive inspection and primary upstream source. No downloaded binary was executed.

## Result

The VLC source base is identified. A follow-up [native provenance check](evidence/README.md) matches every candidate native file to an official release payload.
Actual upstream build records and a [source license catalog](component-licenses.json) now supplement the source recipes.
Exact third-party build selections for the published payloads and complete corresponding source remain unverified.
GPL-3.0-or-later is a distribution policy. This review does not approve the exact native payload for release.

## Source identity

The [official VLC 3.0.24 source archive](https://download.videolan.org/pub/videolan/vlc/3.0.24/vlc-3.0.24.tar.xz) has SHA-256 `e7cab503d1d7d5849b89d2cf0e1ee60d0ef6d012407791b644b9cfc0cc225fdf`. This matches the [upstream checksum](https://download.videolan.org/pub/videolan/vlc/3.0.24/vlc-3.0.24.tar.xz.sha256).

Its `src/revision.txt` contains `3.0.24-rc1-0-g6de05adcba`. That exact string occurs in the examined `build/x64/libvlc.dll`, `build/x64/libvlccore.dll`, `build/macos/osx-x64/lib/libvlc.dylib`, and `build/macos/osx-x64/lib/libvlccore.dylib` in the candidate NuGet archives. The `rc1` string alone is therefore not evidence that these packages use a different VLC base from the official 3.0.24 source archive. The revision string identifies the base. It does not prove that the binaries contain no unrecorded changes.

The [upstream packaging repository](https://code.videolan.org/videolan/libvlc-nuget/-/tree/bff3a598ac3d67f2cc5bfdc39293792890ebe292) was inspected at commit `bff3a598ac3d67f2cc5bfdc39293792890ebe292`. Its Windows script repackages the official VLC Windows 7z releases. Its macOS script repackages the official arm64 and Intel DMGs. A script at the repository head does not establish which commit produced an already published NuGet package: the examined package metadata contains no packaging commit or upstream archive checksum.

## FFmpeg and static dependencies

Both examined x64 libvlccore files contain VLC configure commands with `--enable-merge-ffmpeg`. In the matching VLC source, `modules/codec/Makefile.am` explains this option: it combines VLC's avformat demux, avio access, and avparser sources into the avcodec plugin and links the FFmpeg avformat and avutil libraries there. It does not mean that FFmpeg is merged into libvlccore.

In that same source archive, `contrib/src/ffmpeg/rules.mak` selects FFmpeg 8.1.2, enables static libraries, disables shared libraries, enables libgsm and OpenJPEG, and enables LAME when encoders are selected. Its dependency rules select GSM 1.0.13, OpenJPEG 2.5.4, and LAME 3.100. The default recipe has no `--enable-gpl`, `--enable-version3`, or `--enable-nonfree` option. Both examined avcodec plugins contain `Lavc62.28.102`; this is useful build evidence but does not independently establish the complete FFmpeg configuration.

[FFmpeg's licensing page](https://ffmpeg.org/legal.html) states that the default library license is LGPL-2.1-or-later and that enabling its optional GPL parts makes GPL apply to FFmpeg. Its compliance guidance requires matching source, build configuration, changes, and review of external linked libraries. The absence of GPL options in the VLC recipe is evidence about the source default. It is insufficient to approve the exact compiled plugin or to infer its complete linked dependency set.

## Other source recipe evidence

The following facts come from the named files in the checksum-pinned VLC source archive. Versions below are recipe selections, not a confirmed binary bill of materials.

| Source recipe | Selected version or dependency | License selection evidence |
| --- | --- | --- |
| `contrib/src/gnutls/rules.mak` | GnuTLS 3.8.13, with included libtasn1 and libunistring; depends on Nettle | Builds when GPL or GNUV3 is selected. The recipe records that the Nettle/GMP combination cannot use LGPLv2 terms. |
| `contrib/src/nettle/rules.mak` | Nettle 3.10.2; depends on GMP | Requires GNUV3 when GPL is not selected. |
| `contrib/src/gmp/rules.mak` | GMP 6.3.0 | Requires GNUV3 when GPL is not selected. Its comment records GPLv2 or LGPLv3 alternatives. |
| `contrib/src/live555/rules.mak` | LIVE555 2026.06.24, with local patches and `NO_OPENSSL=1` | Requires GNUV3. |
| `contrib/src/freetype2/rules.mak` | FreeType 2.14.3; depends on zlib | Requires GPL when `AD_CLAUSES` is not selected. The exact chosen license alternative needs to be recorded. |

These source checks show why the outer VLC plugin declaration cannot establish the licenses of all code inside a plugin. They do not replace the actual component license texts. This review did not fetch and independently examine every selected third-party source archive, nested dependency, or asset license. Those entries remain unverified.

## Specific missing records

1. The connection from the recorded Windows release jobs to the individual published native files. NuGet-to-official-release byte identity is now established for all five platform trees. Original Windows job artifacts return 404, and their container hashes differ from the later published containers.
2. The actual contributor package manifest for each shipped architecture: package names, versions, source hashes, configure options, patches, and locally supplied dependencies. In particular, obtain the FFmpeg configuration and dependency selections used for each avcodec plugin.
3. The identity of the prebuilt contributor archive, if one was used. The matching macOS `extras/package/macosx/build.sh` can build dependencies from source, use `VLC_PREBUILT_CONTRIBS_URL`, or use the default prebuilt archive. In `contrib/src/main.mak`, the default URL ends in `vlc-contrib-$(HOST)-latest.tar.zst`. That mutable filename cannot identify the exact archive consumed by a past build. The record must supply the immutable URL or archive plus its hash and manifest.
4. An inventory that maps the compiled linked components, including nested dependencies, to their actual source license texts and notices. Record any selected dual-license alternative and evaluate compatibility with the chosen combined release terms. The source defaults above cannot clear an unidentified linked dependency.
5. A complete retained corresponding-source bundle with the required build scripts, dependency source, changes, and release delivery method for the exact distributed payload. The official VLC source tar identifies and supplies VLC base source and contributor recipes. The recipes alone are not the downloaded contributor sources or a receipt for a particular compiled dependency set.

The inspected [official release root](https://download.videolan.org/pub/videolan/vlc/3.0.24/), [Windows x64 directory](https://download.videolan.org/pub/videolan/vlc/3.0.24/win64/), and [macOS directory](https://download.videolan.org/pub/videolan/vlc/3.0.24/macosx/) expose VLC source or binaries and checksums. They do not list a per-binary contributor source manifest or build receipt.
Follow-up [public CI and issue searches](evidence/README.md) recovered revision-matched source receipts and build configurations.
Those records do not establish the exact release input chain described above. The search report records inspected locations and access limits.

## Action to clear the remaining gap

Obtain those records from the package producer, or build the chosen VLC and dependencies from pinned sources while retaining the complete manifest, license mapping, and source bundle. Then audit the actual resulting Windows and macOS payload. No new human authorization is needed for further public-source investigation. Approval to distribute still depends on the missing exact-build evidence.
