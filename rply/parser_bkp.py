from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *
from lexer import Lexer, Token
from collections import defaultdict
import sys

class Node:
	name=""
	childs=[]
	def __init__(self,name):
		self.name=name

	def add(self,child):
		self.childs.append(child)

pg = ParserGenerator(["Token.Literal.Number.Float","Token.Keyword.Val","Token.Keyword.Var","Token.Keyword.Equal","Token.Operator.Equal","Token.Keyword.Constant","Token.Keyword.Colon","Token.Keyword.Def","Token.Keyword.Object","Token.Name.Print","Token.Operator.Plus","Token.Operator.Prod","Token.Operator.Minus","Token.Operator.Div","Token.Operator.Mod","Token.Literal.Number.Integer", "Token.Name", "Token.Keyword.Type", "Token.Operator","Token.Name.Class","Token.Text", "Token.Keyword", "Token.Literal.String","Token.Operator.LCurl","Token.Operator.RCurl","Token.Operator.LBrac","Token.Operator.LSquare","Token.Operator.RSquare","Token.Operator.RBrac", "Token.Operator.SColon"],

        precedence=[("left", ['Token.Operator', 'MINUS'])], cache_id="myparser")

@pg.production("main : start")
def main(p):
	newnod=Node("main")
	newnod.add(p[0])
	return ("main",p[0])

@pg.production("start : Token.Keyword.Object Token.Name.Class Token.Operator.LCurl multifunction Token.Operator.RCurl")
def start_op(p):
	newnod=Node("Object"+"_"+p[1].getstr())
	newnod.add(p[3])
	return ("Object",p[3])
@pg.production("start : multiexpr")
def start_op2(p):
	return ("Start",p[0])
@pg.production("start : multifunction")
def start_op3(p):
	return ("Start",p[0])


@pg.production("multifunction : function multifunction")
def multifn_op(p):
	return ("Multifunc",p[0],p[1])
@pg.production("multifunction : eps")
def multifn_op2(p):
	return ("Multifunc",p[0])


@pg.production("function : Token.Keyword.Def Token.Name Token.Operator.LBrac Token.Name Token.Keyword.Colon Token.Keyword.Type Token.Operator.LSquare Token.Keyword.Type Token.Operator.RSquare Token.Operator.RBrac Token.Keyword.Colon Token.Keyword.Type Token.Operator.Equal Token.Operator.LCurl multiexpr Token.Operator.RCurl")
def fun_op(p):
	newnod=Node("Function"+"_"+p[1].getstr())
	newnod.add(p[11])
	return ("Function",p[14])

@pg.production("multiexpr : expr multiexpr")
def multiexpr_op(p):
	return ("MultiExpr",p[0],p[1])
@pg.production("multiexpr : eps")
def multiexpr_op2(p):
	return ("MultiExpr",p[0])


@pg.production("expr : Token.Name.Print Token.Operator.LBrac Token.Literal.String Token.Operator.RBrac Token.Operator.SColon")
def bigexpr_op(p):
	newnod=Node("Print")
	newnod.add(p[2])
	return ("Print",p[2])



@pg.production("expr : expr Token.Operator.Plus expr")
@pg.production("expr : expr Token.Operator.Minus expr")
@pg.production("expr : expr Token.Operator.Prod expr")
@pg.production("expr : expr Token.Operator.Div expr")
@pg.production("expr : expr Token.Operator.Mod expr")
def expr_op(p):
	newnod=Node(p[1])
	newnod.add(p[0])
	newnod.add(p[2])
	return ("EXP",p[1],p[0],p[2])


@pg.production("expr : Token.Keyword.Var Token.Name Token.Keyword.Colon Token.Keyword.Type")
def var_dec(p):
        return ("VAR",p[1],p[3])
@pg.production("expr : Token.Keyword.Val Token.Name Token.Keyword.Colon Token.Keyword.Type")
def val_dec(p):
        return ("VAL",p[1],p[3])
@pg.production("expr : Token.Name Token.Keyword.Equal expr")
def var_init(p):
        return ("VAR_EQUALS",p[0],p[2])

@pg.production("expr : expr_atomic")
def expr_atomic(p):
	return ("ATOM", p[0])

@pg.production("expr_atomic : Token.Literal.String")
def expr_string(p):
	print "tttttt"
        return ("String",p[0])

@pg.production("expr_atomic : Token.Literal.Number.Integer")
def expr_num(p):
    return ("NUM",p[0])
@pg.production("expr_atomic : Token.Literal.Number.Float")
def expr_float(p):
	return ("FLOAT",p[0])
@pg.production("expr_atomic : Token.Name")
def expr_var(p):
	return ("VAR", p[0])

@pg.production("expr_atomic : Token.Keyword.Constant")
def expr_const(p):
	return ("CONSTANT",p[0])
@pg.production("expr : Token.Operator.Minus expr_atomic")
def epr_op2(p):
	return ("UMINUS", p[1])

@pg.production("expr : eps")
def expr_eps(p):
    print ("Expr",p[0])
    return 

@pg.production("eps : ")
def eps(p):
    return ("EPSILON",Token("EPS",""))


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



def main():
	if(len(sys.argv)>1):
		fname=sys.argv[1]
		lexer = Lexer(fname)
	        parser = pg.build()
		mypar=parser.parse(lexer.lex())
	        recprint(mypar,0)

	else:
		while(1):
			lexer=Lexer("hw.scala")
			parser=pg.build()
			mypar=parser.parse(lexer.lex(raw_input("scaladoll> ")))
#			print mypar
			recprint(mypar,0)


main()

