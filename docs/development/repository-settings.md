# Recommended repository settings

These settings are **not applied** by the bootstrap. A maintainer must apply them in GitHub Settings. They are documented here so that the configuration is reviewable.

## General

- Default branch: `main`.
- Pull requests: allow **squash merge only**. Default commit message: pull request title and description.
- Automatically delete head branches: on.
- Private vulnerability reporting: on (Settings > Code security).
- Dependabot alerts and security updates: on.
- Secret scanning and push protection: on.
- Actions > General > Workflow permissions: **Read repository contents**. Do not allow Actions to approve pull requests.

## Branch rulesets

Apply one ruleset to `main` and one to `dev`:

| Setting | `main` | `dev` |
| --- | --- | --- |
| Require pull request | yes | yes |
| Required approvals | 0 (see below) | 0 |
| Dismiss stale approvals on push | yes | yes |
| Require conversation resolution | yes | yes |
| Required status checks (strict, up to date) | see list | see list |
| Block force pushes | yes | yes |
| Block deletion | yes | yes |
| Require linear history | yes | yes |
| Bypass list | none | none |

Required status checks:

- `verify (linux-x64)`
- `verify (windows-x64)`
- `verify (macos-arm64)`
- `verify (macos-x64)`
- `pr-title (Conventional Commits)`
- `dependency-review`

Required approvals are 0 because the project has one maintainer, and GitHub does not let an author approve their own pull request. Independent agent reviews (architecture, standards, correctness/tests) and green CI are the gate. If a second maintainer joins, set required approvals to 1.

## Exceptions

Nobody bypasses the rules. If an emergency needs a bypass, open an issue that records the reason, the change, and the follow-up, before the bypass.

## Labels

Created by the bootstrap: `type:*`, `area:*`, `priority:*`, `milestone:M0`, `status:blocked`. See `.github/labels.md`.
