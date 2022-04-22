import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
#     def test_400(self):
#         """Simple program: int main() {} """
#         input = """Class a{
#                     Var a:Int;
#                     Var a:Int;
#                     }
#                     Class b{}
#                     Class c{}
#                     Class d{}"""
#         expect = "Redeclared Attribute: a"
#         self.assertTrue(TestChecker.test(input,expect,400))
#     def test_401(self):
#         """Simple program: int main() {} """
#         input = """Class a{}
#         Class a{}"""
#         expect = "Redeclared Class: a"
#         self.assertTrue(TestChecker.test(input,expect,401))
#     def test_402(self):
#         """Simple program: int main() {} """
#         input = """Class a{
#                     a(a:int;a:tring){}
#                     }"""
#         expect = "Redeclared Parameter: a"
#         self.assertTrue(TestChecker.test(input,expect,402))
#
#     def test_403(self):
#         """Simple program: int main() {} """
#         input = """Class A{
#     Var b:Int;
#     a(){}
#     a(){}
# }"""
#         expect = "Redeclared Method: a"
#         self.assertTrue(TestChecker.test(input,expect,403))
#
#     def test_404(self):
#         """Simple program: int main() {} """
#         input = """Class a{
#                     b(){
#                         Var a:int;
#                         Var a:int;
#                     }
#                     }"""
#         expect = "Redeclared Variable: a"
#         self.assertTrue(TestChecker.test(input,expect,404))
#
#     def test_405(self):
#         """Simple program: int main() {} """
#         input = """Class a{
#                     b(){
#                         Val a:int = 1;
#                         Val a:int = 1;
#                     }
#                     }"""
#         expect = "Redeclared Constant: a"
#         self.assertTrue(TestChecker.test(input,expect,405))
#
#     def test_406(self):
#         """Simple program: int main() {} """
#         input = """Class a{
#                     b(a:int){
#                         Val a:int = 1;
#                     }
#                     }"""
#         expect = "Redeclared Constant: a"
#         self.assertTrue(TestChecker.test(input,expect,406))
#
#     def test_407(self):
#         """Simple program: int main() {} """
#         input = """Class a{
#                     b(a:int){
#                         Var a:int = 1;
#                     }
#                     }"""
#         expect = "Redeclared Variable: a"
#         self.assertTrue(TestChecker.test(input,expect,407))

    def test_408(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Var a:int = 1;
                        {
                            Var a:int = 1;
                            Var b:int = 1;
                            Var b:int = 1;
                        }
                    }
                    }"""
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_409(self):
        """Simple program: int main() {} """
        input = """Class a{
                    b(){
                        Var a:int = 1;
                        {
                            Var a:int = 1;
                            Var b:int = 1;
                            Val b:int = 1;
                        }
                    }
                    }"""
        expect = "Redeclared Constant: b"
        self.assertTrue(TestChecker.test(input,expect,409))

