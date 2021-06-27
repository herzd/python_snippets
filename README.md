

# About

 In this file I organize parts of python code that are of interest to me. org-format is used as it allows me to tangle Python-files from emacs from where I do my version control too. The python-files in this repo are exported from this file.
The github-repo itself is set to public for convenience and not for suggesting usage or expectations about contentual stability.


## structures


### dictionary of matrix-lists

Making a dictionary with 52 keys and a list of 100 200x200 numpy-array-objects (matrices with fraction-values). This version requires numpy to be in the environment. If I make a larger value-object (eg 100 300x300, or 1000 100x100 matrices), my laptop runs out of its 8GB memory and kills the process at normal usage with graphical browser on. It can be run with `python3 numpy_matrix_dict_creator.py`.

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

    0.0002167224884033203 seconds for dict-initiation
    1.240699291229248 seconds for dict-creation
    11.510791540145874 seconds for pickling
    2.4318695068359375e-05 seconds for random key query
    12.75179147720337 seconds total runtime

This is the loader for the created dictionary. It can be run with `python3 numpy_matrix_dict_loader.py`.

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

    9.956590414047241 seconds for pickle-loading
    1.9311904907226562e-05 seconds for entry query
    9.956644535064697 seconds total runtime

And this is the created pickle-file.

    INFILE=$INPUT
    ls -lha $INFILE

    -rw-r--r-- 1 daniel users 990M 28. Jun 01:31 ../numpy_matrix_dict.p

