# 0004. Testing: xUnit v3 on Microsoft.Testing.Platform

- Status: Accepted
- Date: 2026-10-14

## Context

The .NET 10 SDK `dotnet test` no longer supports VSTest mode for projects that use Microsoft.Testing.Platform (MTP). xUnit v3 is built on MTP.

## Decision

- `xunit.v3` 4.0.2 as the test framework, MTP as the runner (`global.json` `test.runner`).
- `coverlet.MTP` for coverage (Cobertura). It is MIT licensed and works offline.
- xUnit v3 native TRX output (`--report-xunit-trx`).
- No `Microsoft.NET.Test.Sdk` and no `xunit.runner.visualstudio`. They are only needed for VSTest.

## Consequences

- Empty test projects return MTP exit code 8 ("zero tests"). Projects without tests pass `--ignore-exit-code 8` in their `.csproj`, with a comment to remove it when the first test is added. A project that has tests keeps the default and fails when its tests disappear.
- Some IDE test explorers need MTP support enabled.
