from lexer import Lexer, Token
from parser import Parser
from itertools import *
from collections import defaultdict


def recprint(what,offset):
                for i in range(0,offset):
                        print "\t",

                if(isinstance(what,Token)):
                        print what.gettokentype(),what.getstr()
                        return (what.gettype(),what.getstr())

                print what[0]
                for which in what[1:]:
                        recprint(which,offset+1)



def myfunction(mypar):
	recprint(mypar,0)

def main():
	parser=Parser(myfunction,0)


main()
