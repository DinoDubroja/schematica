# Current status

13-11-2026. **New-project cleanup reviewed and accepted by the user for GitHub
synchronization.** Website deployment and further feature work are separate actions.

The same repository and Git history remain. Main was fast-forwarded to published
baseline `e97aa17` before restructuring. The original working copy, both worktrees,
Git refs/history and meaningful ignored files were backed up and verified outside
the checkout. The laptop's intervening documentation commits are preserved in
history, with their relevant results carried forward below.

The active layout is `app/`, `tests/`, `docs/`, `context/`, with a short README,
root developer guide and new-project agent instructions. Legacy instructions and
assets are archived; nothing loads them automatically. Only documented geometry
and serialization regression fixtures are retained.

Verified locally:

- 25 tests pass; static build `971b3b876b93` and website ZIP match the published
  version byte for byte. All 486 generated standalone-TeX files match the archive.
- All 54 configurations freshly compile with identical catalog and SVG geometry;
  independent Inkscape checks pass 42 palette comparisons and nine library round
  trips. Maximum palette coordinate deviation is 0.00124 mm (tolerance 0.005 mm).
- Native CircuitikZ and bounded editable-label edit/save/reopen pass.
- All 54 browser configurations, dark/light persistence, search, grid toggle,
  export-dialog focus and actual single/library downloads pass. No horizontal
  overflow in the checked desktop/narrow layouts.
- Documentation links/anchors pass; README and developer pages were rendered and
  inspected. Windows launcher works from the root. A repository-only recovery
  audit found no actionable issue or dependency on removed legacy material.
- A separate source copy with a new virtual environment and only runtime
  requirements passes all 25 tests, builds the same website and launches correctly.
  This checks clean app setup on this computer, not another Windows installation.

The earlier laptop setup report (Git commit `9f4673f`) records build 971b3b876b93,
25 tests, a fresh coil render, nine Inkscape library round trips and focused local
Chrome/download checks. These are reported results from that device, not tests
rerun during cleanup. Dark Reader overrode its light palette; a browser without
extensions displayed it correctly. The old preference skill was installed there;
it is not an instruction source for the new project.

Still unverified: the updated checkout on the laptop, the full hosted two-device
checklist, clean-machine/offline TeX setup, profile-wide Inkscape Symbols installation
and a new grid-snapping GUI walkthrough. Existing GUI evidence is archived, not
presented as a fresh test.

Start with [the developer guide](../DEVELOPMENT.md) for changes, commands and
action → expected result checks. [Roadmap](../docs/ROADMAP.md) separates implemented,
partial, missing and deferred work; [decisions](DECISIONS.md) records current scope.
Next: update the existing laptop checkout and follow the developer guide's review
checklist. No missing product capabilities are being implemented in this run.
