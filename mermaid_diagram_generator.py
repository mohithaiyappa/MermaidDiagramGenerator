"""Command-line utility to analyze Kotlin and Swift projects for Mermaid diagrams."""
from __future__ import annotations

import argparse
import datetime as _dt
import fnmatch
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Set

LOGGER = logging.getLogger(__name__)

KOTLIN_CLASS_PATTERN = re.compile(r"\b(class|interface|object)\s+(\w+)\s*(?:\:\s*([^\{]+))?", re.MULTILINE)
SWIFT_CLASS_PATTERN = re.compile(r"\b(class|struct|protocol|enum)\s+(\w+)\s*(?:\:\s*([^\{]+))?", re.MULTILINE)
KOTLIN_FUNCTION_PATTERN = re.compile(r"\bfun\s+(?:[A-Za-z0-9_<>@]+\s+)?(\w+)\s*\(([^)]*)\)")
SWIFT_FUNCTION_PATTERN = re.compile(r"\bfunc\s+(?:[A-Za-z0-9_<>@]+\s+)?(\w+)\s*\(([^)]*)\)")
CALL_PATTERN = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\s*\(')

CONTROL_KEYWORDS = {
    "if",
    "guard",
    "switch",
    "when",
    "for",
    "while",
    "repeat",
    "do",
    "try",
}

DEFAULT_TEST_DIR_NAMES = {
    "test",
    "tests",
    "__tests__",
    "androidTest",
    "iosTest",
    "commonTest",
    "uiTest",
    "uitest",
    "UITest",
    "UITests",
    "UnitTest",
    "UnitTests",
    "integrationTest",
    "IntegrationTests",
    "spec",
    "Specs",
    "mocks",
}

DEFAULT_DEMO_DIR_NAMES = {
    "example",
    "examples",
    "sample",
    "samples",
}

KEYWORD_EXCLUSIONS = CONTROL_KEYWORDS | {
    "return",
    "class",
    "struct",
    "enum",
    "protocol",
    "object",
    "fun",
    "func",
    "package",
    "import",
    "val",
    "var",
    "let",
}


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze Kotlin and Swift projects to generate JSON summaries and prompts "
            "for Mermaid diagram creation."
        )
    )
    parser.add_argument(
        "--input-path",
        required=True,
        help="Path to the repository or module to analyze.",
    )
    parser.add_argument(
        "--output-json",
        default="diagram_data.json",
        help="Destination file for the generated JSON summary.",
    )
    parser.add_argument(
        "--output-prompt",
        default="diagram_prompt.txt",
        help="Destination file for the generated prompt text.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Additional glob pattern to exclude (can be specified multiple times).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging output for debugging.",
    )
    return parser.parse_args(argv)


@dataclass
class FunctionInfo:
    name: str
    parameters: List[str]
    file: str
    language: str
    body: str
    calls: Set[str] = field(default_factory=set)
    control_structures: List[str] = field(default_factory=list)


