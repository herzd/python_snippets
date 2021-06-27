OUTPUT="../numpy_matrix_dict.p"
import fractions
import numpy
import pickle
import string
import time

OUTFILE = OUTPUT
ABSOLUTE_START_TIME = time.time()
THE_DICT_NUMPY = {}
THE_DICT_NUMPY = dict.fromkeys(list(string.ascii_letters))
print("%s seconds for dict-initiation" % (time.time() - ABSOLUTE_START_TIME))
START_TIME_DICT_CREATION = time.time()
for KEY in THE_DICT_NUMPY.keys():
    VALUE_LIST = []
    for MATRIX in range(100): VALUE_LIST.append(numpy.full((200,200), \
							   fractions.Fraction(2,3)))
    THE_DICT_NUMPY[KEY] = VALUE_LIST
print("%s seconds for dict-creation" % (time.time() - START_TIME_DICT_CREATION))
START_TIME_PICKLE = time.time()
with open(OUTFILE, "wb") as PICKLE_DESTINATION:
    pickle.dump(THE_DICT_NUMPY, PICKLE_DESTINATION)
print("%s seconds for pickling" % (time.time() - START_TIME_PICKLE))
START_TIME_QUERY = time.time()
THE_DICT_NUMPY['a']
print("%s seconds for entry query runtime" % (time.time() - START_TIME_QUERY))
print("%s seconds total runtime" % (time.time() - ABSOLUTE_START_TIME))
