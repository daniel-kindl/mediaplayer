# 0006. MIT source with GPL native binary distribution

- Status: Accepted
- Date: 2026-10-15
- Evidence: [Native dependency audit](../development/native-audit/README.md), [issue #1](https://github.com/daniel-kindl/sonumio/issues/1)

## Context

Sonumio application source is MIT. LibVLCSharp and libVLC core declare LGPL-2.1-or-later.
The candidate VideoLAN Windows and macOS NuGet archives contain plugins with explicit GPL-2.0-or-later declarations.
Package metadata and upstream plugin exclusion lists do not establish an LGPL-only payload.
A complete source-level license audit of linked components remains open.

## Decision

Keep Sonumio source under MIT. Keep LibVLCSharp assemblies separate and link native libVLC dynamically.
Select GPL-3.0-or-later terms for combined Sonumio binary releases that include the audited GPL plugins.
Use the later-version option of GPL-2.0-or-later components for that distribution policy.
Preserve the individual licenses and notices of all third-party components.
Do not claim that this policy establishes license compatibility for unreviewed linked components.
Do not approve an LGPL-only plugin set from these candidate packages.

Use distribution-provided libVLC on Linux. Defer Flatpak and other bundled Linux runtimes to separate audits.
Retain LibVLCSharp.Avalonia 3.10.2 as a compatible candidate for Avalonia 12 based on tagged upstream source.
Resolve its project placement during integration because it references both Avalonia and LibVLCSharp.

## Consequences

MIT source remains usable under MIT terms. The planned combined binary distribution has GPL obligations.
The project must supply notices, applicable license texts, and corresponding source through a compliant delivery method.
Exact linked dependencies and auxiliary assets require review before any binary release.
The [licensing guide](../development/licensing.md) defines those release requirements.
Accepting this distribution policy does not approve the candidate archives for release.
No build artifact includes libVLC until the relevant integration and release requirements are met.
