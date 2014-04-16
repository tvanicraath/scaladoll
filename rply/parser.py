from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox
from itertools import *
from lexer import Lexer, Token
from collections import defaultdict
import sys,os
seed=118

def newvar(type):
		global seed
                seed+=1
                if(type=="Int"):        return "t@@"+str(seed)
                if(type=="Float"):      return "f@@"+str(seed)
                if(type=="String"):     return "s@@"+str(seed)


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
				"Token.Keyword.InRange",
				"Token.Keyword.To",
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
				precedence=[	
						("right", ['Token.Operator.Equal']),
						("left", ['Token.Operator.NE']),
                                                ("left", ['Token.Operator.EE']),
                                                ("left", ['Token.Operator.LT','Token.Operator.GE','Token.Operator.LE','Token.Operator.GT']),
                                                ("right", ['Token.Operator.Xor']),
                                                ("left", ['Token.Operator.And']),
                                                ("left", ['Token.Operator.Or']),
                                                ("left", ['Token.Operator.Mod']),
						("left", ['Token.Operator.Plus','Token.Operator.Minus']),
                                                ("left", ['Token.Operator.Prod','Token.Operator.Div']),
						("left", ['Token.Operator']),
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

	@pg.production("vtype : Token.Keyword.Array Token.Operator.LSquare Token.Keyword.Type Token.Operator.RSquare sizeval")
	def vtype_op2(p):
		return ("Array of type",p[2])

	@pg.production("sizeval : Token.Operator.LBrac Token.Literal.Number.Integer Token.Operator.RBrac")
	def arr_sizeval_op(p):
		return ("Array Size",None)
        @pg.production("sizeval : Token.Operator.LBrac Token.Literal.Number.Integer Token.Operator.Comma Token.Literal.Number.Integer Token.Operator.RBrac")
        def arr_sizeval_op(p):
                return ("Array Size",None)


	@pg.production("arglist : Token.Name Token.Keyword.Colon vtype")
	def arglist_op(p):
		return ("Arglist",(p[0],p[2]))
	@pg.production("arglist : arglist Token.Operator.Comma Token.Name Token.Keyword.Colon vtype")
	def arglist_op(p):
		p[0].append((p[2],p[4]))

	@pg.production("multiexpr : expr multiexpr")
	def multiexpr_op(p):
		newtype=p[1][0].split(" ")[0]
		if(newtype=="Void"):
			newtype=p[0][0].split(" ")[0]
		#print newtype
		return (newtype+" MultiExpr",p[0],p[1])
	@pg.production("multiexpr : eps")
	def multiexpr_op2(p):
		return ("Void MultiExpr",p[0])

	@pg.production("expr : Token.Keyword.While Token.Operator.LBrac expr Token.Operator.RBrac Token.Operator.LCurl multiexpr Token.Operator.RCurl")
	def while_op(p):
		t0=p[2][0].split(" ")[0]
		if(t0 != "Int"):
			raise AssertionError("[Sementic Error] Expression should be boolean '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))
		truetype=p[5][0].split(" ")[0]
		return (truetype+" While",p[2],p[5])
	
	@pg.production("expr : Token.Keyword.If Token.Operator.LBrac expr Token.Operator.RBrac Token.Operator.LCurl multiexpr Token.Operator.RCurl Else_Cond")
	def expr_if(p):
		#print "--------",p[2]
                t0=p[2][0].split(" ")[0]
		target=p[7][1]
		if t0 != "Int":
			raise AssertionError("[Sementic Error] Expression should be boolean '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))
		iftype=p[5][0].split(" ")[0]
		elsetype=p[7][0].split(" ")[0]
		if(elsetype!="Void"):
			if(iftype!=elsetype):
				raise AssertionError("[Sementic Error] If/Else return type mismatch at '"+p[1].getstr()+"' at Line: "+str(p[1].getsourcepos()))
		return (iftype+" If",p[2], p[5], target) 
	

	@pg.production("Else_Cond : Token.Keyword.Else Token.Operator.LCurl multiexpr Token.Operator.RCurl")	
	def expr_else1(p):
		return (p[2][0].split(" ")[0]+" Else",p[2])
	@pg.production("Else_Cond : eps")
	def expr_else2(p):
		return ("Void Else",p[0])
	

	@pg.production("expr : Token.Keyword.For Token.Operator.LBrac Token.Name Token.Keyword.InRange expr Token.Keyword.To expr Token.Operator.RBrac Token.Operator.LCurl multiexpr Token.Operator.RCurl")
	def for_range(p):
		if(p[4][0].split(" ")[0]!="Int"):	raise AssertionError("[Sementic Error] Expression should be boolean '"+p[4].getstr()+"' at Line: "+str(p[4].getsourcepos()))
		if(p[6][0].split(" ")[0]!="Int"):       raise AssertionError("[Sementic Error] Expression should be boolean '"+p[6].getstr()+"' at Line: "+str(p[6].getsourcepos()))
		if(p[2].type!="Int"):       raise AssertionError("[Sementic Error] Expression should be boolean '"+p[3].getstr()+"' at Line: "+str(p[3].getsourcepos()))		
		return ("Void For_Range",p[2],p[4],p[6],p[9])
	
	
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
                type=p[0][0]
                t0=type.split(" ")[0]
                type=p[2][0]
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
		print p[0]
                type=p[0][0]
                t0=type.split(" ")[0]
                type=p[2][0]
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
                type=p[2][0]
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
			
	
	@pg.production("expr : Token.Operator.LBrac expr Token.Operator.RBrac")
	def expr_brac(p):
		type=p[1][0].split(" ")[0]
		return (type+" EXP", p[1]);


	@pg.production("expr : Token.Name Token.Operator.LBrac expr Token.Operator.RBrac")
	def array_getval1(p):
		if(p[2][0].split(" ")[0]!="Int"):
			raise AssertionError("[Sementic Error] Type mismatch at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
		print p[0].size1,p[0].size2
		if(p[0].size2!=0):
			raise AssertionError("[Sementic Error] Use 1D array at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
		return (p[0].type+" GetVal1",p[0],p[2],p[0].size1)

        @pg.production("expr : Token.Name Token.Operator.LBrac expr Token.Operator.Comma expr Token.Operator.RBrac")
        def array_getval2(p):
                if(p[2][0].split(" ")[0]!="Int" or p[4][0].split(" ")[0]!="Int"):
                        raise AssertionError("[Sementic Error] Type mismatch at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
		if(p[0].size2==0):
			raise AssertionError("[Sementic Error] Use 2D array at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
                return (p[0].type+" GetVal2",p[0],p[2],p[4],p[0].size1,p[0].size2)

        @pg.production("expr : Token.Name Token.Operator.LBrac expr Token.Operator.RBrac Token.Operator.Equal expr")
        def array_init1(p):
                if(p[0].size2!=0):
                        raise AssertionError("[Sementic Error] Use 1D array at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
		if(p[2][0].split(" ")[0]!="Int"):
			raise AssertionError("[Sementic Error] Use integer index '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
		
                t0=p[0].type
                t1=p[5][0].split(" ")[0]
                if(t0=="Int" or t0=="Float"):   t0="Int"
                if(t1=="Int" or t1=="Float"):   t1="Int"
                if(t0==t1):
                        if(p[0].type=="Int" and p[5][0].split(" ")[0]=="Float"):
                                print ("[Warning] Implicit typecast to INT at "+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
                                t0="Int"
                        elif(p[0].type=="Float" or p[5][0].split(" ")[0]=="Float"):        t0="Float"
                        return (t0+" SetVal1",p[0],p[2],p[5],p[0].size1)
                else:
                        raise AssertionError("[Sementic Error] Type mismatch at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))

        @pg.production("expr : Token.Name Token.Operator.LBrac expr Token.Operator.Comma expr Token.Operator.RBrac Token.Operator.Equal expr")
        def array_init2(p):
                if(p[0].size2==0):
                        raise AssertionError("[Sementic Error] Use 2D array at '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
                if(p[2][0].split(" ")[0]!="Int" or p[4][0].split(" ")[0]!="Int"):
                        raise AssertionError("[Sementic Error] Use integer index '"+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))

                t0=p[0].type
                t1=p[7][0].split(" ")[0]
                if(t0=="Int" or t0=="Float"):   t0="Int"
                if(t1=="Int" or t1=="Float"):   t1="Int"
                if(t0==t1):
                        if(p[0].type=="Int" and p[7][0].split(" ")[0]=="Float"):
                                print ("[Warning] Implicit typecast to INT at "+p[0].getstr().split("@")[0]+"' at Line: "+str(p[0].getsourcepos()))
                                t0="Int"
                        elif(p[0].type=="Float" or p[7][0].split(" ")[0]=="Float"):        t0="Float"
                        return (t0+" SetVal2",p[0],p[2],p[4],p[7],p[0].size1,p[0].size2)
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
		return (p[0].type+" ASSIGN", p[0])
	
        @pg.production("expr : Token.Operator.Minus expr_atomic")
        def epr_op2(p):
                (type,fake)=p[1]
                type=type.split(" ")[0]
                return (type+" UMINUS", p[1])

	@pg.production("expr_atomic : Token.Keyword.Constant")
	def expr_const(p):
		raise AssertionError("hey dude! what brought you here? o.O")
		return ("CONSTANT",p[0])

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
		if(isinstance(what,int)):
			print ("intval: "+str(what))
			return

	
		print what[0]
		for which in what[1:]:
			self.recprint(which,offset+1)

	def readfromprompt(self):
		lines=""
		line=raw_input("scaladoll > ")
		if(line.upper() in ("CLEAR","EXIT")):
			return line.upper()
		lines=lines+line+"@@@\n"
		blankcount=0
		while(1):
			line=raw_input("... > ")
	                if(line.upper() in ("CLEAR","EXIT")):
        	               return line.upper()
			if(line=="@"):
				break
			if(line==""):
				blankcount+=1
				if(blankcount>3):
					break
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
			oldlines=""
	                while(1):
        	                lexer=Lexer(None,debug)
				newline=self.readfromprompt()
				if(newline=="CLEAR"):
					oldlines=""
					os.system('clear')
					continue
				if(newline=="EXIT"):
					return
				oldlines=oldlines+newline
	                        mypar=parser.parse(lexer.lex(oldlines))
        	                if(debug):	self.recprint(mypar,0)
				afterparse(mypar)

def main():
	parser=Parser(function_name,debug=1)
#main()
