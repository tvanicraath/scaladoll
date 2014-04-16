from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *
from lexer import Lexer, Token
from collections import defaultdict
import sys

class Parser:

	def __init__(self):
		self.seed=104

	pg = ParserGenerator([  "Token.Keyword.If",
				"Token.Keyword.Else",
				"Token.Keyword.For",
				"Token.Keyword.While",
				"Token.Keyword.Constant",
				"Token.Keyword.Colon",
				"Token.Keyword.Def",
				"Token.Keyword.Object",
				"Token.Keyword.Val",
				"Token.Keyword.Var",
				"Token.Keyword.Type",
				"Token.Keyword.Array",
				"Token.Keyword",

                                "Token.Literal.Number.Float",
				"Token.Literal.Number.Integer",
				"Token.Literal.String",

				"Token.Operator.Equal",
				"Token.Operator.Plus",
				"Token.Operator.Prod",
				"Token.Operator.Minus",
				"Token.Operator.Div",
				"Token.Operator.Mod",
				"Token.Operator.LCurl",
				"Token.Operator.RCurl",
				"Token.Operator.LBrac",
				"Token.Operator.LSquare",
				"Token.Operator.RSquare",
				"Token.Operator.RBrac",
				"Token.Operator.SColon",
				"Token.Operator.Comma",
				"Token.Operator.LT",
				"Token.Operator.LE",
				"Token.Operator.GE",
				"Token.Operator.GT",
				"Token.Operator.EE",
				"Token.Operator.NE",
				"Token.Operator.And",
				"Token.Operator.Or",
				"Token.Operator.Xor",
				"Token.Operator",

				"Token.Name.Print",
				"Token.Name",
				"Token.Name.Class",
				"Token.Text"],
				precedence=[	("left", ['Token.Operator']),
						("right", ['Token.Operator.Equal']),
						("left", ['Token.Operator.Plus','Token.Operator.Minus']),
						("left", ['Token.Operator.Prod','Token.Operator.Div']),
						("left", ['Token.Operator.Mod']),
						("left", ['Token.Operator.And']),
						("left", ['Token.Operator.Or']),
						("right", ['Token.Operator.Xor']),
						("left", ['Token.Operator.EE']),
						("left", ['Token.Operator.LT','Token.Operator.GE','Token.Operator.LE','Token.Operator.GT']),
						("left", ['Token.Operator.NE'])

				], 
				cache_id="myparser")

	@pg.production("main : start")
	def main(p):
		return ("main",p[0])
	
	@pg.production("start : Token.Keyword.Object Token.Name.Class Token.Operator.LCurl multifunction Token.Operator.RCurl")
	def start_op(p):
		return ("Object",p[3])
	@pg.production("start : multiexpr")
	def start_op2(p):
		return ("Start",p[0])
	@pg.production("start : multifunction")
	def start_op3(p):
		return ("Start",p[0])

        @pg.production("function : Token.Keyword.Def Token.Name Token.Operator.LBrac arglist Token.Operator.RBrac Token.Keyword.Colon vtype Token.Operator.Equal Token.Operator.LCurl multiexpr Token.Operator.RCurl")
        def fun_op(p):
                return ("Function",p[1],p[3],p[6],p[8])
	
	
	@pg.production("multifunction : function multifunction")
	def multifn_op(p):
		return ("Multifunc",p[0],p[1])
	@pg.production("multifunction : eps")
	def multifn_op2(p):
		return ("Multifunc",p[0])

	@pg.production("vtype : Token.Keyword.Type")
	def vtype_op(p):
		return ("Type", p[0])

	@pg.production("vtype : Token.Keyword.Array Token.Operator.LSquare vtype Token.Operator.RSquare")
	def vtype_op2(p):
		return ("Array of type",p[2])

	@pg.production("arglist : Token.Name Token.Keyword.Colon vtype")
	def arglist_op(p):
		return ("Arglist",(p[0],p[2]))
	@pg.production("arglist : arglist Token.Operator.Comma Token.Name Token.Keyword.Colon vtype")
	def arglist_op(p):
		p[0].append((p[2],p[4]))

	@pg.production("multiexpr : expr multiexpr")
	def multiexpr_op(p):
		return ("Void MultiExpr",p[0],p[1])
	@pg.production("multiexpr : eps")
	def multiexpr_op2(p):
		return ("Void MultiExpr",p[0])
	
	@pg.production("expr : Token.Keyword.If Token.Operator.LBrac expr Token.Operator.RBrac Token.Operator.LCurl multiexpr Token.Operator.RCurl Else_Cond")
	def expr_if(p):
		print "--------",p[2]
                t0=p[2][0].split(" ")[0]
		(fake,target)=p[7]
		if t0 != "Int":
			raise AssertionError("[Sementic Error] Expression should be boolean '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))	
		return ("Void If",p[2], p[5], target) 
	

	@pg.production("Else_Cond : Token.Keyword.Else Token.Operator.LCurl multiexpr Token.Operator.RCurl")	
	def expr_else1(p):
		return ("Void Else",p[2])	
	@pg.production("Else_Cond : eps")
	def expr_else2(p):
		return ("Void Else",p[0])
	
	
	
	
	@pg.production("expr : Token.Name.Print Token.Operator.LBrac Token.Literal.String Token.Operator.RBrac")
	def bigexpr_op(p):
		return ("Void Print",p[2])

        @pg.production("expr : expr Token.Operator.And expr")
        @pg.production("expr : expr Token.Operator.Or expr")
        @pg.production("expr : expr Token.Operator.Xor expr")
	def expr_op3(p):
		if(p[0][0].split(" ")[0]=="Int" and p[2][0].split(" ")[0]=="Int"):
			return("Int Exp",p[1],p[0],p[2])
		raise AssertionError("[Sementic Error] Type mismatch at '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))
	
	@pg.production("expr : expr Token.Operator.LE expr")
	@pg.production("expr : expr Token.Operator.GE expr")
	@pg.production("expr : expr Token.Operator.LT expr")
	@pg.production("expr : expr Token.Operator.GT expr")
	@pg.production("expr : expr Token.Operator.EE expr")
	@pg.production("expr : expr Token.Operator.NE expr")
        def expr_op2(p):
                (type,fake)=p[0]
                t0=type.split(" ")[0]
                (type,fake)=p[2]
                t2=type.split(" ")[0]
                if(t0=="String" or t2=="String"):
                        raise AssertionError("[Sementic Error] Type mismatch at '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))
		return("Int EXP",p[1],p[0],p[2])

	@pg.production("expr : expr Token.Operator.Plus expr")
	@pg.production("expr : expr Token.Operator.Minus expr")
	@pg.production("expr : expr Token.Operator.Prod expr")
	@pg.production("expr : expr Token.Operator.Div expr")
	@pg.production("expr : expr Token.Operator.Mod expr")
	def expr_op(p):
                (type,fake)=p[0]
                t0=type.split(" ")[0]
                (type,fake)=p[2]
                t2=type.split(" ")[0]
		if(t0=="String" or t2=="String"):
			raise AssertionError("[Sementic Error] Type mismatch at '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))
		t00="Int"
		if(t0=="Float" or t2=="Float"):	t00="Float"
		return (t00+" EXP",p[1],p[0],p[2])
	
	
	@pg.production("expr : Token.Keyword.Var Token.Name Token.Keyword.Colon vtype")
	def var_dec(p):
	        return ("VAR",p[1],p[3])
	@pg.production("expr : Token.Keyword.Val Token.Name Token.Keyword.Colon vtype")
	def val_dec(p):
	        return ("VAL",p[1],p[3])
	@pg.production("expr : Token.Name Token.Operator.Equal expr")
	def var_init(p):
		t0=p[0].type
                (type,fake)=p[2]
                t1=type.split(" ")[0]
		if(t0=="Int" or t0=="Float"):	t0="Int"
		if(t1=="Int" or t1=="Float"):	t1="Int"
		if(t0==t1):
			if(p[0].type=="Int" and type.split(" ")[0]=="Float"):
				print ("[Warning] Implicit typecast to INT at "+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
				t0="Int"
			elif(p[0].type=="Float" or type.split(" ")[0]=="Float"):	t0="Float"
		        return (t0+" VAR_EQUALS",p[0],p[2])
		else:
			raise AssertionError("[Sementic Error] Type mismatch at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
			
	
	@pg.production("expr : expr_atomic")
	def expr_atomic(p):
		(type,fake)=p[0]
		type=type.split(" ")[0]
		return (type+" ATOM", p[0])
	
	@pg.production("expr_atomic : Token.Literal.String")
	def expr_string(p):
	        return ("String Const",p[0])
	
	@pg.production("expr_atomic : Token.Literal.Number.Integer")
	def expr_num(p):
	    return ("Int Const",p[0])
	@pg.production("expr_atomic : Token.Literal.Number.Float")
	def expr_float(p):
		return ("Float Const",p[0])
	@pg.production("expr_atomic : Token.Name")
	def expr_var(p):
		return (p[0].type+" VAR", p[0])
	
	@pg.production("expr_atomic : Token.Keyword.Constant")
	def expr_const(p):
		return ("CONSTANT",p[0])
	@pg.production("expr : Token.Operator.Minus expr_atomic")
	def epr_op2(p):
		(type,fake)=p[1]
		type=type.split(" ")[0]
		return (type+" UMINUS", p[1])
	
	#@pg.production("expr : eps")
	#def expr_eps(p):
	#    print ("Expr",p[0])
	#    return 
	
	@pg.production("eps : ")
	def eps(p):
	    return ("Void EPSILON",Token("EPS",""))
	

	def recprint(self,what,offset):
	        for i in range(0,offset):
	                print "\t",
	
		if(isinstance(what,Token)):
			print what.gettokentype(),what.getstr()
			return
	
		print what[0]
		for which in what[1:]:
			self.recprint(which,offset+1)

	def readfromprompt(self):
		lines=""
		line=raw_input("scaladoll > ")
		lines=lines+line+"@@@\n"
		while(1):
			line=raw_input("... > ")
			if(line=="@"):
				break
			if(line==""):
				continue
			lines=lines+line+"@@@\n"
		return lines

	def __init__(self,afterparse,debug):
		parser=self.pg.build()
	        if(len(sys.argv)>1):
        	        fname=sys.argv[1]
                	lexer = Lexer(fname,debug)
        	        mypar=parser.parse(lexer.lex())
                	if(debug):	self.recprint(mypar,0)
			afterparse(mypar)
		
		else:
	                while(1):
        	                lexer=Lexer(None,debug)
	                        mypar=parser.parse(lexer.lex(self.readfromprompt()))
        	                if(debug):	self.recprint(mypar,0)
				afterparse(mypar)

	def newvar(self,type):
		self.seed+=1
		if(type=="Int"):	return "t@@"+str(self.seed)
		if(type=="Float"):	return "f@@"+str(self.seed)
		if(type=="String"):	return "s@@"+str(self.seed)


def main():
	parser=Parser(function_name,debug=1)
#main()

