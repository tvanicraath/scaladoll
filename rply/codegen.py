from lexer import Lexer, Token
from parser import Parser
from itertools import *
from collections import defaultdict
seed=118
def newvar(type):
                global seed
                seed+=1
                if(type=="Int"):        return "t@@"+str(seed)
                if(type=="Float"):      return "f@@"+str(seed)
                if(type=="String"):     return "s@@"+str(seed)


def recprint(what,offset):
                for i in range(0,offset):
                        print "\t",

                if(isinstance(what,Token)):
                        print what.gettokentype(),what.getstr()
                        return ( (what.gettype(),what.getstr()), [] )

                print what[0]
		if(what[0].split(" ")[-1]=="ATOM" or what[0].split(" ")[-1]=="Const" or what[0].split(" ")[-1]=="ASSIGN"):
			return recprint(what[1],offset+1)

		if(what[0].split(" ")[-1]=="EXP"):
			if(len(what)==2):
				op=recprint(what[1],offset+1)
				L=[]
				L=op[1]
				opret=op[0][1]
				optype=op[0][0]
				type=what[0].split(" ")[0]
				var=newvar(type)
				L.append( ( ( (var,type), (":=","COPY"), (opret) ), "COPY" ) )
				return ( (type,var), L)

			else:
				op=what[1].getstr()
				op1=recprint(what[2],offset+1)
				op2=recprint(what[3],offset+1)
				L=[]
				L=op1[1]+op2[1]
				op1ret=op1[0][1]
				op1type=op1[0][0]
				op2ret=op2[0][1]
				op2type=op2[0][0]
				type=what[0].split(" ")[0]
				var=newvar(type)
				L.append( ( ( (var,type), (":=","ASSIGNMENT"), (op1ret,op1type), (op,"OPR"), (op2ret,op2type) ), "ASSIGNMENT" ) )
				return ( (type,var), L )

		if(what[0].split(" ")[-1]=="VAR_EQUALS"):
			var=what[1].getstr()
			type=what[0].split(" ")[0]
			valexp=recprint(what[2],offset+1)
			L=valexp[1]
			valname=valexp[0][1]
			L.append( ( ( (var,type) ,(":=","COPY"), (valname,valexp[0][0]) ), "COPY" ) )
			return ( (what[0].split(" ")[0],var), L)

		if(what[0].split(" ")[-1]=="MultiExpr"):
			L1=recprint(what[1],offset+1)[1]
			try:
				L2=recprint(what[2],offset+1)[1]
				return ( (None,None), L1+L2)
			except IndexError:
				return ( (None,None), L1)

		if(what[0]=="VAR" or what[0].split(" ")[-1]=="EPSILON"):
			#for which in what[1:]:
			#	recprint(which,offset+1)
			return ( (None,None), [])
		if(what[0] in ("Start","main")):
			L=recprint(what[1],offset+1)
			return L

		if(what[0]=="ASSIGN"):
			return ( (None,None), [])

		if(what[0].split(" ")[-1]=="If"):
			condn=recprint(what[1],offset+1)
			sif=recprint(what[2],offset+1)
			selse=recprint(what[3],offset+1)

			L=[]
			L=condn[1]
			condvar=condn[0][0]
			condtype=condn[0][1]

			sizeif=len(sif[1])
			sizeelse=len(selse[1])
		
			selse[1].append( ( ( ('->', 'SKIP'), ('LINE', sizeif) ), 'SKIP') )

			condstmnt = ( ( (condvar,condtype), ('?', 'IF'), ('->', 'SKIP'), ('LINE', sizeelse+1) ), 'IF')
			
			L.append(condstmnt)
			L=L+selse[1]+sif[1]

			return ( (None,None), L)


		print what[0]+"MAY NOT WORK"
                for which in what[1:]:
                        recprint(which,offset+1)



def myfunction(mypar):
	L=recprint(mypar,0)[1]
	for l in L:
		print l

def main():
	parser=Parser(myfunction,1)


main()
