# Symbol implementation checkpoint

This folder implements the locally authorized first batch described in
`CHECKPOINT.md`. The accepted palette in `references/accepted-palette/` overrides
older blanket wire-relative normalization for this implementation. Size and stroke
are independent. Existing preferences, examples, and their links remain intact.

The user accepted the rendering proof and authorized six appearances and 54
configurations. On 13-11-2026 they authorized the browsing-first UI revision,
single SVG export, six-symbol library export at the chosen size/stroke, compact
docs and a static build for a public-by-link Cloudflare preview. They subsequently
accepted the result and explicitly authorized publishing the reviewed build.
Build 971b3b876b93 is now published; see CHECKPOINT.md for the URLs and verification.
The user subsequently explicitly authorized committing and pushing this completed
implementation and its docs to the existing GitHub repository. That releases the
first-batch Git hold. Further implementation or website publication needs its own
scope authorization; this approval is not an automatic-deploy policy.
No connections, personal variants, in-app creation or schematic editor.

After every implementation run, update CHECKPOINT.md with what changed, how the
user opens the result, numbered tests with expected results, checks actually run,
known limits and pending review. Keep DEVELOPMENT.md commands current. The user
must be able to assess the change without reconstructing the chat or reading code.

Geometry lives in parameterized TeX recipes. YAML describes semantics and supported
presets. The Python core compiles and packages converter output; it must not become
a second symbol-drawing backend. Read `README.md` and `CHECKPOINT.md` on resume.
