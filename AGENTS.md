# New Schematica

- Read [current status](context/CURRENT.md), then the relevant part of
  [DEVELOPMENT.md](DEVELOPMENT.md). Consult [decisions](context/DECISIONS.md) when
  scope or precedence matters.
- This checkout contains the new symbol app. Legacy preferences, AOE collections,
  installers and skills are archived outside it. Do not load their instructions,
  including an older installed Schematica skill, as defaults for this project.
  Consult archived material only for a specific, justified reuse task.
- Integration work: read [agent setup and checks](docs/AGENT_INTEGRATION.md) and
  [host evidence](docs/HOST_VERIFICATION.md). Current search/creation skills live
  in `.agents/skills/`; they are separate from B's batch workflow. Creation/save
  tests require an explicitly initialized isolated store. Never equate protocol
  or browser checks with embedded-host verification.
- Preserve the accepted UI and geometry. Parameterized TeX is the drawing
  authority; YAML holds semantics and presets. Python packages converter output.
  Size and stroke remain independent on the accepted 1 mm connection grid.
- Before a symbol batch, reuse the [construction reference](docs/SYMBOL_REFERENCE.md)
  and [batch workflow](docs/RESISTOR_BATCH.md#repeatable-creation-workflow).
  Refine representatives before production; visually compare related designs and
  crowded Small/Thick cases. Render/check every declared option combination before
  promotion, even though Variations compares one setting per row.
- Keep app code in `app/`, tests and essential fixtures in `tests/`, human guides
  and images in `docs/`. Generate bundles and ZIPs into ignored build output.
- Keep the developer guide's latest review current using the
  [delivery checklist](DEVELOPMENT.md#delivery-checklist). Keep context concise;
  record decisions rather than a transcript.
- Maintain context after consequential discussions as well as implementation.
  Record the source chat and original turn/message timestamp with timezone, status
  and any superseding decision; keep review time separate. Read actual accessible
  chat messages when reconciling context. Git being clean does not establish chat
  coverage. Preserve pending topics when concurrent work prevents shared writes.
- New designs enter Unverified after technical and visual checks. Apply human
  approvals only through the [verification handoff](docs/VERIFICATION.md). Geometry
  or connection changes require fresh review; never copy an old approval forward.
- Check branch/index/files before changes; preserve concurrent work. Run the
  [applicable checks](DEVELOPMENT.md#test-and-review) and verify links after moves.
- Parallel work: `work/agent-b-symbols` belongs to symbol work; Agent A uses
  `work/agent-a-integration` in a separate checkout. Read the current ownership
  note and [parallel-work guide](DEVELOPMENT.md#parallel-work) before editing.
  Integrate only exact commits marked READY FOR INTEGRATION in the owner's
  handoff, never an assumed branch tip. Do not switch another agent's checkout.
- Before declaring work finished, complete the
  [delivery checklist](DEVELOPMENT.md#delivery-checklist) and report blocked items.
  Agent A coordinates integration. Branch pushes, main updates and deployments
  are separate actions within the current authorization; do not add approval
  pauses for actions already authorized. Roadmap gaps do not authorize new work.
