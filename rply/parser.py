from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *
from lexer import Lexer

pg = ParserGenerator(["Token.Literal.Number.Integer", "Token.Operator"],
        precedence=[("left", ['Token.Operator', 'MINUS'])], cache_id="myparser")

@pg.production("main : expr")
def main(p):
    return p[0]

@pg.production("expr : expr Token.Operator expr")
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    return  BoxInt(lhs + rhs)

    if p[1].gettokentype() == "PLUS":
	if p[1].getstr() == "+":
	        return BoxInt(lhs + rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : Token.Literal.Number.Integer")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

lexer = Lexer("bf.scala")
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value

mypar=parser.parse(lexer.lex("7+3+2"))
print mypar
