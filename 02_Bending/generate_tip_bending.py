from pazy_wing_model import PazyWing
import numpy as np
import configobj
import os


def run_bending_simulation(case_id, tip_load, skin_on, case_root='./cases/', output_folder='./output/'):
    # pazy structural settings
    pazy_settings = {'skin_on': skin_on,
                     'discretisation_method': 'michigan',
                     'num_elem': 2}
    case_name = 'pazy_bending_{}'.format(case_id)
    # case_route = './cases/' + case_name + '/'
    case_route = case_root + '/' + case_name + '/'

    if not os.path.isdir(case_route):
        os.makedirs(case_route, exist_ok=True)

    # output_folder = './output/'

    pazy = PazyWing(case_name, case_route, pazy_settings)
    pazy.generate_structure()

    # Lumped mass
    pazy.structure.add_lumped_mass((tip_load/2, pazy.structure.n_node - 1))
    pazy.structure.add_lumped_mass((tip_load/2, pazy.structure.n_node - 2))

    pazy.save_files()

    # simulation settings
    config = configobj.ConfigObj()
    config.filename = case_route + '/{}.sharpy'.format(case_name)
    settings = dict()

    settings['SHARPy'] = {
        'flow': ['BeamLoader',
                 'NonLinearStatic',
                 'BeamPlot',
                 'WriteVariablesTime',
                 ],
        'case': case_name, 'route': case_route,
        'write_screen': 'off', 'write_log': 'on',
        'log_folder': output_folder + '/' + case_name + '/',
        'log_file': case_name + '.log'}

    settings['BeamLoader'] = {'unsteady': 'off'}

    settings['NonLinearStatic'] = {'print_info': 'off',
                                   'max_iterations': 350,
                                   'num_load_steps': 10,
                                   # 'num_steps': 10,
                                   # 'dt': 2.5e-4,
                                   'delta_curved': 1e-1,
                                   'min_delta': 1e-6,
                                   'gravity_on': 'on',
                                   'relaxation_factor': 0.1,
                                   'gravity': 9.81}

    settings['BeamPlot'] = {'folder': output_folder}

    settings['WriteVariablesTime'] = {'folder': output_folder,
                                       'structure_variables': ['pos'],
                                       'structure_nodes': list(range(0, pazy.structure.n_node)),
                                       'cleanup_old_solution': 'on'}

    for k, v in settings.items():
        config[k] = v

    config.write()

    import sharpy.sharpy_main

    sharpy.sharpy_main.main(['', case_route + case_name + '.sharpy'])


if __name__ == '__main__':

    tip_load = np.linspace(0, 3, 20)
    skin = 'off'

    for case_id in range(len(tip_load)):
        print('running {}, tip_load {}'.format(case_id, tip_load[case_id]))
        run_bending_simulation(case_id, tip_load[case_id], skin_on=skin,
                               case_root='./cases/skin_{}/'.format(skin),
                               output_folder='./output/skin_{}/'.format(skin))
    #
    # run_bending_simulation(99, 2, 'off', './cases/tests/', './output/tests/')