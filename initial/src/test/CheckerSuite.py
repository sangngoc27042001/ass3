import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_400(self):
        """Simple program: int main() {} """
        input = """
                    Class c{
                        Var a:Int;
                        Var b:Int;
                        Var c:Int;
                    }
                    Class a{
                    Var a:Int;
                    Var a:Int;
                    }
                    Class b{}
                    Class d{}"""
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    def test_401(self):
        """Simple program: int main() {} """
        input = """Class a{}
        Class a{}"""
        expect = "Redeclared Class: a"
        self.assertTrue(TestChecker.test(input,expect,401))
    def test_402(self):
        """Simple program: int main() {} """
        input = """Class a{
                    a(a:Int;a:String){}
                    }"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_403(self):
        """Simple program: int main() {} """
        input = """Class a{
    Var a:Int;
    a(){}
}"""
        expect = "Redeclared Method: a"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_404(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Var a:Int;
                        Var a:Int;
                    }
                    }"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_405(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Val a:Int = 1;
                        Val a:Int = 1;
                    }
                    }"""
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_406(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(a:Int){
                        Val a:Int = 1;
                    }
                    }"""
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_407(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(a:Int){
                        Var a:Int = 1;
                    }
                    }"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_408(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Var a:Int = 1;
                        {
                            Var a:Int = 1;
                            Var b:Int = 1;
                            Var b:Int = 1;
                        }
                    }
                    }"""
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_409(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Var a:Int = 1;
                        {
                            Var a:Int = 1;
                            Var b:Int = 1;
                            Val b:Int = 1;
                        }
                    }
                    }"""
        expect = "Redeclared Constant: b"
        self.assertTrue(TestChecker.test(input,expect,409))
    def test_410(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Var b:Int = 1;
                        Var c:Int = 1;
                        a=1;
                    }
                    }"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_411(self):
        """Simple program: int main() {} """
        input = """
                    Class B{}
                    Class A{
                    b(){
                        Var b:Int = 1;
                        Var c:A;
                        Var a:C;
                    }
                    }"""
        expect = "Undeclared Class: C"
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_412(self):
        """Simple program: int main() {} """
        input = """
                    Class B{
                        Var b:Int = 1;
                    }
                    Class A{
                    b(){
                        Var b:Int = 1;
                        Var c:B;
                        c.b = 1;
                        c.c = 1;
                    }
                    }"""
        expect = "Undeclared Attribute: c"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_413(self):
        """Simple program: int main() {} """
        input = """
                    Class B{
                        Var b:Int = 1;
                        c(){}
                    }
                    Class A{
                    b(){
                        Var b:Int = 1;
                        Var c:B;
                        c.b = 1;
                        c.c = 1;
                    }
                    }"""
        expect = "Undeclared Attribute: c"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_414(self):
        """Simple program: int main() {} """
        input = """
                    Class B{
                        Var b:Int = 1;
                        c(){}
                    }
                    Class A{
                    b(){
                        Var b:Int = 1;
                        Var c:B;
                        c.b = 1;
                        c.c();
                        c.d();
                    }
                    }"""
        expect = "Undeclared Method: d"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_415(self):
        """Simple program: int main() {} """
        input = """
                    Class B{
                        Var b:Int = 1;
                        c(){}
                    }
                    Class A:B{
                    }
                    Class C:D{
                    }"""
        expect = "Undeclared Class: D"
        self.assertTrue(TestChecker.test(input, expect, 415))


    def test_416(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(){}
                        }
                        Class A:B{
                        }
                        Class C{
                            e(){
                                Var a:A;
                                a.b = 2;
                                a.c();
                                a.e = 2;
                            }
                        }"""
        expect = "Undeclared Attribute: e"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_417(self):
        """Simple program: int main() {} """
        input = """ 
                        Class B{
                            Var b:Int = 1;
                            c(){}
                        }
                        Class A:B{
                        }
                        Class C{
                            e(){
                                Var a:A;
                                a.b= 2;
                                a.c();
                                a.e();
                            }
                        }"""
        expect = "Undeclared Method: e"
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_418(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Val a:Int = 2;
                                a=3;
                            }
                        }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(a),IntLit(3))"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_419(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 2;
                                Var b:Array[Int,5];
                                b[1]=1;
                                a[1]=1;
                            }
                        }"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(1)])"
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test_420(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 2;
                                Var b:Array[Int,5];
                                b[1.2]=1;
                            }
                        }"""
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),[FloatLit(1.2)])"
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test_421(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 1+2;
                                Var b:Float = 1+2.2;
                                Var c:Float = 1+True;
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,IntLit(1),BooleanLit(True))"
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_422(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var c:String = "abc" +. "def";
                                Var d:Boolean = ("abc" +. "def") ==. "ghi";
                                Var e:String = ("abc" ==. "def") +. "ghi";
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(+.,BinaryOp(==.,StringLit(abc),StringLit(def)),StringLit(ghi))"
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_423(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var c:Float = 1.22;
                                Var d:Boolean = (("abc" +. "def") ==. "ghi") || False;
                                Var e:Boolean = 0==False;
                                Var f:Boolean = "abc"||1;
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(||,StringLit(abc),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_424(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var c:Float = --------1.22;
                                Var d:Boolean = !((("abc" +. "def") ==. "ghi") || False);
                                Var e:Float = !!!!--1.22;
                            }
                        }"""
        expect = "Type Mismatch In Expression: UnaryOp(!,UnaryOp(-,UnaryOp(-,FloatLit(1.22))))"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_425(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Int = a.c(1,2);
                                Var e:Int = a.c(1,"abc");
                            }
                        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(a),Id(c),[IntLit(1),StringLit(abc)])"
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_426(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Float = a.c(1,2);
                                Var e:String = a.c(1.1,2);
                            }
                        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(a),Id(c),[FloatLit(1.1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_427(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Float = a.c(1,2);
                                Var e:String = a.c(1.1,2);
                            }
                        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(a),Id(c),[FloatLit(1.1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_428(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Float = a.c(1,2);
                                Var e:String = a.c(1,2);
                            }
                        }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(e),StringType,CallExpr(Id(a),Id(c),[IntLit(1),IntLit(2)]))"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_429(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Float = a.c(1,2);
                                a.d();
                                Var e:String = a.d();
                            }
                        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(a),Id(d),[])"
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_430(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Float = a.c(1,2);
                                a.d();
                                Var e:Float = a.b;
                                Var f:Float = a.d;
                            }
                        }"""
        expect = "Undeclared Attribute: d"
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_431(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Var a:B;
                                Var d:Float = a.c(1,2);
                                a.d();
                                Var e:Float = a.b;
                                Var f:String = a.b;
                            }
                        }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(f),StringType,FieldAccess(Id(a),Id(b)))"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_432(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Val a:B = New B();
                                Val d:Float = a.c(1,2);
                                Val e:String = a.c(1,2);
                            }
                        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(e),StringType,CallExpr(Id(a),Id(c),[IntLit(1),IntLit(2)]))"
        self.assertTrue(TestChecker.test(input, expect, 432))
    def test_433(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Val a : Int = 1.2;
                            }
                        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),IntType,FloatLit(1.2))"
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_434(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Val a : Float = -(1.2 +1);
                                Val b : Float = -(1 + 1);
                                Val c : Boolean = !!((1>2)&&(True || ("abc"==."cef")));
                                Val d :String = ("abc" +. "def")+."ghi";
                                Val e :String = True==1;
                            }
                        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(e),StringType,BinaryOp(==,BooleanLit(True),IntLit(1)))"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_435(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(){}
                        }
                        Class C{
                            e(){
                                Val a:B = New B();
                                Val d:Float = a.c(1,2);
                                Val e:String = a.d(1,2);
                            }
                        }"""
        expect = "Type Mismatch In Expression: CallExpr(Id(a),Id(d),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_436(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(x:Int; y:Float; z:String){}
                        }
                        Class C{
                            e(){
                                Val a:B = New B();
                                Val d:Float = a.c(1,2);
                                a.d(1,2,"a");
                                a.d(1,2,3);
                            }
                        }"""
        expect = "Type Mismatch In Statement: Call(Id(a),Id(d),[IntLit(1),IntLit(2),IntLit(3)])"
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_437(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(x:Int; y:Float; z:String){}
                        }
                        Class C{
                            e(){
                                Val a:B = New B();
                                Val d:Float = a.c(1,2);
                                a.d(1+2,2--2.0,"a"+."bcd");
                                a.c(1,2);
                            }
                        }"""
        expect = "Type Mismatch In Statement: Call(Id(a),Id(c),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_438(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(x:Int; y:Float; z:String){}
                        }
                        Class C{
                            e(){
                                Val a:B = New B();
                                Val d:Float = a.c(1,2);
                                a.d(1+2,2--2.0,"a"==."bcd");
                            }
                        }"""
        expect = "Type Mismatch In Statement: Call(Id(a),Id(d),[BinaryOp(+,IntLit(1),IntLit(2)),BinaryOp(-,IntLit(2),UnaryOp(-,FloatLit(2.0))),BinaryOp(==.,StringLit(a),StringLit(bcd))])"
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_439(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(x:Int; y:Float; z:String){}
                        }
                        Class C{
                            e(){
                                Val a:B = New B();
                                Val d:Float = a.c(1,2);
                                a.d(1+2,2--2.0,("a"==."bcd")+1);
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,BinaryOp(==.,StringLit(a),StringLit(bcd)),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 439))

    def test_440(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(x:Int; y:Float; z:String){}
                        }
                        Class A{}
                        Class C{
                            e(){
                                Var a:B = New B();
                                a = New A();
                            }
                        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),NewExpr(Id(A),[]))"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_441(self):
        """Simple program: int main() {} """
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(g:Int; h:Float){
                                Return 1;
                            }
                            d(x:Int; y:Float; z:String){}
                        }
                        Class A:B{}
                        Class C{
                            e(){
                                Var x:B = New B();
                                x = New A();
                                Var y:A = New A();
                                y = New B();
                            }
                        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(y),NewExpr(Id(B),[]))"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_442(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Val a:Int = 1;
                                Val b:Float = 1;
                                Val c:Float = a+b;
                                Val d:Int = a+b;
                            }
                        }"""
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(d),IntType,BinaryOp(+,Id(a),Id(b)))"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_443(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 1;
                                Var b:Float = 1;
                                Var c:Float = a+b;
                                Var d:Int = a+b;
                            }
                        }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(d),IntType,BinaryOp(+,Id(a),Id(b)))"
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_444(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 1;
                                Var b:Int = 1;
                                If (True){
                                    Var a:Int = 2;
                                }
                                Elseif(True){
                                    Var a:Int = 2;
                                }
                                Else{
                                    Var a:Int = 2;
                                }
                                Var b:Int = 2 ;
                            }
                        }"""
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input, expect, 444))

    def test_445(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 1;
                                Var b:Int = 1;
                                Var i:Int = 0;
                                Foreach(i In 1 .. 10 By 1){
                                    Var a:Int = 1;
                                    Break;
                                    If (True){
                                        Var a:Int = 1;
                                        Continue;
                                    }
                                }
                                Var b:Int = 2 ;
                            }
                        }"""
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_446(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var i:Int = 0;
                                Foreach(i In 1 .. 10 By 1){
                                    Var a:Int = 1;
                                    Break;
                                    If (True){
                                        Var a:Int = 1;
                                        Continue;
                                    }
                                }
                                Break;
                            }
                        }"""
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_447(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var i:Int = 0;
                                Foreach(i In 1 .. 10 By 1){
                                    Var a:Int = 1;
                                    Break;
                                    If (True){
                                        Var a:Int = 1;
                                        Continue;
                                    }
                                }
                                Continue;
                            }
                        }"""
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_448(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 0;
                                Val b:Int = 1;
                                Val c:Float = b+1;
                                Val d:Float = a+1;
                            }
                        }"""
        expect = "Illegal Constant Expression: BinaryOp(+,Id(a),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_449(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 0;
                                Val b:Int = 1;
                                Val c:Float = b+1;
                                Val d:Float = a + "abc";
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),StringLit(abc))"
        self.assertTrue(TestChecker.test(input, expect, 449))

    def test_450(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 0;
                                Val b:Int = 1;
                                Val c:Float = b+1;
                                Val d:Float = a + "abc";
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),StringLit(abc))"
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_451(self):
        """Simple program: int main() {} """
        input = """
                        Class C{
                            e(){
                                Var a:Int = 0;
                                Val b:Int = 1;
                                Val c:Float = b+1;
                            }
                        }
                         Class Car {

                            Var a : Int = 10;
                            foo() {
                                Var x : Int = Self.a;
                                Var y : Int = a;
                            }
                        }"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_452(self):
        """Simple program: int main() {} """
        input = """
                         Class Car {
                            foo() {
                                Var a:Array[Int,2];
                                a = Array(1,2);
                                a = Array(1,2.3);
                            }
                        }"""
        expect = "Illegal Array Literal: [IntLit(1),FloatLit(2.3)]"
        self.assertTrue(TestChecker.test(input, expect, 452))

    def test_453(self):
        """Simple program: int main() {} """
        input = """         
                        Class B{
                        func(){
                            count.foo();
                        }
                        }"""
        expect = "Undeclared Identifier: count"
        self.assertTrue(TestChecker.test(input, expect, 453))

    def test_454(self):
        """Simple program: int main() {} """
        input = """
                        Class A{
                            Var $a:Int = 5;
                            Var b:Int = 4;
                        }         
                        Class B{
                        func(){
                            Var b:Int = A::$a;
                            b = count.foo();
                        }
                        }"""
        expect = "Undeclared Identifier: count"
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_455(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            Var $a:Int = 5;
                            Var b:Int = 4;
                        }         
                        Class B{
                        func(){
                            Var b:Int = A::$a;
                            b = A.b;
                        }
                        }"""
        expect = "Illegal Member Access: FieldAccess(Id(A),Id(b))"
        self.assertTrue(TestChecker.test(input, expect, 455))

    def test_456(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            Var $a:Int = 5;
                            Var b:Int = 4;
                        }         
                        Class B{
                        func(){
                            Var b:A = New A();
                            Var c:Int = b.b;
                            Var d:Int = b::$a;
                        }
                        }"""
        expect = "Illegal Member Access: FieldAccess(Id(b),Id($a))"
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_457(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){}
                            b(){}
                        }         
                        Class B{
                        func(){
                            A::$a();
                            Var b:A = New A();
                            b.b();
                            b::$a();
                        }
                        }"""
        expect = "Illegal Member Access: Call(Id(b),Id($a),[])"
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_458(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){}
                            b(){}
                        }         
                        Class B{
                        func(){
                            A::$a();
                            Var b:A = New A();
                            b.b();
                            A.b();
                        }
                        }"""
        expect = "Illegal Member Access: Call(Id(A),Id(b),[])"
        self.assertTrue(TestChecker.test(input, expect, 458))

    def test_459(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        }         
                        Class B{
                        func(){
                            Var b:A = New A();
                            Var c:Int = A::$a();
                            c = b.b();
                            c = A.b();
                        }
                        }"""
        expect = "Illegal Member Access: CallExpr(Id(A),Id(b),[])"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_460(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        }         
                        Class B{
                        func(){
                            Var b:A = New A();
                            Var c:Int = A::$a();
                            c = b.b();
                            c = b::$a();
                        }
                        }"""
        expect = "Illegal Member Access: CallExpr(Id(b),Id($a),[])"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_461(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        } """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_462(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        } 
                        Class Program{
                            c(){
                                Return 1;
                            }
                        }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_463(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        } 
                        Class Program{
                            $main(){
                                Return 1;
                            }
                        }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 463))

    def test_464(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        } 
                        Class Program{
                            $main(a:Int){
                            }
                        }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 464))

    def test_465(self):
        """Simple program: int main() {} """
        input = """         
                        Class A{
                            $a(){
                                Return 1;
                            }
                            b(){
                                Return 1;
                            }
                        } 
                        Class Program{
                            main(){}
                        }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 465))


