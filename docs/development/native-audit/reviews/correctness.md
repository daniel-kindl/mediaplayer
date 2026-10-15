# PR 11 correctness and audit evidence review

Reviewed commit: `a0439c2dd9ec657d1bf4323e4e2f6362ee48f74a`.
Base: `origin/dev`.
Review date: 2026-10-15.
Reviewer: independent correctness/tests agent session.

## Decision

The recorded module inventory is reproducible and consistent with the inspected archives. No new correctness defect was found in the documentation or generator for these exact candidates. Issue #1 is not complete. This review does not approve binary redistribution.

## Open acceptance requirement

Priority: P1 for completing issue #1, already disclosed in the PR.

`docs/development/native-audit/README.md:10` records the native file license criterion as PARTIAL. Lines 50–55 correctly distinguish module declarations from the licenses of statically linked components. Every TSV row contains `NOT-CLEARED-see-README` for linked components. The module declarations cannot prove the full license expression for each binary. Selecting GPL-3.0-or-later binary terms does not prove compatibility of unresolved linked dependencies.

Required evidence: identify the components linked into the exact candidate binaries and establish their licenses from matching build sources. Record compatible terms for each file or component. If exact build provenance cannot be obtained, select payloads with auditable build provenance before closing this acceptance criterion. Auxiliary files also need review before a release copies them, as the README already states.

This is an existing completeness limit, not an undisclosed regression.

## Checks performed

- Read repository AGENTS.md, the issue body, and the complete changed documentation and generator.
- Regenerated the inventory from `/tmp/sonumio-audit/windows.nupkg` and `mac.nupkg`. `cmp` confirmed a byte-for-byte match with the committed TSV.
- Read both embedded `.nuspec` files. They confirm `VideoLAN.LibVLC.Windows` version `3.0.24` and `VideoLAN.LibVLC.Mac` version `3.1.3.2`. Both metadata files declare `LGPL-2.1-or-later`.
- Independently counted 968 Windows entries, including 956 DLLs and 12 import libraries, and 606 macOS dylibs.
- Confirmed license totals: Windows has 956 LGPL module declarations or library identities and 12 GPL module declarations. macOS has 598 LGPL entries and 8 GPL entries.
- Confirmed the evidence totals: 1,557 embedded module declarations and 17 library identity entries, including five libvlc API libraries and 12 import libraries.
- Inspected the magic bytes of every ZIP entry excluded by the filename filter. Found no excluded PE, ELF, Mach-O, or ar binary in these two archives.
- Confirmed `3.0.24-rc1-0-g6de05adcba` in all five platform core libraries.
- `git diff --check origin/dev` passed.

No native payload was loaded or executed. No repository file was changed. No external comment was posted. Full .NET verification was not repeated in this review because the changed artifacts are documentation and a standalone Python inventory generator. The inventory generator itself was executed against the real candidate archives.
