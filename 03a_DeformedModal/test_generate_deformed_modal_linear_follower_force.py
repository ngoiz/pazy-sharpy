from pazy_wing_model import PazyWing
import numpy as np
import configobj
import os


def run_coupled_bending_simulation(case_id, tip_load, skin_on, case_root='./cases/', output_folder='./output/'):
    # uses a dummy StaticCoupled solution in order to use the num_load_steps feature which has no effect
    # on gravity forces in NonlinearStatic

    # pazy structural settings
    pazy_settings = {'skin_on': skin_on,
                     'discretisation_method': 'michigan',
                     'num_elem': 2,
                     'surface_m': 1}
    case_name = 'pazy_bending_{}'.format(case_id)
    case_route = case_root + '/' + case_name + '/'

    num_modes = 10
    dt = 0.1 / 4 / 10000

    if not os.path.isdir(case_route):
        os.makedirs(case_route, exist_ok=True)

    pazy = PazyWing(case_name, case_route, pazy_settings)
    pazy.generate_structure()
    switch_for = False
    pazy.structure.mirror_wing(switch_for=switch_for)
    pazy.generate_aero()

    # Lumped mass
    mid_chord_b = (pazy.get_ea_reference_line() - 0.5) * 0.1

    pazy.structure.app_forces[pazy.structure.n_node // 2, 2] = tip_load
    if switch_for:
        pazy.structure.app_forces[-1, 2] = tip_load
    else:
        pazy.structure.app_forces[pazy.structure.n_node // 2 + 1, 2] = tip_load
    # mt = 1e-3
    # cg =
    # pazy.structure.add_lumped_mass([(mt, pazy.structure.n_node//2, np.zeros((3, 3), cg)),
    #                                 (mt, pazy.structure.n_node//2 + 1)])
    pazy.save_files()

    # simulation settings
    config = configobj.ConfigObj()
    config.filename = case_route + '/{}.sharpy'.format(case_name)
    settings = dict()

    settings['SHARPy'] = {
        'flow': ['BeamLoader',
                 'AerogridLoader',
                 # 'Modal',
                 'StaticCoupled',
                 'BeamPlot',
                 'WriteVariablesTime',
                 'AerogridPlot',
                 'Modal',
                 'LinearAssembler',
                 'AsymptoticStability',
                 'SaveParametricCase'
                 ],
        'case': case_name, 'route': case_route,
        'write_screen': 'on', 'write_log': 'on',
        'log_folder': output_folder + '/' + case_name + '/',
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
                                   # 'num_steps': 10,
                                   # 'dt': 2.5e-4,
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
        'aero_solver': 'StaticUvlm',
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
                                                            'remove_sym_modes': 'on',
                                                            'remove_dofs': []},
                                          'rigid_body_motion': False}


    settings['AsymptoticStability'] = {'print_info': True,
                                          'folder': output_folder,
                                          'export_eigenvalues': 'on',
                                          'target_system': ['aeroelastic', 'structural'],
                                          # 'velocity_analysis': [160, 180, 20]}
                                          }
    settings['SaveParametricCase'] = {'folder': output_folder + pazy.case_name + '/',
                                      'save_case': 'off',
                                      'parameters': {'mass': tip_load}}
    for k, v in settings.items():
        config[k] = v

    config.write()

    import sharpy.sharpy_main

    sharpy.sharpy_main.main(['', case_route + case_name + '.sharpy'])


if __name__ == '__main__':
    tip_load = np.linspace(0, 30, 25)  # Newtons
    # tip_load = [30]
    for skin in ['on', 'off']:

        for case_id in range(len(tip_load)):
            print('Running case {}, {}, tip_load {} N'.format(case_id, skin, tip_load[case_id]))
            run_coupled_bending_simulation(case_id, tip_load[case_id], skin_on=skin,
                                           case_root='./cases/test_followerforce_LB_FF_skin_{}/'.format(skin),
                                           output_folder='./output/test_followerforce_LB_FF_skin_{}/'.format(skin))
