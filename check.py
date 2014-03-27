from pygments import *
import pygments.lexers.jvm
from itertools import *


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
		global lexed_tokens
		try:
			return lexed_tokens.next()
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
