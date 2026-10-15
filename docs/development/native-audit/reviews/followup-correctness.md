# PR 11 follow-up correctness review

Parent HEAD reviewed: `3803015468b865503392593914a8056d0b02c373`.
Date: 2026-10-15.
Scope: uncommitted files under `docs/development/native-audit`: component-license-findings.md, component-licenses.json, upstream-records-request.md, verify_provenance.py, verify_source_evidence.py, and every file in evidence/.
Reviewer: independent correctness/tests agent session.

## Decision

No blocking correctness defect found in the new verification scripts or evidence claims. Both scripts reproduce their recorded results against the real downloaded inputs. The evidence correctly distinguishes exact native byte provenance from unresolved binary-to-component build provenance. Issue #1 and redistribution clearance remain incomplete.

## Nonblocking completeness observations

1. The conditional module map names four components without corresponding source catalog rows: xau, xcb-proto, xorg-macros, and xproto. Their presence in a conditional source map does not prove inclusion in a binary. The catalog must not be described as a complete review of every component named by that map. The current evidence guide does not make that claim.
2. The findings introduction identifies x264 as a Git-commit archive with a measured SHA-512. Fluidlite is another such archive. Its catalog correctly sets sha512_verified=false and gives a pinned commit URL. Mentioning both would make the findings introduction clearer. This does not invalidate the statement about release archives because Fluidlite is a commit archive.

## Verification evidence

- Ran verify_provenance.py against `/tmp/sonumio-audit` and `/tmp/sonumio-upstream-comparison`. Its output matches evidence/upstream-native-files.tsv byte for byte.
- All 1,574 candidate native and linker files match official release archive files. The helper independently checks both NuGet hashes and all five release archive hashes before extraction.
- Ran verify_source_evidence.py against `/tmp/sonumio-component-licenses/archives`. It verified 81 component records, 294 license evidence files, and 38 supplemental source files.
- Independently compared the module map with native-files.tsv. All 339 module groups and all 1,552 plugin binary counts match. The ten remaining runtime files are five libVLC and five libvlccore libraries.
- Checked all five full raw job trace SHA-256 values against upstream-build-receipts.json. They match.
- Compared every retained configuration line and SHA-512/component archive receipt with its referenced line in each normalized local trace. There were zero mismatches. Raw traces and upload fields were not printed.
- Changed a source archive hash in a temporary catalog. The source helper rejected it.
- Changed a license evidence hash in a temporary catalog. The source helper rejected it.
- Changed a supplemental source hash in a temporary catalog. The source helper rejected it.
- Supplied a changed NuGet file. The provenance helper rejected it before extraction.

No downloaded native file or source build script was executed. Only the audit helpers and installed archive reader were executed. No repository file was changed and no external message was posted.

## Scope limits

This is an evidence and script correctness review. It does not independently establish every source license expression or prove inclusion of each component in the release binary. Those source/build relationships remain explicitly conditional in the artifacts.

The earlier review described the 12 Windows .lib entries as import libraries. This review corrects that description. They comprise six import archives and six GNU linker scripts. All 12 remain correctly represented in the inventory.

## Reviewed file hashes

SHA-256 values identify the uncommitted inputs before subsequent revisions.

- `de0fa1c82d6597cdac91cb4e48b57847112ebbf088a80c23659939b0c1645249` docs/development/native-audit/component-license-findings.md
- `3301db4bffd48217a4be5cd70c17e14d33721cbcd01083fdc968c5766d07624a` docs/development/native-audit/component-licenses.json
- `457964bc2d23b1e5ce4d73ca555bff9aab549304b9990c913f42c81fde600220` docs/development/native-audit/evidence/README.md
- `4b7078752c99b2fc891658d5c2a3670a9f25fdf429dc24b4eb5c28c15c92ed0c` docs/development/native-audit/evidence/module-component-candidates.tsv
- `4438e700ef3fe035ae072ee8256f3e3f41e65b4ff40b61637c6b172a38400a01` docs/development/native-audit/evidence/upstream-build-receipts.json
- `687112d2848c62529874aceb6b94ebba8645e71773e3494123cd76215c6efab6` docs/development/native-audit/evidence/upstream-issue-search.md
- `dc4981315c63de2de8372a4c11c272804815a7cd97b28cf4011052e6f6c49f2d` docs/development/native-audit/evidence/upstream-native-files.tsv
- `f820db94362478b01295910e83997418bf4a2bd9b59d308e9695df693389438f` docs/development/native-audit/evidence/upstream-releases.json
- `df4dec1a9174d3dbb36d1c6c9b2325fd701d5dfa0123116c8c43d1acf2f57860` docs/development/native-audit/upstream-records-request.md
- `675b6a869e141f4f43337527556baddbb89142de23295ec15c0e88fd944b8394` docs/development/native-audit/verify_provenance.py
- `f20b23817c98a4bb78e82475bc294768651c411d222caad6270405f76894a64c` docs/development/native-audit/verify_source_evidence.py

## Incremental source-map addendum

Reviewed the added `map_module_sources.py` and regenerated module TSV after the initial follow-up review. No blocking defect found in this bounded change.

- Ran the portable helper against `/tmp/sonumio-audit/vlc-3.0.24`. The complete output matches the retained TSV byte for byte and contains 339 rows.
- Confirmed `modules/codec/fluidsynth.c:41` selects `<fluidsynth.h>` or `<fluidlite.h>` through `HAVE_FLUIDLITE_H`.
- Confirmed the FluidLite contrib recipe names Vorbis as a dependency. The regenerated FluidSynth row includes both conditional implementations and the Ogg/Vorbis closure.
- Confirmed all three Windows job package selections name FluidLite. Neither retrieved macOS CI selection names it. The evidence guide limits the corresponding statement to Windows.
- The helper uses only the Python standard library, reads supplied local source and inventory paths, and contains no fixed temporary-directory input or process/network dependency.
- The helper and guide preserve the conditional union scope. They do not claim to evaluate build conditions or establish exact binary linkage.
- Confirmed the findings now disclose both Git-commit hash exceptions and the four uncataloged conditional X-related candidates. This addresses the earlier nonblocking wording observations.

Reviewed SHA-256 values:

- `890a3b74dec711c7c6ca490d707d03037c0de9e308c8c963051b64be8e8d5d15` docs/development/native-audit/map_module_sources.py
- `a2a3376ab8e492f9a88c53a640804c568ce4b20dfd24b28a75213deff3fb44f5` docs/development/native-audit/evidence/module-component-candidates.tsv

The earlier full archive checks were not repeated. No repository file was changed.
