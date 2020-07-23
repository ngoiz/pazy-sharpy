import numpy as np
import sys
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import linear.stability as stability
import os


def prepare_cases_db(sharpy_output_folder, source_cases, param_vec):
    cases_db = []

    for ith, src_path in enumerate(source_cases):
        res = Actual(sharpy_output_folder + src_path + '/*')
        res.case_parameter = param_vec[ith]
        res.systems = ['aeroelastic']
        res.load_bulk_cases('eigs', 'deflection')
        cases_db.append(res)

    return cases_db

def deflection_at_flutter(case, speed, deflection_list):
    case_im = case.aeroelastic.find_parameter_value(int(speed), return_idx=True)
    deflection_im = deflection_list[case_im][-1] / 0.55
    case_ip = case.aeroelastic.find_parameter_value(int(speed + 1), return_idx=True)
    deflection_ip = deflection_list[case_ip][-1] / 0.55
    d = np.interp(speed, [int(speed), int(speed + 1)], [deflection_im, deflection_ip])
    return d

# write eigenvalues:
def save_eigenvalues(case):
    vel, eigs = case.eigs('aeroelastic')
    dest_file = output_folder + '/velocity_eigenvalues_alpha{:04g}.txt'.format(case.case_parameter * 100)
    np.savetxt(dest_file, np.column_stack((vel, eigs)))
    print('Saved velocity/eigs array to {}'.format(dest_file))

    v, damp, fn = stability.modes(vel, eigs, use_hz=True, wdmax=50*2*np.pi)
    np.savetxt(output_folder + 'velocity_damping_frequency_alpha{:04g}.txt'.format(case.case_parameter * 100),
               np.column_stack((v, damp, fn)))

    vel, deflection = case.wing_tip_deflection(frame='g', alpha=case.case_parameter)
    np.savetxt(output_folder + '/velocity_wingtip_deflection_g_alpha{:04g}.txt'.format(case.case_parameter * 100),
               np.column_stack((vel, deflection)))

    flutter_speeds = stability.find_flutter_speed(v, damp)
    deflection_flutter = []
    for ith, speed in enumerate(flutter_speeds):
        deflection_flutter.append(deflection_at_flutter(case, speed, deflection))
    np.savetxt(output_folder + '/flutter_speeds_alpha{:04g}.txt'.format(case.case_parameter * 100),
               np.column_stack((flutter_speeds, deflection_flutter)))


skin = False
alpha_vec = np.array([0.5, 1, 2, 3])
sharpy_output_folder = './output/'
output_folder = '../../pazy-aepw3-results/06_DeformedWingFlutter/' # place to save results

if skin:
    skin_str = 'skin_on'
else:
    skin_str = 'skin_off'

output_folder += 'sharpy_{}/'.format(skin_str)
os.makedirs(output_folder, exist_ok=True)

flutter_case_name = 'deformed_flutter_{}'.format(skin)

source_cases = ['pazy_M16N1Ms20_alpha{:04g}_skin{:g}'.format(alpha * 100, skin) for alpha in alpha_vec]

results = prepare_cases_db(sharpy_output_folder, source_cases, alpha_vec)

for case in results:
    save_eigenvalues(case)

