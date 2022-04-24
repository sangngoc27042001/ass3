
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *

class Ctype:
    pass

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None, kind = None, scope = None, isClassMember = None):
        self.name = name
        self.mtype = mtype
        self.value = value
        self.kind = kind
        self.scope = scope
        self.isClassMember = isClassMember

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
    Symbol("getInt",MType([],IntType())),
    Symbol("putIntLn",MType([IntType()],VoidType()))
    ]
            
    
    def __init__(self,ast):
        self.ast = ast

 
    
    def check(self):
        return self.visit(self.ast,[])

    def visitProgram(self, ast: Program, c):
        for x in ast.decl:
            self.visit(x, c)
        return

    def visitClassDecl(self,ast:ClassDecl, c):
        self.visit(ast.classname, ([x for x in c if type(x.mtype) is Ctype],Class()))
        c.append(Symbol(ast.classname.name, Ctype(), None))
        localBound = len(c)
        for mem in ast.memlist:
            self.visit(mem, (c, localBound))
        thisClass = list(filter(lambda x: x.name == ast.classname.name, c))[0]
        thisClass.scope = (localBound, len(c))
        return

    def visitId(self, ast: Id, c):
        if c[1] == 'CHECK_UNDECLARED_METHOD':
            object = list(filter(lambda x: x.name == c[3], c[0]))[-1]
            classObject = list(filter(lambda x: x.name == object.mtype.classname.name, c[0]))[0]
            upperBound, lowerBound = classObject.scope
            attributeInClass = [x.name for x in c[0][upperBound: lowerBound] if x.isClassMember and type(x.mtype) == MType]
            if ast.name not in attributeInClass:
                raise Undeclared(c[2], ast.name)
        elif c[1] == 'CHECK_UNDECLARED_ATTRIBUTE':
            object = list(filter(lambda x: x.name == c[3], c[0]))[-1]
            classObject = list(filter(lambda x: x.name == object.mtype.classname.name, c[0]))[0]
            upperBound, lowerBound = classObject.scope
            attributeInClass = [x.name for x in c[0][upperBound: lowerBound] if x.isClassMember and type(x.mtype) != MType]
            if ast.name not in attributeInClass:
                raise Undeclared(c[2], ast.name)
        elif c[1] == 'CHECK_UNDECLARED_CLASS':
            allClasses = [x.name for x in c[0] if type(x.mtype) is Ctype]
            if c[3] not in allClasses:
                raise Undeclared(c[2], ast.name)
        elif c[1] == 'CHECK_UNDECLARED_IDENTIFIER':
            nearestClass = [x for x in c[0] if type(x.mtype) is Ctype][-1]
            localBound = c[0].index(nearestClass) + 1
            a = [x.name for x in c[0][localBound:]]
            if ast not in a:
                raise Undeclared(c[2],ast.name)
        elif ast.name in [x.name for x in c[0]]:
            raise Redeclared(c[1],ast.name)

        return ast.name

    def visitAttributeDecl(self,ast: AttributeDecl, c_localBound):
        c, localBound = c_localBound
        name = self.visit(ast.decl.variable, (c[localBound:], Attribute())) if type(ast.decl) is VarDecl else self.visit(ast.decl.constant, (c[localBound:], Attribute()))
        mtype = ast.decl.varType if type(ast.decl) is VarDecl else ast.decl.constType
        value = ast.decl.varInit if type(ast.decl) is VarDecl else ast.decl.value
        kind = ast.kind

        c.append(Symbol(name, mtype, value, kind, isClassMember=True))
        return

    def visitMethodDecl(self,ast: MethodDecl, c_localBound):
        c, localBound = c_localBound
        name = self.visit(ast.name, (c[localBound:],Method()))
        mtype = MType(None, None)
        c.append(Symbol(name, mtype, isClassMember=True))
        localBound = len(c)
        for param in ast.param:
            self.visit(param, (c, localBound, 'PARAM'))
        self.visit(ast.body, (c, localBound))
        thisMethod = list(filter(lambda x: x.name == ast.name.name, c))[0]
        thisMethod.scope = (localBound, len(c))
        return

    def visitVarDecl(self,ast: VarDecl, c_localBound_flag):
        c, localBound, flag = c_localBound_flag
        name = self.visit(ast.variable, (c[localBound:], Parameter() if flag=='PARAM' else Variable()))
        mtype = ast.varType
        value = ast.varInit
        if type(mtype) is ClassType:
            self.visit(ast.varType.classname, (c, 'CHECK_UNDECLARED_CLASS', Class(), mtype.classname.name))
        c.append(Symbol(name, mtype, value, Instance()))
        return

    def visitConstDecl(self,ast: ConstDecl, c_localBound_flag):
        c, localBound, flag = c_localBound_flag
        name = self.visit(ast.constant, (c[localBound:], Constant()))
        mtype = ast.constType
        value = ast.value
        c.append(Symbol(name, mtype, value, Instance()))
        return

    def visitBlock(self, ast: Block, c_localBound):
        c, localBound = c_localBound
        for inst in ast.inst:
            if type(inst) in [VarDecl, ConstDecl]:
                self.visit(inst, (c, localBound, 'INST'))
            elif type(inst) in [Block]:
                self.visit(inst, (c, len(c)))
            elif type(inst) in [Assign]:
                self.visit(inst, (c, localBound))
            elif type(inst) in [CallStmt]:
                self.visit(inst, (c, localBound))
        return

    def visitAssign(self, ast: Assign, c_localBound):
        c, localBound = c_localBound
        if type(ast.lhs) == Id:
            self.visit(ast.lhs, (c, 'CHECK_UNDECLARED_IDENTIFIER', Identifier()))
        elif type(ast.lhs) == FieldAccess:
            if type(ast.lhs.obj) == Id:
                self.visit(ast.lhs.fieldname, (c, 'CHECK_UNDECLARED_ATTRIBUTE', Attribute(), ast.lhs.obj.name))

    def visitCallStmt(self, ast: CallStmt, c_localBound):
        c, localBound = c_localBound
        if type(ast.obj) == Id:
            self.visit(ast.method, (c, 'CHECK_UNDECLARED_METHOD', Method(), ast.obj.name))

    

