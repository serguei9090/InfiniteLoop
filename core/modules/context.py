"""
Context Engine - Tree-Sitter based JIT Context Management
PURPOSE: Parse and compress code for LLM injection.
CONTRACT:
- get_skeleton(file_path): Returns class/function headers.
- get_full_compressed(file_path): Returns code without comments/docstrings.
"""

import tree_sitter_python as tspython
import tree_sitter_typescript as tstypescript
import tree_sitter_html as tshtml
import tree_sitter_css as tscss
import tree_sitter_markdown as tsmarkdown
from tree_sitter import Language, Parser, Query, QueryCursor
from pathlib import Path
from typing import List


class ContextEngine:
    def __init__(self):
        self.py_lang = Language(tspython.language())
        self.ts_lang = Language(tstypescript.language_typescript())
        self.html_lang = Language(tshtml.language())
        self.css_lang = Language(tscss.language())
        self.md_lang = Language(tsmarkdown.language())
        self.parser = Parser()

    def get_skeleton(self, file_path: Path) -> str:
        """
        Parses a file and returns its 'skeleton' (classes, functions, methods).
        """
        if not file_path.exists():
            return f"File {file_path.name} not found."

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        suffix = file_path.suffix
        if suffix == ".py":
            self.parser.language = self.py_lang
            return self._parse_python_skeleton(content)
        elif suffix in [".ts", ".tsx"]:
            self.parser.language = self.ts_lang
            return self._parse_typescript_skeleton(content)
        elif suffix == ".html":
            self.parser.language = self.html_lang
            return self._parse_html_skeleton(content)
        elif suffix == ".css":
            self.parser.language = self.css_lang
            return self._parse_css_skeleton(content)
        elif suffix == ".md":
            self.parser.language = self.md_lang
            return self._parse_markdown_skeleton(content)
        else:
            return f"File: {file_path.name} (Non-parsable)"

    def get_full_compressed(self, file_path: Path) -> str:
        """
        Returns full file content without comments or docstrings.
        """
        if not file_path.exists():
            return f"File {file_path.name} not found."

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        suffix = file_path.suffix
        if suffix == ".py":
            self.parser.language = self.py_lang
            return self._compress_python(content)
        elif suffix in [".ts", ".tsx"]:
            self.parser.language = self.ts_lang
            return self._compress_typescript(content)
        
        return content

    def _compress_python(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        root = tree.root_node
        
        query = Query(self.py_lang, """
            (expression_statement (string)) @docstring
            (comment) @comment
        """)
        
        cursor = QueryCursor(query)
        captures = cursor.captures(root)
        
        to_remove = []
        for tag, nodes in captures.items():
            for node in nodes:
                if tag == "docstring":
                    parent = node.parent
                    if parent and parent.type in ["module", "block"] and parent.children and parent.children[0] == node:
                            to_remove.append((node.start_byte, node.end_byte))
                else:
                    to_remove.append((node.start_byte, node.end_byte))

        return self._remove_ranges(content, to_remove)

    def _compress_typescript(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = Query(self.ts_lang, """
            (comment) @comment
        """)
        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        
        to_remove = []
        for nodes in captures.values():
            for node in nodes:
                to_remove.append((node.start_byte, node.end_byte))
        
        return self._remove_ranges(content, to_remove)

    def _remove_ranges(self, content: str, ranges: List[tuple]) -> str:
        sorted_ranges = sorted(ranges, key=lambda x: x[0], reverse=True)
        result = bytearray(content, "utf8")
        for start, end in sorted_ranges:
            del result[start:end]
        
        text = result.decode("utf8")
        lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    def _parse_python_skeleton(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = Query(self.py_lang, """
            (class_definition name: (identifier) @class.name)
            (function_definition name: (identifier) @func.name)
        """)

        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        skeleton = []
        
        # We need to preserve order if possible, but the dict loses it.
        # However, for skeleton it's okay for now.
        for tag, nodes in captures.items():
            for node in nodes:
                name = node.text.decode('utf8')
                if tag == "class.name":
                    skeleton.append(f"class {name}:")
                elif tag == "func.name":
                    if (
                        node.parent
                        and node.parent.parent
                        and node.parent.parent.type == "class_definition"
                    ):
                        skeleton.append(f"  def {name}(...)")
                    else:
                        skeleton.append(f"def {name}(...)")

        return "\n".join(skeleton)

    def _parse_typescript_skeleton(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = Query(self.ts_lang, """
            (class_declaration name: (type_identifier) @class.name)
            (function_declaration name: (identifier) @func.name)
            (method_definition name: (property_identifier) @method.name)
            (interface_declaration name: (type_identifier) @interface.name)
        """)

        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        skeleton = []
        
        for tag, nodes in captures.items():
            for node in nodes:
                name = node.text.decode('utf8')
                if tag == "class.name":
                    skeleton.append(f"class {name} {{...}}")
                elif tag == "func.name":
                    skeleton.append(f"function {name}(...) {{...}}")
                elif tag == "method.name":
                    skeleton.append(f"  method {name}(...)")
                elif tag == "interface.name":
                    skeleton.append(f"interface {name} {{...}}")

        return "\n".join(skeleton)

    def _parse_html_skeleton(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = Query(self.html_lang, """
            (element
                (start_tag
                    (tag_name) @tag.name
                    (attribute
                        (attribute_name) @attr.name
                        (quoted_attribute_value) @attr.value))
                (#match? @attr.name "id|class"))
        """)

        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        skeleton = []
        if "tag.name" in captures:
            for node in captures["tag.name"]:
                tag_text = node.text.decode("utf8")
                skeleton.append(f"<{tag_text} ... />")

        return "\n".join(skeleton[:20])

    def _parse_css_skeleton(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = Query(self.css_lang, """
            (rule_set
                (selectors) @selectors)
        """)

        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        skeleton = []
        if "selectors" in captures:
            for node in captures["selectors"]:
                skeleton.append(node.text.decode("utf8") + " { ... }")
        return "\n".join(skeleton[:20])

    def _parse_markdown_skeleton(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = Query(self.md_lang, """
            (atx_heading) @heading
        """)

        cursor = QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        skeleton = []
        if "heading" in captures:
            for node in captures["heading"]:
                skeleton.append(node.text.decode("utf8"))
        return "\n".join(skeleton)
