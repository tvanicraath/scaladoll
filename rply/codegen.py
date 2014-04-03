from lexer import Lexer, Token
from parser import Parser
from itertools import *
from collections import defaultdict


def myfunction(mypar):
	print mypar

def main():
	parser=Parser(myfunction,1)


main()
