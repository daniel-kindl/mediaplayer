# 0002. Module layout and dependency direction

- Status: Accepted
- Date: 2026-10-14

## Context

The player has three volatile technologies (Avalonia, libVLC, OS APIs) and a stable center (domain and use cases). The bootstrap specification defines five source projects.

## Decision

Use the five projects in `docs/architecture/README.md`. Dependencies point inward (ports and adapters). Enforce the allowed project references with architecture tests that read `.csproj` files.

The projects are empty in M0. Ports are added only when a feature needs them.

## Consequences

- The UI and libVLC can be replaced or tested in isolation.
- Five projects add some build overhead. This is accepted because the spec requires them and the boundaries are cheap to keep now and expensive to add later.
- Moving a reference across a boundary requires a new ADR and a change to the architecture test.
