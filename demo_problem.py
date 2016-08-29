#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
import os
import joblib
from joblib import Parallel, delayed

print('pandas version', pd.__version__)
print('joblib version', joblib.__version__)
# mysize= 1000000
def workers(i, filename='test.hdf'):
    mysize= 10
    df = pd.DataFrame(dict(nums=np.arange(i, i+mysize, 1)))
    print 'compute done for worker {}'.format(i)
    with pd.get_store(filename) as store:
        print 'will append to hdf for worker {}'.format(i)
        store.append('output_{}'.format(i), df)
        print 'appended to hdf for worker {}'.format(i)
# first do this serially
fname = 'test_serial.hdf'
tstart = time.time()
list(workers(i, fname) for i in range(20))
tend = time.time()
print(tend -  tstart)/60.

fname = 'test_parallel.hdf'
if os.path.exists(fname):
    os.remove(fname)

tstart = time.time()
Parallel(n_jobs=-1)(delayed(workers)(i, fname) for i in range(20))
tend = time.time()
print(tend -  tstart)/60.
