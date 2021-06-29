OUTPUT="../matrix_dict_lists.json"
KEYLEN=5
NKEYS=2
NMATRIX=2
MATRIXX=3
MATRIXY=4
NULLDICT="../matrix_dict_lists_nullspaces.json"
import json
import os
import random
import string
import time
import sympy

# define values

KEYLENGTH = KEYLEN
KEYCOUNT = NKEYS
MATRIXCOUNT = NMATRIX
XMATRIX = MATRIXX
YMATRIX = MATRIXY
OUTFILE = OUTPUT
OUTFILE_NULLDICT = NULLDICT

# define functions

def create_keylist(KEYCOUNT,KEYLENGTH):
    KEYLIST = []
    for KEYSTRING in range(KEYCOUNT):
        KEYLIST.append(''.join(random.choice(string.ascii_letters) for LETTER in range(KEYLENGTH)))

    return KEYLIST


def create_matrix_list_dict(KEYLIST, MATRIXCOUNT, XMATRIX, YMATRIX):
    START_TIME = time.time()
    INIT_DICT = dict.fromkeys(KEYLIST)
    for KEY in INIT_DICT.keys():
        VALUE_LIST = []
        for MATRIX_COUNT in range(MATRIXCOUNT):
            MATRIX = []
            for ROW in range(YMATRIX):
                MATRIX_ROW = []
                for COLUMN in range(XMATRIX):
                    MATRIX_ROW.append((2,3))
                MATRIX.append(MATRIX_ROW)
            VALUE_LIST.append(MATRIX)
        DICT = INIT_DICT
        DICT[KEY] = VALUE_LIST
    print("{} seconds for creating dict of matrix lists".format(time.time() - START_TIME))

    return DICT


def create_nullspace_dict(KEYLIST, DICT):
    START_TIME = time.time()
    THE_NULL_DICT = dict.fromkeys(KEYLIST)
    for KEY in THE_NULL_DICT.keys():
        VALUE_LIST = []
        for MATRIX in DICT[KEY]:
            NEW_MATRIX = []
            for ROW in MATRIX:
                NEW_MATRIX_ROW = []
                for TUPLE in ROW:
                    NEW_MATRIX_ROW.append(sympy.Rational(int(TUPLE[0]), int(TUPLE[1])))
                NEW_MATRIX.append(NEW_MATRIX_ROW)
            NULLSPACES = sympy.Matrix(NEW_MATRIX).nullspace()
            VALUE_LIST.append(NULLSPACES)
        THE_NULL_TUPLE_LIST = []
        for MATRIXLIST in VALUE_LIST:
            VECTORLIST = []
            for MATRIX in MATRIXLIST:
                TUPLED_VALUES = []
                for VALUE in list(MATRIX):
                    if type(VALUE) == "sympy.core.numbers.Rational":
                        RECOVERED_TUPLE = int(VALUE.p),int(VALUE.q)
                    else:
                        RECOVERED_TUPLE = int(VALUE),1
                    TUPLED_VALUES.append(RECOVERED_TUPLE)
                VECTORLIST.append(TUPLED_VALUES)
            THE_NULL_TUPLE_LIST.append(VECTORLIST)
        THE_NULL_DICT[KEY] = THE_NULL_TUPLE_LIST
    print("{} seconds for creating dict of nullspace vectors".format(time.time() - START_TIME))

    return THE_NULL_DICT


def save_to_json(DICT,OUTFILE):
    START_TIME = time.time()
    with open(OUTFILE, "w") as JSON_DESTINATION:
        json.dump(DICT, JSON_DESTINATION)
    print("{} seconds for saving dict to json".format(time.time() - START_TIME))

    
def check_query_time(DICT):
    START_TIME = time.time()
    DICT[list(DICT.keys())[random.randrange(len(DICT.keys()))]]
    print("{} seconds for random key query".format(time.time() - START_TIME))

    
def check_file_size(FILE):
    START_TIME = time.time()
    print("Filesize of {} {} MB".format(FILE,os.path.getsize(FILE)/(1024**2)))
    print("{} seconds for checking filesize".format(time.time() - START_TIME))

    
# run program

TOTAL_START_TIME = time.time()
KEYLIST = create_keylist(KEYCOUNT,KEYLENGTH)
MATRIX_LIST_DICT = create_matrix_list_dict(KEYLIST, MATRIXCOUNT, XMATRIX, YMATRIX)
save_to_json(MATRIX_LIST_DICT,OUTFILE)
check_query_time(MATRIX_LIST_DICT)
print("displaying dict of matrix lists:")
print(MATRIX_LIST_DICT)
NULLSPACE_DICT = create_nullspace_dict(KEYLIST, MATRIX_LIST_DICT)
save_to_json(NULLSPACE_DICT,OUTFILE_NULLDICT)
check_query_time(NULLSPACE_DICT)
print("displaying dict of nullspace vectors from matrix-list-dict")
print(NULLSPACE_DICT)
check_file_size(OUTFILE)
check_file_size(OUTFILE_NULLDICT)
print("Total program runtime: {} seconds.".format(time.time() - TOTAL_START_TIME))
