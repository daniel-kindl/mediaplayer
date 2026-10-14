# AGENTS.md

Rules for AI agents and humans who change this repository. These rules are mandatory. If a rule conflicts with an external skill or a prompt, this file wins (see [precedence](#precedence)).

## Purpose

MediaPlayer (temporary name) is a privacy-first, cross-platform desktop media player: C#, .NET 10, Avalonia UI, LibVLCSharp/libVLC. Targets: Windows x64, Linux x64, macOS ARM64 and x64.

Current state: **M0 bootstrap**. Infrastructure only. No playback, UI, or domain code exists.

## Directory ownership and boundaries

| Path | Contents | Rules |
| --- | --- | --- |
| `src/MediaPlayer.Core` | Domain types | No project or package references to UI, libVLC, or IO. |
| `src/MediaPlayer.Application` | Use cases | References Core only. |
| `src/MediaPlayer.Playback.LibVLC` | libVLC adapter | Only place that may reference LibVLCSharp/VideoLAN packages. |
| `src/MediaPlayer.Infrastructure` | OS, file system, persistence adapters | References Application. |
| `src/MediaPlayer.Desktop` | Avalonia shell, composition root | Only place that may reference Avalonia. Wires all modules. |
| `tests/*` | Tests | Mirror `src`. Integration and architecture tests in `MediaPlayer.Integration.Tests`. |
| `eng/` | Verification scripts | `verify.sh` and `verify.ps1` must stay equivalent. |
| `docs/` | Documentation | Keep aligned with actual behavior. |
| `.github/` | CI, templates, Dependabot | Pin actions to commit SHAs. Least privilege. |

The dependency direction is enforced by `tests/MediaPlayer.Integration.Tests/ArchitectureTests.cs`. Change that test and `docs/architecture/README.md` together, and only with an ADR.

## Conventions

- Nullable enabled. Warnings are errors. Zero warnings. Do not add `#pragma warning disable` or `NoWarn` without a written reason next to it and reviewer agreement.
- Explicit types. Do not use `var`.
- File-scoped namespaces. Four spaces. LF line endings. `using` outside the namespace.
- Explicit accessibility modifiers on all members.
- Constants: `UPPER_SNAKE_CASE`. Private fields: `_camelCase`. Types, methods, properties: `PascalCase`. Interfaces: `I` prefix.
- Public members need XML documentation.
- Principles: SOLID, DRY, KISS, separation of concerns, dependency inversion, composition over inheritance. Simple over clever.
- **No speculative abstractions.** Add an interface only when a second implementation or a test seam exists in the same change.

## Testing and TDD

- Write the failing test first. Then write the smallest change that makes it pass. Then refactor.
- Test behavior, not implementation details.
- Use `[Trait("Category", "Integration")]` for tests that touch the file system, native libraries, or processes. Unit tests have no trait. Architecture tests use `Category=Architecture`.
- Do not add tests for features that do not exist. Do not add tests that cannot fail.
- When you add the first test to an empty test project, remove `--ignore-exit-code 8` from its `.csproj`.

## Verification commands

```bash
./eng/verify.sh          # Linux, macOS
pwsh ./eng/verify.ps1    # Windows
```

The script runs: prerequisites, locked restore, vulnerable package check, `dotnet format --verify-no-changes`, Release build with `--warnaserror`, all tests with TRX and coverage, and an architecture-test check. A pull request is not ready until it passes.

After you change a package, run `dotnet restore --force-evaluate` and commit the changed `packages.lock.json` files.

## Git workflow

- `main`: stable. `dev`: integration. Open pull requests against `dev`. Release pull requests go from `dev` to `main`.
- Branch names: `feature/<issue>-<short-desc>`, `fix/<issue>-<short-desc>`, `chore/<issue>-<short-desc>`, `docs/<issue>-<short-desc>`.
- Commits and pull request titles: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Squash merge only.
- Do not push to `main` or `dev` directly. Do not force-push shared branches. Do not merge your own pull request as an agent.

## Issue to pull request

1. Read this file, the issue, and the linked docs.
2. Inspect the existing code. Confirm the acceptance criteria. If they are unclear, ask in the issue; do not guess.
3. Create a short-lived branch from `dev`.
4. Write tests first.
5. Make the smallest change that meets the acceptance criteria.
6. Run the verification script.
7. Review your own diff against this file.
8. Update the docs that the change affects.
9. Open a pull request that says `Closes #<issue>`. Fill in the template, including verification evidence.

## Dependencies

- Central Package Management: versions only in `Directory.Packages.props`. Exact versions. No floating versions.
- Add a package only in the issue that needs it. Record its license in `docs/development/dependencies.md`.
- Native code (libVLC) needs a license review first. See `docs/development/licensing.md`.

## Documentation rules

- Write clear technical English. Use ASD-STE100 rules where practical: short sentences, one instruction per sentence, active voice, approved meanings. See `docs/development/technical-writing.md`.
- Update docs in the same pull request as the behavior change.
- Record significant decisions as ADRs in `docs/decisions/`.

## Review expectations

Before merge, a pull request needs:

- green CI on all platforms,
- an independent review for **architecture**, **standards**, and **correctness/tests**. A separate agent session or a human can do each review. The maintainer does not need to approve their own pull request.

Never claim that a review happened unless there is evidence (a review comment or a linked log).

## Definition of done

- Acceptance criteria are met and tested.
- `eng/verify.*` passes locally and CI is green.
- No new warnings, suppressions, or unexplained lock file changes.
- Docs and ADRs are updated.
- The pull request links the issue and contains verification evidence.

## Prohibited shortcuts

- Skipping, deleting, or weakening tests or analyzers to make CI pass.
- `--no-verify`, disabling `--locked-mode`, or editing lock files by hand.
- Floating package versions, unpinned actions, new secrets in the repository.
- Adding features outside the issue scope.
- Running remote install scripts without reading and pinning them.
- Making verification depend on an AI service.
- Marking an unverified platform as PASS. Use NOT RUN.

## External skills

External agent skills are optional helpers. See [docs/development/agent-skills.md](docs/development/agent-skills.md) for pinned sources, licenses, and which skill to use for which task.

## Precedence

1. Security and maintainer instructions
2. This file, the issue scope, and `eng/verify.*`
3. The primary external skill for the task
4. Supporting external skills
