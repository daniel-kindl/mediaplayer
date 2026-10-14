# 0005. Versioning with Nerdbank.GitVersioning

- Status: Accepted
- Date: 2026-10-14

## Context

Builds must have deterministic SemVer versions. The maintainer already uses Nerdbank.GitVersioning (NBGV) in other repositories.

## Decision

Use NBGV 3.10.94 for all projects. `version.json` holds major.minor and the prerelease tag. NBGV adds the git height as the patch number. Only `main` and `v*` tags produce public (non-commit-suffixed) versions. No other versioning system is used.

## Consequences

- Builds need full git history. CI checks out with `fetch-depth: 0`. The verify scripts fail on shallow clones.
- Release process: see `docs/development/versioning.md`.
