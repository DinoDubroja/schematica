# First-release readiness

**Historical audit:** the state below refers to `40be8ef`, not the latest checkout.
The [11-11-2026 repository review](MCP_TRANSITION_REVIEW.md) supersedes its inventory:
seven rules, a Windows Codex installer, and automated tests now exist. The agreed
first-release direction now includes MCP integration for Claude Desktop and
OpenAI/ChatGPT, a minimal visual catalogue, and isolated user-data testing; see
[DIRECTION.md](../DIRECTION.md#agreed-first-release-direction). Retain the quality
goals below, but use [CURRENT.md](CURRENT.md) for the active next step.

Reviewed: 08-11-2026, against checkout `40be8ef` and the user's first-release criteria.

**Verdict: not ready for a public first release.** The reference library, preference bank, and collection workflow exist. Repeatable style generation, synthetic validation, complete reference pictures, and installation for a new user remain unfinished.

This is an audit and proposed sequence, not authorization to implement new style parameters, drawings, or preferences. The user's instruction not to infer style generalization during image collection remains active.

## Required outcome

- The Art of Electronics style works on several new tasks, including generalization from the existing Thevenin reference to a Norton-equivalent explanation.
- Reviewed good synthetic examples preserve their prompts, editable sources, previews, feedback, and validation evidence.
- General preferences produce attractive generic drawings and can grow through suggestions, visual comparisons, interviews, or corrections during normal use.
- The repository is attractive and easy to browse, with visible pictures for every collected reference and a small selected showcase.
- Another user can install and use Schematica without this chat or the maintainer's personal configuration.

## Current state and gaps

| Area | Verified state | Before release |
| --- | --- | --- |
| AOE implementation | Qualitative, provisional guidance. Five recreations use individual TikZ paths inside CircuitikZ. No shared numeric preset or component template is tracked. | Approve concrete parameters and implement one reusable preset for native components, text, lines, symbols, spacing, and annotations. Keep approved general preferences inherited and any style exceptions explicit. |
| Validation | All 31 example records have reference origin; none is a generated/synthetic case. A separate output-stage trial is not in the versioned collection. | Run new-prompt trials, review technical correctness and appearance, save approved good cases, and demonstrate correction handling. Historical tracing/compilation is not proof of generalization. |
| General preferences | Three accepted rules: supply arrows, hollow signal terminals, and junction dots with a 10:1 diameter-to-wire-width ratio. Suggestions and explicit approval are already documented. | Review candidates for ground symbols, typography/value sizing, label clearance, wire routing/crossings, spacing/alignment, and overall layout. Adopt only approved choices, each with a visual good example and optional bad example. |
| Reference pictures | 31 records; five have LaTeX, SVG, and PNG. The other 26 have no repository image. | Import original screenshots unchanged; show each in its example page and category gallery. Optional recreation must not block image availability. |
| Presentation | Small SVG showcase and category navigation exist. Preference galleries validate successfully. Current categories hold 15 schematic, 1 plot, and 15 mixed records. | Select showcase favorites, subdivide crowded galleries as pictures arrive, and inspect navigation and rendering on GitHub in both themes. Originals retain their white backgrounds; recreations use the existing light/dark SVG route. |
| Installation | A repository-owned skill exists, with links resolved through its physical checkout. No public installation procedure, dependency manifest, installer, or clean-install evidence is tracked. | Pick an initial supported agent/host; document checkout, skill registration, TeX/CircuitikZ/font dependencies, Python/PyMuPDF, invocation, and troubleshooting. Verify the documented procedure from a clean environment. |
| User customization | General/style precedence exists; personal customization and storage are explicitly still undesigned. | Define how a new user's overrides and examples are saved without altering shared defaults unintentionally or losing them during updates. |
| Release packaging | No license, release tag, changelog, CI workflow, or committed automated test suite is tracked. | Choose the project license and which externally sourced assets belong in the public distribution; declare supported versions, add proportionate automated checks, tag the reviewed release, and verify remote publication. |

## Small validation set

These are proposed prompts, not completed or approved examples.

1. **Norton equivalent:** Create a schematic explaining the concept, using the existing Thevenin illustration as a composition reference. Check current-source/parallel-resistance topology and equivalent terminal behavior independently of visual similarity.
2. **Practical amplifier:** Draw a noninverting amplifier with supplied values, terminals, and supplies. Check exact connections, polarity, identifiers, values, readable labels, and inherited general rules.
3. **Circuit and waveform:** Explain an RC circuit with a corresponding signal sketch and compact annotation. Check that circuit, labels, and waveform convey the same behavior.

Also render the practical-amplifier task without a named style to review the general defaults. This can reuse the circuit specification.

For each trial, record the original prompt, inputs/references, style version, first result, meaningful corrections, final source and previews, technical checks, and actual user review status. Inspect both light/dark exports for contrast, hollow interiors, clipping, and overlaps. A successful compile is necessary but does not establish correctness or beauty. Mark a saved result as a good synthetic example only after user acceptance; it has `Origin: generated`.

## Proposed order

1. Complete the already-authorized original-image import and gallery visibility. This is currently blocked on transferring image files, not on LaTeX work.
2. Obtain authorization for style consolidation; use the screenshots as evidence to propose parameters, then review a compact calibration drawing. Do not recreate all references.
3. Implement the approved preset and run the three trials above. Use concrete corrections to propose the next general preferences; the user may also choose short visual interviews.
4. Save the accepted synthetic cases and approved rules; refine the showcase and category pages. Preserve unapproved suggestions separately from defaults.
5. Finish supported installation, user customization, dependency/version documentation, automated checks, license/distribution decisions, and a clean-environment first-prompt trial.
6. Verify the final repository and remote state, then publish a versioned release after authorization.

An editor integration, support for every agent host, recreation of all 31 references, and a comprehensive style for every electronics artifact are not proposed first-release prerequisites.

## Verification and outstanding access

- Inspected tracked files, style/domain guides, example origins, preference index, workflow, scripts, and root README.
- Ran `python scripts/build_preference_galleries.py --check`: current galleries and local references passed.
- Repository-wide Markdown references and original-asset preservation are checked separately at handoff and recorded in the context log.
- No fresh compile, synthetic trial, clean installation, or live GitHub theme review was performed in this audit.
- The authorized image download failed before any transfer with `hosted apps tools/list request failed: DNS`. No original screenshot was imported. The ignored `build/aoe-reference-import/` folder is available for locally supplied originals; filenames must be matched against visible figure captions before publication.
- Git pushes from this executor have failed with `getaddrinfo() thread failed to start`. Local commits are not evidence that GitHub contains them.

[Current checkpoint](CURRENT.md) · [Project direction](../DIRECTION.md) · [All AOE examples](../styles/THE_ART_OF_ELECTRONICS/examples/README.md)
