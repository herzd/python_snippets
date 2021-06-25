import sympy
from sympy import *
import string
import json
import pickle
import time
import numpy

print("---------- libraries loaded, starting process ---------------")
ABSOLUTE_START_TIME = time.time()

# unpickle sympy matrix dictionary
START_TIME_UNPICKLE_SYMPY = time.time()
with open("../dictionary_sympy.p", "rb") as PICKLE_ORIGIN:
    THE_DICT_SYMPY = pickle.load(PICKLE_ORIGIN)
print("------- %s seconds for pickle-loading (sympy) ----" % (time.time() - START_TIME_UNPICKLE_SYMPY))

# query one dictionary entry
START_TIME_EXTRACT = time.time()
THE_DICT_SYMPY['a']
print("--- %s seconds for entry query runtime (sympy) ---------" % (time.time() - START_TIME_EXTRACT))

# unpickle numpy matrix dictionary
START_TIME_UNPICKLE_NUMPY = time.time()
with open("../dictionary_numpy.p", "rb") as PICKLE_ORIGIN:
    THE_DICT_NUMPY = pickle.load(PICKLE_ORIGIN)
print("------- %s seconds for pickle-loading (numpy) ----" % (time.time() - START_TIME_UNPICKLE_NUMPY))

# query one dictionary entry
START_TIME_EXTRACT = time.time()
THE_DICT_NUMPY['a']
print("--- %s seconds for entry query runtime (numpy) ---------" % (time.time() - START_TIME_EXTRACT))
# print total runtime
print("---------- %s seconds total runtime ---------" % (time.time() - ABSOLUTE_START_TIME))


# output from lifebook-a557
# >>> ---------- libraries loaded, starting process ---------------
# ------- 0.11948919296264648 seconds for pickle-loading (sympy) ----
# --- 1.1920928955078125e-06 seconds for entry query runtime (sympy) ---------
# ------- 0.04269909858703613 seconds for pickle-loading (numpy) ----
# --- 1.430511474609375e-06 seconds for entry query runtime (numpy) ---------
# ---------- 0.1622757911682129 seconds total runtime ---------

# dired about loaded files
# -rw-r--r--  1 daniel users 41623417 25. Jun 03:40 dictionary_numpy.p
# -rw-r--r--  1 daniel users 10423795 25. Jun 03:40 dictionary_sympy.p
