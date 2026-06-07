# Tasks

Active work board for this project.

Update this file when you start a task, finish a task, or discover a blocker.
See [`.agent-workflow.md`](.agent-workflow.md) for the full workflow and format guide.

Always re-read this file immediately before editing it so you do not work from stale task state.

---

## In Progress

_No tasks in progress._

## Ready For Review

- [Codex]: Add guided installation wizard
  - Branch: codex/install-wizard
  - Review assigned to: Claude or Copilot
  - Implementation notes:
    - Added `scripts/install.py`, a stdlib Python wizard for new-project scaffolds and append-to-existing installs.
    - Added repository scanning, mode recommendation, tool selection, dry-run, confirmation, `--yes`, `--force`, and optional README updates.
    - Added `tests/test_install_wizard.py` for scanner, planner, and apply behavior.
    - Documented guided installer usage in `README.md`.
    - Verified with `python3 -m unittest tests/test_install_wizard.py`.
    - Verified new-project apply mode under `/private/tmp/pitcrew-preview-apply`.
    - Verified append-mode dry run against `/Users/mgzwarrior/dev/mgz-pkmn`.

- [Codex]: Remove backlog task list and add fresh `TASKS.md` read rule
  - Implementation notes:
    - Removed the `Backlog` section from `TASKS.md`.
    - Updated workflow docs so `docs/roadmap.md` owns planned work and `TASKS.md` only tracks active work state.
    - Added instructions for agents to re-read `TASKS.md` immediately before relying on or editing task status.
    - Updated README, shared agent instructions, tool-specific instructions, and Claude personas to match the simplified model.

## Blocked

_No blocked tasks._

## Done

_No completed tasks yet._
