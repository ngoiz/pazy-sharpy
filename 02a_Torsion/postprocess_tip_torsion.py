import sys
import os
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import numpy as np


#####################################
# INPUTS

sharpy_output_folder = './output/'
output_folder = '../../pazy-aepw3-results/'
aepw3_output_folder = output_folder + '/02_Torsion/'

#####################################
chord = 0.1

def compute_twist_angle(le_deflection, te_deflection):
    twist = np.arctan((le_deflection[:, 2] - te_deflection[:, 2]) / (le_deflection[:, 0] - te_deflection[:, 0]))
    twist *= -1  # for convention
    return twist

for skin in [True, False]:
    if skin:
        sharpy_case_name = 'skin_on'
        skin_wo = 'w'
        ea_location = 0.531
    else:
        sharpy_case_name = 'skin_off'
        skin_wo = 'wo'
        ea_location = 0.441

    modal_case_output_folder = 'sharpy_bending_skin{:g}'.format(skin)

    dataset = Actual(sharpy_output_folder + sharpy_case_name + '/*')

    dataset.load_bulk_cases('deflection', 'beam_modal_analysis')

    le_pos = ea_location * chord
    te_pos = - (1 - ea_location) * chord
    mid_chord = - (0.5 - ea_location) * chord

    param_array, le_deflection = dataset.wing_tip_deflection(reference_line=np.array([0, le_pos, 0]))
    _, te_deflection = dataset.wing_tip_deflection(reference_line=np.array([0, te_pos, 0]))
    _, mid_deflection = dataset.wing_tip_deflection(reference_line=np.array([0, mid_chord, 0]))

    crv = np.zeros((param_array.shape[0], 4))
    for i_case, case in enumerate(dataset.aeroelastic):
        crv[i_case, 0] = case.parameter_value
        crv[i_case, 1:] = case.crv[-1, :]

    order = np.argsort(crv[:, 0])
    crv = crv[order]

    file_name = 'torsion_SHARPy_{:s}_skin_wingtip_coordinates.txt'.format(skin_wo)

    np.savetxt(aepw3_output_folder + file_name,
               np.column_stack((param_array, mid_deflection, le_deflection,  te_deflection)))

    file_name = 'torsion_SHARPy_{:s}_skin_wingtip_crv.txt'.format(skin_wo)

    np.savetxt(aepw3_output_folder + file_name,
               crv)

    file_name = 'torsion_SHARPy_{:s}_skin.txt'.format(skin_wo)
    twist = compute_twist_angle(le_deflection, te_deflection) * 180 / np.pi
    np.savetxt(aepw3_output_folder + file_name,
               np.column_stack((param_array, mid_deflection[:, 2], twist)))
