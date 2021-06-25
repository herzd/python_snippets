import sympy
from sympy import *
import string
import json
import pickle
import time
import numpy

print("---------- libraries loaded, starting process ---------------")

ABSOLUTE_START_TIME = time.time()

# fill 52-key-dictionary with list of 10 100x100 sympy-matrices as value for each key
# initiate dictionary with 52 keys
START_TIME_SYMPY = time.time()
THE_DICT_SYMPY = {}
THE_DICT_SYMPY = dict.fromkeys(list(string.ascii_letters))
print("---------- %s seconds for dict-initiation ---------" % (time.time() - START_TIME_SYMPY))
# create dictionary
START_TIME_DICT_CREATION = time.time()
for KEY in THE_DICT.keys():
    VALUE_LIST = []
    for MATRIX in range(10):
        VALUE_LIST.append(ones(100,100))
    THE_DICT_SYMPY[KEY] = VALUE_LIST
print("----- %s seconds for dict-creation (sympy) -----" % (time.time() - START_TIME_DICT_CREATION))

# save dictionary  to pickle-file
START_TIME_PICKLE = time.time()
with open("../dictionary_sympy.p", "wb") as PICKLE_DESTINATION:
    pickle.dump(THE_DICT_SYMPY, PICKLE_DESTINATION)
print("---------- %s seconds for pickling (sympy) ---------" % (time.time() - START_TIME_PICKLE))

# Object of type MutableDenseMatrix is not JSON serializable

# query one dictionary entry
START_TIME_EXTRACT = time.time()
THE_DICT_SYMPY['a']
print("---- %s seconds for entry query runtime (sympy) -------" % (time.time() - START_TIME_EXTRACT))

# fill 52-key-dictionary with list of 10 100x100 numpy-arrays as value for each key
# initiate dictionary with 52 keys
START_TIME_NUMPY = time.time()
THE_DICT_NUMPY = {}
THE_DICT_NUMPY = dict.fromkeys(list(string.ascii_letters))
print("---------- %s seconds for dict-initiation ---------" % (time.time() - START_TIME_NUMPY))

START_TIME_DICT_CREATION = time.time()
for KEY in THE_DICT.keys():
    VALUE_LIST = []
    for MATRIX in range(10):
        VALUE_LIST.append(numpy.ones((100,100)))
    THE_DICT_NUMPY[KEY] = VALUE_LIST
print("-------- %s seconds for dict-creation (numpy) -----" % (time.time() - START_TIME_DICT_CREATION))

# save dictionary  to pickle-file
START_TIME_PICKLE = time.time()
with open("../dictionary_numpy.p", "wb") as PICKLE_DESTINATION:
    pickle.dump(THE_DICT_NUMPY, PICKLE_DESTINATION)
print("---------- %s seconds for pickling (numpy) ---------" % (time.time() - START_TIME_PICKLE))

# Object of type ndarray is not JSON serializable

# query one dictionary entry
START_TIME_EXTRACT = time.time()
THE_DICT_NUMPY['a']
print("------ %s seconds for entry query runtime (numpy) ----" % (time.time() - START_TIME_EXTRACT))

# print total runtime
print("---------- %s seconds total runtime ---------" % (time.time() - ABSOLUTE_START_TIME))

# output from lifebook a-557
# >>> ---------- libraries loaded, starting process ---------------
# ---------- 0.012186288833618164 seconds for dict-initiation ---------
# ----- 15.842413663864136 seconds for dict-creation (sympy) -----
# ---------- 0.08799481391906738 seconds for pickling (sympy) ---------
# ---- 8.106231689453125e-06 seconds for entry query runtime (sympy) -------
# ---------- 0.0005838871002197266 seconds for dict-initiation ---------
# -------- 0.011739015579223633 seconds for dict-creation (numpy) -----
# ---------- 0.0661773681640625 seconds for pickling (numpy) ---------
# ------ 1.430511474609375e-06 seconds for entry query runtime (numpy) ----
# ---------- 16.021559715270996 seconds total runtime ---------

# dired about created files
# -rw-r--r--  1 daniel users 41623417 25. Jun 03:32 dictionary_numpy.p
# -rw-r--r--  1 daniel users 10423795 25. Jun 03:32 dictionary_sympy.p

