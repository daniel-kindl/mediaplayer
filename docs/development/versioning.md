# Versioning and releases

- SemVer 2.0. Nerdbank.GitVersioning computes the version from `version.json` (`0.1-alpha`) and the git height.
- `main` and `vX.Y.Z` tags give public versions. Other branches add a commit suffix (for example `0.1.5-alpha-g1a2b3c4`).
- Check the version: `dotnet tool run nbgv get-version` (the `nbgv` local tool is pinned in `.config/dotnet-tools.json`; run `dotnet tool restore` first).

## Release process (when releases start)

1. Open a pull request from `dev` to `main` with title `chore(release): vX.Y.Z`.
2. In that pull request, update `version.json` if the major or minor version changes, and remove the prerelease tag for a stable release.
3. After merge, tag the merge commit `vX.Y.Z` on `main`.
4. Breaking changes (`feat!`, `BREAKING CHANGE:`) increase the major version (minor while in 0.x).

M0 has no release or publish workflow. That is deliberate.
