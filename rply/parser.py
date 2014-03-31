from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *
from lexer import Lexer, Token
from collections import defaultdict


pg = ParserGenerator(["Token.Literal.Number.Integer", "Token.Operator.Plus", "Token.Operator.Minus"],
        precedence=[("right", ['Token.Operator.Plus', 'Token.Operator.Minus'])], cache_id="myparser")

@pg.production("main : expr")
def main(p):
	return ("main",p[0])



@pg.production("expr : expr Token.Operator.Plus expr")
def expr_op(p):
	return ("expr_add",p[0],p[2])

@pg.production("expr : expr Token.Operator.Minus expr")
def expr_op(p):
        return ("expr_minus",p[0],p[2])


@pg.production("expr : Token.Literal.Number.Integer")
def expr_num(p):
	return ("terminal",p[0])

lexer = Lexer("bf.scala")
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value



def recprint(what,offset):
        for i in range(0,offset):
                print "\t",

	if(isinstance(what,Token)):
		print what.gettokentype(),what.getstr()
		return

	print what[0]	
	for which in what[1:]:
		recprint(which,offset+1)

mypar=parser.parse(lexer.lex("7+3-4"))
print mypar
recprint(mypar,0)
