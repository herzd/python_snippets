OUTPUT="../matrix_dict_lists.json"
NKEYS=2
NMATRIX=2
MATRIXX=5
MATRIXY=4
NULLDICT="../matrix_dict_nullspaces.json"
INIT_NUM=2
INIT_DENOM=3
CPUS=4
import itertools
import json
import multiprocessing
import os
import random
import string
import time
import sympy


# define values

KEYCOUNT = NKEYS
MATRIXCOUNT = NMATRIX
XMATRIX = MATRIXX
YMATRIX = MATRIXY
OUTFILE = OUTPUT
OUTFILE_NULLDICT = NULLDICT
INIT_FRACTION_VALUE = INIT_NUM,INIT_DENOM
CPU_COUNT = CPUS


# define functions

def create_keylist(KEYCOUNT, KEYLENGTH = 5):
    KEYLIST = []
    for KEYSTRING in range(KEYCOUNT):
        KEYLIST.append(''.join(random.choice(string.ascii_letters) for LETTER in range(KEYLENGTH)))
    return KEYLIST

def create_sample_value_matrix(YMATRIX, XMATRIX=YMATRIX, VALUE=(2,3)):
    MATRIX = []
    for ROW in range(YMATRIX):
        MATRIX_ROW = []
        for COLUMN in range(XMATRIX):
            MATRIX_ROW.append(VALUE)
        MATRIX.append(MATRIX_ROW)
    return MATRIX

def create_matrix_dict(KEYLIST, MATRIX, MATRIXCOUNT):
    DICT = dict.fromkeys(KEYLIST)
    for KEY in DICT.keys():
        VALUE = []
        for ITEM in range(MATRIXCOUNT):
            VALUE.append(MATRIX)
        DICT[KEY] = VALUE
    return DICT

def create_nullspace_dict(KEYLIST, DICT):
    START_TIME = time.time()
    THE_NULL_DICT = dict.fromkeys(KEYLIST)
    for KEY in THE_NULL_DICT.keys():
        NULLSPACE_LIST = []
        for MATRIX in DICT[KEY]:
            NEW_MATRIX = []
            for ROW in MATRIX:
                NEW_MATRIX_ROW = []
                for TUPLE in ROW:
                    NEW_MATRIX_ROW.append(sympy.Rational(int(TUPLE[0]), int(TUPLE[1])))
                NEW_MATRIX.append(NEW_MATRIX_ROW)
            NULLSPACE_LIST.append(sympy.Matrix(NEW_MATRIX).nullspace())
        NULLSPACE_VECTOR_LIST = []
        for MATRIXLIST in NULLSPACE_LIST:
            VECTOR = []
            for VECTOR_MATRIX in MATRIXLIST:
                TUPLED_VALUES = []
                for VALUE in VECTOR_MATRIX:
                    if type(VALUE) == "sympy.core.numbers.Rational":
                        RECOVERED_TUPLE = int(VALUE.p),int(VALUE.q)
                    else:
                        RECOVERED_TUPLE = int(VALUE),1
                    TUPLED_VALUES.append(RECOVERED_TUPLE)
                VECTOR.append(TUPLED_VALUES)
            NULLSPACE_VECTOR_LIST.append(VECTOR)
        THE_NULL_DICT[KEY] = NULLSPACE_VECTOR_LIST
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

def main():
    START_TIME = time.time()
    KEYLIST = create_keylist(KEYCOUNT)
    VALUE_MATRIX = create_sample_value_matrix(YMATRIX)
    MATRIX_LIST_DICT = create_matrix_dict(KEYLIST, VALUE_MATRIX, MATRIXCOUNT)
    save_to_json(MATRIX_LIST_DICT,OUTFILE)
    NULLSPACE_DICT = create_nullspace_dict(KEYLIST, MATRIX_LIST_DICT)
    save_to_json(NULLSPACE_DICT,OUTFILE_NULLDICT)
    print("Total program runtime: {} seconds.".format(time.time() - START_TIME))

if __name__=="__main__":
    main()
