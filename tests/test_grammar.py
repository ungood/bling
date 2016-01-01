from bling import grammar
import pytest
from pyparsing import ParseException
from decimal import Decimal
from colour import Color

def parse(parser, input):
    return parser.parseString(input, parseAll=True).asList()[0]

@pytest.mark.parametrize("input, expected", [
    ("null", None),
    ("true", True),
    ("false", False),
    ("1", Decimal(1)),
    ("0", Decimal(0)),
    ("-1", Decimal(-1)),
    ("3.1415", Decimal('3.1415')),
    ("1e10", Decimal('1e10')),
    ("1.2E10", Decimal('1.2e10')),
    ("#fff", Color("white")),
    ("#ff0000", Color("red"))
])
def test_literals(input, expected):
    node = parse(grammar.literal, input)
    assert node.value == expected

@pytest.mark.parametrize("name", [
    "foo", "_foo", "foo_bar", "__foobar__"
])
def test_references(name):
    node = parse(grammar.reference, name)
    assert node.name == name

@pytest.mark.parametrize("input, expected_name, expected_args", [
    ("a()", "a", ()),
    ("b(null)", "b", (None,)),
    ("c(true, false)", "c", (True, False)),
    ("d(-1, #fff)", "d", (Decimal(-1), Color("white")))
])
def test_function_calls(input, expected_name, expected_args):
    node = parse(grammar.function_call, input)
    assert node.name == expected_name
    actual_args = tuple([arg.value for arg in node.arguments])
    assert actual_args == expected_args

