import tree_sitter_python as tspython
import tree_sitter_typescript as tstypescript
import tree_sitter_html as tshtml
import tree_sitter_css as tscss
import tree_sitter_markdown as tsmarkdown
from tree_sitter import Language, Parser
from pathlib import Path


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
            return self._parse_python(content)
        elif suffix in [".ts", ".tsx"]:
            self.parser.language = self.ts_lang
            return self._parse_typescript(content)
        elif suffix == ".html":
            self.parser.language = self.html_lang
            return self._parse_html(content)
        elif suffix == ".css":
            self.parser.language = self.css_lang
            return self._parse_css(content)
        elif suffix == ".md":
            self.parser.language = self.md_lang
            return self._parse_markdown(content)
        else:
            # For non-code files, just return first few lines or name
            return f"File: {file_path.name} (Non-parsable)"

    def _parse_python(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = self.py_lang.query("""
            (class_definition name: (identifier) @class.name)
            (function_definition name: (identifier) @func.name)
        """)

        captures = query.captures(tree.root_node)
        skeleton = []
        for node, tag in captures:
            if tag == "class.name":
                skeleton.append(f"class {node.text.decode('utf8')}:")
            elif tag == "func.name":
                # Check if it's a method
                if (
                    node.parent
                    and node.parent.parent
                    and node.parent.parent.type == "class_definition"
                ):
                    skeleton.append(f"  def {node.text.decode('utf8')}(...)")
                else:
                    skeleton.append(f"def {node.text.decode('utf8')}(...)")

        return "\n".join(skeleton)

    def _parse_typescript(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = self.ts_lang.query("""
            (class_declaration name: (type_identifier) @class.name)
            (function_declaration name: (identifier) @func.name)
            (method_definition name: (property_identifier) @method.name)
            (interface_declaration name: (type_identifier) @interface.name)
        """)

        captures = query.captures(tree.root_node)
        skeleton = []
        for node, tag in captures:
            if tag == "class.name":
                skeleton.append(f"class {node.text.decode('utf8')} {{...}}")
            elif tag == "func.name":
                skeleton.append(f"function {node.text.decode('utf8')}(...) {{...}}")
            elif tag == "method.name":
                skeleton.append(f"  method {node.text.decode('utf8')}(...)")
            elif tag == "interface.name":
                skeleton.append(f"interface {node.text.decode('utf8')} {{...}}")

        return "\n".join(skeleton)

    def _parse_html(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        # Query for tags with IDs or important structures
        query = self.html_lang.query("""
            (element
                (start_tag
                    (tag_name) @tag.name
                    (attribute
                        (attribute_name) @attr.name
                        (quoted_attribute_value) @attr.value))
                (#match? @attr.name "id|class"))
        """)

        captures = query.captures(tree.root_node)
        skeleton = []

        for node, tag in captures:
            if tag == "tag.name":
                tag_text = node.text.decode("utf8")
                skeleton.append(f"<{tag_text} ... />")

        return "\n".join(skeleton[:20])

    def _parse_css(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = self.css_lang.query("""
            (rule_set
                (selectors) @selectors)
        """)

        captures = query.captures(tree.root_node)
        skeleton = [node.text.decode("utf8") + " { ... }" for node, _ in captures]
        return "\n".join(skeleton[:20])

    def _parse_markdown(self, content: str) -> str:
        tree = self.parser.parse(bytes(content, "utf8"))
        query = self.md_lang.query("""
            (atx_heading) @heading
        """)

        captures = query.captures(tree.root_node)
        skeleton = [node.text.decode("utf8") for node, _ in captures]
        return "\n".join(skeleton)
