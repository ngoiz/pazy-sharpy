import numpy as np
import os
import sys
import glob
sys.path.append('/home/ng213/pazy_code/sharpy-analysis-tools')

import linear.stability as stability

skin = True
if skin:
    case_name = 'skin_on'
else:
    case_name = 'skin_off'

case_name += 'te_mass'

# path_to_case = './output/pazy_um16N1Ms10_alpha0000_skin{:g}/pazi_uinf0010_alpha0000'.format(skin)
path_to_case = './output/te_mass_pazy_um16N1Ms10_alpha0000_skin{:g}/pazi_uinf0010_alpha0000'.format(skin)

output_folder = '/home/ng213/pazy_code/pazy-aepw3-results/05_StraightWingFlutter/{}/'.format(case_name)
os.makedirs(output_folder, exist_ok=True)

stab = stability.Stability(path_to_case + '/stability/')
stab.process(use_hz=True, wdmax=120 * 2 * np.pi)
stab.save_to_file(output_folder)

print('Saved eigenvalue data to {:s}'.format(output_folder))


