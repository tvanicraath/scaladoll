import pygments.lexers.jvm
from pygments.lexer import Lexer, RegexLexer, include, bygroups

f=open("intro.scala")
lines=""
for line in f:
	lines=lines+line

pygments.lexers.jvm.ScalaLexer(lines.Regex)


