# Architecture

Status: proposed for M0. No module contains code yet. This document defines responsibilities and boundaries so that the first feature work starts in the correct place.

## Modules

| Project | Responsibility | Must not contain |
| --- | --- | --- |
| `MediaPlayer.Core` | Domain types and rules that do not depend on any technology. | IO, UI, libVLC, threading primitives tied to a UI framework. |
| `MediaPlayer.Application` | Use cases. It coordinates Core and defines the ports (interfaces) that adapters implement. | Avalonia, libVLC, direct file system or OS calls. |
| `MediaPlayer.Playback.LibVLC` | Adapter that implements Application playback ports with LibVLCSharp. | UI code. Business rules. |
| `MediaPlayer.Infrastructure` | Adapters for the OS, file system, settings storage, and other IO. | UI code. libVLC. |
| `MediaPlayer.Desktop` | Avalonia application shell and composition root. It wires adapters to ports. | Business rules. Direct libVLC calls outside the adapter. |

Ports are added only in the issue that needs them (for example, the playback contracts issue). M0 bootstrap adds no interfaces.

## Dependency direction

```
            MediaPlayer.Desktop
           /        |          \
          v         v           v
 Playback.LibVLC  Infrastructure  |
          \         |            /
           v        v           v
          MediaPlayer.Application
                    |
                    v
             MediaPlayer.Core
```

Dependencies point inward. Allowed project references:

| Project | May reference |
| --- | --- |
| Core | nothing |
| Application | Core |
| Playback.LibVLC | Application |
| Infrastructure | Application |
| Desktop | Application, Infrastructure, Playback.LibVLC |

Core is transitively visible to all outer projects.

## Enforcement

`tests/MediaPlayer.Integration.Tests/ArchitectureTests.cs` reads the `.csproj` files and fails when:

- a project in `src/` is not in the table above,
- a project references a project that the table does not allow,
- Core or Application references an Avalonia, LibVLCSharp, or VideoLAN package.

`eng/verify.*` fails if no architecture test ran.

## Boundaries for later work

- Only `Playback.LibVLC` references LibVLCSharp and VideoLAN native packages. Native library initialization happens there, and the composition root starts it.
- Only `Desktop` references Avalonia. ViewModels live in Desktop unless an ADR moves them.
- Native-library tests are integration tests (`Category=Integration`).
