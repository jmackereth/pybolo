import numpy as np
import subprocess
import os
from contextlib import contextmanager

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

try:
    _BOLOPATH = os.environ['BOLOPATH']
except KeyError:
    raise KeyError('Ensure you set the environment variable BOLOPATH to point at your compiled bolometric-corrections')




def generate_input(logg, feh, teff):
    """
    Generate the input file for bolometric corrections (overwrites file)
    """
    with open(os.path.join(_BOLOPATH, 'BCcodes', 'input.sample'), 'w') as f:
        for i in range(len(logg)):
            f.write('%s %s %s \n' % (logg[i], feh[i], teff[i]))

def run_bc():
    """
    run bolometric-corrections on the data
    """
    with cd(os.path.join(_BOLOPATH, 'BCcodes')):
        subprocess.call(['./bcgo', '0'])
