from pygments import *
import pygments.lexers.jvm
from itertools import *
import sys

class Token:

	def opname(self,value):
		if(value=="+"):	return "Plus"
		if(value=="-"):	return "Minus"
		if(value=="*"):	return "Prod"
		if(value=="/"):	return "Div"
		if(value=="%"):	return "Mod"
		if(value=="("):	return "LBrac"
		if(value==")"):	return "RBrac"
		if(value=="{"): return "LCurl"
		if(value=="}"): return "RCurl"
		if(value=="["): return "LSquare"		
		if(value=="]"): return "RSquare"
		if(value==";"):	return "SColon"
		if(value=="="):	return "Equal"
		if(value==","):	return "Comma"
		if(value=="<"):	return "LT"
		if(value==">"):	return "GT"
		if(value==">="):	return "GE"
		if(value=="<="):	return "LE"
		if(value=="=="):	return "EE"
		if(value=="!="):	return "NE"
		if(value=="&&"):	return "And"
		if(value=="||"):	return "Or"
		if(value=="^"):		return "Xor"
		if(value=="@@@"):	return "LineSeperator"
		return "Rachit"

	def namename(self,value):
		if(value=="println"):	return "Print"

	def keyname(self,value):
		if(value=="object"):	return "Object"
		if(value=="def"):	return "Def"
		if(value==":"):		return "Colon"
		if(value=="var"):	return "Var"
		if(value=="val"):	return "Val"
		if(value=="="):		return "Equal"
		if(value=="if"):	return "If"
		if(value=="else"):	return "Else"
		if(value=="for"):	return "For"
		if(value=="else"):	return "Else"
		if(value=="Array"):	return "Array"
		if(value=="while"):	return "While"
		if(value=="<-"):	return "InRange"

	def removedots(self,name,value):

		name=str(name)
		if(name=="Token.Operator"):
			name=name+"."+self.opname(value)
		if(name=="Token.Name"):
			if(self.namename(value)):
				name=name+"."+self.namename(value)
		if(name=="Token.Keyword"):
			if(self.keyname(value)):
				name=name+"."+self.keyname(value)
		if(value=="Array"):
			name="Token.Keyword.Array"
		if(value=="to"):
			name="Token.Keyword.To"
		if(value=="until"):
			name="Token.Keyword.Until"


		return name			

	
	def __init__(self,name,value):
		name=self.removedots(name,value)
		self.name=name
		self.value=value
		self.lineno=5
		self.sourcepos=34
		self.type=None
	
	def gettokentype(self):
		return self.name

        def getsourcepos(self):
                return self.lineno

        def getstr(self):
                return self.value

	def gettype(self):
		return self.type
	
class Lexer:

	lexed_token={}
	debug=0
	filename=None
	def __init__(self,filename,debug=0):
		self.debug=debug
		try:
	                f=open(filename)
        	        lines=""
                	for line in f:
                        	lines=lines+line+"@@@"
	                self.lexed_tokens=lex(lines, pygments.lexers.jvm.ScalaLexer())
			self.filename=filename
		except TypeError:
			return
	
	def tokenize_string(self,string):
		self.lexed_tokens={}
		self.lexed_tokens=lex(string, pygments.lexers.jvm.ScalaLexer())

	def lex(self,string=None):
		if(string):
			self.tokenize_string(string)
		tokens=[]
		line_count=1
		for token in self.lexed_tokens:
			(name,value)=token
			if(value=="="):
				name="Token.Operator"
			if(str(name)=="Token.Text"):	continue
			if(str(value)=="@@@"):
				line_count+=1
				continue
			tokens.append(Token(name,value))
			tokens[-1].lineno=line_count

		tokens=self.rename_tokens(tokens)

		if(self.debug):
			for token in tokens:
				if(token.gettokentype()=="Token.Name"):
					print token.getstr(),token.gettokentype(),token.gettype()
				else:
					print token.getstr(),token.gettokentype()

		return chain(tokens)


	def rename_tokens(self,tokens):
		start_of_scope=["Token.Keyword.Def","Token.Keyword.If","Token.Keyword.Else","Token.Keyword.For","Token.Keyword.While"]
		variable_names={}
		token_type={}
		i=0
		uniq_counter=102
		curly_count=0

		for token in tokens:
			if(token.name in start_of_scope):	curly_count+=1
			if(token.name=="Token.Operator.RCurl"):
				for name in variable_names.keys():
					(oldname,ccount)=variable_names[name][-1]
					if(ccount==curly_count):
						variable_names[name].pop()
					if(len(variable_names[name])==0):
						del variable_names[name]

				curly_count-=1

			if(token.name=="Token.Literal.Number.Integer"):
				token.type="Int"
			if(token.name=="Token.Literal.Number.Float"):
				token.type="Float"
			if(token.name=="Token.Literal.String"):
				token.type="String"

			if(token.name=="Token.Name"):
			   try:
				if(len(tokens)>(i+1) and tokens[i+1].name=="Token.Keyword.Colon"):
					#declaration
					newname=token.value+"@"+str(uniq_counter)
					if(token.value in variable_names):
						(oldname,oldscope)=variable_names[token.value][-1]
						if(oldscope==curly_count):
							sys.exit("[Sementic Error] Cannot redeclare variable '"+ token.value + "' in same scope as '"+token.value+"' (Line: "+str(token.getsourcepos())+").")
						variable_names[token.value].append((newname,curly_count))
					else:
						 variable_names[token.value]=[]
						 variable_names[token.value].append((newname,curly_count))
					uniq_counter+=1
					token.value=newname
					token.type=tokens[i+2].value
					token_type[newname]=token.type

				elif(len(tokens)>(i+1) and tokens[i+1].name=="Token.Operator.LBrac"):
					#its function, do nothing
					pass

				else:
					#use
					if(not token.value in variable_names):
						sys.exit("[Sementic Error] Cannot use variable '"+ token.value + "' without initializing it (Line: "+str(token.getsourcepos())+").")
					(newname,scope)=variable_names[token.value][-1]
					token.value=newname
					token.type=token_type[newname]
			   except IndexError:
				sys.exit("[Sementic Error] Cannot use variable '"+ token.value + "' without initializing it (Line: "+str(token.getsourcepos())+").")

			i+=1

		return tokens

def main():
	rac=Lexer("hw.scala")
	rac.lex()

#main()
