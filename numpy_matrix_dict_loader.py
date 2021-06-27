INPUT="../numpy_matrix_dict.p"
import fractions
import numpy
import pickle
import string
import time

INFILE = INPUT
ABSOLUTE_START_TIME = time.time()
START_TIME_UNPICKLE_NUMPY = time.time()
with open(INFILE, "rb") as PICKLE_ORIGIN:
    THE_DICT_NUMPY = pickle.load(PICKLE_ORIGIN)
print("%s seconds for pickle-loading" % (time.time() - START_TIME_UNPICKLE_NUMPY))
START_TIME_EXTRACT = time.time()
THE_DICT_NUMPY['a']
print("%s seconds for entry query" % (time.time() - START_TIME_EXTRACT))
print("%s seconds total runtime" % (time.time() - ABSOLUTE_START_TIME))
