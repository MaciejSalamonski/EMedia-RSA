import sys
import os
sys.path.append(os.path.abspath("Functions"))
from KeysGenerator import *

if __name__ == '__main__':

    CreateKeyFiles(1024)