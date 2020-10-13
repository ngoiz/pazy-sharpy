import sys
import os
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import numpy as np
import sharpy.utils.algebra as algebra
import shutil


def cga(alpha):
    return algebra.quat2rotation(algebra.euler2quat(np.array([0, alpha * np.pi / 180, 0])))

#####################################
# INPUTS

sharpy_output_folder = './output/'
output_folder = '../../pazy-aepw3-results/'
modal_output_folder = output_folder + '/04_DeformedModal/'

#####################################

if not os.path.isdir(output_folder):
    raise FileNotFoundError('Output Directory not found - please create it prior to running the script')

for skin in [True, False]:
    if skin:
        sharpy_case_name = 'test_followerforce_LB_FF_skin_on'
        skin_wo = 'w'
    else:
        sharpy_case_name = 'test_followerforce_LB_FF_skin_off'
        skin_wo = 'wo'

    modal_case_output_folder = 'sharpy_followerforce_LB_FF_skin{:g}'.format(skin)

    dataset = Actual(sharpy_output_folder + sharpy_case_name + '/*')

    dataset.load_bulk_cases('deflection', 'eigs')

    wing_tip_deflection = []
    tip_mass = []
    beam_frequencies = []

    for case in dataset.aeroelastic:
        #     wing_tip_deflection.append(case.deflection[-1, -1])
        tip_mass.append(case.parameter_value)
        eigs = np.abs(case.eigs[:20, 1])
        e_order = np.argsort(eigs)
        beam_frequencies.append(eigs[e_order])
        wing_tip_deflection.append(cga(0).dot(case.deflection[-1, 1:])[-1])

    tip_mass = np.array(tip_mass)
    order = np.argsort(tip_mass)
    wing_tip_deflection = np.array(wing_tip_deflection)[order]
    beam_frequencies = [beam_frequencies[i] for i in order]

    # save bending data z displacement only

    mode_data = []

    if os.path.isdir(modal_output_folder + modal_case_output_folder):
        print('Cleaning output directory')
        shutil.rmtree(modal_output_folder + modal_case_output_folder)
    os.makedirs(modal_output_folder + modal_case_output_folder, exist_ok=True)

    for i_mode in range(0, 10, 2):
        mode_data.append(np.array([freq[i_mode] for freq in beam_frequencies]))
        np.savetxt(modal_output_folder + modal_case_output_folder + '/mode_{:02g}.txt'.format(i_mode // 2),
                   np.column_stack((tip_mass, wing_tip_deflection, mode_data[i_mode // 2])))
    print('Saved data to {}'.format(modal_output_folder + modal_case_output_folder))
