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

sys_dict  =  {'2mass':1, 'hst_ab':2, 'hst_st':3, 'hst_vega':4, 'sdss':5,
                 'ubvri12':6, 'ubvri90':7, 'jwst_miri_ab':8, 'jwst_miri_st':9,
                 'jwst_miri_vega':10, 'jwst_moda_ab':11, 'jwst_moda_st':12,
                 'jwst_moda_vega':13, 'jwst_modab_ab':14, 'jwst_modab_st':15,
                 'jwst_modab_vega':16, 'jwst_modb_ab':17,  'jwst_modb_st':18,
                 'jwst_modb_vega':19, 'SkyMapper':20, 'Tycho':21,
                 'PanSTARRS1':22, 'Gaia_pro_ab':23, 'Gaia_pro_vega':24,
                 'Gaia_rev_ab':25, 'Gaia_rev_vega':26, 'Gaia_DR2':27
                 }
filter_dict = {'J':1, 'H':2, 'K':3, 'acs_f435w':4, 'acs_f475w':5, 'acs_f555w':6,
               'acs_f606w':7, 'acs_f814w':8, 'wfc3_f218w':9,
                'wfc3_f225w':10, 'wfc3_f275w':11, 'wfc3_f336w':12,
                'wfc3_f350lp':13,  'wfc3_f390m':14,  'wfc3_f390w':15,
                'wfc3_f438w':16,  'wfc3_f475w':17, 'wfc3_f547m':18,
                'wfc3_f555w':19,   'wfc3_f606w':20, 'wfc3_f625w':21,
                'wfc3_f775w':22,    'wfc3_f814w':23,  'wfc3_f850lp':24,
                'wfc3ir_f98m':25,  'wfc3ir_f110w':26, 'wfc3ir_f125w':27,
                'wfc3ir_f140w':28,  'wfc3ir_f160w':29,
                'u':30, 'g':31, 'r':32, 'i':33, 'z':34,
                'U':35, 'B':36, 'V':37, 'R_C':38, 'I_C':39,
                'UX':40, 'BX':41,
                'miri_f560w':42, 'miri_f770w':43, 'miri_f1000w':44,
                'miri_f1130w':45, 'miri_f1280w':46, 'miri_f1500w':47,
                'jwst_f070w':48, 'jwst_f090w':49,'jwst_f115w':50,
                'jwst_f140m':51, 'jwst_f150w2':52, 'jwst_f150w':53,
                'jwst_f162m':54, 'jwst_f182m':55, 'jwst_f200w':56,
                'jwst_f210m':57, 'jwst_f250m':58, 'jwst_f277w':59,
                'jwst_f300m':60, 'jwst_f322w2':61, 'jwst_f335m':62,
                'jwst_f356w':63, 'jwst_f360m':64, 'jwst_f410m':65,
                'jwst_f430m':66, 'jwst_f444w':67, 'jwst_f460m':68,
                'jwst_f480m':69,
                'u':70, 'v':71, 'g':72, 'r':73, 'i':74, 'z':75,
                'Hp':76, 'B_T':77, 'V_T':78,
                'PSg':79, 'PSr':80, 'PSi':81, 'PSz':82, 'PSy':83, 'PSw':84, 'PSo':85,
                'G_BP':86, 'G':87, 'G_RP':88
                }

sets_dict = {'GaiaDR2':(sys_dict['Gaia_DR2'], filter_dict['G'],  filter_dict['G_BP'], filter_dict['G_RP']),
             '2MASS':(sys_dict['2mass'], filter_dict['J'],filter_dict['H'],  filter_dict['K'])}

def set_filters(filter_set='GaiaDR2'):
    """ write the relevant filter set into the parameter file """
    filters = sets_dict[filter_set]
    sys_ind = filters[0]
    filt_ind = filters[1:]
    nfil = len(filt_ind)
    ialf = 1
    with open(os.path.join(_BOLOPATH, 'BCcodes', 'selectbc.data'), 'r') as f:
        lines = f.readlines()
    lines[0] = str(int(ialf)).rjust(3)+lines[0][3:]
    lines[1] = str(int(nfil)).rjust(3)+lines[1][3:]
    for i in range(nfil):
        lines[2+i] = str(int(sys_ind)).rjust(4)+' '+str(int(filt_ind[i]))+lines[2+i][7:]
    with open(os.path.join(_BOLOPATH, 'BCcodes', 'selectbc.data'), 'w') as f:
         f.writelines(lines)


def generate_input(sid, logg, feh, teff, exbv):
    """
    Generate the input file for bolometric corrections (overwrites existing file in bolometric-corrections directory)
    INPUT:
        sid - IDs for the stars
        logg - logg for stars
        feh - feh of each star
        teff - teff of each star
        exbv - E(B-V) for each star
    """
    with open(os.path.join(_BOLOPATH, 'BCcodes', 'input.sample.all'), 'w') as f:
        for i in range(len(logg)):
            f.write('%s %s %s %s %s\n' % (sid[i], logg[i], feh[i], teff[i], exbv[i]))

def run_bc():
    """
    run bolometric-corrections on the data
    """
    with cd(os.path.join(_BOLOPATH, 'BCcodes')):
        process = subprocess.run(['./bcall'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

def read_output(filter_set='GaiaDR2'):
    inv_sys = {v: k for k, v in sys_dict.items()}
    inv_filt = {v: k for k, v in filter_dict.items()}
    filters = sets_dict[filter_set][1:]
    nfil = len(filters)
    output_dtype = [('ID', '<U18'),
                    ('LOGG', float),
                    ('FE_H', float),
                    ('TEFF', float),
                    ('EBV', float)]
    for i in range(5):
        if i < nfil:
            output_dtype.append(('BC_'+inv_filt[filters[i]], float))
        else:
            output_dtype.append(('BC_'+str(i), float))
    outfile = os.path.join(_BOLOPATH,'BCcodes','output.file.all')
    return np.genfromtxt(outfile,dtype=output_dtype, skip_header=1)
