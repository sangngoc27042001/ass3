import os
import shutil
os.system('python run.py gen')
try:
    os.mkdir("../submission")
except:
    print("The folder submission already created")

CheckSuite = 'test/CheckerSuite.py'
StaticCheck='main/d96/checker/StaticCheck.py'

shutil.copy(CheckSuite,'../submission/CheckerSuite.py')
shutil.copy(StaticCheck,'../submission/StaticCheck.py')
