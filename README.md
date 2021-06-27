

# About

 In this file I organize parts of python code that are of interest to me. org-format is used as it allows me to tangle Python-files from emacs from where I do my version control too. The python-files in this repo are exported from this file.
The github-repo itself is set to public for convenience and not for suggesting usage or expectations about contentual stability.


## structures


### dictionary of matrix-lists

Making a dictionary with 52 keys and a list of 100 200x200 numpy-array-objects (matrices with fraction-values). This version requires numpy to be in the environment. If I make a larger value-object (eg 100 300x300, or 1000 100x100 matrices), my laptop runs out of its 8GB memory and kills the process at normal usage with graphical browser on. It can be run with `python3 numpy_matrix_dict_creator.py`.

    import fractions
    import numpy
    import pickle
    import string
    import time
    
    OUTFILE = OUTPUT
    ABSOLUTE_START_TIME = time.time()
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
    print("%s seconds for entry query" % (time.time() - START_TIME_QUERY))
    print("%s seconds total runtime" % (time.time() - ABSOLUTE_START_TIME))

    7.3909759521484375e-06 seconds for dict-initiation
    1.2408761978149414 seconds for dict-creation
    10.574112176895142 seconds for pickling
    2.384185791015625e-06 seconds for entry query
    11.81505799293518 seconds total runtime

This is the loader for the created dictionary. It can be run with `python3 numpy_matrix_dict_loader.py`.

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

    8.18607783317566 seconds for pickle-loading
    1.1920928955078125e-06 seconds for entry query
    8.186107873916626 seconds total runtime

And this is the created pickle-file.

    INFILE=$INPUT
    ls -lha $INFILE

    -rw-r--r-- 1 daniel users 990M 27. Jun 05:31 ../numpy_matrix_dict.p

