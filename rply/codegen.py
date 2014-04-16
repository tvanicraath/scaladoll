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


def newlabel():
		global seed
		seed+=1
		return "L"+str(seed)

def recprint(what,offset):
                for i in range(0,offset):
                        print "\t",

                if(isinstance(what,Token)):
                        print what.gettokentype(),what.getstr()
                        return ( (what.gettype(),what.getstr()), [] )

                print what[0]
		if(what[0].split(" ")[-1]=="ATOM" or what[0].split(" ")[-1]=="Const" or what[0].split(" ")[-1]=="ASSIGN"):
#			print "i am return "+str(recprint(what[1],offset+1))
			ans=recprint(what[1],offset+1)
			var=newvar(ans[0][0])
			L=ans[1]
			L.append( ( ( (var,ans[0][0]), (":=","COPY"), (ans[0][1]) ), "COPY") )
			return ( (ans[0][0],var), L)

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
			e1=recprint(what[1],offset+1)
			L1=e1[1]
			try:
				e2=recprint(what[2],offset+1)
				L2=e2[1]
				if(e2[0][0]==None):
					return ( e1[0], L1+L2)
				return ( e2[0], L1+L2 )
			except IndexError:
				return ( e1[0], L1)

		if(what[0].split(" ")[0]=="VAR"):
			recprint(what[1],offset+1)
			recprint(what[2],offset+1)
			return ( (None,None), [])

		if(what[0].split(" ")[-1]=="EPSILON"):
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

			newt=sif[0][0]
			newv=newvar(newt)
			sif[1].append( ( ( (newv,newt), (":=","COPY"), (sif[0][1]) ), "COPY") )
			
			if(selse[0][0]!=None):
				selse[1].append( ( ( (newv,newt), (":=","COPY"), (selse[0][1]) ), "COPY") )

			L=[]
			L=condn[1]
			condvar=condn[0][1]
			condtype=condn[0][0]

			sizeif=len(sif[1])
			sizeelse=len(selse[1])
			endstmt = newlabel()
			selse[1].append( ( ( ('->', 'GOTO'), ('LABEL', endstmt) ), 'GOTO') )
			labeltrue = newlabel()
			selse[1].append( ( ( ('L', 'LABEL'), ('LABEL', labeltrue) ), 'LABEL') )
			condstmnt = ( ( (condvar,condtype), ('?', 'IF'), ('->', 'GOTO'), ('LABEL', labeltrue) ), 'IF')
			sif[1].append( ( ( ('L', 'LABEL'), ('LABEL', endstmt) ), 'LABEL') )
						
			L.append(condstmnt)
			L=L+selse[1]+sif[1]

			return ( (newt,newv), L)

		if(what[0].split(" ")[-1]=="While"):
			condn=recprint(what[1],offset+1)
			strue=recprint(what[2],offset+1)

			newt=strue[0][0]
			newv=newvar(newt)
			strue[1].append( ( ( (newv,newt), (":=","COPY"), (strue[0][1]) ), "COPY") )

			startlabel=newlabel()	
			L=[]
			L.append( ( ( ('L', 'LABEL'), ('LABEL', startlabel) ), 'LABEL') )
			L=L+condn[1]
			condvar=condn[0][0]
			condtype=condn[0][1]
			endlabel=newlabel()
			strue[1].append( ( ( ("->", "GOTO"), ("LABEL", startlabel) ), "GOTO") )

			condnstmnt = ( ( (condvar,condtype), ("?", "IF"), ("->", "GOTO"), ("LABEL", endlabel) ), "WHILE_IF")
			L.append( condnstmnt );
			L=L+strue[1];
			L.append( ( ( ('L', 'LABEL'), ('LABEL', endlabel) ), 'LABEL') )
			return ( (newt, newv), L)

		'''
		if(what[0].split(" ")[-1]=="For_Range"):
			main=recprint(what[1],offset+1)
			mainvar=main[0][0]
			maintype=main[0][1]

			start=recprint(what[2],offset+1)
			startvar=start[0][0]
			starttype=start[0][1]
		
			end=recprint(what[3],offset+1)
			endvar=end[0][0]
			endtype=end[0][1]

			strue=recprint(what[4],offset+1)

			L=[]
			L=start[1]+end[1]
			L.append( ( ( (mainvar,maintype), (":=","COPY"), (startvar) ), "COPY" )  )

			var=newvar("Int")
			L.append( ( ( (var,"Int"), (":=","ASSIGNMENT"), (mainvar,maintype), ("<=","OPR"), (endvar,endtype) ), "ASSIGNMENT" ) )
		'''			

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
