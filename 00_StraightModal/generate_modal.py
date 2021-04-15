from pazy_wing_model import PazyWing
import numpy as np
import configobj
import os


def run_modal_simulation(case_id, skin_on, case_root='./cases/', output_folder='./output/'):

    # pazy structural settings
    pazy_settings = {'skin_on': skin_on,
                     'model_id': 'pazy',
                     'discretisation_method': 'michigan',
                     'num_elem': 3,
                     'surface_m': 1}
    case_name = 'pazy_modal'.format(case_id)
    case_route = case_root + '/' + case_name + '/'

    num_modes = 40
    dt = 0.1 / 4 / 10000

    if not os.path.isdir(case_route):
        os.makedirs(case_route, exist_ok=True)

    pazy = PazyWing(case_name, case_route, pazy_settings)
    pazy.generate_structure()
    pazy.structure.mirror_wing()

    pazy.save_files()

    # simulation settings
    config = configobj.ConfigObj()
    config.filename = case_route + '/{}.sharpy'.format(case_name)
    settings = dict()

    settings['SHARPy'] = {
        'flow': ['BeamLoader',
                 'Modal'
                 ],
        'case': case_name, 'route': case_route,
        'write_screen': 'on', 'write_log': 'on',
        'log_folder': output_folder + '/',
        'log_file': case_name + '.log'}

    settings['BeamLoader'] = {'unsteady': 'off'}

    settings['AerogridLoader'] = {
        'unsteady': 'off',
        'aligned_grid': 'on',
        'mstar': 1,
        'wake_shape_generator': 'StraightWake',
        'wake_shape_generator_input': {'u_inf': 100,
                                       'dt': dt}}

    settings['NonLinearStatic'] = {'print_info': 'off',
                                   'max_iterations': 900,
                                   'num_load_steps': 10,
                                   'delta_curved': 1e-5,
                                   'min_delta': 1e-6,
                                   'gravity_on': 'off',
                                   'relaxation_factor': 0.,
                                   'gravity': 9.81}

    settings['StaticCoupled'] = {
        'print_info': 'on',
        'max_iter': 200,
        'n_load_steps': 4,
        'tolerance': 1e-5,
        'relaxation_factor': 0.1,
        'aero_solver': 'NoAero',
        'aero_solver_settings': {
            'rho': 1e-8,
            'print_info': 'off',
            'horseshoe': 'on',
            'num_cores': 4,
            'n_rollup': 0,
            'rollup_dt': 0.1,
            'rollup_aic_refresh': 1,
            'rollup_tolerance': 1e-4,
            'velocity_field_generator': 'SteadyVelocityField',
            'velocity_field_input': {
                'u_inf': 1,
                'u_inf_direction': [1.0, 0., 0.]},
            'vortex_radius': 1e-10
        },
        'structural_solver': 'NonLinearStatic',
        'structural_solver_settings': settings['NonLinearStatic']}

    settings['BeamPlot'] = {'folder': output_folder}

    settings['WriteVariablesTime'] = {'folder': output_folder,
                                      'structure_variables': ['pos', 'psi'],
                                      'structure_nodes': list(range(0, pazy.structure.n_node)),
                                      'cleanup_old_solution': 'on'}

    settings['AerogridPlot'] = {'folder': output_folder,
                                'include_rbm': 'off',
                                'include_applied_forces': 'on',
                                'minus_m_star': 0}

    settings['Modal'] = {'folder': output_folder,
                         'NumLambda': num_modes,
                         'rigid_body_modes': 'off',
                         'print_matrices': 'off',
                         'keep_linear_matrices': 'on',
                         'write_dat': 'on',
                         'continuous_eigenvalues': 'off',
                         'write_modes_vtk': 'on',
                         'use_undamped_modes': 'on'}

    settings['LinearAssembler'] = {'linear_system': 'LinearBeam',
                                   'linear_system_settings': {'modal_projection': 'on',
                                                              'inout_coords': 'modes',
                                                              'discrete_time': 'on',
                                                              'newmark_damp': 0.5e-6,
                                                              'discr_method': 'newmark',
                                                              'dt': dt,
                                                              'proj_modes': 'undamped',
                                                              'use_euler': 'off',
                                                              'num_modes': num_modes,
                                                              'print_info': 'off',
                                                              'gravity': 'off',
                                                              'remove_sym_modes': 'on'}
                                   }

    settings['AsymptoticStability'] = {'print_info': 'on',
                                       'folder': output_folder,
                                       'export_eigenvalues': 'on',
                                       'target_system': ['aeroelastic', 'structural'],
                                       }

    for k, v in settings.items():
        config[k] = v

    config.write()

    import sharpy.sharpy_main

    sharpy.sharpy_main.main(['', case_route + case_name + '.sharpy'])


if __name__ == '__main__':
    for skin in ['on', 'off']:
        print('Running case {}, {}'.format(0, skin))
        run_modal_simulation(0, skin_on=skin,
                                       case_root='./cases/pazy/'.format(skin),
                                       output_folder='./output/pazy/'.format(skin))
