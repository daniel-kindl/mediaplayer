# Sonumio

Sonumio is a lightweight, privacy-first, desktop media player, as an alternative to VLC media player. It uses .NET 10, Avalonia UI, and LibVLCSharp/libVLC.

## Development status

**Milestone M0, bootstrap only.** The repository contains build, test, and verification infrastructure. It does not contain a media player yet. The application does not play media and does not open a window. See the [M0 issues](https://github.com/daniel-kindl/sonumio/issues) for planned work.

## Supported platforms

| Platform | Status |
| --- | --- |
| Windows x64 | Target. Verified in CI. |
| Linux x64 | Target. Verified in CI and locally. |
| macOS ARM64 | Target. Verified in CI. |
| macOS x64 | Target. Verified in CI. |

"Verified" means the solution builds and the tests pass. Playback is not implemented on any platform.

## Prerequisites

- .NET SDK `10.0.402` or a later 10.0.4xx patch (see `global.json`)
- git (full history, because versioning uses Nerdbank.GitVersioning)
- bash (Linux, macOS) or PowerShell 7.2+ (all platforms)

## Bootstrap

```bash
git clone https://github.com/daniel-kindl/sonumio.git
cd sonumio
dotnet --version            # must satisfy global.json
dotnet restore --locked-mode
```

## Build

```bash
dotnet build Sonumio.slnx -c Release --no-restore --warnaserror
```

## Test

```bash
dotnet test --solution Sonumio.slnx -c Release --no-build
```

## Verify

Run the full verification before you open a pull request. CI runs the same script.

```bash
./eng/verify.sh      # Linux, macOS
pwsh ./eng/verify.ps1  # Windows (or any platform with PowerShell 7.2+)
```

## Documentation

- [AGENTS.md](AGENTS.md): rules for AI agents and humans
- [CONTRIBUTING.md](CONTRIBUTING.md): workflow, branches, commits, pull requests
- [docs/architecture](docs/architecture/README.md): modules and dependency direction
- [docs/decisions](docs/decisions/README.md): architecture decision records
- [docs/development](docs/development/README.md): environment, tooling, dependencies, licensing
- [docs/testing](docs/testing/README.md): test strategy and coverage
- [SECURITY.md](SECURITY.md): how to report a vulnerability

## License

The application source code is MIT ([LICENSE](LICENSE)). Distributed binaries will include libVLC, which uses other licenses. See [docs/development/licensing.md](docs/development/licensing.md).
