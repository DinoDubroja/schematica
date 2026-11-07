# Project direction

Schematica aims to enable AI agents to automatically create beautiful, useful electronic schematics with CircuitikZ from text prompts, sketches, or screenshots. It is intended for engineering documentation, papers, teaching, and in-chat discussions with ChatGPT or other AI agents.

It should be available for anyone to use in their agent environment and work well from the first prompt.

It should come with consistent, predefined drawing preferences. Users should be able to modify and save their preferences without having to establish everything from scratch. The user's circuit connections, component names, and supplied values should be preserved.

## Development approach

- Recreate selected good schematics in CircuitikZ so the examples themselves provide guidance.
- Compare examples from the same circuit category, infer recurring design patterns, and document the agreed lessons.
- Use realistic circuits and functional subsystems for demonstrations.
- Provide prompts and inputs users can run with and without Schematica to compare results themselves.
- Document useful examples and conclusions as development progresses.

During discussions, present schematics inline by default, blending into the chat where supported. Explicit requests for another format or save location take precedence.

How personal preferences are stored and how multiple templates would be managed remain open decisions.
