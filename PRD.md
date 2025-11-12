# Mermaid Diagram Generator Script PRD

## 1. Product Overview
The Mermaid Diagram Generator Script is a command-line Python utility that analyzes native mobile codebases (Android/Kotlin and iOS/Swift) to extract structural information and produce diagram-ready data. By walking the project directory, the script generates a consolidated JSON description of relevant classes, interfaces, and key call flows while omitting test sources. The JSON output and a companion prompt text file equip large language models (LLMs) such as ChatGPT to quickly render Mermaid diagrams (class, sequence, and flowchart) that document the application's architecture.

## 2. Goals and Objectives
- Provide an automated way to summarize native mobile projects into a format that LLMs can consume for diagram generation.
- Support Jenkins and other CI environments so teams can refresh architecture documentation on demand.
- Ensure outputs are consistent, well-structured, and easy to upload or reference when crafting Mermaid diagrams.
- Deliver the capability as a self-contained single Python file that can be dropped into any repository or CI job without additional packaging steps.

## 3. Target Audience & Personas
- **Mobile Tech Lead (Maya):** Needs architecture diagrams for design reviews and onboarding engineers without manually tracing code.
- **DevOps Engineer (Devon):** Integrates the script into CI pipelines (e.g., Jenkins) to keep system documentation current.
- **Consultant (Carlos):** Audits client codebases and delivers quick visual summaries using LLM-generated diagrams.

## 4. User Stories
1. As a mobile tech lead, I can run the script against a Kotlin/Android or Swift/iOS project and receive a JSON file describing the code structure suitable for Mermaid diagrams.
2. As a user, I can optionally provide an output directory and receive both the JSON artifact and a pre-populated prompt text file that guides an LLM to create class, sequence, and flowchart diagrams.
3. As a developer, I can point the script at the root of an individual Android or iOS module so that the resulting JSON focuses on that module's production code.
4. As a DevOps engineer, I can execute the script in Jenkins with a single command that accepts an input path and produces deterministic outputs.
5. As a user, I can trust that test files and directories are excluded from the analysis to keep diagrams focused on production code.
6. As a consultant, I can run the script repeatedly on different client repositories without additional configuration.

## 5. Functional Requirements
### 5.1 Command-Line Interface
- Implement the solution as a single Python script with no external dependencies beyond the standard library where feasible.
- Distribute the script as one physical file (e.g., `mermaid_diagram_generator.py`) that encapsulates argument parsing, project traversal, JSON generation, and prompt creation logic.
- Accept mandatory input arguments:
  - `--input-path` (or positional equivalent) pointing to the root of the module or repository to analyze.
- Accept optional arguments:
  - `--output-json` to specify the target JSON file path (default: `diagram_data.json` in the current working directory).
  - `--output-prompt` to specify the prompt text file path (default: `diagram_prompt.txt`).
  - `--exclude` to accept additional glob patterns or directories to ignore beyond built-in test exclusions.
- Exit with non-zero status codes on invalid arguments or processing failures to integrate cleanly with CI pipelines.

### 5.2 Project Analysis
- Traverse the provided input path, detecting whether the project is Android/Kotlin, iOS/Swift, or a mixed repository.
- Parse relevant source files:
  - Kotlin: `.kt` and `.kts` files under `src/main`, `app/src/main`, or similar production directories.
  - Swift: `.swift` files under `Sources`, `App`, or app module directories.
- Exclude test directories by default (`src/test`, `src/androidTest`, `src/commonTest`, `*/Tests`, `*/Test`, `*/UITests`, etc.).
- Capture structural elements needed for diagramming, such as:
  - Class and interface names, inheritance/implementation relationships, and key properties or methods for class diagrams.
  - Significant function calls, message passing, and asynchronous flows to inform sequence diagrams.
  - High-level module or package boundaries, data paths, and decision points to support flowchart generation.
- Organize extracted data into a normalized schema suitable for all three diagram types, including metadata about relationships and interactions, with sufficient granularity for LLMs to synthesize complete diagrams without additional reverse-engineering.

### 5.3 Output Generation
- Produce a JSON file containing:
  - Project metadata (name, platform(s), timestamp, analyzed module path).
  - Arrays for classes/interfaces, relationships, function interactions, process flows, and any conditional logic captured during traversal.
  - Clear keys and consistent casing to simplify downstream parsing by LLMs.
  - Diagram-type specific sections (e.g., `class_diagram`, `sequence_diagram`, `flowchart`) that aggregate the elements most relevant to each Mermaid representation.
- Generate a prompt text file that:
  - Describes the purpose of the JSON artifact.
  - Provides example instructions/questions tailored for class, sequence, and flowchart Mermaid diagrams.
  - Suggests how to handle large outputs (e.g., chunking or focusing on modules).
- Ensure output files are deterministic given the same input repository state.

### 5.4 Jenkins & CI Compatibility
- Ensure the script runs via `python script_name.py --input-path <path>` without requiring interactive input.
- Emit informative logging to stdout/stderr, including progress indicators and summary statistics (e.g., files scanned, classes discovered).
- Support execution on typical Jenkins agents (Linux/macOS) without special setup.

## 6. Non-Functional Requirements
- Complete analysis of medium-sized mobile projects (up to ~5k source files) within a reasonable CI time budget (target under 10 minutes).
- Use efficient file traversal to minimize I/O overhead and avoid loading entire files into memory when unnecessary.
- Maintain readability and maintainability through clear function decomposition and inline documentation.
- Provide predictable behavior across different Python 3.9+ environments.
- Keep all runtime behavior within a single-file artifact to simplify change control and Jenkins deployment.

## 7. Success Metrics
- Teams can generate accurate Mermaid diagrams via LLMs using the produced JSON and prompt with minimal manual editing.
- Jenkins jobs incorporating the script complete successfully on the first run in at least 90% of pilot projects.
- Reduction of manual diagramming effort by at least 50% as reported by initial users within the first month.

## 8. Assumptions & Dependencies
- Source projects follow common Android and iOS directory conventions, enabling heuristics to differentiate production from test code.
- Python 3.9 or later is available in environments where the script runs.
- LLM providers (e.g., ChatGPT) can process the generated JSON within their input limits.

## 9. Open Questions
- Should the script attempt lightweight parsing (e.g., using regex) or leverage AST tooling for Kotlin and Swift while remaining dependency-light?
- How should mixed-language modules (e.g., shared Kotlin Multiplatform code) be represented in the JSON schema?
- What level of detail is most useful for sequence diagrams (e.g., include asynchronous callbacks, networking layers)?

## 10. Milestones
1. **Milestone 1 – CLI & Directory Traversal (Week 1):** Implement argument parsing, Jenkins-friendly logging, and recursive traversal with test directory exclusion.
2. **Milestone 2 – Parsing & JSON Schema (Weeks 2-3):** Extract class structures and interactions for Kotlin/Swift files and define the normalized JSON format.
3. **Milestone 3 – Prompt Generation & Validation (Week 4):** Produce the prompt template, validate outputs on sample Android/iOS projects, and document usage instructions.
