# New Schematica

- Read [current status](context/CURRENT.md), then the relevant part of
  [DEVELOPMENT.md](DEVELOPMENT.md). Consult [decisions](context/DECISIONS.md) when
  scope or precedence matters.
- This checkout contains the new symbol app. Legacy preferences, AOE collections,
  installers and skills are archived outside it. Do not load their instructions,
  including an older installed Schematica skill, as defaults for this project.
  Consult archived material only for a specific, justified reuse task.
- Preserve the accepted UI and geometry. Parameterized TeX is the drawing
  authority; YAML holds semantics and presets. Python packages converter output.
  Size and stroke remain independent on the accepted 1 mm connection grid.
- Keep app code in `app/`, tests and essential fixtures in `tests/`, human guides
  and images in `docs/`. Generate bundles and ZIPs into ignored build output.
- After each implementation run, update the developer guide's latest review with
  changes, action → expected result checks, actual results and unverified limits.
  Keep context concise; record decisions rather than a transcript.
- Check branch/index/files before changes; preserve concurrent work. Run the
  [applicable checks](DEVELOPMENT.md#test-and-review) and verify links after moves.
- Commit, push and deploy only within the user's current authorization. Source
  synchronization and website deployment are separate actions. Missing capabilities
  in the roadmap are not authorization to implement them.
