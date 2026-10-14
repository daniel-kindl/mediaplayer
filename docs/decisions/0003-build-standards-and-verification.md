# 0003. Build standards and single verification script

- Status: Accepted
- Date: 2026-10-14

## Context

The repository must be deterministic and independently verifiable on three operating systems, by humans, agents, and CI.

## Decision

- Pin the SDK in `global.json` (`10.0.402`, `rollForward: latestPatch`).
- Central Package Management with exact versions, transitive pinning, and committed `packages.lock.json` files. CI restores in locked mode.
- `AnalysisMode=All`, `TreatWarningsAsErrors`, `EnforceCodeStyleInBuild`. Style rules in `.editorconfig`. Each suppression has a reason in `.globalconfig`.
- One verification entry point: `eng/verify.sh` with an equivalent `eng/verify.ps1`. CI calls the same scripts.

## Consequences

- Every analyzer warning blocks the build. New analyzer releases can break the build after an SDK update. Dependabot SDK pull requests show this in CI.
- `CA1707` is off because it conflicts with the required `UPPER_SNAKE_CASE` constants.
- Two scripts must stay equivalent. Reviewers check both when one changes.
