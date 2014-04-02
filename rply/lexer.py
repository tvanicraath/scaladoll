from pygments import *
import pygments.lexers.jvm
from itertools import *

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

		return name			

	
	def __init__(self,name,value):
		name=self.removedots(name,value)
		self.name=name
		self.value=value
		self.lineno=None
		self.sourcepos=None
	
	def gettokentype(self):
		return self.name

        def getsourcepos(self):
                return None

        def getstr(self):
                return self.value
	
class Lexer:

	lexed_token={}
	debug=0
	def __init__(self,filename,debug=0):
		self.debug=debug
		try:
	                f=open(filename)
        	        lines=""
                	for line in f:
                        	lines=lines+line
	                self.lexed_tokens=lex(lines, pygments.lexers.jvm.ScalaLexer())
		except TypeError:
			return
	
	def tokenize_string(self,string):
		self.lexed_tokens={}
		self.lexed_tokens=lex(string, pygments.lexers.jvm.ScalaLexer())

	def lex(self,string=None):
		if(string):
			self.tokenize_string(string)
		tokens=[]
		for token in self.lexed_tokens:
			(name,value)=token
			if(str(name)=="Token.Text"):	continue
			tokens.append(Token(name,value))
		if(self.debug):
			for token in tokens:
				print token.getstr(),token.gettokentype()
		return chain(tokens)


def main():
	rac=Lexer("hw.scala")
	rac.lex()

#main()
