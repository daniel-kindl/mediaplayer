# Contributing

Read [AGENTS.md](AGENTS.md) first. It applies to humans and agents.

## Development workflow

1. Find or open an issue. Every change starts from an issue.
2. Create a branch from `dev`.
3. Write tests first, then the change.
4. Run `./eng/verify.sh` or `pwsh ./eng/verify.ps1`.
5. Open a pull request to `dev`.

## Branching

| Branch | Purpose |
| --- | --- |
| `main` | Stable. Only release pull requests from `dev`. |
| `dev` | Integration. Feature and fix pull requests target `dev`. |
| `feature/<issue>-<desc>` | New capability. Example: `feature/12-libvlc-backend`. |
| `fix/<issue>-<desc>` | Bug fix. |
| `chore/<issue>-<desc>`, `docs/<issue>-<desc>` | Tooling and documentation. |

Branches are short-lived. Delete them after merge.

## Commits

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<optional scope>): <summary>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `revert`. Use `!` or a `BREAKING CHANGE:` footer for breaking changes.

## Pull requests

- Squash merge only. The pull request title becomes the commit message, so CI checks that it is a Conventional Commit.
- Fill in the pull request template. Include verification output.
- Link the issue (`Closes #N`).
- CI must be green on all four platforms.
- Get independent reviews for architecture, standards, and correctness/tests (see AGENTS.md).

## Tests

See [docs/testing](docs/testing/README.md). Test behavior. Do not test features that do not exist.

## Coding standards

The build enforces them. See `.editorconfig`, `.globalconfig`, and `Directory.Build.props`. A summary is in [docs/development/README.md](docs/development/README.md#enforced-standards).

## Versioning

Nerdbank.GitVersioning computes SemVer from `version.json` and git history. See [docs/development/versioning.md](docs/development/versioning.md).
