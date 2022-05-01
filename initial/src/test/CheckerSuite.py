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
                                Var a:B;
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
                                Var a:B;
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
                                Var a:B;
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
                                Var a:B;
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
                                Var a:B;
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
                                Var a:B;
                                Val d:Float = a.c(1,2);
                                a.d(1+2,2--2.0,("a"==."bcd")+1);
                            }
                        }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,BinaryOp(==.,StringLit(a),StringLit(bcd)),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 439))

