import sys
import os
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import numpy as np
import sharpy.utils.algebra as algebra


def cga(alpha):
    return algebra.quat2rotation(algebra.euler2quat(np.array([0, alpha * np.pi / 180, 0])))


alpha_vec = np.array([1, 5, 7])
sharpy_output_folder = './output/'
output_folder = '../../pazy-aepw3-results/04_DeformedModal/'

for skin in [True, False]:
    for alpha in alpha_vec:
        sharpy_case_name = 'pazy_um116N64Ms1_alpha{:04g}_skin{}'.format(alpha * 100, skin)
        case_out_folder = 'sharpy_alpha{:04g}_skin{:g}'.format(alpha*100, skin)

        dataset = Actual(sharpy_output_folder + sharpy_case_name + '/*')

        dataset.load_bulk_cases('deflection', 'beam_modal_analysis')

        wing_tip_deflection = []
        velocity = []
        beam_frequencies = []

        for case in dataset.aeroelastic:
            #     wing_tip_deflection.append(case.deflection[-1, -1])
            velocity.append(case.parameter_value)
            beam_frequencies.append(case.beam_eigs)
            wing_tip_deflection.append(cga(alpha).dot(case.deflection[-1, 1:])[-1])

        velocity = np.array(velocity)
        order = np.argsort(velocity)
        wing_tip_deflection = np.array(wing_tip_deflection)[order]
        beam_frequencies = [beam_frequencies[i] for i in order]

        mode_data = []

        os.makedirs(output_folder + case_out_folder, exist_ok=True)

        for i_mode in range(0, 10, 2):
            mode_data.append(np.array([freq[i_mode, 1] for freq in beam_frequencies]))
            np.savetxt(output_folder + case_out_folder + '/mode_{:02g}.txt'.format(i_mode//2), np.column_stack((wing_tip_deflection, mode_data[i_mode//2])))
