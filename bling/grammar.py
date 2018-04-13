import pyparsing as pp
from bling import ast

expression = pp.Forward()

null = pp.Keyword('null').setParseAction(ast.Null)
boolean = pp.Keyword('true') | pp.Keyword('false')
boolean.setParseAction(ast.Boolean)

"""
BNF from Python's decimal module:
sign           ::=  '+' | '-'
digit          ::=  '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
indicator      ::=  'e' | 'E'
digits         ::=  digit [digit]...
decimal-part   ::=  digits '.' [digits] | ['.'] digits
exponent-part  ::=  indicator [sign] digits
infinity       ::=  'Infinity' | 'Inf'
nan            ::=  'NaN' [digits] | 'sNaN' [digits]
numeric-value  ::=  decimal-part [exponent-part] | infinity
numeric-string ::=  [sign] numeric-value | [sign] nan
"""
sign      = pp.Optional(pp.Literal('+') | pp.Literal('-'), default='+')
indicator = pp.Word('eE', exact=1)
digits    = pp.Word(pp.nums, min=1)
decimal   = digits + '.' + pp.Optional(digits) | pp.Optional('.') + digits
exponent  = indicator + pp.Optional(sign) + digits
number    = pp.Combine(sign + decimal + pp.Optional(exponent))
number.setParseAction(ast.Number)

nibble   = pp.Word(pp.hexnums, exact=1).setParseAction(lambda tokens: int(tokens[0] + tokens[0], 16))
byte     = pp.Word(pp.hexnums, exact=2).setParseAction(lambda tokens: int(tokens[0], 16))
hex_rgb  = pp.Suppress('#') + (byte * 3 | nibble * 3)
color    = hex_rgb.setParseAction(ast.Color)

literal = null | boolean | number | color

identifier = pp.Combine(pp.Word(pp.alphas + "_", exact=1) + pp.Optional(pp.Word(pp.alphanums + "_")))

reference = identifier("target").setParseAction(ast.Reference)

arguments = pp.Group(pp.Suppress('(') + pp.Optional(pp.delimitedList(expression)) + pp.Suppress(')'))
function_call = identifier("name") + arguments("arguments")
function_call.setParseAction(ast.FunctionCall)

expression << literal | function_call | reference