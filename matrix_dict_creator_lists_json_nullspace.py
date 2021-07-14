OUTPUT="../matrix_dict.json"
KEYLEN=5
NKEYS=52
NMATRIX=10
MATRIXX=200
MATRIXY=200
NULLDICT="../matrix_dict_nullspaces.json"
INIT_NUM=2
INIT_DENOM=3
import functools
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

# define functions
def create_keylist(KEYCOUNT, KEYLENGTH = 5):
    KEYLIST = []
    for KEYSTRING in range(KEYCOUNT):
        KEYLIST.append(''.join(random.choice(string.ascii_letters) for LETTER in range(KEYLENGTH)))
    return tuple(KEYLIST)

def create_sample_value_matrix(YMATRIX, XMATRIX=YMATRIX, VALUE=(2,3)):
    MATRIX = []
    for ROW in range(YMATRIX):
        MATRIX_ROW = []
        for COLUMN in range(XMATRIX):
            MATRIX_ROW.append(VALUE)
        MATRIX.append(MATRIX_ROW)
    return MATRIX

def create_list_of_matrices(MATRIX, MATRIXCOUNT=5):
    LIST_OF_MATRICES = []
    for TO_BE_ADDED in range(MATRIXCOUNT):
        LIST_OF_MATRICES.append(MATRIX)
    return LIST_OF_MATRICES

def create_dict(KEYLIST):
    DICT = dict.fromkeys(KEYLIST)
    return DICT

def detuple_and_sympyfy_value_matrix(MATRIX):
    NEW_MATRIX = []
    for ROW in MATRIX:
        NEW_MATRIX_ROW = []
        for TUPLE in ROW:
            NEW_MATRIX_ROW.append(sympy.Rational(int(TUPLE[0]), int(TUPLE[1])))
        NEW_MATRIX.append(NEW_MATRIX_ROW)
    return NEW_MATRIX

def calculate_nullspaces_and_retuple_matrix(MATRIX):
    '''calculates the nullspace vectors of a given matrix
    and returns a list of vectors'''
    NULLSPACE_LIST_SYMPY = sympy.Matrix(MATRIX).nullspace()
    NULLSPACE_VECTORLIST =[]
    for VECTOR_MATRIX in NULLSPACE_LIST_SYMPY:
        TUPLED_VALUES = []
        for VALUE in VECTOR_MATRIX:
            if type(VALUE) == "sympy.core.numbers.Rational":
                RECOVERED_TUPLE = int(VALUE.p),int(VALUE.q)
            else:
                RECOVERED_TUPLE = int(VALUE),1
            TUPLED_VALUES.append(RECOVERED_TUPLE)
        NULLSPACE_VECTORLIST.append(TUPLED_VALUES)
    return NULLSPACE_VECTORLIST

def fill_dict(MATRIX_DICT_MULTI, KEY, MATRIXLIST):
    '''creates a dictionary with a list of matrices appended
    to given key. meant to be run within a multiprocessing
    Manager that provides the dictionary'''
    MATRIX_DICT_MULTI[KEY] = MATRIXLIST
    return MATRIX_DICT_MULTI

def save_to_json(DICT,OUTFILE):
    with open(OUTFILE, "w") as JSON_DESTINATION:
        json.dump(DICT, JSON_DESTINATION)
        
def check_query_time(DICT):
    DICT[list(DICT.keys())[random.randrange(len(DICT.keys()))]]

def check_file_size(FILE):
    print("Filesize of {} {} MB\n".format(FILE,os.path.getsize(FILE)/(1024**2)))

# dependent functions

def calculate_nullspace_list(MATRIX_LIST):
    '''calculates the nullspaces of the matrices in 
    a given list of matrices and returns them as a list of list of 
    vectors'''
    NULLSPACE_LIST = []
    for MATRIX in MATRIX_LIST:
        DETUPLED = detuple_and_sympyfy_value_matrix(MATRIX)
        CALCULATED_RETUPLED = calculate_nullspaces_and_retuple_matrix(DETUPLED)
        NULLSPACE_LIST.append(CALCULATED_RETUPLED)
    return NULLSPACE_LIST

def calculate_nullspaces(NULLSPACE_DICT_MULTI, KEY, MATRIX_DICT):
    '''takes a dictionary with list of matrices and 
    returns them as dict with resulting nullspace-vectors. the
    output dictionary is meant to be provided by a multiprocessing Manager'''
    NULLSPACE_DICT_MULTI[KEY] = calculate_nullspace_list(MATRIX_DICT[KEY])
    return NULLSPACE_DICT_MULTI


# program

def main():
    START_TIME = time.time()
    KEYLIST = create_keylist(KEYCOUNT)
    VALUE_MATRIX = create_sample_value_matrix(YMATRIX)
    MATRIX_LIST = create_list_of_matrices(VALUE_MATRIX)
    NULLSPACE_LIST = calculate_nullspace_list(MATRIX_LIST)
    START_TIME_DICT_FILL = time.time()
    MANAGER_01 = multiprocessing.Manager()
    MATRIX_DICT_M = MANAGER_01.dict()
    JOBS_01 = [multiprocessing.Process(target=fill_dict, args=(MATRIX_DICT_M, KEY, MATRIX_LIST)) for KEY in KEYLIST]
    _ = [PROCESS.start() for PROCESS in JOBS_01]
    _ = [PROCESS.join() for PROCESS in JOBS_01]
    MATRIX_DICT = dict(MATRIX_DICT_M)
    print("loading dict with array of matrices: {} seconds\n".format(time.time() - START_TIME_DICT_FILL))
    #print(MATRIX_DICT)
    #print("")
    START_TIME_NULLSPACES = time.time()
    MANAGER_02 = multiprocessing.Manager()
    NULLSPACE_DICT_M = MANAGER_02.dict()
    JOBS_02 = [multiprocessing.Process(target=calculate_nullspaces, args=(NULLSPACE_DICT_M, KEY, MATRIX_DICT)) for KEY in KEYLIST]
    _ = [PROCESS.start() for PROCESS in JOBS_02]
    _ = [PROCESS.join() for PROCESS in JOBS_02]
    NULLSPACE_DICT = dict(NULLSPACE_DICT_M)
    print("nullspace calculation time: {} seconds\n".format(time.time() - START_TIME_NULLSPACES))
    #print(NULLSPACE_DICT)
    #print("")
    START_TIME_SAVING_DICTS = time.time()
    with multiprocessing.Pool() as POOL:
        POOL.starmap(save_to_json, [(MATRIX_DICT,OUTFILE),(NULLSPACE_DICT,OUTFILE_NULLDICT)])
    print("time for saving matrix dict and nullspace dict: {} seconds\n".format(time.time() - START_TIME_SAVING_DICTS))
    START_TIME_QUERIES = time.time()
    for DICT in [MATRIX_DICT,NULLSPACE_DICT]:
        check_query_time(DICT)
# this does not enhance speed, as pool-creation takes about 1 second. might be handy with multiple queries though.
#    with multiprocessing.Pool() as POOL:
#        POOL.starmap(check_query_time, [(MATRIX_DICT,),(NULLSPACE_DICT,)])
    print("time for random query in both dictionaries: {} seconds\n".format(time.time() - START_TIME_QUERIES))
    START_TIME_SIZECHECK = time.time()
    with multiprocessing.Pool() as POOL:
        POOL.starmap(check_file_size, [(OUTFILE,),(OUTFILE_NULLDICT,)])
    print("total runtime: {} seconds\n".format(time.time() - START_TIME))


# program execution

if __name__=="__main__":
    main()
