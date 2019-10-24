#-*- coding: utf-8 -*-

import antlr4
from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream

from ConjuntosLexer import ConjuntosLexer
from ConjuntosParser import ConjuntosParser
from ConjuntosListener import ConjuntosListener

class Visitador(ConjuntosListener):

    def __init__(self):
        self.variables = {}

    def enterProgram(self, ctx:ConjuntosParser.ProgramContext):
        for nodo in ctx.children:
            self.visitStatement(nodo)

    def visitStatement(self, ctx:ConjuntosParser.StatementContext):
        if type(ctx.children[0]) == ConjuntosParser.ExpressionContext:
            valor = self.visitExpression(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.If_statementContext:
            self.visitIf_statement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Assign_statementContext:
            self.visitAssignStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Assign_conjuntostatementContext:
            self.visitAssignConjuntoStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.While_statementContext:
            self.visitWhileStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.For_statementContext:
            self.visitForStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Add_conjuntoContext:
            self.visitAddConjunto(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Conjunto_initContext:
            self.visitDeclareConjunto(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Union_statementContext:
            self.visitUnionStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Interseccion_statementContext:
            self.visitInterseccionStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Difference_statementContext:
            self.visitDifferenceStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Remove_conjuntoContext:
            self.visitRemoveConjunto(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Suma_statementContext:
            self.visitSumaStatement(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.Promedio_statementContext:
            self.visitPromedioStatement(ctx.children[0])
        else:
            #print(type(ctx)) # No deberia llegar nunca
            print("error")

    def visitForStatement(self, ctx:ConjuntosParser.For_statementContext):
        for statement in ctx.children[5:-1]:
            for x in range(int(ctx.a.text), int(ctx.b.text)):
                self.visitStatement(statement)

    def visitWhileStatement(self, ctx:ConjuntosParser.While_statementContext):
        conditionValue = self.visitBooleanexpression(ctx.children[1])
        while conditionValue:
            for nodo in ctx.children[3:-1]:
                self.visitStatement(nodo)

            conditionValue = self.visitBooleanexpression(ctx.children[1])

    def visitAddConjunto(self, ctx:ConjuntosParser.Add_conjuntoContext):
        print ("Estoy en add")
        value = self.visitArrExpression(ctx.children[2])
        self.variables[ctx.children[0].symbol.text].append(value[0]) 



    def visitAssignStatement(self, ctx:ConjuntosParser.Assign_statementContext):
        value = self.visitExpression(ctx.children[2])
        self.variables[ctx.children[0].symbol.text] = value


    def visitAssignConjuntoStatement(self, ctx:ConjuntosParser.Assign_conjuntostatementContext):
        value = self.visitArrExpression(ctx.children[2])
        self.variables[ctx.children[0].symbol.text] = value

    def visitIf_statement(self, ctx:ConjuntosParser.If_statementContext):
        logicValue = self.visitBooleanexpression(ctx.children[1])
        if logicValue:
            for nodo in ctx.children[3:-1]:  # Desde la 4ta posic hasta la anteultima
                self.visitStatement(nodo)

    def visitBooleanexpression(self, ctx:ConjuntosParser.BooleanexpressionContext):
        value1 = self.visitExpression(ctx.children[0])
        value2 = self.visitExpression(ctx.children[2])
        op = ctx.children[1].symbol.text
        return eval(str(value1) + op + str(value2))

    def visitExpression(self, ctx:ConjuntosParser.ExpressionContext):
        
        valor = 0
        if type(ctx.children[0]) == ConjuntosParser.TermContext:
            valor = self.visitTerm(ctx.children[0])
        elif type(ctx.children[0]) == ConjuntosParser.ExpressionContext:
            valor1 = self.visitExpression(ctx.children[0])
            valor2 = self.visitTerm(ctx.children[2])
            if ctx.children[1].symbol.text == "+":
                valor = valor1 + valor2
            else:
                valor = valor1 - valor2

        return valor

    def visitArrExpression(self, ctx:ConjuntosParser.ExpressionContext):
        listElements = []
        
        #Esto quiere decir que es un array con mas de un componente
        if (len(ctx.children) > 1):
            for nodo in ctx.children:
                if type(nodo) == ConjuntosParser.TermContext:
                    listElements.append(self.visitTerm(nodo))
        else:
            listElements.append(self.visitTerm(ctx.children[0]))

        return listElements


    def visitTerm(self, ctx:ConjuntosParser.TermContext):
        valor = 0
        if type(ctx.children[0]) == ConjuntosParser.FactorContext:
            valor = self.visitFactor(ctx.children[0])
        else:
            valor1 = self.visitTerm(ctx.children[0])
            valor2 = self.visitFactor(ctx.children[2])
            if ctx.children[1].symbol.text == "*":
                valor = valor1 * valor2
            elif ctx.children[1].symbol.text == "/":
                valor = valor1 / valor2
            else:
                valor = valor1 ** valor2

        return valor

    def visitFactor(self, ctx:ConjuntosParser.FactorContext):
        valor = 0
        
        if len(ctx.children) == 1:
            if ctx.var:
                valor = self.variables[ctx.var.text]
                print (ctx.var.text , "->" , valor)
            else:
                valor = int(ctx.num.text)

        else:
            valor = self.visitExpression(ctx.children[1])

        return valor


    def visitDeclareConjunto(self, ctx:ConjuntosParser.Conjunto_initContext):
        thislist = []

        for nodo in ctx.children:
            self.visitExpression(nodo)

    #union_statement
    def visitUnionStatement (self, ctx:ConjuntosParser.Union_statementContext):
        print("estoy en la union")
        final_list = list(set(self.variables[ctx.children[0].symbol.text]) | set(self.variables[ctx.children[2].symbol.text])) 
        print(final_list )
        
    #interseccion_statement
    def visitInterseccionStatement (self, ctx:ConjuntosParser.Interseccion_statementContext):
        print("estoy en la interseccion")
        #final_list = list(set(self.variables[ctx.children[0].symbol.text]) | set(self.variables[ctx.children[2].symbol.text])) 
        final_list = list(set(self.variables[ctx.children[0].symbol.text]) & set(self.variables[ctx.children[2].symbol.text])) 
        print(final_list )

    #difference_statement
    def visitDifferenceStatement (self, ctx:ConjuntosParser.Difference_statementContext):
        print("estoy en la difference")
        #final_list = list(set(self.variables[ctx.children[0].symbol.text]) | set(self.variables[ctx.children[2].symbol.text])) 
        final_list = list(set(self.variables[ctx.children[0].symbol.text]) - set(self.variables[ctx.children[2].symbol.text])) 
        print(final_list )

    #remove_conjunto
    def visitRemoveConjunto(self, ctx:ConjuntosParser.Remove_conjuntoContext):
        print ("Estoy en remove")
        value = self.visitArrExpression(ctx.children[2])
        #Algo asi tengo que hacer: if thing in some_list: some_list.remove(thing)
        if value[0] in self.variables[ctx.children[0].symbol.text]: self.variables[ctx.children[0].symbol.text].remove(value[0])
       

    #suma_statement
    def visitSumaStatement (self, ctx:ConjuntosParser.Suma_statementContext):
        print ("Estoy en suma")
        #Algo asi tengo que hacer: if thing in some_list: some_list.remove(thing)
        print (sum(self.variables[ctx.children[0].symbol.text]) )
        

    
    #promedio_statement
    def visitPromedioStatement (self, ctx:ConjuntosParser.Promedio_statementContext):
        print ("Estoy en promedio")
        print ( self.Average(self.variables[ctx.children[0].symbol.text])  )

    #Metodo para sacar el promedio
    def Average(self, lst): 
        return sum(lst) / len(lst) 


expr = '''
a []= 1,2,3
b []= 4
c []= 8,7,1
a []+ 8
a []- 2

a

a++
a%

a u c
a w c
a diff c

'''


print('Comenzando...')
input = InputStream(expr)
lexer = ConjuntosLexer(input)
stream = CommonTokenStream(lexer)
parser = ConjuntosParser(stream)

tree = parser.program()

nuestroListener = Visitador()
walker = ParseTreeWalker()
walker.walk(nuestroListener, tree)

print('Fin.')