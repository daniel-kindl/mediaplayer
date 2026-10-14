# Licensing

This is engineering guidance, not legal advice. The native dependency and redistribution audit issue must confirm it before the first binary release.

## Application code

MIT ([LICENSE](../../LICENSE)). Contributions are accepted under MIT.

## LibVLCSharp

LGPL-2.1-or-later. It is a managed library that the application references. Obligations when we distribute it:

- Ship the LGPL text and a notice.
- Let users replace the LibVLCSharp assembly with a modified version. Normal dynamic loading of a separate DLL meets this. Do not merge, IL-weave, or trim it in a way that blocks replacement.
- If we modify LibVLCSharp, publish the modified source.

## libVLC (native core)

`libvlc` and `libvlccore` are LGPL-2.1-or-later. Link dynamically. Ship the license and a source offer (or a link to the exact upstream source version). Do not statically link.

## Native VLC plugins

Plugins have different licenses. Many are LGPL. Some are GPL-2.0-or-later (some demuxers, filters, and codecs that use GPL libraries). Also, some codecs can have patent issues in some countries.

If a distributed package includes a GPL plugin, the distribution as a whole must meet the GPL. MIT code can be combined with GPL code, but the combined binary is then distributed under GPL terms.

Options for the audit:

1. Ship only LGPL (and more permissive) plugins. The binary package stays non-GPL.
2. Ship the full plugin set and distribute the binary package under GPL-2.0-or-later. The source stays MIT.

## Native redistribution

- Windows and macOS: VideoLAN NuGet packages contain prebuilt libVLC and plugins. The audit lists every included plugin and its license.
- Linux: use the distribution's libVLC. The application does not ship libVLC on Linux unless the audit decides otherwise (for example in a Flatpak).
- Every binary release includes `THIRD-PARTY-NOTICES` with all native and managed licenses.

## Current state (M0)

No libVLC, LibVLCSharp, or plugin is installed, bundled, or initialized.
