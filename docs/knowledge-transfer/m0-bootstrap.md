# M0 bootstrap: knowledge transfer

Date: 2026-10-14. Scope: repository infrastructure only. No application features.

## Summary

The bootstrap creates an empty, compilable .NET 10 solution with five source projects and four test projects, strict analyzer and style gates, locked dependency restore, one verification script (bash and PowerShell), CI on four platforms, Dependabot, documentation, and the remaining M0 issues.

The whole repository works like this:

1. `global.json` selects SDK 10.0.402 and the Microsoft.Testing.Platform test runner.
2. `Directory.Build.props` applies the same compiler, analyzer, determinism, lock file, and NuGet audit settings to every project, and adds Nerdbank.GitVersioning.
3. `Directory.Packages.props` holds all package versions. `packages.lock.json` files pin the full graph.
4. `.editorconfig` and `.globalconfig` define style and naming. `EnforceCodeStyleInBuild` turns them into build errors.
5. `eng/verify.sh` / `eng/verify.ps1` run every gate in order. CI runs the same scripts on Linux x64, Windows x64, macOS ARM64, and macOS x64.
6. `ArchitectureTests` read the `.csproj` files and enforce the dependency direction.

## Tooling decisions

| Decision | Reason | ADR |
| --- | --- | --- |
| SDK 10.0.402, `rollForward: latestPatch` | Latest stable 10.0 SDK on 2026-10-14. Patch roll-forward gets security fixes without feature-band changes. | 0003 |
| AnalysisMode All + warnings as errors | Strictest available built-in gate. | 0003 |
| CA1707 off | Conflicts with required `UPPER_SNAKE_CASE` constants. | 0003 |
| xUnit v3 on Microsoft.Testing.Platform | .NET 10 `dotnet test` dropped VSTest mode for MTP projects. | 0004 |
| coverlet.MTP | MIT, works with MTP, Cobertura output. | 0004 |
| Nerdbank.GitVersioning | Already used in kexiva. Deterministic SemVer from git. | 0005 |
| Architecture tests read `.csproj` XML | No extra package. Works before any type exists. | 0002 |
| Avalonia, LibVLCSharp not installed | Spec: install only what infrastructure needs. Listed in `docs/development/dependencies.md`. | 0006 |
| Empty `Main` in Desktop | An `Exe` project needs an entry point to compile. It returns 0 and does nothing. | - |
| Local tools `reportgenerator`, `nbgv` | Pinned in `.config/dotnet-tools.json`. Optional, not used by verification. | - |

## Verification evidence

See the pull request description for the full command output. Summary from the bootstrap run on Linux x64 (Debian 13, SDK 10.0.402):

| Check | Result |
| --- | --- |
| `eng/verify.sh` | PASS |
| `eng/verify.ps1` (PowerShell 7.6.7 on Linux) | PASS |
| Locked restore | PASS |
| Vulnerable packages (incl. transitive) | PASS, none |
| `dotnet format --verify-no-changes` | PASS |
| Release build, `--warnaserror` | PASS, 0 warnings, 0 errors |
| Tests | 8 discovered, 8 passed, 0 failed (all architecture tests) |
| Coverage files and HTML report | PASS (no production lines exist yet) |
| Negative check: `var`, block namespace, lowercase constant, missing modifier | Build fails with IDE0008, IDE0161, IDE1006, IDE0040 |
| Negative check: CRLF line ending | `dotnet format` fails (ENDOFLINE) |
| actionlint 1.7.12 on workflows | PASS |
| CI verify, linux-x64 (ubuntu-24.04) | PASS: SDK 10.0.402, 0 warnings, 8/8 tests, architecture check |
| CI verify, windows-x64 (windows-2025, verify.ps1) | PASS: SDK 10.0.402, 0 warnings, 8/8 tests, architecture check |
| CI verify, macos-arm64 (macos-15) | PASS: SDK 10.0.402, 0 warnings, 8/8 tests, architecture check |
| CI verify, macos-x64 (macos-15-intel) | PASS: SDK 10.0.402, 0 warnings, 8/8 tests, architecture check |
| CI pr-title, dependency-review | PASS |

CI evidence: workflow run https://github.com/daniel-kindl/sonumio/actions/runs/38525816201 (pull request #7).

## Known limitations

- Windows and macOS were not run locally (NOT RUN locally). CI ran them and passed.
- No coverage threshold yet. There is no production code.
- No SBOM yet. Lock files are the inventory.
- Branch protection and repository settings are documented, not applied.
- `LibVLCSharp.Avalonia` support for Avalonia 12 is not confirmed.
- Linux has no official libVLC NuGet package. The plan is the system package.

## Deferred work

Tracked as M0 issues: playback contracts, libVLC backend integration, Avalonia application shell and UI, cross-platform rendering validation, native dependency and redistribution audit, M0 acceptance and knowledge transfer. Also deferred: SBOM, coverage threshold, release workflow.
