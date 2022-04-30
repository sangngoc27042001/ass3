
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
    def __init__(self,name,mtype,value = None, kind = None, scope = None, isClassMember = None, inherit = None, immutable = False, returnType = None):
        self.name = name
        self.mtype = mtype #Ctype, MType, IntType, FloatType, BoolType, StringType
        self.value = value
        self.kind = kind # Static, Instance
        self.scope = scope
        self.isClassMember = isClassMember # True if is a class member
        self.inherit = inherit # String, name of a class
        self.immutable = immutable # True if Symbol is a constant, otherwise, False

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
    Symbol("getInt",MType([],IntType())),
    Symbol("putIntLn",MType([IntType()],VoidType()))
    ]

    returnTypeStack = []
    
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
        inherit = self.visit(ast.parentname, (c, 'CHECK_UNDECLARED_CLASS', Class(), ast.parentname.name)) if ast.parentname is not None else None
        c.append(Symbol(ast.classname.name, Ctype(), None, inherit=inherit))
        localBound = len(c)
        for mem in ast.memlist:
            self.visit(mem, (c, localBound))
        thisClass = list(filter(lambda x: x.name == ast.classname.name, c))[0]
        thisClass.scope = (localBound, len(c))
        return

    def visitId(self, ast: Id, c):
        if c[1] == 'CHECK_UNDECLARED_ATTRIBUTE':
            object = list(filter(lambda x: x.name == c[3], c[0]))[-1]
            attributeInClass = findingMemArrRecursively(c[0], object.mtype.classname.name)
            if ast.name not in attributeInClass:
                raise Undeclared(c[2], ast.name)
            return ast.name
        if c[1] =='CHECK_CANNOT_ASSIGN_TO_CONSTANT':
            object = list(filter(lambda x: x.name == ast.name, c[0]))[-1]
            if object.immutable:
                raise CannotAssignToConstant(c[2])
            return ast.name

        if c[1] == 'CHECK_UNDECLARED_METHOD':
            object = list(filter(lambda x: x.name == c[3], c[0]))[-1]
            methodInClass = findingMemArrRecursively(c[0], object.mtype.classname.name, False)
            if ast.name not in methodInClass:
                raise Undeclared(c[2], ast.name)
            return ast.name
        if c[1] == 'CHECK_UNDECLARED_CLASS':
            allClasses = [x.name for x in c[0] if type(x.mtype) is Ctype]
            if c[3] not in allClasses:
                raise Undeclared(c[2], ast.name)
            return ast.name
        if c[1] == 'CHECK_UNDECLARED_IDENTIFIER':
            nearestClass = [x for x in c[0] if type(x.mtype) is Ctype][-1]
            localBound = c[0].index(nearestClass) + 1
            a = [x.name for x in c[0][localBound:]]
            if ast.name not in a:
                raise Undeclared(c[2], ast.name)
            return ast.name
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
        mtype = MType([], None)
        c.append(Symbol(name, mtype, isClassMember=True))
        localBound = len(c)
        for param in ast.param:
            self.visit(param, (c, localBound, 'PARAM'))
        self.visit(ast.body, (c, localBound))
        thisMethod = list(filter(lambda x: x.name == ast.name.name, c))[0]
        thisMethod.scope = (localBound, len(c))
        thisMethod.mtype.partype = [param.varType for param in ast.param]
        thisMethod.mtype.rettype = self.returnTypeStack.pop() if len(self.returnTypeStack) != 0 else None
        return

    def visitVarDecl(self,ast: VarDecl, c_localBound_flag):
        c, localBound, flag = c_localBound_flag
        name = self.visit(ast.variable, (c[localBound:], Parameter() if flag=='PARAM' else Variable()))
        mtype = ast.varType
        value = ast.varInit
        if type(mtype) is ClassType:
            self.visit(ast.varType.classname, (c, 'CHECK_UNDECLARED_CLASS', Class(), mtype.classname.name))

        if not((value is None) or ( isinstance(value, NullLiteral))):
            typeRHS = self.visit(ast.varInit, c)
            if not checkCoerceType(type(ast.varType), type(typeRHS)):
                raise TypeMismatchInStatement(ast)
        c.append(Symbol(name, mtype, value, Instance()))
        return

    def visitConstDecl(self,ast: ConstDecl, c_localBound_flag):
        c, localBound, flag = c_localBound_flag
        name = self.visit(ast.constant, (c[localBound:], Constant()))
        mtype = ast.constType
        value = ast.value
        if type(mtype) is ClassType:
            self.visit(ast.constType.classname, (c, 'CHECK_UNDECLARED_CLASS', Class(), mtype.classname.name))

        if not((value is None) or ( isinstance(value, NullLiteral))):
            typeRHS = self.visit(ast.value, c)
            if not checkCoerceType(type(ast.constType), type(typeRHS)):
                raise TypeMismatchInConstant(ast)
        c.append(Symbol(name, mtype, value, Instance(), immutable=True))
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
            elif type(inst) in [Return]:
                self.visit(inst, c)
        return

    def visitAssign(self, ast: Assign, c_localBound):
        c, localBound = c_localBound
        typeLHS = None
        if type(ast.lhs) == Id:
            self.visit(ast.lhs, (c, 'CHECK_UNDECLARED_IDENTIFIER', Identifier()))
            self.visit(ast.lhs, (c, 'CHECK_CANNOT_ASSIGN_TO_CONSTANT', ast))
            typeLHS = list(filter(lambda x: x.name == ast.lhs.name, c))[-1].mtype
        elif type(ast.lhs) == FieldAccess:
            if type(ast.lhs.obj) == Id:
                self.visit(ast.lhs.fieldname, (c, 'CHECK_UNDECLARED_ATTRIBUTE', Attribute(), ast.lhs.obj.name))
            typeLHS = self.visit(ast.lhs,c)
        elif type(ast.lhs) == ArrayCell:
            if type(ast.lhs.arr) == Id:
                objectArr = list(filter(lambda x: x.name == ast.lhs.arr.name, c))[-1]
                if type(objectArr.mtype) != ArrayType:
                    raise TypeMismatchInExpression(ast.lhs)
                typeLHS = list(filter(lambda x: x.name == ast.lhs.arr.name, c))[-1].mtype.eleType

            if type(ast.lhs.idx) != IntLiteral:
                raise TypeMismatchInExpression(ast.lhs)


        typeRHS = self.visit(ast.exp, c)
        if not checkCoerceType(typeLHS, typeRHS):
            raise TypeMismatchInStatement(ast)

    def visitBinaryOp(self, ast:BinaryOp, c):
        typeLeft = self.visit(ast.left, c)
        typeRight = self.visit(ast.right, c)
        op = ast.op
        if op in ['+', '-', '*', '/']:
            if not isinstance(typeLeft, (IntType, FloatType)) or not isinstance(typeRight, (IntType, FloatType)):
                raise TypeMismatchInExpression(ast)
            if isinstance(typeLeft, FloatType) or isinstance(typeRight, FloatType):
                return FloatType()
            return IntType()
        elif op in ['%']:
            if not isinstance(typeLeft, IntType) or not isinstance(typeRight, IntType):
                raise TypeMismatchInExpression(ast)
            return IntType()
        elif op in ['&&', '||']:
            if not isinstance(typeLeft, BoolType) or not isinstance(typeRight, BoolType):
                raise TypeMismatchInExpression(ast)
            return BoolType()
        elif op in ['==.', '+.']:
            if not isinstance(typeLeft, StringType) or not isinstance(typeRight, StringType):
                raise TypeMismatchInExpression(ast)
            if op == '==.':
                return BoolType()
            return StringType()
        elif op in ['==', '!=']:
            if not isinstance(typeLeft, (IntType, BoolType)) or not isinstance(typeRight, (IntType, BoolType)):
                raise TypeMismatchInExpression(ast)
            return BoolType()
        elif op in ['==', '!=']:
            if not isinstance(typeLeft, (IntType, BoolType)) or not isinstance(typeRight, (IntType, BoolType)):
                raise TypeMismatchInExpression(ast)
            return BoolType()
        elif op in ['<', '>', '<=', '>=']:
            if not isinstance(typeLeft, (IntType, FloatType)) or not isinstance(typeRight, (IntType, FloatType)):
                raise TypeMismatchInExpression(ast)
            return BoolType()

    def visitUnaryOp(self, ast: UnaryOp, c):
        exp = self.visit(ast.body, c)
        op = ast.op
        if op in ['-']:
            if not isinstance(exp, (IntType, FloatType)):
                raise TypeMismatchInExpression(ast)
            return IntType() if isinstance(exp, IntType) else FloatType()
        if op in ['!']:
            if not isinstance(exp, BoolType):
                raise TypeMismatchInExpression(ast)
            return BoolType()

    def visitFloatLiteral(self, ast, c):
        return FloatType()

    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()

    def visitIntLiteral(self, ast: IntLiteral, c):
        return IntType()

    def visitNullLiteral(self, ast: NullLiteral, c):
        return NullLiteral()


    def visitCallStmt(self, ast: CallStmt, c_localBound):
        c, localBound = c_localBound
        if type(ast.obj) == Id:
            self.visit(ast.method, (c, 'CHECK_UNDECLARED_METHOD', Method(), ast.obj.name))

    def visitReturn(self, ast: Return, c):
        returnType = self.visit(ast.expr, c)
        self.returnTypeStack.append(returnType)

    def visitCallExpr(self, ast:CallExpr, c):
        if type(ast.obj) == Id:
            object = list(filter(lambda x: x.name == ast.obj.name, c))[-1]
            if type(object.mtype) != ClassType:
                raise TypeMismatchInExpression(ast)
            classObject = list(filter(lambda x: x.name == object.mtype.classname.name and type(x.mtype) == Ctype, c))[0]
            upperBound, lowerBound = classObject.scope
            methodObject = list(filter(lambda x: x.name == ast.method.name and type(x.mtype) == MType, c[upperBound:lowerBound]))[0]
            if methodObject.mtype.rettype is None:
                raise TypeMismatchInExpression(ast)
            typeDeclList = [type(x) for x in methodObject.mtype.partype]
            typeAssignList = [type(self.visit(x, c)) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInExpression(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList,typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInExpression(ast)
            return methodObject.mtype.rettype
    def visitFieldAccess(self, ast:FieldAccess, c):
        if type(ast.obj) == Id:
            object = list(filter(lambda x: x.name == ast.obj.name, c))[-1]
            if type(object.mtype) != ClassType:
                raise TypeMismatchInExpression(ast)
            classObject = list(filter(lambda x: x.name == object.mtype.classname.name and type(x.mtype) == Ctype, c))[0]
            upperBound, lowerBound = classObject.scope
            attributeObjectList = findingMemArrObjectRecursively(c, classObject.name)
            attributeObject = list(filter(lambda x: x.name == ast.fieldname.name, attributeObjectList))
            if len(attributeObject) == 0:
                raise Undeclared(Attribute(), ast.fieldname.name)
            attributeObject = attributeObject[-1]
            return attributeObject.mtype


#HELP Function
def findingMemArrRecursively(c, classname, attribute=True):
    classObject = list(filter(lambda x: x.name == classname and type(x.mtype) == Ctype, c))[0]
    upperBound, lowerBound = classObject.scope
    if attribute:
        arrAttributeTemp = [x.name for x in c[upperBound: lowerBound] if x.isClassMember and type(x.mtype) != MType]
    else:
        arrAttributeTemp = [x.name for x in c[upperBound: lowerBound] if x.isClassMember and type(x.mtype) == MType]
    if classObject.inherit == None:
        return arrAttributeTemp
    else:
        return arrAttributeTemp + findingMemArrRecursively(c, classObject.inherit, attribute)

def findingMemArrObjectRecursively(c, classname, attribute=True):
    classObject = list(filter(lambda x: x.name == classname and type(x.mtype) == Ctype, c))[0]
    upperBound, lowerBound = classObject.scope
    if attribute:
        arrAttributeTemp = [x for x in c[upperBound: lowerBound] if x.isClassMember and type(x.mtype) != MType]
    else:
        arrAttributeTemp = [x for x in c[upperBound: lowerBound] if x.isClassMember and type(x.mtype) == MType]
    if classObject.inherit == None:
        return arrAttributeTemp
    else:
        return arrAttributeTemp + findingMemArrObjectRecursively(c, classObject.inherit, attribute)

def checkCoerceType(typeDecl, typeAssign):
    if typeDecl is FloatType:
        if typeAssign in [FloatType, IntType]:
            return True
    return typeDecl == typeAssign


    

