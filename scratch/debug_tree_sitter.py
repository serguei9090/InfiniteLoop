from tree_sitter import Language, Parser, Query, QueryCursor
import tree_sitter_python as tspython

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)
tree = parser.parse(b"def foo(): # comment\n    pass")

query = Query(PY_LANGUAGE, "(comment) @comment")
cursor = QueryCursor(query)
captures = cursor.captures(tree.root_node)

print(f"Type of captures: {type(captures)}")
if isinstance(captures, dict):
    for key, value in captures.items():
        print(f"Key: {key}, Value Type: {type(value)}")
        if isinstance(value, list):
            print(f"  First item type: {type(value[0])}")
