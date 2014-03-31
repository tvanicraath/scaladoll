from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *
from lexer import Lexer

pg = ParserGenerator(["Token.Literal.Number.Integer", "Token.Operator"],
        precedence=[("left", ['Token.Operator', 'MINUS'])], cache_id="myparser")

@pg.production("main : expr")

class Node:
	mynode=[]
	me=""
	def __init__(self,what):
		self.me=what

	def add(self,what):
		self.mynode.append(what)	

def main(p):
	newnode=Node("main")
	newnode.add(p[0])
	return newnode



@pg.production("expr : expr Token.Operator expr")
def expr_op(p):
	newnode=Node("expr_op")
	print p[0],[1]
	newnode.add(p[0])
	newnode.add(p[2])
	return newnode


@pg.production("expr : Token.Literal.Number.Integer")
def expr_num(p):
	newnode=Node("TERMINAL")
	print p[0]
	newnode.add(p[0])

lexer = Lexer("bf.scala")
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value



def recprint(what):
	return
	print what.me

	if(isinstance(what,Node)):
		print "upar",what.me
		if(what.me=="TERMINAL"):
			return
		for child in what.mynode:
			recprint(child)
		return

	print "niche",what
	try:
		print "aur niche",what.name
	except AttributeError:
		return

	



mypar=parser.parse(lexer.lex("7+3"))
recprint(mypar)
