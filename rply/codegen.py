from lexer import Lexer, Token
from parser import Parser
from itertools import *
from collections import defaultdict
seed=118

class Codegen:

	def dumpstrings(self):
		f=open("strings.txt","w")
		f.write(', '.join([' : '.join((k, str(self.all_prints[k]))) for k in sorted(self.all_prints, key=self.all_prints.get, reverse=True)]))


	def newvar(self,type):
        	        global seed
                	seed+=1
	                if(type=="Int"):        return "t@@"+str(seed)
        	        if(type=="Float"):      return "f@@"+str(seed)
                	if(type=="String"):     return "s@@"+str(seed)

	def newstr(self):
		global seed
		seed+=1
		return "@.str"+str(seed)
	
	
	def newlabel(self):
			global seed
			seed+=1
			return "L"+str(seed)

	def recprint(self,what,offset):
                for i in range(0,offset):
                        #print "\t",
			pass

                if(isinstance(what,Token)):
                        #print what.gettokentype(),what.getstr()
                        return ( (what.gettype(),what.getstr()), [] )

		if(isinstance(what,int)):
			#print "intval: "+str(what)
			return ( (None,None), [])

                #print what[0]
		if(what[0].split(" ")[-1]=="ATOM" or what[0].split(" ")[-1]=="Const" or what[0].split(" ")[-1]=="ASSIGN"):
