'''This script creates a dictionary of matrix-lists with rational values, and
calculates the nullspaces of these matrices. The results are stored in a dictionary
under the same key. Both dictionaries are saved to json-format'''

import json
import multiprocessing
import os
import random
import string
import time
import sympy

OUTPUT_DICT="../matrix_dict.json"
KEYLEN=5
NKEYS=52
NMATRIX=10
MATRIXX=200
MATRIXY=200
OUTPUT_NULLDICT="../matrix_dict_nullspaces.json"
INIT_NUM=2
INIT_DENOM=3
# define values
KEYCOUNT = NKEYS
KEYLENGTH = KEYLEN
MATRIXCOUNT = NMATRIX
ROW_COUNT = MATRIXY
COL_COUNT = MATRIXX
VALUE = INIT_NUM,INIT_DENOM
OUTFILE = OUTPUT_DICT
OUTFILE_NULLDICT = OUTPUT_NULLDICT

def create_keylist(keycount, keylength):
    '''Function that takes two parameters (KEYCOUNT=int, KEYLENGTH=int) and
    returns the created keylist, consisting of random strings.'''
    keylist = []
    for keystring in range(keycount):
        keylist.append(''.join(random.choice(string.ascii_letters)
                               for letter in range(keylength)))
    return keylist

def create_sample_value_matrix(row_count, col_count, value):
    '''takes a parameter for the matrix' row_count (int), col_count defaults
    to same row_count. value defaults to tuple (2,3). returns matrix (list of lists).'''
    matrix = []
    for row in range(row_count):
        matrix_row = []
        for column in range(col_count):
            matrix_row.append(value)
        matrix.append(matrix_row)
    return matrix

def create_list_of_matrices(matrix, matrixcount=5):
    '''takes a matrix (list of lists) and repeates it according to second parameter
    returns the list of matrices'''
    list_of_matrices = []
    for to_be_added in range(matrixcount):
        list_of_matrices.append(matrix)
    return list_of_matrices

def create_dict(keylist):
    '''returns an empty dictionary from a given keylist'''
    dictionary = {}
    dictionary = dictionary.fromkeys(keylist)
    return dictionary

def detuple_and_sympyfy_value_matrix(matrix):
    '''transforms rational values represented as tuples in given matrix
    to sympy.Rational objects for further processing.
    returns the new matrix with sympy.Rational values'''
    new_matrix = []
    for row in matrix:
        new_matrix_row = []
        for tuple_item in row:
            new_matrix_row.append(sympy.Rational(int(tuple_item[0]), int(tuple_item[1])))
        new_matrix.append(new_matrix_row)
    return new_matrix

def calculate_nullspaces_and_retuple_matrix(matrix):
    '''calculates the nullspace vectors of a given matrix
    and returns a list of vectors.'''
    nullspace_list_sympy = sympy.Matrix(matrix).nullspace()
    nullspace_vectorlist =[]
    for vector_matrix in nullspace_list_sympy:
        tupled_values = []
        for value in vector_matrix:
            if isinstance(value,sympy.core.numbers.Rational):
                recovered_tuple = int(value.p),int(value.q)
            else:
                recovered_tuple = int(value),1
            tupled_values.append(recovered_tuple)
        nullspace_vectorlist.append(tupled_values)
    return nullspace_vectorlist

def fill_dict(matrix_dict_multi, key, matrix_list):
    '''returns a dictionary with a list of matrices appended
    to given key. meant to be run within a multiprocessing
    manager that provides the dictionary'''
    matrix_dict_multi[key] = matrix_list
    return matrix_dict_multi

def save_to_json(dictionary,outfile):
    '''saves dictionary to outfile (given as path string). returns nothing '''
    with open(outfile, "w") as json_destination:
        json.dump(dictionary, json_destination)

def check_filesize(filepath):
    '''prints the size of given file (path as string) in MB.
    returns nothing'''
    print("{} filesize {} MB\n".format(filepath,os.path.getsize(filepath)/(1024**2)))

def calculate_nullspace_list(matrix_list):
    '''calculates the nullspaces of the matrices in
    a given list of matrices and returns them as a list of list of
    vectors'''
    nullspace_list = []
    for matrix in matrix_list:
        detupled = detuple_and_sympyfy_value_matrix(matrix)
        calculated_retupled = calculate_nullspaces_and_retuple_matrix(detupled)
        nullspace_list.append(calculated_retupled)
    return nullspace_list

def calc_nullspaces(nullspace_dict_multi, key, matrix_dict_multi):
    '''takes a dictionary with list of matrices and
    returns them as dict with resulting nullspace-vectors. the
    output dictionary is meant to be provided by a multiprocessing manager'''
    nullspace_dict_multi[key] = calculate_nullspace_list(matrix_dict_multi[key])
    return nullspace_dict_multi

def main():
    '''main procedure using all of above functions. where possible, uses all cpus
    available to the user. prints information to stdout and saves dictionaries
    to folder above location.'''
    start_time = time.time()
    keylist = create_keylist(KEYCOUNT,KEYLENGTH)
    sample_matrix = create_sample_value_matrix(ROW_COUNT,COL_COUNT,VALUE)
    matrix_list = create_list_of_matrices(sample_matrix)
    print("loading initial dict with lists of matrices...\n")
    manager_01 = multiprocessing.Manager()
    matrix_dict_m = manager_01.dict()
    jobs_01 = [multiprocessing.Process(target=fill_dict, args=(matrix_dict_m, key, matrix_list))
               for key in keylist]
    _ = [process.start() for process in jobs_01]
    _ = [process.join() for process in jobs_01]
    matrix_dict = dict(matrix_dict_m)
    start_nullspaces = time.time()
    print("starting nullspace calculation...\n")
    manager_02 = multiprocessing.Manager()
    nullspace_dict_m = manager_02.dict()
    jobs_02 = [multiprocessing.Process(target=calc_nullspaces,
                                       args=(nullspace_dict_m,key, matrix_dict))
               for key in keylist]
    _ = [process.start() for process in jobs_02]
    _ = [process.join() for process in jobs_02]
    nullspace_dict = dict(nullspace_dict_m)
    print("nullspace calculation: {} seconds\n".format(time.time() - start_nullspaces))
    print("saving dicts...\n")
    with multiprocessing.Pool() as process_pool:
        process_pool.starmap(save_to_json, [(matrix_dict,OUTFILE),
                                            (nullspace_dict,OUTFILE_NULLDICT)])

    check_filesize(OUTFILE)
    check_filesize(OUTFILE_NULLDICT)
    print("total runtime: {} seconds\n".format(time.time() - start_time))

# needed for proper wrapping of above's multiprocessing calls
if __name__=="__main__":
    main()
