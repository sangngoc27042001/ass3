import unittest
from TestUtils import TestChecker
class CheckerSuite(unittest.TestCase):
    def test_400(self):
        """ Test Redeclared Attribute """
        input = """
                    Class c{
                        Var a:Int;
                        Var a:Int;
                    }"""
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test_401(self):
        """ Test Redeclared Class """
        input = """Class b{}
        Class b{}"""
        expect = "Redeclared Class: b"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_402(self):
        """ Test Redeclared Parameter """
        input = """Class a{
                    a(c:Int;c:String){}
                    }"""
        expect = "Redeclared Parameter: c"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_403(self):
        """ Test Redeclared Method """
        input = """Class a{
                    d(a:Int; b:String){}
                    d(){}
                    }"""
        expect = "Redeclared Method: d"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_404(self):
        """Test Redeclared Variable """
        input = """Class a{
                    b(){
                        Var e:Int;
                        Var e:Int;
                    }
                    }"""
        expect = "Redeclared Variable: e"
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test_405(self):
        """Test Redeclared Constant """
        input = """Class a{
                    b(){
                        Val f:Int = 1;
                        Val f:Int = 1;
                    }
                    }"""
        expect = "Redeclared Constant: f"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_406(self):
        """Test Redeclared Constant"""
        input = """Class a{
                    b(a:Int){
                        Val a:Int = 1;
                    }
                    }"""
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_407(self):
        """Test Redeclared Variable"""
        input = """Class a{
                    b(a:Int){
                        Var a:Int = 1;
                    }
                    }"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_408(self):
        """STest Redeclared Variable"""
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
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_409(self):
        """Test Redeclared Constant"""
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
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_410(self):
        """Test Undeclared Identifier"""
        input = """Class a{
                    b(){
                        Var b:Int = 1;
                        Var c:Int = a;
                    }
                    }"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_411(self):
        """Test Undeclared Class"""
        input = """
                    Class B{}
                    Class A{
                    b(){
                        Var b:Int = 1;
                        Var f:A;
                        Var g:D;
                    }
                    }"""
        expect = "Undeclared Class: D"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_412(self):
        """Test Undeclared Attribute"""
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
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_413(self):
        """Test Undeclared Attribute"""
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
                        c.d = 2;
                    }
                    }"""
        expect = "Undeclared Attribute: d"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_414(self):
        """Test Undeclared Method"""
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
        """Test Undeclared Class"""
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
        """Test Undeclared Class"""
        input = """
                    Class B{
                        Var b:Int = 1;
                        c(){}
                    }
                    Class A:B{
                    }
                    Class C:A{
                    }
                    Class F:C{
                        Var a:D;
                    }"""
        expect = "Undeclared Class: D"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_417(self):
        """Test Undeclared Attribute with complicated case"""
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(){}
                            Var e:Int = 1;
                        }
                        Class A:B{
                        }
                        Class C{
                            e(){
                                Var a:A;
                                a.b = 2;
                                a.c();
                                a.e = 2;
                                a.f = 2;
                            }
                        }"""
        expect = "Undeclared Attribute: b"
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_418(self):
        """est Undeclared Attribute"""
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
                                a.b = Self.a;
                            }
                        }"""
        expect = "Undeclared Attribute: b"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_419(self):
        """Test Undeclared Attribute"""
        input = """
                        Class B{
                            Var b:Int = 1;
                            c(){}
                        }
                        Class A:B{
                            Var foo:Int = 1;
                        }
                        Class C:A{
                            e(){
                                Var a:A;
                                a.b= 2;
                                a.c();
                                a.b = a.foo;
                                a.b = a.h;
                            }
                        }"""
        expect = "Undeclared Attribute: b"
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test_420(self):
        """Test Undeclared Class"""
        input = """
                    Class B{}
                    Class A{
                        b(){
                            Var b:Int = 1;
                            b = 1.2;
                        }
                    }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),FloatLit(1.2))"
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test_421(self):
        """Test Undeclared Class"""
        input = """
                    Class B{}
                    Class A{
                        b(){
                            Val b:Int;
                            b = 2;
                        }
                    }"""
        expect = "Illegal Constant Expression: None"
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_422(self):
        """Test Undeclared Class"""
        input = """
                    Class B{}
                    Class A{
                        b(){
                            Val b:Int = 2;
                            b = 3;
                        }
                    }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(b),IntLit(3))"
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_423(self):
        """Test Undeclared Class"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        Var b:Float = 12;
                    }
                    Class A{
                        b(){
                            Var class_name:B = New B();
                            Var b:Int = 1;
                            b = class_name.a;
                            b = class_name.b;
                        }
                    }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),FieldAccess(Id(class_name),Id(b)))"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_424(self):
        """Test Undeclared Class"""
        input = """
                    Class B{
                        Var a:Float = 12;
                        $c(){
                            Return 11.2;
                        }
                    }
                    Class A{
                        b(){
                            Var class_name:B = New B();
                            Var b:Int = 1;
                            b = B::$c();
                        }
                    }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),CallExpr(Id(B),Id($c),[]))"
        self.assertTrue(TestChecker.test(input, expect, 424))

    def test_425(self):
        """Test Undeclared Class"""
        input = """
                    Class B{
                        Var a:Float = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        a(){Return 1.2;}
                        b(){
                            Var class_name:B = New B();
                            Var b:Int = 1;
                            b = class_name.b();
                        }
                    }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),CallExpr(Id(class_name),Id(b),[]))"
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_426(self):
        """Test Undeclared Class"""
        input = """
                    Class B{
                        Var a:Float = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        a(){Return 1.2;}
                        b(){
                            Var class_name:B = New B();
                            Val b:Int = 1;
                            b = class_name.b();
                        }
                    }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(b),CallExpr(Id(class_name),Id(b),[]))"
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_427(self):
        """Test Assignment Statement"""
        input = """
                    Class B{
                        Var a:Float = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        a(){Return New B();}
                        b(){
                            Var class_name:B = New B();
                            Var b:Int = 1;
                            b = Self.a().a;
                        }
                    }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),FieldAccess(CallExpr(Self(),Id(a),[]),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_428(self):
        """Test Assignment Statement"""
        input = """
                    Class B{
                        Var a:Float = 12; ##Error here##
                        b(){Return 1.2;}
                    }
                    Class A{
                        a(){Return New B();}
                        b(){
                            Var class_name:B = New B();
                            Var b:Int = 1;
                            b = Self.a().a;
                        }
                    }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),FieldAccess(CallExpr(Self(),Id(a),[]),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_429(self):
        """Test Undeclared Class"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        Var a: B = New B();
                        a(){Return Self.a;}
                        b(){
                            Var class_name:B = New B();
                            Val b:Int = Self.a().a;
                        }
                    }"""
        expect = "Illegal Constant Expression: FieldAccess(CallExpr(Self(),Id(a),[]),Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_430(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        Var b: B = New B();
                        Var a: A = New A();
                        Var c: B = New A();
                    }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(c),ClassType(Id(B)),NewExpr(Id(A),[]))"
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_431(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        Var b: B = New B();
                        Var c: B = New B(1,2); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Expression: NewExpr(Id(B),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_432(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                        Constructor(a:Int; b:Int){}
                    }
                    Class A{
                        Var b: B = New B();
                        Var c: B = New B(1,2); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Expression: NewExpr(Id(B),[])"
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test_433(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                        Constructor(a:Int; b:Int){}
                    }
                    Class A{
                        Var c: B = New B(1,"Hello"); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Expression: NewExpr(Id(B),[IntLit(1),StringLit(Hello)])"
        self.assertTrue(TestChecker.test(input, expect, 433))

    def test_434(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                        Constructor(a:Int; b:Int){}
                        Constructor(){}
                    }
                    Class A{
                        Var c: B = New B(1,"Hello"); ## Error Here ##
                    }"""
        expect = "Redeclared Method: Constructor"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_435(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                        Constructor(a:Int; b:Int){
                            Return 1;
                        }
                    }
                    Class A{
                        Var c: B = New B(1,"Hello"); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 435))

    def test_436(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                        Constructor(a:Int; b:Int){Return 1;}
                    }
                    Class A{
                        Var c: B = New B(1,"Hello"); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_437(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                        Constructor(a:Int; b:Int){Return;}
                    }
                    Class A{
                        Var c: B = New B(1,"Hello"); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Expression: NewExpr(Id(B),[IntLit(1),StringLit(Hello)])"
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_438(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        Var c: B = New B(1,"Hello",3); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Expression: NewExpr(Id(B),[IntLit(1),StringLit(Hello),IntLit(3)])"
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test_439(self):
        """Test Constructor"""
        input = """
                    Class B{
                        Val a:Int = 12;
                        b(){Return 1.2;}
                    }
                    Class A{
                        Var c: B = New B(1,"Hello",3); ## Error Here ##
                    }"""
        expect = "Type Mismatch In Expression: NewExpr(Id(B),[IntLit(1),StringLit(Hello),IntLit(3)])"
        self.assertTrue(TestChecker.test(input, expect, 439))

    def test_440(self):
        input = """
                Class A {

                    foo() {
                        Var a: Array[Int, 3] = Array(1,2,3);
                        a[4] = 5; ## Index out of bound ##
                        a[1][2] = 4; ## Error with dimension##
                    }
                }
            """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_441(self):
        # NOTE: This case check for param compatiblity of Constructor
        input = """
                        Class Student
                        {
                            Var name: String;
                            Var ID: Int;
                            Constructor(newName: String; newID : Int)
                            {
                                Self.name = newName;
                                Self.ID = newID;
                            }
                        }
                        Class Program
                        {
                            main()
                            {
                                Var myStudent: Student = New Student ();
                            }
                        }
            """
        expect = "Type Mismatch In Expression: NewExpr(Id(Student),[])"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_442(self):
        input = """
                        Class A
                        {
                        }
                        Class B:A
                        {
                            Var a: A = New C();
                        }
            """
        expect = "Undeclared Class: C"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_443(self):
        # NOTE: This case check for param compatiblity of Constructor
        input = """
                        Class A
                        {
                        }
                        Class B:A
                        {
                            Var a: A = New B();
                        }
            """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),ClassType(Id(A)),NewExpr(Id(B),[]))"
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_444(self):
        input = """
                        Class Program{
                            Val $someStatic : Int = 10;
                            foo() {
                                Var Program : Float = 1.0;
                                Var x : Int = Program::$someStatic;
                           }
                        }
            """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 444))

    def test_445(self):
        input = """
                Class A {
                      Var foo: Int = 1;
                      foo() {
                      }
                }
            """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_446(self):
        input = """
                Class A {
                    Val $a: Int = 1;
                }
                Class B{
                    Var $a:Int = 1;
                    Val $b:Int = A::$a;
                    foo(){
                        Val c:Int = B::$b+1;
                        Return 1;
                    }
                }
            """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_447(self):
        """Simple program: int main() {} """
        input = """
                            Class A {
                               $fooExp1(x:Float; y:String){
                                    Var a:Array[Int, 2] = Array(1,1);
                                    a = Array("a", "b");
                               }
                            }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),[StringLit(a),StringLit(b)])"
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_448(self):
        """Simple program: int main() {} """
        input = """
                        Class A {
                           $fooExp1(x:Float; y:String){
                                Var a: Array[Array[Int, 2],2] = Array(Array(1,1),Array(1,1));
                                Var b: Array[Array[Int, 2],2] = Array(Array(1,1),Array(1));
                           }
                        }"""
        expect = "Illegal Array Literal: [[IntLit(1),IntLit(1)],[IntLit(1)]]"
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_449(self):
        """Simple program: int main() {} """
        input = """
                        Class A {
                           $fooExp1(x:Float; y:String){
                                Var a: Array[Array[Int, 2],2] = Array(Array(1,1),Array(1,1));
                                Var b: Array[Array[Int, 2],2] = Array(Array("a","a"),Array("a","abc"));
                           }
                        }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(b),ArrayType(2,ArrayType(2,IntType)),[[StringLit(a),StringLit(a)],[StringLit(a),StringLit(abc)]])"
        self.assertTrue(TestChecker.test(input, expect, 449))

    def test_449(self):
        """Simple program: int main() {} """
        input = """
                        Class A {
                           $fooExp1(x:Float; y:String){
                                Var a: Array[Array[Int, 2],2] = Array(Array(1,1),Array(1,1,"a"));
                           }
                        }"""
        expect = "Illegal Array Literal: [[IntLit(1),IntLit(1)],[IntLit(1),IntLit(1),StringLit(a)]]"
        self.assertTrue(TestChecker.test(input, expect, 449))

    def test_450(self):
        """Simple program: int main() {} """
        input = """
                        Class A {
                           $fooExp1(){
                                Var a: Array[Array[Int, 2],2] = Array(Array(1,1),Array(1,1));
                                a[1] = Array(1,1);
                                a[1][1] = 1;
                                a = 1;
                           }
                        }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_451(self):
        """Simple program: int main() {} """
        input = """
                        Class A {
                           $fooExp1(){
                                Val a: Array[Array[Int, 2],2] = Array(Array(1,1),Array(1,1));
                                a[1] = Array(1,1);
                           }
                        }"""
        expect = "Cannot Assign To Constant: AssignStmt(ArrayCell(Id(a),[IntLit(1)]),[IntLit(1),IntLit(1)])"
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_452(self):
        """Simple program: int main() {} """
        input = """
                        Class A {
                        Val a:Int = 2;
                           $fooExp1(){
                                Self.a = "abc";
                           }
                        }"""
        expect = "Illegal Member Access: FieldAccess(Self(),Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 452))

    def test_453(self):
        input = """
                Class A {

                    Var $myArray: Array[Array[Array[Int,4],2],2] = Array(
                        Array(
                            Array(1,2,3,4),
                            Array(5,6,7,8)
                        ),
                        Array(
                            Array(-1,-2,-3,-4),
                            Array(-5,-6,-7, False)
                        )
                    );

                }
            """
        expect = "Illegal Array Literal: [[[IntLit(1),IntLit(2),IntLit(3),IntLit(4)],[IntLit(5),IntLit(6),IntLit(7),IntLit(8)]],[[UnaryOp(-,IntLit(1)),UnaryOp(-,IntLit(2)),UnaryOp(-,IntLit(3)),UnaryOp(-,IntLit(4))],[UnaryOp(-,IntLit(5)),UnaryOp(-,IntLit(6)),UnaryOp(-,IntLit(7)),BooleanLit(False)]]]"
        self.assertTrue(TestChecker.test(input, expect, 453))

    def test_454(self):
        input = """
                Class Program {
                    main(a:Int){}
                }
            """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_455(self):
        input = """
                Class Program {
                    main(){
                        Return 1;
                    }
                }
            """
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 455))

    def test_456(self):
        input = """Class A{}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_457(self):
        input = """Class Program{}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_458(self):
        input = """Class Program{main(a:Int){}}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 458))

    def test_459(self):
        input = """Class Program{not_main(){}} Class not_Program{main(){}}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_460(self):
        input = """Class Program{$main(){}}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 460))

    def test_461(self):
        input = """Class Program{ Var x: Float = 1.0 + True; }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,FloatLit(1.0),BooleanLit(True))"
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_462(self):
        input = """Class Program{ Var x: Int = 1.0 + 2.0; }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(x),IntType,BinaryOp(+,FloatLit(1.0),FloatLit(2.0)))"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_463(self):
        input = """Class Program{ Var x: String = "hello" + "world"; }"""
        expect = "Type Mismatch In Expression: BinaryOp(+,StringLit(hello),StringLit(world))"
        self.assertTrue(TestChecker.test(input, expect, 463))

    def test_464(self):
        input = """Class Program{ main(a:Int){} Var x: String = "hello" +. "world"; }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 464))

    def test_465(self):
        input = """Class Program{ main(a:Int){} Var x: Float = (-1 + 2.0) * 3 / 4; }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_466(self):
        input = """Class Program{ main(a:Int){} Var x: Int = 3 / 4; }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test_467(self):
        input = """Class Program{ main(a:Int){} Var x: Boolean = ((3 / 4) < 5) || !True || False; }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 467))

    def test_468(self):
        input = """Class Program{ main(a:Int){} Var x: Boolean = ("hello" +. "world") ==. "helloworld"; }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test_469(self):
        input = """Class Program{ main(){} Var x: Boolean = (1.0 == 2.0) && False; }"""
        expect = "Type Mismatch In Expression: BinaryOp(==,FloatLit(1.0),FloatLit(2.0))"
        self.assertTrue(TestChecker.test(input, expect, 469))

    def test_470(self):
        input = """Class Program{ main(a:Int){} Var x: Boolean = (True == False) || (1 != 2) && False; }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test_471(self):
        input = """Class Program{ main(){} Var x: String = 1 == 2; }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(x),StringType,BinaryOp(==,IntLit(1),IntLit(2)))"
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_472(self):
        input = """
        Class A{
            Var myVar: String = "Hello World";
            dummy(a: Int){
                Return a + 4;
            }
            dummy2(){
                Return;
            }
            d(a: Int){
                Self.dummy2();
                Var s: Int = Self.dummy(2 + 2);
                Var d: Int = Self.dummy(s);
            }
            s(){
                Self.d(2);
            }
        }
        Class Program{
            main() {
                Return 1;
            }
        }
        """
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 472))

    def test_473(self):
        input = """
        Class A{
            Var a, d: Int;
            sickle(s: String; e: Int){
                Foreach(i In Self.a .. 10 By Self.d){
                   Break;
                   Continue;
                }
            }
        }
        Class Program{
            main(){
                Return;
            }
        }
        """
        expect = "Undeclared Identifier: i"
        self.assertTrue(TestChecker.test(input, expect, 473))

    def test_474(self):
        input = """
        Class A {
            Var a: Array[Int, 1] = Array(1, 2, 3, 4);
            Var b: Array[Int, 1] = Array(True);

            Var d,e: Int;
            Val f: Array[Array[Int,1], 2] = Array( Array(d), Array(e) );
        }
        Class Program{
            main(){
                Return;
            }
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),ArrayType(1,IntType),[IntLit(1),IntLit(2),IntLit(3),IntLit(4)])"
        self.assertTrue(TestChecker.test(input, expect, 474))

    def test_475(self):
        input = """
        Class A {
            Var b: Array[Int, 1] = Array(True);

            Var d,e: Int;
            Val f: Array[Array[Int,1], 2] = Array( Array(d), Array(e));
        }
        Class Program{
            main(){
                Return;
            }
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(b),ArrayType(1,IntType),[BooleanLit(True)])"
        self.assertTrue(TestChecker.test(input, expect, 475))

    def test_476(self):
        input = """
        Class A {
            Var b: Array[Int, 1] = Array(True);

            Var d,e: Int;
            Val f: Array[Array[Int,1], 2] = Array( Array(d), Array(e));
        }
        Class Program{
            main(){
                Return;
            }
        }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(b),ArrayType(1,IntType),[BooleanLit(True)])"
        self.assertTrue(TestChecker.test(input, expect, 476))

    def test_477(self):
        input = """
        Class A {
            Val a: Array[Int, 4] = Array(1,2,3,4);
            foo() {
                Val a : Array[Int, 3] = Array(Self.a, 1, 2);
                Val b : Int = a[0];
            }
        }
        Class Program{
            main(){
                Return;
            }
        }
        """
        expect = "Illegal Array Literal: [FieldAccess(Self(),Id(a)),IntLit(1),IntLit(2)]"
        self.assertTrue(TestChecker.test(input, expect, 477))

    def test_478(self):
        input = """
        Class Program{
            Val $someStatic : Int = 10;
            main() {
                Var Program : Float = 1.0;
                Var x : Int = Program::$someStatic;
                Var d: Int = 1 && 3.0;
            }
        }
        """
        expect = "Type Mismatch In Expression: BinaryOp(&&,IntLit(1),FloatLit(3.0))"
        self.assertTrue(TestChecker.test(input, expect, 478))

    def test_479(self):
        input = """
        Class A{
            Val $a: Int = 2;
            Val a: Int = 3;
        }
        Class B : A {
            Sicla(){
                Var s: Int = Self.a;
                Return 1;
            }
        }
        Class Program{
            main() {

            }
        }
        """
        expect = "Undeclared Attribute: a"
        self.assertTrue(TestChecker.test(input, expect, 479))

    def test_480(self):
        input = """
        Class A {
            $foo(){
                Val a: Int = 1;
                Foreach(a In 1 .. a){
                    Break;
                }
                Return;
            }
        }
        Class Program {
            main(){
                Var y : A = New A();
                Var z : Int = 10;
                y::$foo();
                z::$foo();
            }
        }
        """
        expect = "Cannot Assign To Constant: AssignStmt(Id(a),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 480))

    def test_481(self):
        input = '''
        Class A{
            Val $B: Int = 10;
        }
        Class B{
            Val C: Int = A::$B;
            cast(a: Int){
                Return "Stuff";
            }
            i2s(a: Int){
                If(a == 1){
                    Return "One";
                }
                Elseif(a == 0){
                    Return "Zero";
                }
                Elseif(a == 0x2){
                    Return "Two";
                }
                Elseif(a == (0x4 - 0b1)){
                    Return "Three";
                }
                Else{
                    Return Self.cast(a - 1);
                }
                Return "2";
            }
        }
        Class C{
            Var B: String = "String";
            Val C: Array[Int, 2] = Array(1, 2, A::$B);
        }
        Class Program {
            Var C: C = New C();
            main(){
                Return;
            }
        }
        '''
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(C),ArrayType(2,IntType),[IntLit(1),IntLit(2),FieldAccess(Id(A),Id($B))])"
        self.assertTrue(TestChecker.test(input, expect, 481))


    def test_483(self):
        input = '''
        Class A{
            Val $B: Int = 10;
        }

        Class B{
            Val C: Int = A::$B;
            a(a : Int){
                If (a % 2 == 0){
                    Return Array("a");
                }
                Else{
                    Return Array("b");    
                }
            }
            func1(){
                Var s, ss: Int;
                Var result : String = "I";
                Foreach(s In 1 .. 100){
                    Foreach(ss In 1 .. 100){
                        result = result +. (Self.a(ss))[0];
                        Break;
                    }
                }
                Return result;
                Break;
            }
        }
        Class Program {
            Var C: A = New A();
            main(){
                Val b: Int = Self.C.B;
            }
        }
        '''
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 483))

    def test_484(self):
        input = '''
        Class A{
            Var a1, a2, a3: String;
            Var $s: Int = 0; 
            Constructor(a, b, c : String){
                A::$s = A::$s + 1;
                Self.a1 = a;
                Self.a2 = b;
                Self.a3 = c;
            }
        }
        Class Program{
            Var x : A = Null;
            main(){
                Return 1;
            }
        }
        '''
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 484))

    def test_485(self):
        input = '''
        Class A{
            Var arr1: Array[Array[String, 2], 2] = Array(Array("Kangzi", "Ploew"), Array("Quanzan", "Fuming"));
            Var arr2: Array[String, 4] = Array(Self.arr1[0][0], Self.arr1[1][0], Self.arr1[0][1], Self.arr1[1][1]);
            Constructor(){
                Return 1;
            }
            Destructor(){
                Return;
            }
        }
        Class Program{
            main(){
                Return;
            }
        }
        '''
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test_486(self):
        input = """
        Class A{
            Var a, d: Int;
            sickle(s: String){
                Break;
                Return 1;
            }
        }
        Class Program{
            main(){

            }
        }
            """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_487(self):
        input = """
        Class A{
            Val a, d: Int = 1, 2;
        }
        Class Program{
            main(a:Int){
                
            }
        }
            """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_488(self):
        input = """
        Class A{
            Val a, d: Int = 1, 7.5;
        }
        Class Program{
            main(){

            }
        }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(d),IntType,FloatLit(7.5))"
        self.assertTrue(TestChecker.test(input, expect, 488))

    def test_489(self):
        input = """
        Class A{
            Var a, d: Int;
            sickle(s: String; e: Int){
                Var i: Int;
                Foreach(i In 1 .. 10 By 2){
                   Break; 
                }
                Return;
            }
        }
        Class Program{
            main(a:Int){
            }
        }
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test_490(self):
        input = """
            Class Program {
                Var a: Int = 20;
                main() {
                    a = 10;
                }
            }
        """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test_491(self):
        input = """
            Class Triangle {
                main(){
                    Var Triangle : String;
                }
            }
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test_492(self):
        input = """
            Class A {
                Var a: Int;
                Val b: Int = 1+Self.a;
            }
        """
        expect = "Illegal Constant Expression: BinaryOp(+,IntLit(1),FieldAccess(Self(),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_493(self):
        input = """
            Class A {
                Var a: Int;
                Val b: Int = 1;
                c()
                {
                    Val c: Int = Self.a - 1;
                }
            }
        """
        expect = "Illegal Constant Expression: BinaryOp(-,FieldAccess(Self(),Id(a)),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_494(self):
        input = """
            Class A {
                Var a: Int;
                Val b: Int = 1;
                c()
                {
                    Val c: Int = Self.b - 1;
                }
            }
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_495(self):
        input = """
            Class A {
                Var a: Int;
                Val b: Int = 1;
                c()
                {
                    Val c: Int = Self.b - 1;
                    Val d: Int = Self.a - 1;
                }
            }
        """
        expect = "Illegal Constant Expression: BinaryOp(-,FieldAccess(Self(),Id(a)),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test_497(self):
        input = """
            Class A {
                Var a: Int;
                Val arr: Array[Int,2] = Array(1,Self.a);
            }
        """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_498(self):
        input = """
            Class A {
                Var a: Int = 2.2;
            }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),IntType,FloatLit(2.2))"
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test_499(self):
        input = """
            Class A {
                foo() {
                    Var a: Int = 2.2;
                }
            }
        """
        expect = "Type Mismatch In Statement: VarDecl(Id(a),IntType,FloatLit(2.2))"
        self.assertTrue(TestChecker.test(input, expect, 499))

    def test_500(self):
        input = """
            Class A {
                foo() {
                    Var a: Int = 2;
                }
            }
            Class B {
                func() {
                    count.foo();
                }
            }
        """
        expect = "Undeclared Identifier: count"
        self.assertTrue(TestChecker.test(input, expect, 500))