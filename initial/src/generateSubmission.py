import os
import shutil
os.system('python run.py gen')
try:
    os.mkdir("../../../submissionass3")
except:
    print("The folder submission already created")

CheckSuite = 'test/CheckerSuite.py'
StaticCheck='main/d96/checker/StaticCheck.py'

shutil.copy(CheckSuite,'../../../submissionass3/CheckerSuite.py')
shutil.copy(StaticCheck,'../../../submissionass3/StaticCheck.py')
