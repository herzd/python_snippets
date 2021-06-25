import sympy
from sympy import *
import string
import json
import pickle
import time
import numpy

print("---------- libraries loaded, starting process ---------------")

# initiate dictionary with 52 keys
ABSOLUTE_START_TIME = time.time()
THE_DICT = {}
THE_DICT = dict.fromkeys(list(string.ascii_letters))
print("---------- %s seconds for dict-initiation ---------" % (time.time() - ABSOLUTE_START_TIME))

# fill dictionary with list of 10 100x100 sympy-matrices as value for each key
START_TIME_DICT_CREATION = time.time()
for KEY in THE_DICT.keys():
    VALUE_LIST = []
    for MATRIX in range(10):
        VALUE_LIST.append(ones(100,100))
    THE_DICT[KEY] = VALUE_LIST
print("---------- %s seconds for dict-creation ---------" % (time.time() - START_TIME_DICT_CREATION))

# save dictionary  to pickle-file
START_TIME_PICKLE = time.time()
with open("dictionary.p", "wb") as PICKLE_DESTINATION:
    pickle.dump(THE_DICT, PICKLE_DESTINATION)
print("---------- %s seconds for pickling ---------" % (time.time() - START_TIME_PICKLE))

# query one dictionary entry
START_TIME_EXTRACT = time.time()
THE_DICT['a']
print("---------- %s seconds for entry query runtime ---------" % (time.time() - START_TIME_EXTRACT))
# print total runtime
print("---------- %s seconds total runtime ---------" % (time.time() - ABSOLUTE_START_TIME))

# save dictionary to json-file -- DOES NOT WORK for 'MutableDenseMatrix' object type
# will need modification to do this
# with open("dictionary.json", "w") as JSON_DESTINATION:
#     json.dump(THE_DICT, JSON_DESTINATION)

# output from lifebook a557
# >>> ---------- libraries loaded, starting process ---------------
# ---------- 0.012124776840209961 seconds for dict-initiation ---------
# ---------- 12.183879137039185 seconds for dict-creation ---------
# ---------- 0.06589651107788086 seconds for pickling ---------
# ---------- 2.86102294921875e-06 seconds for entry query runtime ---------
# ---------- 12.262035131454468 seconds total runtime ---------

