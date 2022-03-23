import Crolling
import PNGtoExcel
import merge
import os
import sys

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

Crolling.main()
PNGtoExcel.main()
merge.main()