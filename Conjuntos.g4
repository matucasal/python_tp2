grammar Conjuntos;

program:
    (statement)+
    ;

statement:
      expression
    | if_statement
    | assign_statement
    | while_statement
    | for_statement
    | assign_conjuntostatement
    ;

for_statement:
    'from' a=NUMBER 'to' b=NUMBER '?' (statement)+ '.?'
    ;

while_statement:
    'while' booleanexpression '?' (statement)+ '.?'
    ;

if_statement:
    'if' booleanexpression '?' (statement)+ '.?'
    ;

assign_statement:
    VARIABLE '<-' expression
    ;

assign_conjuntostatement:
    VARIABLE '[]=' arr_expression
    ;

booleanexpression:
    expression COMPARATION_OPERATOR expression
    ;

conjunto_init:
    expression ( ',' expression )*
;

arr_expression:
     term ( ',' term )*
    ;

expression:
      term
    | expression '+' term
    | expression '-' term
    | term ( ',' term )*
    ;

term:
      factor
    | term ('*'|'/'|'^') factor
    ;

factor:
      num=NUMBER
    | var=VARIABLE
    | '(' expression ')'
    ;

VARIABLE: [a-zA-Z]+[a-zA-Z0-9]*;

COMPARATION_OPERATOR: '=='|'!='|'>='|'>'|'<='|'<' ;

NUMBER : DIGIT+;
DIGIT  : [0-9];

WS : [ \r\n\t] -> skip;
