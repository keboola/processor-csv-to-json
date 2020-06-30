import sys
import os
print(os.getcwd())
sys.path.append(os.getcwd() + "/src")
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.getcwd())
print(sys.path)
