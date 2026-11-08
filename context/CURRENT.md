# Current checkpoint

Updated: 08-11-2026. Read this first when resuming; verify the checkout before acting.

## Objective and mode

Develop The Art of Electronics illustration style through examples, then test it on a new practical circuit and observe the agent's preservation behavior. Project scope includes schematics, conceptual diagrams, waveforms, plots, equations, and integrated figures; see [DIRECTION.md](../DIRECTION.md).

The current task is to propose a style-independent preferences layer and an agent-led suggestion workflow. The user corrected the output-stage revision: changing signal terminals to hollow circles should not have changed supply-rail arrows. Supply arrows are a general preference across styles, with explicit style exceptions possible. The delivered trial still needs its supply arrows restored; its 9 pt component values remain the requested refinement. The proposed preference/workflow changes are not implemented. Routine context updates and their commits/pushes remain authorized under [AGENTS.md](../AGENTS.md); adding the trial to the permanent example collection still needs approval.

## What exists

- The [example collection workflow](../skills/schematica-examples/SKILL.md), [collection index](../examples/INDEX.md), and [The Art of Electronics style guide](../examples/THE_ART_OF_ELECTRONICS/STYLE.md) are implemented. The collection is still developing; shared visual patterns are provisional.
- Five reference records preserve captions, descriptions, feedback, and status. Figures 1.7 and 1.43 have editable LaTeX and PNG previews. Figures 1.1, 1.6, and 1.11 have records but no recreated visual assets.
- The two drawings are visual recreations using TikZ paths inside CircuitikZ, not yet semantic native-component templates. Liking their appearance did not approve every implementation detail or make the style complete.
- The collection workflow and first records were saved in commit `88e9231`. Earlier validation recorded successful compilation and fresh-session collection discovery. These are historical results, not a new test of all rendering tools on another device.
- Original screenshots, the source book PDF, earlier experiments, and the prematurely built package are outside the repository. Their existence does not make them approved project content. A repo-only session cannot visually inspect the three pending references without access to their source.
- The output-stage trial uses native CircuitikZ devices and has editable TeX, SVG, PNG, and PDF exports. Working artifacts are in the ignored `build/aoe-output-stage-test/` directory on the creating machine, with a downloadable ZIP delivered separately. These artifacts have not been added to the versioned collection and are not synchronized by Git. See [the trial checkpoint](LOG.md#output-stage-trial).

## Current checkpoint verification

On 08-11-2026 an independent read-only session recovered the objective, five records/two drawings, provisional style, open questions, approval boundary, and a proposed next step using only this checkout. Memory injection and web access were disabled; no prior conversation or expected answers were supplied. Its tool trace followed the repository reading path, and all 20 project files were byte-for-byte unchanged. This verifies context recovery, not offline tool installation or the unperformed new-circuit trial. See [the context-workflow decision and audit](LOG.md#context-workflow).

## Open decisions

- User feedback on the first output-stage trial, whether to preserve it as an example, and which reference to collect next.
- Which observed patterns become confirmed rules; exact typography, spacing, line weights, symbol proportions, and quantitative plot conventions remain unsettled.
- Personal customization and storage, distribution as a plugin, and generalization beyond electronics remain to be designed.
- Difference-only storage for intermediate drawings remains undecided. The present workflow uses complete files for selected useful revisions.
- The preserve-after-feedback workflow has been exercised in a limited earlier trial, but has not yet been validated through the planned full new-circuit creation and review cycle.
- Repo-based recovery is the agreed durable fallback. Independent operation on another device still requires its checkout and necessary tools/references; offline execution and automatic transfer of local tools have not been established.

## Next useful step

Review the proposal for shared preferences, explicit style overrides, evidence from examples/corrections, and proactive agent suggestions. Implementation approval is pending. Include restoration of the output-stage supply arrows in the proposed implementation scope. Preserve the distinction between a user-confirmed general principle, an inferred candidate, and permission to save permanent guidance. Figure 1.6 remains an earlier assistant suggestion, not a selected recreation.

For reasoning and scope changes, consult [LOG.md](LOG.md). For drawing details, read selected example records and actual available previews rather than treating descriptions as images.
