# Dependencies

All versions are in `Directory.Packages.props` (Central Package Management, transitive pinning). Lock files: `**/packages.lock.json`.

## Installed (M0)

| Package | Version | License | Used by | Why |
| --- | --- | --- | --- | --- |
| Nerdbank.GitVersioning | 3.10.94 | MIT | all projects (build only, `PrivateAssets=all`) | SemVer from git |
| xunit.v3 | 4.0.2 | Apache-2.0 | tests | test framework and MTP runner |
| coverlet.MTP | 10.1.0 | MIT | tests | coverage |

Transitive packages are listed in the lock files. Check them with:

```bash
dotnet package list --project Sonumio.slnx --include-transitive
```

## Planned (NOT installed)

The [native audit](native-audit/README.md) records the candidate payloads and their license evidence.
Candidate versions below were checked on 2026-10-15. They are not installed or approved for binary redistribution.

Add these only in the issue that implements the feature, after the license audit:

| Package | Candidate version | License | Milestone issue |
| --- | --- | --- | --- |
| Avalonia, Avalonia.Desktop, Avalonia.Themes.Fluent | 12.1.4 | MIT | Avalonia application shell |
| LibVLCSharp | 3.10.2 | LGPL-2.1-or-later | libVLC backend |
| LibVLCSharp.Avalonia | 3.10.2 | LGPL-2.1-or-later | Rendering. Upstream confirms Avalonia 12 support. Project placement needs an ADR. |
| VideoLAN.LibVLC.Windows | 3.0.24 | LGPL-2.1-or-later core, GPL-2.0-or-later plugins also present | libVLC backend (Windows). 968 native files inventoried. |
| VideoLAN.LibVLC.Mac | 3.1.3.2 | LGPL-2.1-or-later core, GPL-2.0-or-later plugins also present | libVLC backend (macOS). VLC 3.0.24, x64 and ARM64. 606 native files inventoried. |
| Linux libVLC | system package (`libvlc-dev`/`vlc`) | LGPL/GPL per plugin | libVLC backend (Linux). No official NuGet package. |

The native inventory records module licenses. Licenses of linked components and auxiliary assets still need source-level verification before release.
Combined binary releases with GPL plugins use GPL-3.0-or-later terms under [ADR 0006](../decisions/0006-licensing-mit-with-lgpl-libvlc.md).
Sonumio source remains MIT. Linux uses system libVLC. Flatpak and bundled Linux runtimes are deferred.

## Vulnerability checks

- NuGet audit on every restore (`NuGetAuditMode=all`, level `low`). Warnings are errors.
- `eng/verify.*` runs `dotnet package list --vulnerable --include-transitive`.
- GitHub dependency review on pull requests.
- Dependabot: NuGet, GitHub Actions, .NET SDK. Weekly, to `dev`.

## SBOM

Deferred. Generate an SBOM when the first release pipeline exists (for example with `CycloneDX` for .NET or `microsoft/sbom-tool`). The lock files are the authoritative inventory until then.
