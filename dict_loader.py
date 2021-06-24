import sympy
from sympy import *
import string
import json
import pickle
import time
import numpy

print("---------- libraries loaded, starting process ---------------")
START_TIME_UNPICKLE = time.time()
with open("dictionary.p", "rb") as PICKLE_ORIGIN:
    THE_DICT = pickle.load(PICKLE_ORIGIN)
print("------- %s seconds for pickle-loading -------------" % (time.time() - START_TIME_UNPICKLE))

# query one dictionary entry
START_TIME_EXTRACT = time.time()
THE_DICT['a']
print("---------- %s seconds for entry query runtime ---------" % (time.time() - START_TIME_EXTRACT))
# print total runtime
print("---------- %s seconds total runtime ---------" % (time.time() - START_TIME_UNPICKLE))
