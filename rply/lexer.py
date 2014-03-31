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
		return "Rachit"


	def removedots(self,name,value):
		name=str(name)
		if(name=="Token.Operator"):
			name=name+"."+self.opname(value)

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
	def __init__(self,filename):
                f=open(filename)
                lines=""
                for line in f:
                        lines=lines+line
                self.lexed_tokens=lex(lines, pygments.lexers.jvm.ScalaLexer())
	
	def tokenize_string(self,string):
		self.lexed_tokens={}
		self.lexed_tokens=lex(string, pygments.lexers.jvm.ScalaLexer())

	def lex(self,string=None):
		if(string):
			self.tokenize_string(string)
		tokens=[]
		for token in self.lexed_tokens:
			(name,value)=token
			if(name=="Token.Text"):
				continue
			tokens.append(Token(name,value))

		tokens=tokens[:-1]
#		for token in tokens:
#			print token.getstr(),token.gettokentype()
		return chain(tokens)


def main():
	rac=Lexer("bf.scala")
	rac.lex()

#main()

'''
class tokens:
	lexed_tokens={}
	tokens = ['NUMBER']

	def input(self):
		s="fff"
	        # Pull off the first character to see if s looks like a string
        	c = s[:1]
	        if not isinstance(c,StringTypes):
	            raise ValueError("Expected a string")
        	self.lexdata = s
	        self.lexpos = 0
        	self.lexlen = len(s)


	def __init__(self,filename="bf.scala"):
		global tokens
		f=open(filename)
		lines=""
		for line in f:
        		lines=lines+line
		self.lexed_tokens=chain(lex(lines, pygments.lexers.jvm.ScalaLexer()))

	def get_next_token(self):
		self.lexed_tokens
		try:
			return self.lexed_tokens.next()
		except StopIteration:
			return False

	def token(self):
		nextToken=self.get_next_token()
		
		if(not nextToken):
			return None;

		class rac_token:
			(type, value, lineno, lexpos) = (None, None, None, None)
			def __init__(self,nextToken):
				(self.type, self.value)=nextToken

		return rac_token(nextToken)


	
def main():
	
	mylexer=tokens("bf.scala")
	while(True):
		nextToken=mylexer.token()
		if(not nextToken):
			break
		print nextToken.type, nextToken.value

#main()
'''
