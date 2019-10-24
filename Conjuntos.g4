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
    | add_conjunto
    | union_statement
    | interseccion_statement
    | difference_statement
    | remove_conjunto
    | suma_statement
    | promedio_statement
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

union_statement:
    VARIABLE 'u' VARIABLE
    | VARIABLE 'U' VARIABLE
    ;

interseccion_statement:
    VARIABLE 'w' VARIABLE
    | VARIABLE 'W' VARIABLE
    ;

difference_statement:
    VARIABLE 'diff' VARIABLE
    | VARIABLE 'DIFF' VARIABLE
    ;

add_conjunto:
    VARIABLE '[]+' expression
    ;

remove_conjunto:
    VARIABLE '[]-' expression
    ;

suma_statement:
    VARIABLE '++' 
    ;

promedio_statement:
    VARIABLE '%' 
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
