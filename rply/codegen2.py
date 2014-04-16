from lexer import Lexer, Token
from parser import Parser
from codegen import Codegen
from itertools import *
from collections import defaultdict


def myfunction(L):
	for l in L:
		print l


codegenerator=Codegen(myfunction,1)
