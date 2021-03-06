"""
 * @author nhphung
"""
from AST import *
from Visitor import *
from StaticError import *


class Ctype:
    pass


class BlockFlag:
    pass


class IfFlag:
    pass


class ForFlag:
    pass


class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype


class Symbol:
    def __init__(self, name, mtype, value=None, kind=None, scope=None, isClassMember=None, inherit=None,
                 immutable=False, belongToClass=None):
        self.name = name
        self.mtype = mtype  # Ctype(), MType(), IntType(), FloatType(), BoolType(), StringType()
        self.value = value
        self.kind = kind  # Static(), Instance()
        self.scope = scope  # tuple if mtype == Ctype()
        self.isClassMember = isClassMember  # True if is a class member (method or attribute)
        self.belongToClass = belongToClass
        self.inherit = inherit  # String, name of a class
        self.immutable = immutable  # True if Symbol is a constant, otherwise, False

    def __str__(self):
        return f'{self.name} || {type(self.mtype)}'


bigProgram = []


def getIndexClassSymbol(classname):
    global bigProgram
    a = list(filter(lambda x: x.name == classname and type(x.mtype) == Ctype, bigProgram))
    if len(a) == 0:
        return False
    return bigProgram.index(a[0])


def getIndexAttributeMethodSymbol(classname, attname, Att=True):
    global bigProgram
    classObjectDecl = list(filter(lambda x: x.name == classname and type(x.mtype) == Ctype, bigProgram))
    if len(classObjectDecl) == 0:
        return False
    classObjectDecl = classObjectDecl[0]
    upperBound, lowerBound = classObjectDecl.scope
    if lowerBound is None:
        lowerBound = len(bigProgram)
    if Att:
        arrAttributeTemp = [x for x in bigProgram[upperBound: lowerBound] if x.isClassMember and type(x.mtype) != MType]
    else:
        arrAttributeTemp = [x for x in bigProgram[upperBound: lowerBound] if x.isClassMember and type(x.mtype) == MType]
    arrAttributeTemp = list(filter(lambda x: x.name == attname, arrAttributeTemp))
    if len(arrAttributeTemp) == 0:
        return False
    return bigProgram.index(arrAttributeTemp[0])


def getIndexVarConstSymbol(name):
    global bigProgram
    bigProgramTemp = bigProgram.copy()
    while True:
        symBolTemp = bigProgramTemp.pop()
        if symBolTemp.name == name:
            return bigProgram.index(symBolTemp)
        if isinstance(symBolTemp.mtype, BlockFlag):
            return False


