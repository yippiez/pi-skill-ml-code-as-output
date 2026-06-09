# pi-skill-ml-code-as-output

Standalone Pi skill package for the `ml-code-as-output` workflow.

This skill guides the agent to train small interpretable models and emit the learned structure as readable source code instead of opaque weights.

## Includes

- `skills/ml-code-as-output/SKILL.md` — main skill instructions.
- `skills/ml-code-as-output/ml/` — trainer scripts used as examples/templates.
- Companion docs: `catalog.md`, `dataset.md`, `codegen.md`, and `adding-a-trainer.md`.

## Install from Git

Global install:

```bash
pi install git:github.com/yippiez/pi-skill-ml-code-as-output
```

Local/project install:

```bash
pi install -l git:github.com/yippiez/pi-skill-ml-code-as-output
```

## Package layout

```text
skills/ml-code-as-output/SKILL.md
skills/ml-code-as-output/ml/
package.json
README.md
```
