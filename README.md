

# About

 In this file I organize parts of python code that are of interest to me. org-format is used as it allows me to tangle Python-files from emacs from where I do my version control too. The python-files in this repo are exported from this file.
The github-repo itself is set to public for convenience and not for suggesting usage or expectations about contentual stability.


## dictionary of matrix-lists

Making a dictionary with 52 keys and a list of 100 200x200 numpy-array-objects (matrices with fraction-values). This version requires numpy to be in the environment. If I make a larger value-object (eg 100 300x300, or 1000 100x100 matrices), my laptop runs out of its 8GB memory and kills the process at normal usage with graphical browser on.


### numpy-approach

Outside org this script can be run with `python3 matrix_dict_creator_numpy.py`.

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

    0.00021719932556152344 seconds for dict-initiation
    1.2198333740234375 seconds for dict-creation
    9.670838117599487 seconds for pickling
    2.6464462280273438e-05 seconds for random key query
    10.890970945358276 seconds total runtime

This is the loader for the created dictionary. It can be run with `python3 matrix_dict_loader_numpy.py`.

    import fractions
    import numpy
    import pickle
    import random
    import string
    import time
    
    INFILE = INPUT
    START_TIME = time.time()
    with open(INFILE, "rb") as PICKLE_ORIGIN:
        THE_DICT = pickle.load(PICKLE_ORIGIN)
    print("%s seconds for pickle-loading" % (time.time() - START_TIME))
    START_TIME_EXTRACT = time.time()
    THE_DICT[list(THE_DICT.keys())[random.randrange(len(THE_DICT.keys()))]]
    print("%s seconds for entry query" % (time.time() - START_TIME_EXTRACT))
    print("%s seconds total runtime" % (time.time() - START_TIME))

    7.346083402633667 seconds for pickle-loading
    1.8835067749023438e-05 seconds for entry query
    7.3461291790008545 seconds total runtime

And this is the created pickle-file.

    INFILE=$INPUT
    ls -lha $INFILE

    -rw-r--r-- 1 daniel users 990M 28. Jun 22:19 ../matrix_dict_numpy.p


### symbolic approach

This is an approach that calculates the nullspaces for all given matrices and returns them under the same key from a second dictionary as a matrix of tuples. sympy is used for the nullspace calculations. All dict items are plain python.  Tuples and sympy-Rationals are interchanged where needed, as storing the sympy-objects in a dictionary did not prove performant.

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

    0.00021791458129882812 seconds for dict-initiation
    2.192533254623413 seconds for dict-creation
    57.554662466049194 seconds for saving to json
    2.6226043701171875e-05 seconds for random key query
    213.80260372161865 seconds for nullspace-calculation
    273.55013060569763 seconds total runtime

FURTHER: The nullspace-result is a list of sympy-Matrices with one column.  This column contains numbers of the class sympy.core.numbers.Rational and sympy.core.numbers.Integer. Getting all these into integer-tuple-format could need a function.  

