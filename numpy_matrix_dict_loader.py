INPUT="../numpy_matrix_dict.p"
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
