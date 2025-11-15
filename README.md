# Mermaid Diagram Generator

This repository contains a single-file Python utility, `mermaid_diagram_generator.py`, that inspects native mobile projects
(Kotlin/Android and Swift/iOS) and extracts structural information to accelerate Mermaid diagram creation.

## Requirements
- Python 3.9 or later
- No additional third-party dependencies

## Usage
Run the script from the command line, pointing it at the root directory of the project or module you want to analyze:

```bash
python mermaid_diagram_generator.py --input-path /path/to/mobile/project \
  --output-json diagram_data.json --output-prompt diagram_prompt.txt \
  --output-format json
```

### Options
- `--input-path` (required): Root path to analyze.
- `--output-json`: Destination for the generated summary (default: `diagram_data.json`). Parent directories are created automatically if they don't exist.
- `--output-format`: Choose `json` (default) or `yaml` for the summary output.
- `--output-prompt`: Destination for the generated prompt guidance (default: `diagram_prompt.txt`). Parent directories are created automatically if they don't exist.
- `--exclude`: Additional glob pattern(s) to skip (can be provided multiple times).
- `--verbose`: Enable debug logging for deeper insight during execution.

## Outputs
- **Summary data (JSON or YAML)** – Contains project metadata, class and function details, inferred relationships,
  sequence interactions, and flow-oriented nodes.
- **Prompt text** – Ready-to-use instructions you can paste into an LLM (e.g., ChatGPT) together with the summary data to generate
  Mermaid class, sequence, and flowchart diagrams.

Both outputs are deterministic for the same input source tree, making them suitable for CI environments like Jenkins.

To emit YAML instead of JSON, supply `--output-format yaml` and point `--output-json` at a `.yaml` (or `.yml`) file.

## Example run against a small Android project

The repository includes a miniature Android-style project under `fixtures/android_sample` so you can exercise the
generator without cloning an external dependency:

```bash
python mermaid_diagram_generator.py \
  --input-path fixtures/android_sample \
  --output-json fixtures/android_sample/diagram.json \
  --output-prompt fixtures/android_sample/prompt.txt \
  --output-format json \
  --verbose
```

When network access is available you can swap in any public Android project, for example the
[`android/kotlin-android-template`](https://github.com/android/kotlin-android-template) sample:

```bash
git clone https://github.com/android/kotlin-android-template.git
python mermaid_diagram_generator.py \
  --input-path kotlin-android-template \
  --output-json kotlin_template.json \
  --output-prompt kotlin_template_prompt.txt \
  --output-format json \
  --verbose
```

If you need to omit large modules or known test fixtures, provide additional `--exclude` patterns.

## Multi-module Android fixture

To test more complex structures without external repositories, the `fixtures/android_multi_module` sample mimics a
multi-module Android app with an application module plus `core` and `feature` libraries. The profile feature alone
contains over twenty Kotlin source files so you can validate traversal depth and module relationships.

```bash
python mermaid_diagram_generator.py \
  --input-path fixtures/android_multi_module \
  --output-json fixtures/android_multi_module/diagram.json \
  --output-prompt fixtures/android_multi_module/prompt.txt \
  --output-format json \
  --verbose
```
