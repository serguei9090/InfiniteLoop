from modules.context import ContextEngine

def test_python_compression(tmp_path):
    """Verify that Python docstrings and comments are stripped."""
    engine = ContextEngine()
    code = '''
"""
This is a module docstring.
"""
def hello():
    # This is a comment
    """Function docstring."""
    print("hello") # inline comment
'''
    py_file = tmp_path / "test.py"
    py_file.write_text(code)
    
    compressed = engine.get_full_compressed(py_file)
    
    assert 'This is a module docstring' not in compressed
    assert 'This is a comment' not in compressed
    assert 'Function docstring' not in compressed
    assert 'inline comment' not in compressed
    assert 'print("hello")' in compressed

def test_typescript_compression(tmp_path):
    """Verify that TypeScript comments are stripped."""
    engine = ContextEngine()
    code = '''
/**
 * JSDoc comment
 */
function test() {
    // Single line comment
    /* Multi-line
       comment */
    console.log("test");
}
'''
    ts_file = tmp_path / "test.ts"
    ts_file.write_text(code)
    
    compressed = engine.get_full_compressed(ts_file)
    
    assert 'JSDoc comment' not in compressed
    assert 'Single line comment' not in compressed
    assert 'Multi-line' not in compressed
    assert 'console.log("test")' in compressed
