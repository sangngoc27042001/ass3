
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
    Symbol("getInt",MType([],IntType())),
    Symbol("putIntLn",MType([IntType()],VoidType()))
    ]
            
    
    def __init__(self,ast):
        self.ast = ast

 
    
    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def visitProgram(self,ast:Program, c):
        programContex = {}
        c.append(programContex)
        for x in ast.decl:
            self.visit(x, c)
        # return [self.visit(x,c) for x in ast.decl]

    def visitClassDecl(self,ast, c):
        programContex = c[-1]
        if ast.classname.name in programContex.keys():
            raise Redeclared(Class(),ast.classname.name)
        else:
            programContex[ast.classname.name] = {}
            for x in ast.memlist:
                self.visit(x, programContex[ast.classname.name])

    def visitAttributeDecl(self,ast, c):
        classContext = c
        kind = ast.kind
        if type(ast.decl) is VarDecl:
            name = ast.decl.variable.name
            typeat = ast.decl.varType
            value = ast.decl.varInit
        else:
            name = ast.decl.constant.name
            typeat = ast.decl.constType
            value = ast.decl.value
        if name in classContext.keys():
            raise Redeclared(Attribute(), name)
        else:
            classContext[name] = [typeat, kind, name, value]

    def visitMethodDecl(self,ast, c):
        classContext = c
        name = ast.name.name
        if name in classContext.keys():
            raise Redeclared(Method(), name)
        kind = ast.kind
        param = []
        for x in ast.param:
            param.append(self.visit(x,(param,'PARAMS')))
        body = self.visit(ast.body,(c, param))
        classContext[name] = [kind, name, param, body]

    def visitVarDecl(self,ast, c):
        if c[1] == 'PARAMS':
            if ast.variable.name in [x[2] for x in c[0]]:
                raise Redeclared(Parameter(), ast.variable.name)
            return [ast.varType, Instance(), ast.variable.name, ast.varInit]
        elif c[1] == 'INST':
            if ast.variable.name in [x[2] for x in c[2]] + [x['information'][2] for x in c[3]]:
                raise Redeclared(Variable(), ast.variable.name)
            return {'instruction_ast': ast, 'information': [ast.varType, Instance(), ast.variable.name, ast.varInit]}

    def visitConstDecl(self,ast, c):
        if c[1] == 'INST':
            if ast.constant.name in [x[2] for x in c[2]] + [x['information'][2] for x in c[3]]:
                raise Redeclared(Constant(), ast.constant.name)
            return {'instruction_ast': ast, 'information': [ast.constType, Instance(), ast.constant.name, ast.value]}

    def visitBlock(self, ast, c):
        param = c[1]
        res = []
        for inst in ast.inst:
            if isinstance(inst,(VarDecl, ConstDecl)):
                res += [self.visit(inst, (c,'INST',param, res))]
        return res


    

