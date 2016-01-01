import pytest
from bling import ast

def test_nested_dict():
    root = ast.NestedDict()
    
    assert 'foo' not in root

    root['foo'] = 'bar'
    assert root['foo'] == 'bar'

    child = ast.NestedDict(root)
    assert child['foo'] == 'bar'

    child['baz'] = 42
    assert child['baz'] == 42
    assert 'baz' not in root
    
    sibling = ast.NestedDict(root)
    assert sibling['foo'] == 'bar'
    assert 'baz' not in sibling
    