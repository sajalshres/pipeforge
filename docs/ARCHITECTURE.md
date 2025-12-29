# PipeForge Architecture (POC)

PipeForge keeps a minimal, vendor-neutral model and plugs parsers/renderers around it so new CI targets can be added without changing the CLI.

## Core

- `pipeforge/models.py` - Internal IR (`Pipeline`, `Job`, `Step`) shared by all parsers/renderers.
- `pipeforge/transpiler.py` - Orchestrates reading files, parsing into the IR, and rendering to a target.
- `pipeforge/errors.py` - Small error hierarchy for CLI-friendly messaging.

## Extensibility

- Parsers live in `pipeforge/parsers/` and produce the IR from vendor-specific specs. The default is `BambooSpecParser`.
- Renderers live in `pipeforge/renderers/` and emit YAML for CI systems (`bitbucket`, `gitlab`, `github` today).
- Registries (`ParserRegistry`, `RendererRegistry`) keep a slug -> implementation map so adding a provider only requires registering a new class.

### Adding a new source parser

1. Create `pipeforge/parsers/<provider>.py` subclassing `BaseParser`.
2. Implement `.parse(raw: dict, name_override: str | None)` to return a `Pipeline`.
3. Register it in `default_parser_registry()` with a unique `slug`.

### Adding a new renderer

1. Create `pipeforge/renderers/<provider>.py` subclassing `BaseRenderer`.
2. Implement `.render(pipeline: Pipeline) -> str` returning YAML.
3. Register it in `default_renderer_registry()` and note any default output filename in `output_hint`.

## CLI

The Click-based CLI (`pipeforge/cli.py`) exposes:

- `pipeforge list` - show supported sources/targets.
- `pipeforge convert <input> --target <slug> [--source <slug>] [-o <file>] [--name <name>]`

The CLI does not assume a single source; it defers to the registered parsers/renderers so you can add Bitbucket or other sources later and reuse the same surface area. Each renderer currently exports variables as shell `export KEY="VALUE"` statements to keep the generated files runnable without extra configuration during the POC phase.
