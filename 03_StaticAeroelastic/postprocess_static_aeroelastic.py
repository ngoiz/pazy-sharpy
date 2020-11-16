import sys
import os
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import numpy as np
import sharpy.utils.algebra as algebra
import shutil


def cga(alpha):
    return algebra.quat2rotation(algebra.euler2quat(np.array([0, alpha * np.pi / 180, 0])))

def prepare_cases_db(sharpy_output_folder, source_cases, param_vec):
    cases_db = []

    for ith, src_path in enumerate(source_cases):
        res = Actual(sharpy_output_folder + src_path + '/*')
        res.case_parameter = param_vec[ith]
        res.systems = ['aeroelastic']
        res.load_bulk_cases('deflection')
        cases_db.append(res)

    return cases_db

# write eigenvalues:
def save_deflection(case, output_folder, skin_str):

    vel, deflection = case.wing_tip_deflection(frame='g', alpha=case.case_parameter, reference_line=[0, -(0.5-0.441)*0.1, 0])
    np.savetxt(output_folder + '/sharpy_{:s}_skin_alpha{:04g}.txt'.format(skin_str, case.case_parameter * 100),
               np.column_stack((vel, deflection[:, -1])))


def main():
    #####################################
    # INPUTS

    sharpy_output_folder = './output/'
    output_folder = '../../pazy-aepw3-results/03_StaticAeroelastic/'
    alpha_vec = [5., 7.]
    #####################################

    if not os.path.isdir(output_folder):
        raise FileNotFoundError('Output Directory not found - please create it prior to running the script')

    for skin in [True, False]:

        if skin:
            skin_str = 'w'
        else:
            skin_str = 'wo'

        source_cases = ['pazy_um116N64Ms1_alpha{:04g}_skin{:s}'.format(
            alpha * 100, str(skin)) for alpha in alpha_vec]

        results = prepare_cases_db(sharpy_output_folder, source_cases, alpha_vec)

        for case in results:
            save_deflection(case, output_folder, skin_str)


if __name__ == '__main__':
    main()

