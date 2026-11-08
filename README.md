# Schematica

Schematica helps AI agents develop electronics illustrations in a consistent style: schematics, conceptual diagrams, waveforms, and related notation, using CircuitikZ and TikZ.

Currently in development. The example-collection workflow is available; the drawing styles are still being developed and tested.

Continuing in a new chat or on another device? Start with [the current checkpoint](context/CURRENT.md). The [context log](context/LOG.md) preserves decisions and open discussions; the repository is the durable handoff.

Start with the [example collections](examples/INDEX.md), including [The Art of Electronics](examples/THE_ART_OF_ELECTRONICS/STYLE.md).

The reusable [Schematica examples workflow](skills/schematica-examples/SKILL.md) can start or resume a collection, record feedback, and preserve useful generated examples after approval. When the skill is installed, try:

> Use $schematica-examples to continue collecting examples for The Art of Electronics.

> Use $schematica-examples to start an example collection from another electronics book.

Link the `skills/schematica-examples` directory into your agent's user skill directory to make it available outside this repository. Keep the link pointed at this checkout; the skill resolves the repository from its physical location. An agent working here can also follow `AGENTS.md` directly.

See [Project direction](DIRECTION.md) for the goals and development approach. Each example record distinguishes user feedback, inferred patterns, and recreation status.
