from bling import grammar
import pytest
from decimal import Decimal
from colour import Color

class NestedDict(dict):
    """A dictionary that defers missing keys to a parent dictionary."""
    def __init__(self, parent=None):
        self.parent = dict() if parent is None else parent
        
    def __missing__(self, key):
        return self.parent[key]

@pytest.mark.parametrize("input,expected", [
    ("null", None),
    ("true", True),
    ("false", False),
    ("1", Decimal(1)),
    ("0", Decimal(0)),
    ("-1", Decimal(-1)),
    ("3.1415", Decimal('3.1415')),
    ("1e10", Decimal('1e10')),
    ("1.2E10", Decimal('1.2e10'))
])
def test_literals(input, expected):
    node = grammar.literal.parseString(input, parseAll=True).asList()[0]
    assert node.value == expected

def compile(*definitions):
    parser = grammar.expression
    
    context = {}
    for key, value in definitions:
        print("let {} = {};".format(key, value))
        expr = parser.parseString(value).asList()[0]
        context[key] = expr
    return context

def test_references():
    from pprint import pprint
    child = compile(("red", "#f00"))
    
    program = compile(
        ("white", "#fff"),
        ("also_white", "white"))
#        ("child", compile(("red", "#f00"))),
#        ("also_red", "child.red"))
    
    for name, expr in program.items():
        value = expr.evaluate(program)
        print("{} ({}) == {}".format(name, expr, value))
