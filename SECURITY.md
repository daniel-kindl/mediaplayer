# Security policy

## Supported versions

The project is in pre-release (M0). Only the latest commit on `main` receives security fixes.

## Report a vulnerability

Do not open a public issue for a vulnerability.

Use GitHub private vulnerability reporting: **Security** tab > **Report a vulnerability** on https://github.com/daniel-kindl/mediaplayer. If that is not available, contact the maintainer through the GitHub profile https://github.com/daniel-kindl.

Include:

- the affected version or commit,
- steps to reproduce,
- the impact that you expect.

You will get a first answer in 7 days, if possible.

## Scope notes

- Vulnerabilities in libVLC or its plugins are upstream issues. Report them to VideoLAN as well: https://www.videolan.org/security/.
- Malformed media files are untrusted input. A crash or memory corruption from a media file is a security issue.

## Automation

- Dependabot updates NuGet packages, GitHub Actions, and the .NET SDK.
- `eng/verify.*` fails on known-vulnerable NuGet packages (direct and transitive).
- NuGet audit runs on every restore. Warnings are errors.
- Pull requests run GitHub dependency review.
- All workflow actions are pinned to commit SHAs. Workflows use `contents: read` by default.
