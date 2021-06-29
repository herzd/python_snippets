OUTPUT="../matrix_dict_lists.json"
KEYLEN=5
NKEYS=52
NMATRIX=10
MATRIXX=200
MATRIXY=200
NULLDICT="../matrix_dict_lists_nullspaces.json"
import fractions
import json
import sympy
import random
import string
import time

KEYLENGTH = KEYLEN
KEYCOUNT = NKEYS
MATRIXCOUNT = NMATRIX
XMATRIX = MATRIXX
YMATRIX = MATRIXY
OUTFILE = OUTPUT
OUTFILE_NULLDICT = NULLDICT

START_TIME = time.time()
KEYLIST = []
for KEYSTRING in range(KEYCOUNT):
    KEYLIST.append(''.join(random.choice(string.ascii_letters) \
    		       for LETTER in range(KEYLENGTH)))
THE_DICT = dict.fromkeys(KEYLIST)
print("%s seconds for dict-initiation" % (time.time() - START_TIME))

START_TIME_DICT_CREATION = time.time()
for KEY in THE_DICT.keys():
    VALUE_LIST = []
    for MATRIX_COUNT in range(MATRIXCOUNT):
        MATRIX = []
        for ROW in range(YMATRIX):
            MATRIX_ROW = []
            for COLUMN in range(XMATRIX):
                MATRIX_ROW.append((2,3))
            MATRIX.append(MATRIX_ROW)
        VALUE_LIST.append(MATRIX)
    THE_DICT[KEY] = VALUE_LIST
print("%s seconds for dict-creation" % (time.time() - START_TIME_DICT_CREATION))

START_TIME_JSON = time.time()
with open(OUTFILE, "w") as JSON_DESTINATION:
    json.dump(THE_DICT, JSON_DESTINATION)
print("%s seconds for saving to json" % (time.time() - START_TIME_JSON))

START_TIME_QUERY = time.time()
THE_DICT[list(THE_DICT.keys())[random.randrange(len(THE_DICT.keys()))]]
print("%s seconds for random key query" % (time.time() - START_TIME_QUERY))

START_TIME_NULLDICT = time.time()
THE_NULL_DICT = dict.fromkeys(KEYLIST)
for KEY in THE_NULL_DICT.keys():
    VALUE_LIST = []
    for MATRIX in THE_DICT[KEY]:
        NEW_MATRIX = []
        for ROW in MATRIX:
            NEW_MATRIX_ROW = []
            for TUPLE in ROW:
                NEW_MATRIX_ROW.append(sympy.Rational(int(TUPLE[0]),int(TUPLE[1])))
            NEW_MATRIX.append(NEW_MATRIX_ROW)
        NULLSPACES = sympy.Matrix(NEW_MATRIX).nullspace()
        VALUE_LIST.append(NULLSPACES)
    THE_NULL_TUPLE_LIST = []
    for MATRIXLIST in VALUE_LIST:
        VECTORLIST = []
        for MATRIX in MATRIXLIST:
            TUPLED_VALUES = []
            for VALUE in list(MATRIX):
                if type(VALUE) == sympy.core.numbers.Rational:
                    RECOVERED_TUPLE = VALUE.p,VALUE.q
                else:
                    RECOVERED_TUPLE = int(VALUE),1
                TUPLED_VALUES.append(RECOVERED_TUPLE)
            VECTORLIST.append(TUPLED_VALUES)
        THE_NULL_TUPLE_LIST.append(VECTORLIST)
    THE_NULL_DICT[KEY] = THE_NULL_TUPLE_LIST
print("%s seconds for nullspace-calculation" % (time.time() - START_TIME_NULLDICT))

print("%s seconds total runtime" % (time.time() - START_TIME))
