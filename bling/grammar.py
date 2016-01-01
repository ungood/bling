import pyparsing as pp
from bling import ast

null = pp.Keyword('null').setParseAction(ast.Null)
boolean = pp.Keyword('true') | pp.Keyword('false')
boolean.setParseAction(ast.Boolean)

number = pp.Combine(
     pp.Optional('-') +
     ('0' | pp.Word('123456789', pp.nums)) +
     pp.Optional('.' + pp.Word(pp.nums)) +
     pp.Optional(pp.Word('eE', exact=1) + pp.Word(pp.nums + '+-', pp.nums)))
number.setParseAction(ast.Number)

nibble   = pp.Word(pp.hexnums, exact=1).setParseAction(lambda tokens: int(tokens[0] + tokens[0], 16))
byte     = pp.Word(pp.hexnums, exact=2).setParseAction(lambda tokens: int(tokens[0], 16))
hex_rgb  = pp.Suppress('#') + (nibble * 3 | byte * 3)
color    = hex_rgb.setParseAction(ast.Color)

literal = null | boolean | number | color

identifier = pp.Word(pp.alphas)
reference = identifier.setParseAction(ast.Reference)

expression = literal | reference
# Literals: null, bool, numbers, colors
#
# Future Enhancment
#
# array = pp.Forward()
# element = ( number | array )
# array << pp.Group(pp.Suppress('[') + pp.Optional(pp.delimitedList(element)) + pp.Suppress(']'))
#
#
# texture = json_list(color)
#
# identifier = pp.Word(pp.alphas + "_")
#
# string = pp.quotedString
# name = string
# value = ( string | number | array )
# definition = pp.Group(name + pp.Suppress(':') + value)
# definitions = pp.delimitedList(definition)
#
# blong = hex_color | texture
# #pp.Dict(pp.Suppress('{') + pp.Optional(definitions) + pp.Suppress('}'))