class ProjectAnalyzer:
    def __init__(self, input_path: str, exclude_patterns: Sequence[str]):
        self.input_path = os.path.abspath(input_path)
        self.exclude_patterns = list(exclude_patterns)
        self.class_entries: List[Dict[str, object]] = []
        self.relationships: List[Dict[str, str]] = []
        self.functions: List[FunctionInfo] = []
        self.sequence_interactions: List[Dict[str, str]] = []
        self.flow_nodes: List[Dict[str, str]] = []
        self.platforms: Set[str] = set()
        self.packages: Dict[str, Set[str]] = {"kotlin": set(), "swift": set()}
        self.file_count = 0

    def analyze(self) -> Dict[str, object]:
        LOGGER.info("Starting analysis for %s", self.input_path)
        for dirpath, dirnames, filenames in os.walk(self.input_path):
            dirnames[:] = [
                d
                for d in dirnames
                if not self._should_skip(os.path.join(dirpath, d))
            ]
            rel_dir = os.path.relpath(dirpath, self.input_path)
            LOGGER.debug("Scanning directory: %s", rel_dir)
            for filename in filenames:
                language = self._detect_language(filename)
                if not language:
                    continue
                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, self.input_path)
                if self._should_exclude_file(rel_path):
                    LOGGER.debug("Excluded file: %s", rel_path)
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except OSError as exc:
                    LOGGER.error("Failed to read %s: %s", rel_path, exc)
                    continue
                LOGGER.info("Processing %s", rel_path)
                self.file_count += 1
                if language == "kotlin":
                    self.platforms.add("android-kotlin")
                    self._process_kotlin_file(rel_path, content)
                elif language == "swift":
                    self.platforms.add("ios-swift")
                    self._process_swift_file(rel_path, content)
        LOGGER.info("Completed analysis. Processed %d files", self.file_count)
        return self._build_output()

    def _should_skip(self, dir_path: str) -> bool:
        rel_path = os.path.relpath(dir_path, self.input_path)
        if rel_path == os.curdir:
            return False
        normalized = rel_path.replace(os.sep, "/")
        basename = os.path.basename(dir_path)
        if basename.startswith("."):
            LOGGER.debug("Skipping hidden directory: %s", normalized)
            return True
        segments = [segment.lower() for segment in normalized.split("/")]
        for idx, segment in enumerate(segments):
            if segment in DEFAULT_TEST_DIR_NAMES:
                LOGGER.debug("Skipping test directory: %s", normalized)
                return True
            if idx == 0 and segment in DEFAULT_DEMO_DIR_NAMES:
                LOGGER.debug("Skipping demo directory: %s", normalized)
                return True
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(normalized, pattern):
                LOGGER.debug("Skipping excluded directory %s by pattern %s", normalized, pattern)
                return True
        return False

    def _should_exclude_file(self, rel_path: str) -> bool:
        normalized = rel_path.replace(os.sep, "/")
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(normalized, pattern):
                return True
        return False

    @staticmethod
    def _detect_language(filename: str) -> Optional[str]:
        if filename.endswith((".kt", ".kts")):
            return "kotlin"
        if filename.endswith(".swift"):
            return "swift"
        return None

    def _process_kotlin_file(self, rel_path: str, content: str) -> None:
        package_match = re.search(r"^\s*package\s+([\w\.]+)", content, flags=re.MULTILINE)
        if package_match:
            self.packages["kotlin"].add(package_match.group(1))
        self._extract_classes(
            language="kotlin",
            rel_path=rel_path,
            matches=KOTLIN_CLASS_PATTERN.finditer(content),
        )
        functions = self._extract_functions(
            language="kotlin",
            rel_path=rel_path,
            matches=KOTLIN_FUNCTION_PATTERN.finditer(content),
            content=content,
        )
        self.functions.extend(functions)

    def _process_swift_file(self, rel_path: str, content: str) -> None:
        module_match = re.search(r"^\s*@?import\s+([\w\.]+)", content, flags=re.MULTILINE)
        if module_match:
            self.packages["swift"].add(module_match.group(1))
        self._extract_classes(
            language="swift",
            rel_path=rel_path,
            matches=SWIFT_CLASS_PATTERN.finditer(content),
        )
        functions = self._extract_functions(
            language="swift",
            rel_path=rel_path,
            matches=SWIFT_FUNCTION_PATTERN.finditer(content),
            content=content,
        )
        self.functions.extend(functions)

    def _extract_classes(
        self,
        *,
        language: str,
        rel_path: str,
        matches: Iterable[re.Match[str]],
    ) -> None:
        for match in matches:
            class_type = match.group(1)
            name = match.group(2)
            inherits = [part.strip() for part in (match.group(3) or "").split(",") if part.strip()]
            class_info = {
                "name": name,
                "type": class_type,
                "language": language,
                "file": rel_path,
            }
            if inherits:
                class_info["inherits"] = inherits
                for parent in inherits:
                    relation = {
                        "source": name,
                        "target": parent,
                        "type": "extends" if class_type in {"class", "struct"} else "implements",
                        "file": rel_path,
                    }
                    self.relationships.append(relation)
            self.class_entries.append(class_info)

    def _extract_functions(
        self,
        *,
        language: str,
        rel_path: str,
        matches: Iterable[re.Match[str]],
        content: str,
    ) -> List[FunctionInfo]:
        functions: List[FunctionInfo] = []
        for match in matches:
            name = match.group(1)
            params_raw = match.group(2)
            params = [param.strip() for param in params_raw.split(",") if param.strip()]
            body = self._extract_block(content, match.end())
            function = FunctionInfo(
                name=name,
                parameters=params,
                file=rel_path,
                language=language,
                body=body,
            )
            function.calls = self._detect_calls(body)
            function.control_structures = self._detect_control_structures(body)
            for call in sorted(function.calls):
                self.sequence_interactions.append(
                    {
                        "caller": name,
                        "callee": call,
                        "file": rel_path,
                        "language": language,
                    }
                )
            for structure in function.control_structures:
                self.flow_nodes.append(
                    {
                        "function": name,
                        "description": f"{structure} detected in {name}",
                        "file": rel_path,
                        "language": language,
                        "type": "decision" if structure in {"if", "when", "switch", "guard"} else "process",
                    }
                )
            if not function.control_structures:
                self.flow_nodes.append(
                    {
                        "function": name,
                        "description": f"Sequential logic in {name}",
                        "file": rel_path,
                        "language": language,
                        "type": "process",
                    }
                )
            functions.append(function)
        return functions

    @staticmethod
    def _extract_block(content: str, start_index: int) -> str:
        length = len(content)
        index = start_index
        while index < length and content[index].isspace():
            index += 1
        if index >= length:
            return ""
        if content[index] == '{':
            depth = 0
            block_chars: List[str] = []
            while index < length:
                char = content[index]
                block_chars.append(char)
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        index += 1
                        break
                index += 1
            return "".join(block_chars)
        # expression-bodied function
        end_line = content.find("\n", index)
        if end_line == -1:
            return content[index:]
        return content[index:end_line]

    @staticmethod
    def _detect_calls(body: str) -> Set[str]:
        calls: Set[str] = set()
        for call_match in CALL_PATTERN.finditer(body):
            identifier = call_match.group(1)
            if identifier not in KEYWORD_EXCLUSIONS:
                calls.add(identifier)
        return calls

    @staticmethod
    def _detect_control_structures(body: str) -> List[str]:
        structures: List[str] = []
        for keyword in CONTROL_KEYWORDS:
            if re.search(rf"\b{keyword}\b", body):
                structures.append(keyword)
        return structures

    def _build_output(self) -> Dict[str, object]:
        metadata = {
            "project_name": os.path.basename(self.input_path.rstrip(os.sep)),
            "timestamp": _dt.datetime.utcnow().isoformat() + "Z",
            "input_path": self.input_path,
            "platforms": sorted(self.platforms),
            "file_count": self.file_count,
            "packages": {
                language: sorted(values)
                for language, values in self.packages.items()
                if values
            },
        }
        class_diagram = {
            "classes": self.class_entries,
            "relationships": self.relationships,
            "functions": [
                {
                    "name": function.name,
                    "parameters": function.parameters,
                    "file": function.file,
                    "language": function.language,
                    "calls": sorted(function.calls),
                }
                for function in self.functions
            ],
        }
        sequence_diagram = {"interactions": self.sequence_interactions}
        flowchart = {"nodes": self.flow_nodes}
        return {
            "metadata": metadata,
            "class_diagram": class_diagram,
            "sequence_diagram": sequence_diagram,
            "flowchart": flowchart,
        }


