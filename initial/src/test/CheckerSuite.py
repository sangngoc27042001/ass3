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
                                a.b= 2;
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



