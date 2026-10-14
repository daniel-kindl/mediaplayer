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

Add these only in the issue that implements the feature, after the license audit:

| Package | Latest stable (2026-10-14) | License | Milestone issue |
| --- | --- | --- | --- |
| Avalonia, Avalonia.Desktop, Avalonia.Themes.Fluent | 12.1.4 | MIT | Avalonia application shell |
| LibVLCSharp | 3.10.2 | LGPL-2.1-or-later | libVLC backend |
| LibVLCSharp.Avalonia | check | LGPL-2.1-or-later | rendering. Check Avalonia 12 support first. |
| VideoLAN.LibVLC.Windows | 3.0.24 | LGPL-2.1-or-later (plugins vary) | libVLC backend (Windows) |
| VideoLAN.LibVLC.Mac | check | LGPL-2.1-or-later (plugins vary) | libVLC backend (macOS) |
| Linux libVLC | system package (`libvlc-dev`/`vlc`) | LGPL/GPL per plugin | libVLC backend (Linux). No official NuGet package. |

## Vulnerability checks

- NuGet audit on every restore (`NuGetAuditMode=all`, level `low`). Warnings are errors.
- `eng/verify.*` runs `dotnet package list --vulnerable --include-transitive`.
- GitHub dependency review on pull requests.
- Dependabot: NuGet, GitHub Actions, .NET SDK. Weekly, to `dev`.

## SBOM

Deferred. Generate an SBOM when the first release pipeline exists (for example with `CycloneDX` for .NET or `microsoft/sbom-tool`). The lock files are the authoritative inventory until then.
