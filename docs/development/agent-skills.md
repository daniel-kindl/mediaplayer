# External agent skills

External skills are optional. They give workflows, not exemptions. `AGENTS.md`, the issue, and `eng/verify.*` always win. No verification step depends on an AI service or on these skills.

## Sources (reviewed 2026-10-14)

| Source | Repository | Pinned revision | License |
| --- | --- | --- | --- |
| Matt Pocock skills | https://github.com/mattpocock/skills | `49dd158d1076134a641b33efb035946536778336` | MIT |
| pstack (Lauren Tan / poteto) | https://github.com/cursor/plugins/tree/79afd75d5bd51383fbb526b72f36db03180b8301/pstack | `79afd75d5bd51383fbb526b72f36db03180b8301` | MIT (`pstack/LICENSE`) |
| pstack standalone mirror | https://github.com/backnotprop/pstack | `1f0f9c3bac03c4297f6fc8f7644fa412eda57085` | MIT |
| ASD-STE100 Simplified Technical English | https://www.asd-ste100.org/ | Issue 9 (or the current issue) | Copyright ASD. Free on request. Do not copy the rules or dictionary into this repository. |

`poteto/pstack` does not exist as a GitHub repository. The upstream is `cursor/plugins/pstack`.

We reference these sources. We do not copy or vendor them. To use one, install it in your own agent environment at the pinned revision, after you read the files. Do not run remote install scripts (`npx skills add ...`, `curl | sh`) without reading them first.

## Which skill for which task

Use one primary workflow per task. Use a supporting skill only for a specific gap.

| Task | Primary | Supporting (optional) |
| --- | --- | --- |
| Clarify requirements | Matt: `grill-with-docs`, `to-spec` | pstack: `architect` for hard design tradeoffs |
| Split work into issues | Matt: `to-tickets` | GitHub Issues stay the source of truth |
| Implement an issue | Matt: `implement` | pstack: `why` for focused analysis |
| TDD | Matt: `tdd` | Do not run pstack `tdd` at the same time |
| Bug diagnosis | Matt: `diagnosing-bugs` | pstack: `correct` |
| Code review | Matt: `code-review` | pstack: `interrogate`, `blast-radius` |
| Architecture review | pstack: `architect`, `principle-boundary-discipline` | Matt: `improve-codebase-architecture` |
| Knowledge transfer | Repository `docs/knowledge-transfer/` | pstack: `how`, `teach` |
| Documentation | `technical-writing.md` in this folder | pstack: `technical-writing`, `unslop` |

## Conflicts resolved

- Matt `setup-pre-commit` and `git-guardrails-claude-code`: not used. This repository uses `eng/verify.*` and CI. No git hooks.
- pstack `no-comments`: XML documentation on public members is still required (CS1591).
- pstack `typescript-best-practices`: not relevant (C#).
- Any skill that tells you to merge, push to `main`/`dev`, or skip tests: ignore that step.

Skill names change. Check the name at the pinned revision before you use it.
