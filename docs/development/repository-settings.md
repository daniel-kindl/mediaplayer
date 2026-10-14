# Recommended repository settings

This file records the repository settings. The pull request settings and the branch rulesets (`protect-main`, `protect-dev`) are applied. Apply the remaining General settings in GitHub Settings if they are not on yet.

## General

- Default branch: `main`.
- Pull requests: allow **squash merge only**. Default commit message: pull request title and description.
- Automatically delete head branches: on.
- Private vulnerability reporting: on (Settings > Code security).
- Dependabot alerts and security updates: on.
- Secret scanning and push protection: on.
- Actions > General > Workflow permissions: **Read repository contents**. Do not allow Actions to approve pull requests.

## Branch rulesets

One ruleset applies to `main` (`protect-main`) and one to `dev` (`protect-dev`):

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
| Allowed merge methods | squash | squash |
| Bypass list | repository admin (always) | repository admin (always) |

Required status checks:

- `verify (linux-x64)`
- `verify (windows-x64)`
- `verify (macos-arm64)`
- `verify (macos-x64)`
- `pr-title (Conventional Commits)`
- `dependency-review`

Required approvals are 0 because the project has one maintainer, and GitHub does not let an author approve their own pull request. Independent agent reviews (architecture, standards, correctness/tests) and green CI are the gate. If a second maintainer joins, set required approvals to 1.

## Exceptions

The repository admin (the owner) can bypass the rulesets. Use the bypass for small, low-risk changes or emergencies. Agents do not bypass the rules: their work lands through a pull request with green CI.

## Labels

Created by the bootstrap: `type:*`, `area:*`, `priority:*`, `milestone:M0`, `status:blocked`. See `.github/labels.md`.
