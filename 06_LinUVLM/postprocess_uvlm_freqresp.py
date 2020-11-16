import sys
import os
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import glob
import numpy as np
import shutil
import sharpy.utils.algebra as algebra

def prepare_cases_db(sharpy_output_folder, source_cases, param_vec):
    cases_db = []

    for ith, src_path in enumerate(source_cases):
        res = Actual(sharpy_output_folder + src_path + '/*')
        # res.case_parameter = param_vec[ith]
        res.systems = ['aeroelastic', 'aerodynamic', 'structural']
        res.load_bulk_cases('eigs', 'deflection', 'bode')
        cases_db.append(res)

    return cases_db

def save_frequency_data(actual_case):
    set_cases = actual_case.aerodynamic
    for case in set_cases:
        yfreq = case.bode.yfreq
        wv = case.bode.wv

        nout, nin = case.bode.ss0.shape
        case_name = 'sharpy_uinf{:04g}_{:s}_skin{:g}'.format(case.parameter_value, 'aero', 0)
        os.makedirs(postprocess_output + '/' + case_name, exist_ok=True)
        for i_out in range(nout):
            for i_in in range(nin):
                res = np.column_stack((wv, yfreq[i_out, i_in, :].real, yfreq[i_out, i_in, :].imag))
                np.savetxt(postprocess_output + '/' + case_name + '/in{:02g}_out{:02g}.txt'.format(i_in, i_out), res)
#######################
# INPUTS
sharpy_output_directory = './output/test_pazy_M16N1Ms16_alpha0000_skin1/'
postprocess_output = './output/postprocess/'

#######################
# if os.path.isdir(postprocess_output):
#     shutil.rmtree(postprocess_output)

# os.makedirs(postprocess_output)

src_cases = glob.glob(sharpy_output_directory)

results = prepare_cases_db('', src_cases, param_vec=5)

# import pdb; pdb.set_trace()
for case in results:
    save_frequency_data(case)