def write_json(path: str, data: Dict[str, object]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    LOGGER.info("JSON summary written to %s", path)


def write_prompt(path: str, data: Dict[str, object]) -> None:
    metadata = data.get("metadata", {})
    project_name = metadata.get("project_name", "Unknown Project")
    platforms = ", ".join(metadata.get("platforms", [])) or "unspecified"
    summary = (
        f"Mermaid Diagram Generator Output\n"
        f"Project: {project_name}\n"
        f"Analyzed Platforms: {platforms}\n"
        f"Timestamp: {metadata.get('timestamp', 'n/a')}\n\n"
        "Instructions for using this data with an LLM such as ChatGPT:\n"
        "1. Provide the JSON summary to the model and request a Mermaid class diagram using the `class_diagram` section.\n"
        "2. Ask for a sequence diagram highlighting the interactions listed under `sequence_diagram.interactions`.\n"
        "3. Request a flowchart based on the decision and process nodes in `flowchart.nodes`.\n"
        "4. For large projects, focus on one module or package at a time using the `metadata.packages` information.\n"
        "5. Encourage the model to include notes about assumptions if the extracted data omits implementation specifics.\n\n"
        "Example prompt:\n"
        "Using the attached JSON, generate a Mermaid class diagram summarizing the primary classes and their relationships."
        " Then produce sequence and flowchart diagrams that align with the documented interactions and decision nodes."
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(summary)
    LOGGER.info("Prompt text written to %s", path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_arguments(argv)
    configure_logging(args.verbose)
    input_path = os.path.abspath(args.input_path)
    if not os.path.exists(input_path):
        LOGGER.error("Input path does not exist: %s", input_path)
        return 1
    analyzer = ProjectAnalyzer(input_path, args.exclude)
    data = analyzer.analyze()
    try:
        write_json(os.path.abspath(args.output_json), data)
        write_prompt(os.path.abspath(args.output_prompt), data)
    except OSError as exc:
        LOGGER.error("Failed to write output files: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
