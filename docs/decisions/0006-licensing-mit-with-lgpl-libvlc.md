# 0006. MIT application code with LGPL libVLC

- Status: Proposed. The native dependency and redistribution audit issue must confirm it.
- Date: 2026-10-14

## Context

The application code is MIT. LibVLCSharp is LGPL-2.1-or-later. libVLC core is LGPL-2.1-or-later. Some VLC plugins are GPL-2.0-or-later.

## Decision

Keep application code MIT. Link libVLC dynamically. Do not modify libVLC. Ship only plugins whose licenses are compatible with distribution next to MIT code, or distribute the whole binary package under terms that allow the GPL plugins. The audit issue decides the plugin set.

## Consequences

See `docs/development/licensing.md`. Until the audit is done, no build artifact includes libVLC.
