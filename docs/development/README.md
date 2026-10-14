# Development

## Environment setup

1. Install the .NET SDK version in `global.json` (`10.0.402`; a later 10.0.4xx patch also works).
   - Windows/macOS: the official installer from https://dotnet.microsoft.com/download/dotnet/10.0.
   - Linux: your distribution package or the Microsoft package feed. If you use `dotnet-install.sh`, download it, read it, and pin the version: `./dotnet-install.sh --version 10.0.402`.
2. Install git. Clone with full history (no `--depth`).
3. For `eng/verify.ps1`, install PowerShell 7.2 or later.
4. Optional: an IDE with Microsoft.Testing.Platform support (Visual Studio 2026, Rider, or VS Code C# Dev Kit).

No libVLC or Avalonia installation is needed in M0.

## Tooling

| Tool | Version | Where it is configured |
| --- | --- | --- |
| .NET SDK | 10.0.402 (`rollForward: latestPatch`) | `global.json` |
| C# | 14.0 | `Directory.Build.props` |
| Solution format | `.slnx` | `Sonumio.slnx` |
| .NET analyzers | AnalysisLevel 10.0, AnalysisMode All | `Directory.Build.props`, `.globalconfig` |
| Code style | IDE rules, enforced in build | `.editorconfig` |
| Formatting | `dotnet format` (SDK) | `.editorconfig` |
| Versioning | Nerdbank.GitVersioning 3.10.94 | `version.json` |
| Test framework | xUnit v3 4.0.2 on Microsoft.Testing.Platform | `global.json`, `tests/Directory.Build.props` |
| Coverage | coverlet.MTP 10.1.0 | `tests/Directory.Build.props` |

## Enforced standards

The build fails on each of these:

| Rule | ID |
| --- | --- |
| Nullable warnings | CS86xx |
| `var` used | IDE0007/IDE0008 |
| Block-scoped namespace | IDE0161 |
| Missing accessibility modifier | IDE0040 |
| Naming (constants `UPPER_SNAKE_CASE`, `_camelCase` private fields, `I` interfaces, PascalCase types and members, camelCase locals/parameters) | IDE1006 |
| Missing braces | IDE0011 |
| Unnecessary `using` | IDE0005 |
| Formatting | IDE0055, `dotnet format` whitespace (includes LF) |
| Missing XML docs on public members | CS1591 |
| All CA rules (AnalysisMode All) except the suppressions in `.globalconfig` | CAxxxx |

Suppressions and reasons are in `.globalconfig` and `.editorconfig` (`[tests/**.cs]` section).

## Build and verification

```bash
dotnet restore Sonumio.slnx --locked-mode
dotnet build Sonumio.slnx -c Release --no-restore --warnaserror
dotnet test --solution Sonumio.slnx -c Release --no-build
./eng/verify.sh            # or: pwsh ./eng/verify.ps1
```

`eng/verify.*` steps, in order. Each step stops the script on failure:

1. Prerequisites: git, dotnet, SDK satisfies `global.json`, not a shallow clone.
2. `dotnet restore --locked-mode` (once).
3. `dotnet package list --vulnerable --include-transitive` (fails on any finding).
4. `dotnet format --verify-no-changes --severity info`.
5. `dotnet build -c Release --no-restore --warnaserror`.
6. `dotnet test --no-build` with TRX (`TestResults/*.trx`) and Cobertura coverage (`TestResults/coverage.cobertura.*.xml`).
7. Check that architecture tests ran and passed.

When `CI=true`, `RestoreLockedMode` is also forced in MSBuild, so any implicit restore fails if lock files are out of date.

## Related documents

- [dependencies.md](dependencies.md): package inventory and planned packages
- [licensing.md](licensing.md): MIT and libVLC licensing
- [versioning.md](versioning.md): SemVer and releases
- [repository-settings.md](repository-settings.md): recommended branch protection and settings
- [agent-skills.md](agent-skills.md): external agent skills
- [technical-writing.md](technical-writing.md): documentation style
