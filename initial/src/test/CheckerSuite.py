import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_400(self):
        """Simple program: int main() {} """
        input = """Class a{
                    Var a:int;
                    Var a:int;
                    }
                    Class b{}
                    Class c{}
                    Class d{}"""
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input,expect,400))
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
#     def test_403(self):
#         """Simple program: int main() {} """
#         input = """Class A{
#     a(){}
#     a(){}
# }"""
#         expect = "Redeclared Method: a"
#         self.assertTrue(TestChecker.test(input,expect,403))
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

    