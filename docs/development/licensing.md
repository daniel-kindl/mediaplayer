# Licensing

The application source is MIT. Planned combined binary releases with GPL native plugins use GPL-3.0-or-later terms.
[ADR 0006](../decisions/0006-licensing-mit-with-lgpl-libvlc.md) records this decision.
The [native audit](native-audit/README.md) records candidates, file licenses, evidence, and unresolved release requirements.
This document is engineering guidance. It does not provide patent clearance or approval to release an unaudited payload.

## Application and managed libraries

Sonumio source and contributions use MIT. Preserve [LICENSE](../../LICENSE) when redistributing source.
LibVLCSharp and LibVLCSharp.Avalonia 3.10.2 declare LGPL-2.1-or-later.
The managed [license text](https://github.com/videolan/libvlcsharp/blob/3.10.2/LICENSE) governs their redistribution.

Keep the binding assemblies separate and replaceable. Keep native libVLC dynamically linked.
Do not merge, statically link, or package the libraries in a way that prevents replacement with compatible modified versions.
Application terms must permit user modification and reverse engineering to debug modifications as required by LGPL 2.1 section 6.

Library binary distribution needs an applicable source-delivery mechanism.
Supply the matching library source, including modifications and required build material, under LGPL 2.1 sections 0 and 4.
For a combined application, also satisfy section 6. Dynamic loading alone does not satisfy all these obligations.
See [LGPL 2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).
A generic upstream link does not establish compliance for an exact binary build.

## Native candidates and binary terms

The audited candidates are VideoLAN.LibVLC.Windows 3.0.24 and VideoLAN.LibVLC.Mac 3.1.3.2.
The [inventory](native-audit/native-files.tsv) lists every native library and import library with its module license and evidence.
It includes 20 files with explicit GPL-2.0-or-later module declarations.
Both package metadata records declare LGPL-2.1-or-later, which does not describe every included plugin.

Select GPL-3.0-or-later terms for combined binary releases that include these GPL plugins.
Keep MIT for Sonumio source. Preserve each upstream component's license and notices.
This policy does not relicense third-party libraries or establish compatibility with every linked dependency.
No LGPL-only plugin set is approved. Removing the known GPL files alone is insufficient.

Before distribution, identify linked components and collect exact corresponding source, dependency sources, patches, and build material.
For a GPL release, implement the applicable [GPLv3 section 6](https://www.gnu.org/licenses/gpl-3.0.html#section6) delivery method.
For downloads, plan equivalent access to corresponding source from the same release location.
Include installation information when section 6 requires it. Do not substitute a general source homepage or an unsupported source offer.
The [audit release requirements](native-audit/README.md#decision-and-release-requirements) remain mandatory.

## Linux

Use the distribution's libVLC and plugins. Sonumio does not redistribute native Linux libraries in the current plan.
Record the tested distribution and libVLC version during backend integration.
Distribution maintainers supply their native package sources and license notices.
Sonumio must still satisfy the licenses of its own distributed components and any combined work.
A future Flatpak or bundled Linux runtime needs a separate payload audit.

## THIRD-PARTY-NOTICES plan

The release issue must generate `THIRD-PARTY-NOTICES` from the actual platform payload.
No notice file is generated in M0 because no application dependency payload exists.
The notice file must include:

- Component names, exact versions, upstream URLs, and copyright notices.
- Per-file or component license mapping for managed libraries, native libraries, plugins, and auxiliary assets.
- Full applicable license texts, including MIT, LGPL, GPL, and licenses of linked dependencies.
- A prominent notice of LGPL library use and instructions for replacing compatible library versions.
- The chosen binary distribution terms and the location of matching corresponding source.
- Modification notices and installation information when required.

Include this material in each archive or installer and expose its location from the application.
Archive the payload inventory and source bundle with the release.
The candidate NuGet archives do not contain complete license and notice files. Add those files before redistribution.

## Codec patents

Copyright license compliance does not establish patent clearance.
[VideoLAN's legal guidance](https://www.videolan.org/legal.html) describes its position under French law.
That position does not grant Sonumio a patent license or decide obligations in other territories.
The release owner must assess the actual codecs, intended territories, and distribution model before a binary release.
This audit makes no finding about royalties or the validity of a particular codec patent.

## Current state

No libVLC, LibVLCSharp, or plugin is installed, bundled, or initialized by Sonumio.
The audit inspects candidate archives only. Source-level verification of linked components remains open.
