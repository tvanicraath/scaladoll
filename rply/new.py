from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *


class P:
        def __init__(self,fale):
                        self.name = "NUMBER"
                        self.value = 7
                        self.lineno = None
                        self.source_pos = None

	def gettokentype(self):
		return self.name

	def getsourcepos(self):
		return None

	def getstr(self):
		return self.value


class mylexer:


	def __init__(self,fake):
		self.rac="rac"

	def next(self,fake=None):
		newt=P("rac")
		return newt

	def lex(self,s):
		lt=[]
		lt.append(P("ff"))
		return chain(lt)


# This is a list of the token names. precedence is an optional list of
# tuples which specifies order of operation for avoiding ambiguity.
# precedence must be one of "left", "right", "nonassoc".
# cache_id is an optional string which specifies an ID to use for
# caching. It should *always* be safe to use caching,
# RPly will automatically detect when your grammar is
# changed and refresh the cache for you.
pg = ParserGenerator(["NUMBER", "PLUS", "MINUS"],
        precedence=[("left", ['PLUS', 'MINUS'])], cache_id="myparser")

@pg.production("main : expr")
def main(p):
    # p is a list, of each of the pieces on the right hand side of the
    # grammar rule
    return p[0]

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    if p[1].gettokentype() == "PLUS":
        return BoxInt(lhs + rhs)
    elif p[1].gettokentype() == "MINUS":
        return BoxInt(lhs - rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

lexer = mylexer("rac")
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value

mypar=parser.parse(lexer.lex("7"))
print mypar.getint()