class StaticChecker(BaseVisitor):
    global_envi = [
        Symbol("getInt", MType([], IntType())),
        Symbol("putIntLn", MType([IntType()], VoidType()))
    ]

    returnTypeStack = []

    def __init__(self, ast):
        self.ast = ast

    def check(self):
        global bigProgram
        bigProgram = []
        self.visit(self.ast, bigProgram)
        if not checkNoEntryPoint(bigProgram):
            raise NoEntryPoint()

    def visitProgram(self, ast: Program, c):
        for x in ast.decl:
            self.visit(x, c)
        return

    def visitClassDecl(self, ast: ClassDecl, c):
        self.visit(ast.classname, ([x for x in c if type(x.mtype) is Ctype], Class(), Ctype()))
        inherit = self.visit(ast.parentname, (
        c, 'CHECK_UNDECLARED_CLASS', Class(), ast.parentname.name)) if ast.parentname is not None else None
        c.append(Symbol(ast.classname.name, Ctype(), None, inherit=inherit))
        localBound = len(c)
        thisClass = c[localBound - 1]
        thisClass.scope = (localBound, None)
        for mem in ast.memlist:
            self.visit(mem, (c, localBound))
        thisClass.scope = (localBound, len(c))
        return

    def visitId(self, ast: Id, c):
        global bigProgram
        if type(c) is not tuple:
            bigProgramTemp = bigProgram.copy()
            while True:
                symBolTemp = bigProgramTemp.pop()
                if isinstance(symBolTemp.mtype, (BlockFlag, Ctype, MType)):
                    raise Undeclared(Identifier(), ast.name)
                elif symBolTemp.name == ast.name:
                    break
            while True:
                symBolTemp2 = bigProgramTemp.pop()
                if isinstance(symBolTemp2.mtype, (BlockFlag, MType)):
                    break
                elif isinstance(symBolTemp2.mtype, Ctype):
                    raise Undeclared(Identifier(), ast.name)
            return symBolTemp.mtype

        if c[1] == 'CHECK_ILLEGAL_MEMBER_ACCESS':
            _, _, ast2 = c
            bigProgramTemp = bigProgram.copy()
            while True:
                symBolTemp = bigProgramTemp.pop()
                if symBolTemp.name == ast.name:
                    if ast.name in [x.name for x in bigProgram if type(x.mtype) is Ctype]:
                        return 'VARCLASS'
                    return 'VAR'

                if isinstance(symBolTemp.mtype, (Ctype, BlockFlag)):
                    if ast.name in [x.name for x in bigProgram if type(x.mtype) is Ctype]:
                        return 'CLASS'
                    raise Undeclared(Identifier(), ast.name)

        if c[1] == 'CHECK_UNDECLARED_ATTRIBUTE':
            object = list(filter(lambda x: x.name == c[3], c[0]))[-1]
            attributeInClass = findingMemArrRecursively(c[0], object.mtype.classname.name)
            if ast.name not in attributeInClass:
                raise Undeclared(c[2], ast.name)
            return ast.name

        if c[1] == 'CHECK_CANNOT_ASSIGN_TO_CONSTANT':
            object = list(filter(lambda x: x.name == ast.name, c[0]))[-1]
            if object.immutable:
                raise CannotAssignToConstant(c[2])
            return ast.name

        if c[1] == 'CHECK_UNDECLARED_METHOD':
            object = list(filter(lambda x: x.name == c[3], c[0]))
            if len(object) == 0:
                raise Undeclared(c[2], ast.name)
            object = object[-1]
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
        else:
            c, typeRaise, mtype = c
            if isinstance(mtype, (Ctype, MType)):
                if ast.name in [x.name for x in c if type(x.mtype) is type(mtype)]:
                    raise Redeclared(typeRaise, ast.name)
            else:
                if ast.name in [x.name for x in c]:
                    raise Redeclared(typeRaise, ast.name)

        return ast.name

    def visitAttributeDecl(self, ast: AttributeDecl, c_localBound):
        c, localBound = c_localBound
        mtype = ast.decl.varType if type(ast.decl) is VarDecl else ast.decl.constType
        name = self.visit(ast.decl.variable, (c[localBound:], Attribute(), mtype)) if type(
            ast.decl) is VarDecl else self.visit(ast.decl.constant, (c[localBound:], Attribute(), mtype))
        value = ast.decl.varInit if type(ast.decl) is VarDecl else ast.decl.value
        kind = ast.kind
        immutable = True if type(ast.decl) is ConstDecl else False

        if not ((value is None) or (isinstance(value, NullLiteral))):
            typeRHS = self.visit(value, c)
            if not checkCoerceType(mtype, typeRHS):
                if isinstance(ast.decl, VarDecl):
                    raise TypeMismatchInStatement(ast.decl)
                else:
                    raise TypeMismatchInConstant(ast.decl)

        classObject = list(filter(lambda x: type(x.mtype) == Ctype, c))[-1]
        c.append(
            Symbol(name, mtype, value, kind, isClassMember=True, belongToClass=classObject.name, immutable=immutable))
        if immutable:
            if not checkIllegalConstantExpression(value):
                raise IllegalConstantExpression(value)
        return

    def visitMethodDecl(self, ast: MethodDecl, c_localBound):
        c, localBound = c_localBound
        mtype = MType([], VoidType())
        name = self.visit(ast.name, (c[localBound:], Method(), mtype))
        kind = ast.kind
        thisMethod = Symbol(name, mtype, isClassMember=True, kind=kind)
        c.append(thisMethod)
        localBound = len(c)
        for param in ast.param:
            self.visit(param, (c, localBound, 'PARAM'))
        blockIdx = len(c)
        self.visit(ast.body, (c, (localBound, blockIdx)))

        thisMethod.scope = (localBound, len(c))
        thisMethod.mtype.partype = [param.varType for param in ast.param]
        thisMethod.mtype.rettype = self.returnTypeStack.pop() if len(self.returnTypeStack) != 0 else VoidType()
        classObject = list(filter(lambda x: type(x.mtype) == Ctype, c))[-1]
        thisMethod.belongToClass = classObject.name
        return

    def visitVarDecl(self, ast: VarDecl, c_localBound_flag):
        c, localBound, flag = c_localBound_flag
        mtype = ast.varType
        name = self.visit(ast.variable, (c[localBound:], Parameter() if flag == 'PARAM' else Variable(), mtype))
        value = ast.varInit
        if type(mtype) is ClassType:
            self.visit(ast.varType.classname, (c, 'CHECK_UNDECLARED_CLASS', Class(), mtype.classname.name))

        if not ((value is None) or (isinstance(value, NullLiteral))):
            typeRHS = self.visit(ast.varInit, c)
            if not checkCoerceType(ast.varType, typeRHS):
                raise TypeMismatchInStatement(ast)
        bigProgram.append(Symbol(name, mtype, value, Instance()))
        return

    def visitConstDecl(self, ast: ConstDecl, c_localBound_flag):
        c, localBound, flag = c_localBound_flag
        mtype = ast.constType
        name = self.visit(ast.constant, (c[localBound:], Constant(), mtype))
        value = ast.value
        if type(mtype) is ClassType:
            self.visit(ast.constType.classname, (c, 'CHECK_UNDECLARED_CLASS', Class(), mtype.classname.name))

        if not ((value is None) or (isinstance(value, NullLiteral))):
            typeRHS = self.visit(ast.value, c)
            if typeRHS is None:
                raise IllegalConstantExpression(value)
            if not checkCoerceType(ast.constType, typeRHS):
                raise TypeMismatchInConstant(ast)

        if not checkIllegalConstantExpression(value):
            raise IllegalConstantExpression(value)
        c.append(Symbol(name, mtype, value, Instance(), immutable=True))
        return

    def visitBlock(self, ast: Block, c_localBound):
        c, localBound = c_localBound
        thisBlock = Symbol('BLOCK', BlockFlag())
        bigProgram.append(thisBlock)
        upperBound = len(c)

        if isinstance(localBound, tuple):
            localBound, blockIdx = localBound
            c[localBound], c[blockIdx] = c[blockIdx], c[localBound]
            upperBound -= blockIdx - localBound

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
            elif type(inst) in [Break, Continue]:
                self.visit(inst, c)
            elif type(inst) in [If]:
                self.visit(inst, c)
            elif type(inst) in [For]:
                self.visit(inst, c)
        thisBlock.scope = (upperBound, len(c))
        return

    def visitAssign(self, ast: Assign, c_localBound):
        c, localBound = c_localBound
        typeLHS = None
        typeRHS = self.visit(ast.exp, c)
        if type(ast.lhs) == Id:
            # self.visit(ast.lhs, (c, 'CHECK_UNDECLARED_IDENTIFIER', Identifier()))
            self.visit(ast.lhs, c)
            self.visit(ast.lhs, (c, 'CHECK_CANNOT_ASSIGN_TO_CONSTANT', ast))
            typeLHS = list(filter(lambda x: x.name == ast.lhs.name, c))[-1].mtype
        elif type(ast.lhs) == FieldAccess:
            typeLHS = self.visit(ast.lhs, c)
            if type(ast.lhs.obj) == Id:
                self.visit(ast.lhs.fieldname, (c, 'CHECK_UNDECLARED_ATTRIBUTE', Attribute(), ast.lhs.obj.name))
            if type(ast.lhs.obj) == SelfLiteral:
                nearestClass = [x for x in c if type(x.mtype) is Ctype][-1]
                fieldnameObject = list(
                    filter(lambda x: x.belongToClass == nearestClass.name and x.name == ast.lhs.fieldname.name,
                           bigProgram))
                if len(fieldnameObject) == 0:
                    raise Undeclared(Attribute(), ast.lhs.fieldname.nane)

                if fieldnameObject[0].immutable:
                    raise CannotAssignToConstant(ast)

        elif type(ast.lhs) == ArrayCell:
            typeLHS = self.visit(ast.lhs, c)
            if isinstance(ast.lhs.arr, Id):
                self.visit(ast.lhs.arr, (c, 'CHECK_CANNOT_ASSIGN_TO_CONSTANT', ast))

        if not checkCoerceType(typeLHS, typeRHS):
            raise TypeMismatchInStatement(ast)

    def visitBinaryOp(self, ast: BinaryOp, c):
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

    def visitArrayLiteral(self, ast: ArrayLiteral, c):
        arrType = self.visitArrayLiteral2(ast, c)
        if not arrType:
            raise IllegalArrayLiteral(ast)
        return arrType

    def visitArrayLiteral2(self, ast: ArrayLiteral, c):
        if len(ast.value) == 0:
            return False
        temp = self.visit(ast.value[0], c) if not isinstance(ast.value[0], ArrayLiteral) else self.visitArrayLiteral2(
            ast.value[0], c)
        if not temp:
            return False
        for ele in ast.value:
            typeEle = self.visit(ele, c) if not isinstance(ast.value[0], ArrayLiteral) else self.visitArrayLiteral2(ele,
                                                                                                                    c)
            if isinstance(temp, ArrayType) and isinstance(typeEle, ArrayType):
                if not ((temp.size == typeEle.size) and (type(temp.eleType) is type(typeEle.eleType))):
                    return False
            elif type(temp) is not type(typeEle):
                return False
        return ArrayType(len(ast.value), temp)

    def visitNewExpr(self, ast: NewExpr, c):
        if ast.classname.name not in [x.name for x in bigProgram if type(x.mtype) is Ctype]:
            raise Undeclared(Class(), ast.classname.name)
        constructorSymbolIdx = getIndexAttributeMethodSymbol(ast.classname.name, 'Constructor', False)
        if not constructorSymbolIdx and len(ast.param) == 0:
            return ClassType(Id(ast.classname.name))
        if not (constructorSymbolIdx and len(ast.param) != 0):
            raise TypeMismatchInExpression(ast)

        typeDeclList = [x for x in bigProgram[constructorSymbolIdx].mtype.partype]
        typeAssignList = [self.visit(x, c) for x in ast.param]
        if len(typeDeclList) != len(typeAssignList):
            raise TypeMismatchInExpression(ast)
        for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
            if not checkCoerceType(typeDecl, typeAssign):
                raise TypeMismatchInExpression(ast)

        return ClassType(Id(ast.classname.name))

    def visitCallStmt(self, ast: CallStmt, c_localBound):
        c, localBound = c_localBound
        if type(ast.obj) == Id:
            objClassVar = self.visit(ast.obj, (bigProgram, 'CHECK_ILLEGAL_MEMBER_ACCESS', ast))
            if objClassVar == 'CLASS':
                if ast.method.name[0] != '$':
                    raise IllegalMemberAccess(ast)
                classObject = list(filter(lambda x: x.name == ast.obj.name and type(x.mtype) == Ctype, c))[0]
            else:
                if ast.method.name[0] == '$':
                    raise IllegalMemberAccess(ast)
                self.visit(ast.method, (c, 'CHECK_UNDECLARED_METHOD', Method(), ast.obj.name))
                object = list(filter(lambda x: x.name == ast.obj.name, c))[-1]
                if type(object.mtype) != ClassType:
                    raise TypeMismatchInExpression(ast)
                classObject = \
                list(filter(lambda x: x.name == object.mtype.classname.name and type(x.mtype) == Ctype, c))[0]

            methodObject = findingMemArrObjectRecursively(c, classObject.name, False)
            methodObject = list(filter(lambda x: x.name == ast.method.name, methodObject))
            if len(methodObject) == 0:
                raise Undeclared(Method(), ast.method.name)
            methodObject = methodObject[0]
            if type(methodObject.mtype.rettype) is not VoidType:
                raise TypeMismatchInStatement(ast)
            typeDeclList = [x for x in methodObject.mtype.partype]
            typeAssignList = [self.visit(x, c) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInStatement(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInStatement(ast)
        elif type(ast.obj) == SelfLiteral:
            classObject = list(filter(lambda x: type(x.mtype) is Ctype, c))[-1]
            methodObject = list(
                filter(lambda x: x.name == ast.method.name and x.belongToClass == classObject.name, bigProgram))
            if len(methodObject) == 0:
                raise Undeclared(Method(), ast.method.name)
            methodObject = methodObject[0]
            if type(methodObject.mtype.rettype) is not VoidType:
                raise TypeMismatchInStatement(ast)
            typeDeclList = [x for x in methodObject.mtype.partype]
            typeAssignList = [self.visit(x, c) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInStatement(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInStatement(ast)
        else:
            typeRHS = self.visit(ast.obj, c)
            if type(typeRHS) != ClassType:
                raise TypeMismatchInExpression(ast)
            methodObject = list(
                filter(lambda x: x.name == ast.method.name and x.belongToClass == typeRHS.classname.name, bigProgram))
            if len(methodObject) == 0:
                raise Undeclared(Method(), ast.method.name)
            methodObject = methodObject[0]
            if type(methodObject.mtype.rettype) is not VoidType:
                raise TypeMismatchInStatement(ast)
            typeDeclList = [x for x in methodObject.mtype.partype]
            typeAssignList = [self.visit(x, c) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInStatement(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInStatement(ast)

    def visitReturn(self, ast: Return, c):
        returnType = self.visit(ast.expr, c)
        self.returnTypeStack.append(returnType)

    def visitCallExpr(self, ast: CallExpr, c):
        if type(ast.obj) == Id:
            objClassVar = self.visit(ast.obj, (bigProgram, 'CHECK_ILLEGAL_MEMBER_ACCESS', ast))

            if objClassVar == 'CLASS':
                if ast.method.name[0] != '$':
                    raise IllegalMemberAccess(ast)
                classObject = list(filter(lambda x: x.name == ast.obj.name and type(x.mtype) == Ctype, c))[0]
            else:
                if ast.method.name[0] == '$':
                    raise IllegalMemberAccess(ast)
                self.visit(ast.method, (c, 'CHECK_UNDECLARED_METHOD', Method(), ast.obj.name))
                object = list(filter(lambda x: x.name == ast.obj.name, c))[-1]
                if type(object.mtype) != ClassType:
                    raise TypeMismatchInExpression(ast)
                classObject = \
                list(filter(lambda x: x.name == object.mtype.classname.name and type(x.mtype) == Ctype, c))[0]

            methodObject = findingMemArrObjectRecursively(c, classObject.name, False)
            methodObject = list(filter(lambda x: x.name == ast.method.name, methodObject))
            if len(methodObject) == 0:
                raise Undeclared(Method(), ast.method.name)
            methodObject = methodObject[0]

            if type(methodObject.mtype.rettype) is VoidType:
                raise TypeMismatchInExpression(ast)
            typeDeclList = [x for x in methodObject.mtype.partype]
            typeAssignList = [self.visit(x, c) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInExpression(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInExpression(ast)
            return methodObject.mtype.rettype
        elif type(ast.obj) == SelfLiteral:
            classObject = list(filter(lambda x: type(x.mtype) is Ctype, c))[-1]
            methodObject = list(filter(
                lambda x: x.name == ast.method.name and x.belongToClass == classObject.name and isinstance(x.mtype,
                                                                                                           MType),
                bigProgram))
            if len(methodObject) == 0:
                raise Undeclared(Method(), ast.method.name)
            methodObject = methodObject[0]
            if type(methodObject.mtype.rettype) is VoidType:
                raise TypeMismatchInStatement(ast)
            typeDeclList = [x for x in methodObject.mtype.partype]
            typeAssignList = [self.visit(x, c) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInStatement(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInStatement(ast)
            return methodObject.mtype.rettype
        else:
            typeRHS = self.visit(ast.obj, c)
            if type(typeRHS) != ClassType:
                raise TypeMismatchInExpression(ast)
            methodObject = list(filter(
                lambda x: x.name == ast.method.name and x.belongToClass == typeRHS.classname.name and isinstance(
                    x.mtype, MType), bigProgram))
            if len(methodObject) == 0:
                raise Undeclared(Method(), ast.method.name)
            methodObject = methodObject[0]
            if type(methodObject.mtype.rettype) is VoidType:
                raise TypeMismatchInStatement(ast)
            typeDeclList = [x for x in methodObject.mtype.partype]
            typeAssignList = [self.visit(x, c) for x in ast.param]
            if len(typeDeclList) != len(typeAssignList):
                raise TypeMismatchInStatement(ast)
            for (typeDecl, typeAssign) in zip(typeDeclList, typeAssignList):
                if not checkCoerceType(typeDecl, typeAssign):
                    raise TypeMismatchInStatement(ast)
            return methodObject.mtype.rettype

    def visitFieldAccess(self, ast: FieldAccess, c):
        global bigProgram
        if type(ast.obj) == Id:
            objClassVar = self.visit(ast.obj, (bigProgram, 'CHECK_ILLEGAL_MEMBER_ACCESS', ast))
            if objClassVar == 'VARCLASS':
                if ast.fieldname.name[0] == '$':
                    classObject = list(filter(lambda x: x.name == ast.obj.name and type(x.mtype) is Ctype, bigProgram))[
                        0]
                else:
                    object = list(filter(lambda x: x.name == ast.obj.name, c))[-1]
                    if type(object.mtype) != ClassType:
                        raise TypeMismatchInExpression(ast)
                    classObject = \
                    list(filter(lambda x: x.name == object.mtype.classname.name and type(x.mtype) == Ctype, c))[0]
            elif objClassVar == 'CLASS':
                if ast.fieldname.name[0] != '$':
                    raise IllegalMemberAccess(ast)
                classObject = list(filter(lambda x: x.name == ast.obj.name and type(x.mtype) == Ctype, c))[0]
            else:
                if ast.fieldname.name[0] == '$':
                    raise IllegalMemberAccess(ast)
                object = list(filter(lambda x: x.name == ast.obj.name, c))[-1]
                if type(object.mtype) != ClassType:
                    raise TypeMismatchInExpression(ast)
                classObject = \
                list(filter(lambda x: x.name == object.mtype.classname.name and type(x.mtype) == Ctype, c))[0]
            attributeObjectList = findingMemArrObjectRecursively(c, classObject.name)
            attributeObject = list(filter(lambda x: x.name == ast.fieldname.name, attributeObjectList))
            if len(attributeObject) == 0:
                raise Undeclared(Attribute(), ast.fieldname.name)
            attributeObject = attributeObject[-1]
            return attributeObject.mtype
        elif type(ast.obj) == SelfLiteral:
            classObject = list(filter(lambda x: type(x.mtype) is Ctype, c))[-1]
            upperBound = c.index(classObject) + 1
            attributeList = [x for x in c[upperBound:] if x.isClassMember and type(x.mtype) != MType]
            if ast.fieldname.name not in [x.name for x in attributeList]:
                raise Undeclared(Attribute(), ast.fieldname.name)
            attributeObject = list(filter(lambda x: x.name == ast.fieldname.name, attributeList))[-1]
            return attributeObject.mtype
        else:
            typeRHS = self.visit(ast.obj, c)
            if type(typeRHS) != ClassType:
                raise TypeMismatchInExpression(ast)
            fieldNameObject = list(
                filter(lambda x: x.name == ast.fieldname.name and x.belongToClass == typeRHS.classname.name,
                       bigProgram))
            if len(fieldNameObject) == 0:
                raise Undeclared(Attribute(), ast.fieldname.name)
            return fieldNameObject[0].mtype

    def visitArrayCell(self, ast: ArrayCell, c):
        typeArr = self.visit(ast.arr, c)
        if not isinstance(typeArr, ArrayType):
            raise TypeMismatchInExpression(ast)

        for i in ast.idx:
            if not isinstance(self.visit(i, c), IntType):
                raise TypeMismatchInExpression(ast)
            if 'eleType' not in dir(typeArr):
                raise TypeMismatchInExpression(ast)
            typeArr = typeArr.eleType
        return typeArr

    def visitIf(self, ast: If, c):
        thisIf = Symbol('IF', IfFlag())
        bigProgram.append(thisIf)
        upperBound = len(c)
        self.visit(ast.expr, c)
        self.visit(ast.thenStmt, (c, upperBound))
        self.visit(ast.elseStmt, (c, upperBound)) if ast.elseStmt is not None else None
        thisIf.scope = (upperBound, len(c))

    def visitFor(self, ast: For, c):
        thisFor = Symbol('FOR', ForFlag())
        bigProgram.append(thisFor)
        upperBound = len(c)
        expr1Type = self.visit(ast.expr1, bigProgram)
        expr2Type = self.visit(ast.expr2, bigProgram)
        if not (checkCoerceType(expr1Type, IntType()) and checkCoerceType(expr2Type, IntType())):
            raise TypeMismatchInStatement(ast)
        expr3Type = self.visit(ast.expr3, bigProgram) if ast.expr3 is not None else None
        self.visit(ast.loop, (bigProgram, upperBound))
        thisFor.scope = (upperBound, len(c))

    def visitBreak(self, ast: Break, c):
        bigProgramTemp = bigProgram.copy()
        while True:
            symBolTemp = bigProgramTemp.pop()
            if type(symBolTemp.mtype) is ForFlag:
                if symBolTemp.scope is None:
                    break
            if isinstance(symBolTemp.mtype, (Ctype, MType)):
                raise MustInLoop(ast)

    def visitContinue(self, ast: Continue, c):
        bigProgramTemp = bigProgram.copy()
        while True:
            symBolTemp = bigProgramTemp.pop()
            if type(symBolTemp.mtype) is ForFlag:
                if symBolTemp.scope is None:
                    break
            if isinstance(symBolTemp.mtype, (Ctype, MType)):
                raise MustInLoop(ast)


# HELP Function
def findingMemArrRecursively(c, classname, attribute=True):
    classObject = list(filter(lambda x: x.name == classname and type(x.mtype) == Ctype, c))[0]
    upperBound, lowerBound = classObject.scope
    if lowerBound is None:
        lowerBound = len(bigProgram)
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
    if lowerBound is None:
        lowerBound = len(bigProgram)
    if attribute:
        arrAttributeTemp = [x for x in c[upperBound: lowerBound] if x.isClassMember and type(x.mtype) != MType]
    else:
        arrAttributeTemp = [x for x in c[upperBound: lowerBound] if x.isClassMember and type(x.mtype) == MType]
    if classObject.inherit == None:
        return arrAttributeTemp
    else:
        return arrAttributeTemp + findingMemArrObjectRecursively(c, classObject.inherit, attribute)


def checkCoerceType(typeDecl, typeAssign):
    global bigProgram
    if type(typeDecl) is FloatType:
        if type(typeAssign) in [FloatType, IntType]:
            return True
    elif type(typeDecl) == ClassType and type(typeAssign) == ClassType:
        if typeDecl.classname.name == typeAssign.classname.name:
            return True
        return False
    elif isinstance(typeDecl, ArrayType) and isinstance(typeAssign, ArrayType):
        if (typeDecl.size == typeAssign.size) and checkCoerceType(typeDecl.eleType, typeAssign.eleType):
            return True
        return False
    return type(typeDecl) == type(typeAssign)


def checkIllegalConstantExpression(ast: Expr):
    if ast is None:
        return False
    if isinstance(ast, BinaryOp):
        return checkIllegalConstantExpression(ast.left) and checkIllegalConstantExpression(ast.right)
    elif isinstance(ast, UnaryOp):
        return checkIllegalConstantExpression(ast.body)
    elif isinstance(ast, (IntLiteral, FloatLiteral, StringLiteral, BooleanLiteral, ArrayLiteral, NewExpr, SelfLiteral)):
        return True
    elif isinstance(ast, Id):
        idObject = list(filter(lambda x: x.name == ast.name, bigProgram))[-1]
        if not idObject.immutable:
            return False
        return True
    elif isinstance(ast, FieldAccess):
        memberName = ast.fieldname.name
        memberObject = list(filter(lambda x: x.name == memberName, bigProgram))  # C?? th??? c?? nhi???u
        if len(memberObject) == 0:
            raise Undeclared(Attribute(), memberName)
        return checkIllegalConstantExpression(ast.obj) and memberObject[0].immutable
    elif isinstance(ast, CallExpr):
        return False
    return False


def checkNoEntryPoint(bigProgram):
    Program = list(filter(lambda x: x.name == "Program" and type(x.mtype) == Ctype, bigProgram))
    if len(Program) == 0:
        return False
    Program = Program[0]
    upperBound, lowerBound = Program.scope
    arrMethodTemp = [x for x in bigProgram[upperBound: lowerBound] if x.isClassMember and type(x.mtype) == MType]
    if '$main' not in [x.name for x in arrMethodTemp]:
        return False
    main = list(filter(lambda x: x.name == "$main", arrMethodTemp))[0]
    if (len(main.mtype.partype) != 0) or not isinstance(main.mtype.rettype, VoidType) or isinstance(main.kind,
                                                                                                    Instance):
        return False
    return True