#			print "i am return "+str(recprint(what[1],offset+1))
			ans=self.recprint(what[1],offset+1)
			var=self.newvar(ans[0][0])
			L=ans[1]
			L.append( ( ( (var,ans[0][0]), (":=","COPY"), (ans[0][1],ans[0][0])), "COPY") )
			return ( (ans[0][0],var), L)

		if(what[0].split(" ")[-1]=="EXP"):
			if(len(what)==2):
				op=rself.ecprint(what[1],offset+1)
				L=[]
				L=op[1]
				opret=op[0][1]
				optype=op[0][0]
				type=what[0].split(" ")[0]
				var=self.newvar(type)
				L.append( ( ( (var,type), (":=","COPY"), (opret,optype) ), "COPY" ) )
				return ( (type,var), L)

			else:
				op=what[1].getstr()
				op1=self.recprint(what[2],offset+1)
				op2=self.recprint(what[3],offset+1)
				L=[]
				L=op1[1]+op2[1]
				op1ret=op1[0][1]
				op1type=op1[0][0]
				op2ret=op2[0][1]
				op2type=op2[0][0]
				type=what[0].split(" ")[0]
				var=self.newvar(type)
				L.append( ( ( (var,type), (":=","ASSIGNMENT"), (op1ret,op1type), (op,"OPR"), (op2ret,op2type) ), "ASSIGNMENT" ) )
				return ( (type,var), L )

		if(what[0].split(" ")[-1]=="VAR_EQUALS"):
			var=what[1].getstr()
			type=what[0].split(" ")[0]
			valexp=self.recprint(what[2],offset+1)
			L=valexp[1]
			valname=valexp[0][1]
			L.append( ( ( (var,type) ,(":=","COPY"), (valname,valexp[0][0]) ), "COPY" ) )
			return ( (what[0].split(" ")[0],var), L)

		if(what[0].split(" ")[-1]=="MultiExpr"):
			e1=self.recprint(what[1],offset+1)
			L1=e1[1]
			try:
				e2=self.recprint(what[2],offset+1)
				L2=e2[1]
				if(e2[0][0]==None):
					return ( e1[0], L1+L2)
				return ( e2[0], L1+L2 )
			except IndexError:
				return ( e1[0], L1)

		if(what[0].split(" ")[0]=="VAR"):
			#recprint(what[1],offset+1)
			#recprint(what[2],offset+1)
			return ( (None,None), [])

		if(what[0].split(" ")[-1]=="EPSILON"):
			#for which in what[1:]:
			#	recprint(which,offset+1)
			return ( (None,None), [])
		if(what[0] in ("Start","main")):
			L=self.recprint(what[1],offset+1)
			if(what[0]=="main"):	self.dumpstrings()
			return L

		if(what[0]=="ASSIGN"):
			return ( (None,None), [])

		if(what[0].split(" ")[-1]=="If"):
			condn=self.recprint(what[1],offset+1)
			sif=self.recprint(what[2],offset+1)
			selse=self.recprint(what[3],offset+1)

			newt=sif[0][0]
			newv=self.newvar(newt)
			if(newt!=None):
				sif[1].append( ( ( (newv,newt), (":=","COPY"), (sif[0][1],newt) ), "COPY") )
			
			if(selse[0][0]!=None):
				selse[1].append( ( ( (newv,newt), (":=","COPY"), (selse[0][1],newt) ), "COPY") )

			L=[]
			L=condn[1]
			condvar=condn[0][1]
			condtype=condn[0][0]

			sizeif=len(sif[1])
			sizeelse=len(selse[1])
			endstmt = self.newlabel()
			selse[1].append( ( ( ('->', 'GOTO'), ('LABEL', endstmt) ), 'GOTO') )
			labeltrue = self.newlabel()
			selse[1].append( ( ( ('L', 'LABEL'), ('LABEL', labeltrue) ), 'LABEL') )
			condstmnt = ( ( (condvar,condtype), ('?', 'IF'), ('->', 'GOTO'), ('LABEL', labeltrue) ), 'IF')
			sif[1].append( ( ( ('L', 'LABEL'), ('LABEL', endstmt) ), 'LABEL') )
						
			L.append(condstmnt)
			L=L+selse[1]+sif[1]

			return ( (newt,newv), L)

		if(what[0].split(" ")[-1]=="While"):
			condn=self.recprint(what[1],offset+1)
			strue=self.recprint(what[2],offset+1)

			newt=strue[0][0]
			newv=self.newvar(newt)
			strue[1].append( ( ( (newv,newt), (":=","COPY"), (strue[0][1],newt) ), "COPY") )

			startlabel=self.newlabel()	
			L=[]
			L.append( ( ( ('L', 'LABEL'), ('LABEL', startlabel) ), 'LABEL') )
			L=L+condn[1]
			condvar=condn[0][0]
			condtype=condn[0][1]
			endlabel=self.newlabel()
			strue[1].append( ( ( ("->", "GOTO"), ("LABEL", startlabel) ), "GOTO") )

			condnstmnt = ( ( (condvar,condtype), ("?", "IF"), ("->", "GOTO"), ("LABEL", endlabel) ), "WHILE_IF")
			L.append( condnstmnt );
			L=L+strue[1];
			L.append( ( ( ('L', 'LABEL'), ('LABEL', endlabel) ), 'LABEL') )
			return ( (newt, newv), L)


		if(what[0].split(" ")[-1]=="GetVal1"):
			array=self.recprint(what[1],offset+1)
			index=self.recprint(what[2],offset+1)
			var=self.newvar(array[0][0])

			L=index[1]
			L.append( ( ( (var,array[0][0]), (":=","COPY"), (array[0][1],"ARRAY"), (index[0][1],"INDEX")), "GET_VAL") )

			return ( (array[0][0],var), L)

		if(what[0].split(" ")[-1]=="SetVal1"):
			array=self.recprint(what[1],offset+1)
			index=self.recprint(what[2],offset+1)
			value=self.recprint(what[3],offset+1)
			newv=self.newvar(array[0][0])

			L=index[1]+value[1]
			L.append( ( ( (array[0][1],array[0][0]), (index[0][1],"INDEX"), (":=","COPY"), (value[0][1],value[0][0])), "SET_VAL") )
			L.append( ( ( (newv,array[0][0]), (":=","COPY"), (value[0][1],value[0][0]) ), "COPY") )
			
			return ( (array[0][0],newv), L)


		if(what[0].split(" ")[-1]=="GetVal2"):
			array=self.recprint(what[1],offset+1)
			index1=self.recprint(what[2],offset+1)
			index2=self.recprint(what[3],offset+1)
			size2=int(what[5])
			var=self.newvar(array[0][0])

			L=index1[1]+index2[1]

			actindex=self.newvar("Int")
			L.append( ( ( (actindex,"Int"), (":=","ASSIGNMENT"), (index1[0][1],"Int"), ("*","OPR"), (size2,"Int") ), "ASSIGNMENT" ) )
			L.append( ( ( (actindex,"Int"), (":=","ASSIGNMENT"), (actindex,"Int"), ("+","OPR"), (index2[0][1],"Int") ), "ASSIGNMENT" ) )
			L.append( ( ( (var,array[0][0]), (":=","COPY"), (array[0][1],"ARRAY"), (actindex,"INDEX")), "GET_VAL") )

			return ( (array[0][0],var), L)

                if(what[0].split(" ")[-1]=="SetVal2"):
                        array=self.recprint(what[1],offset+1)
                        index1=self.recprint(what[2],offset+1)
                        index2=self.recprint(what[3],offset+1)
			value=self.recprint(what[4],offset+1)
                        size2=int(what[6])
                        newv=self.newvar(array[0][0])

                        L=index1[1]+index2[1]+value[1]

                        actindex=self.newvar("Int")
                        L.append( ( ( (actindex,"Int"), (":=","ASSIGNMENT"), (index1[0][1],"Int"), ("*","OPR"), (size2,"Int") ), "ASSIGNMENT" ) )
                        L.append( ( ( (actindex,"Int"), (":=","ASSIGNMENT"), (actindex,"Int"), ("+","OPR"), (index2[0][1],"Int") ), "ASSIGNMENT" ) )
                        L.append( ( ( (array[0][1],array[0][0]), (actindex,"INDEX"), (":=","COPY"), (value[0][1],value[0][0])), "SET_VAL") )
			L.append( ( ( (newv,array[0][0]), (":=","COPY"), (value[0][1],value[0][0]) ), "COPY") )

                        return ( (array[0][0],newv), L)

		if(what[0].split(" ")[-1]=="PrintInt"):
			toprint=self.recprint(what[1],offset+1)
			L=toprint[1]
			mystr=self.newstr()
			self.all_prints[mystr]="%d"
			L.append( ( ( (">>","PrintInt"), (mystr,"VALUE"), (toprint[0][1],toprint[0][0])), "PRINT") )
			return ( (toprint[0][0],toprint[0][1]), L)
		if(what[0].split(" ")[-1]=="PrintFloat"):
                        toprint=self.recprint(what[1],offset+1)
                        L=toprint[1]
			mystr=self.newstr()
			self.all_prints[mystr]="%f"
                        L.append( ( ( (">>","PrintFloat"), (mystr,"VALUE"), (toprint[0][1],toprint[0][0])), "PRINT") )             
                        return ( (toprint[0][0],toprint[0][1]), L)
		if(what[0].split(" ")[-1]=="PrintString"):
			L=[]
			mystr=self.newstr()
			self.all_prints[mystr]=what[1].value
			L.append( ( ( (">>","PrintString"), (mystr,"VALUE")), "PRINT") )
			return ( (None,None), L)



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
                        self.recprint(which,offset+1)



	def myfunction(self,mypar):
		L=self.recprint(mypar,0)[1]
		self.returnfunction(L)

	def __init__(self,returnfunction,debuglevel):
		self.returnfunction=returnfunction
		self.all_prints={}
		parser=Parser(self.myfunction,debuglevel)
		pass


def main():
	parser=Parser(myfunction,1)


#main()
