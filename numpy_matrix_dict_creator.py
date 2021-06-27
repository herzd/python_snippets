OUTPUT="../numpy_matrix_dict.p"
KEYLEN=5
NKEYS=52
NMATRIX=100
MATRIXX=200
MATRIXY=200
import fractions
import numpy
import pickle
import random
import string
import time

START_TIME = time.time()
KEYLENGTH = KEYLEN
KEYCOUNT = NKEYS
MATRIXCOUNT = NMATRIX
XMATRIX = MATRIXX
YMATRIX = MATRIXY
OUTFILE = OUTPUT
KEYLIST = []
for KEYSTRING in range(KEYCOUNT):
    KEYLIST.append(''.join(random.choice(string.ascii_letters) \
			   for LETTER in range(KEYLENGTH)))
THE_DICT = dict.fromkeys(KEYLIST)
print("%s seconds for dict-initiation" % (time.time() - START_TIME))
START_TIME_DICT_CREATION = time.time()
for KEY in THE_DICT.keys():
    VALUE_LIST = []
    for MATRIX in range(MATRIXCOUNT): VALUE_LIST.append(numpy.full((XMATRIX,YMATRIX), \
								   fractions.Fraction(2,3)))
    THE_DICT[KEY] = VALUE_LIST
print("%s seconds for dict-creation" % (time.time() - START_TIME_DICT_CREATION))
START_TIME_PICKLE = time.time()
with open(OUTFILE, "wb") as PICKLE_DESTINATION:
    pickle.dump(THE_DICT, PICKLE_DESTINATION)
print("%s seconds for pickling" % (time.time() - START_TIME_PICKLE))
START_TIME_QUERY = time.time()
THE_DICT[list(THE_DICT.keys())[random.randrange(len(THE_DICT.keys()))]]
print("%s seconds for random key query" % (time.time() - START_TIME_QUERY))
print("%s seconds total runtime" % (time.time() - START_TIME))
