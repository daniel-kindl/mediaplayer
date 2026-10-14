# Testing

## Strategy

- Test behavior through public APIs. Do not test private details.
- Write the test first (TDD). Each test must be able to fail.
- Do not test features that do not exist. M0 has no feature tests. The only M0 tests are architecture tests.
- Keep unit tests fast, deterministic, and free of IO, time, and randomness. Inject clocks and random seeds.

## Projects

| Project | Tests for | Kind |
| --- | --- | --- |
| `MediaPlayer.Core.Tests` | `MediaPlayer.Core` | Unit |
| `MediaPlayer.Application.Tests` | `MediaPlayer.Application` | Unit |
| `MediaPlayer.Playback.Tests` | `MediaPlayer.Playback.LibVLC` | Unit; native-library tests are `Integration` |
| `MediaPlayer.Integration.Tests` | Cross-module, file system, native, architecture | Integration, Architecture |

## Categories

Use the xUnit trait `Category`:

| Category | Meaning | Example |
| --- | --- | --- |
| (none) | Unit test. No IO, no native code. | domain rule |
| `Integration` | Touches the file system, processes, native libraries, or several modules. | libVLC loads on this OS |
| `Architecture` | Checks project structure and dependency rules. | `ArchitectureTests` |

Run one category (xUnit v3 on Microsoft.Testing.Platform):

```bash
dotnet test --solution MediaPlayer.slnx -c Release --no-build --filter-trait "Category=Architecture"
dotnet test --solution MediaPlayer.slnx -c Release --no-build --filter-not-trait "Category=Integration"
```

Note: a filter can make a project run zero tests. Projects that already have tests then return exit code 8. Use filters for local work. The verification script runs all tests without a filter.

## Empty test projects

Microsoft.Testing.Platform fails with exit code 8 when a project runs zero tests. Test projects that have no tests yet pass `--ignore-exit-code 8` in their `.csproj`. Remove it when the first test is added.

## Coverage

- Collector: coverlet.MTP (`--coverlet --coverlet-output-format cobertura`). `eng/verify.*` always collects coverage into `TestResults/`.
- HTML report:

  ```bash
  dotnet tool restore
  dotnet tool run reportgenerator -reports:"TestResults/coverage.cobertura.*.xml" -targetdir:coverage-report -reporttypes:"Html;TextSummary"
  ```

- Policy: there is no coverage threshold in M0, because there is no production code. The M0 acceptance issue sets a line-coverage threshold for Core and Application (proposed: 80%) and adds it to `eng/verify.*`. Coverage is a signal, not a goal. Do not write tests only to raise it.

## Results

`eng/verify.*` writes TRX files to `TestResults/`. CI uploads `TestResults/` as the artifact `test-results-<platform>`.
