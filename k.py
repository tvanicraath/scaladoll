import ply.yacc as yacc

def p_assign(p):

 '''assign : NAME EQUALS expr'''

def p_expr(p):

 '''expr : expr PLUS term

 | expr MINUS term

 | term'''

def p_term(p):

 '''term : term TIMES factor

 | term DIVIDE factor

 | factor'''

def p_factor(p):

 '''factor : NUMBER'''

yacc.yacc()
