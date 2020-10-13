import numpy as np
import os
import sharpy.sharpy_main
from pazy_wing_model import PazyWing
import sharpy.utils.algebra as algebra


def generate_pazy(u_inf, case_name, output_folder='/output/', cases_subfolder='', **kwargs):
    # u_inf = 60
    alpha_deg = kwargs.get('alpha', 0.)
    rho = 1.225
    num_modes = 10
    gravity_on = kwargs.get('gravity_on', True)
    skin_on = kwargs.get('skin_on', False)

    # Lattice Discretisation
    M = kwargs.get('M', 4)
    N = kwargs.get('N', 32)
    M_star_fact = kwargs.get('Ms', 10)

    # SHARPy nonlinear reference solution
    route_test_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    case_route = route_test_dir + '/cases/' + cases_subfolder + '/' + case_name
    if not os.path.exists(case_route):
        os.makedirs(case_route)

    model_settings = {'skin_on': skin_on,
                      'discretisation_method': 'michigan',
                      'num_elem': N,
                      'surface_m': M,
                      'num_surfaces': 2}

    pazy = PazyWing(case_name=case_name, case_route=case_route, in_settings=model_settings)

    pazy.create_aeroelastic_model()
    pazy.save_files()

    u_inf_direction = np.array([1., 0., 0.])
    dt = pazy.aero.main_chord / M / u_inf

    pazy.config['SHARPy'] = {
        'flow':
            ['BeamLoader',
            'AerogridLoader',
             'StaticCoupled',
             'AerogridPlot',
             'BeamPlot',
             'WriteVariablesTime',
             'DynamicCoupled',
             'Modal',
             'LinearAssembler',
             'FrequencyResponse',
             'AsymptoticStability',
             'SaveParametricCase',
             ],
        'case': pazy.case_name, 'route': pazy.case_route,
        'write_screen': 'on', 'write_log': 'on',
        'log_folder': route_test_dir + output_folder + pazy.case_name + '/',
        'log_file': pazy.case_name + '.log'}

    pazy.config['BeamLoader'] = {
        'unsteady': 'off',
        'orientation': algebra.euler2quat([0., alpha_deg * np.pi / 180, 0])}

    pazy.config['AerogridLoader'] = {
        'unsteady': 'off',
        'aligned_grid': 'on',
        'mstar': M_star_fact * M,
        'freestream_dir': u_inf_direction,
        'wake_shape_generator': 'StraightWake',
        'wake_shape_generator_input': {'u_inf': u_inf,
                                       'u_inf_direction': u_inf_direction,
                                       'dt': dt}}

    pazy.config['StaticUvlm'] = {
        'rho': rho,
        'velocity_field_generator': 'SteadyVelocityField',
        'velocity_field_input': {
            'u_inf': u_inf,
            'u_inf_direction': u_inf_direction},
        'rollup_dt': dt,
        'print_info': 'on',
        'horseshoe': 'off',
        'num_cores': 4,
        'n_rollup': 0,
        'rollup_aic_refresh': 0,
        'rollup_tolerance': 1e-4}

    settings = dict()
    settings['NonLinearStatic'] = {'print_info': 'off',
                                   'max_iterations': 200,
                                   'num_load_steps': 5,
                                   'delta_curved': 1e-6,
                                   'min_delta': 1e-8,
                                   'gravity_on': gravity_on,
                                   'gravity': 9.81}

    pazy.config['StaticCoupled'] = {
        'print_info': 'on',
        'max_iter': 200,
        'n_load_steps': 4,
        'tolerance': 1e-5,
        'relaxation_factor': 0.1,
        'aero_solver': 'StaticUvlm',
        'aero_solver_settings': {
            'rho': rho,
            'print_info': 'off',
            'horseshoe': 'off',
            'num_cores': 4,
            'n_rollup': 0,
            'rollup_dt': dt,
            'rollup_aic_refresh': 1,
            'rollup_tolerance': 1e-4,
            'vortex_radius': 1e-10,
            'velocity_field_generator': 'SteadyVelocityField',
            'velocity_field_input': {
                'u_inf': u_inf,
                'u_inf_direction': u_inf_direction}},
        'structural_solver': 'NonLinearStatic',
        'structural_solver_settings': settings['NonLinearStatic']}

    pazy.config['AerogridPlot'] = {'folder': route_test_dir + output_folder,
                                 'include_rbm': 'off',
                                 'include_applied_forces': 'on',
                                 'minus_m_star': 0}

    pazy.config['AeroForcesCalculator'] = {'folder': route_test_dir + '/{:s}/forces'.format(output_folder),
                                         'write_text_file': 'on',
                                         'text_file_name': pazy.case_name + '_aeroforces.csv',
                                         'screen_output': 'on',
                                         'unsteady': 'off'}

    pazy.config['BeamPlot'] = {'folder': route_test_dir + output_folder,
                             'include_rbm': 'off',
                             'include_applied_forces': 'on'}

    pazy.config['BeamCsvOutput'] = {'folder': route_test_dir + output_folder,
                                  'output_pos': 'on',
                                  'output_psi': 'on',
                                  'screen_output': 'on'}

    pazy.config['WriteVariablesTime'] = {'folder': route_test_dir + output_folder,
                                        'structure_variables': ['pos'],
                                        'structure_nodes': list(range(0, pazy.structure.n_node//2))}

    pazy.config['Modal'] = {'folder': route_test_dir + output_folder,
                            'NumLambda': 20,
                            'rigid_body_modes': 'off',
                            'print_matrices': 'off',
                            'keep_linear_matrices': 'on',
                            'write_dat': 'on',
                            'continuous_eigenvalues': 'off',
                            'write_modes_vtk': 'on',
                            'use_undamped_modes': 'on'}

    pazy.config['LinearAssembler'] = {'linear_system': 'LinearAeroelastic',
                                      # 'modal_tstep': 0,
                                      'linear_system_settings': {
                                          'beam_settings': {'modal_projection': 'on',
                                                            'inout_coords': 'modes',
                                                            'discrete_time': 'on',
                                                            'newmark_damp': 0.5e-4,
                                                            'discr_method': 'newmark',
                                                            'dt': dt,
                                                            'proj_modes': 'undamped',
                                                            'use_euler': 'off',
                                                            'num_modes': num_modes,
                                                            'print_info': 'off',
                                                            'gravity': gravity_on,
                                                            'remove_sym_modes': 'on',
                                                            'remove_dofs': []},
                                          'aero_settings': {'dt': dt,
#                                                             'ScalingDict': {'length': 0.5 * pazy.aero.main_chord,
#                                                                             'speed': u_inf,
#                                                                             'density': rho},
                                                            'integr_order': 2,
                                                            'density': rho,
                                                            'remove_predictor': 'off',
                                                            'use_sparse': 'on',
                                                            'rigid_body_motion': 'off',
                                                            'use_euler': 'off',
                                                            'remove_inputs': ['u_gust'],
                                                            'vortex_radius': 1e-10,
                                                            'rom_method': ['Krylov'],
                                                            'rom_method_settings':
                                                                {'Krylov':
                                                                     {'frequency': [0.],
                                                                      'algorithm': 'mimo_rational_arnoldi',
                                                                      'r': 6,
                                                                      'single_side': 'observability',
                                                                      }
                                                                 }
                                                            },
                                          'rigid_body_motion': False}
                                      }

    pazy.config['AsymptoticStability'] = {'print_info': True,
                                        'folder': route_test_dir + output_folder,
                                        'export_eigenvalues': 'on',
                                        'target_system': ['aeroelastic', 'aerodynamic', 'structural'],
                                        # 'velocity_analysis': [160, 180, 20]}
                                        }

    pazy.config['FrequencyResponse'] = {'print_info': 'on',
                                        'folder': route_test_dir + output_folder,
                                        'target_system': ['aeroelastic', 'aerodynamic', 'structural'],
                                        'quick_plot': 'off',
                                        'frequency_unit': 'k',
                                        'frequency_bounds': [1e-3, 0.1],
                                        'frequency_scaling': {'length': 0.5 * pazy.aero.main_chord,
                                                              'speed': u_inf}}

    pazy.config['SaveParametricCase'] = {'folder': route_test_dir + output_folder + pazy.case_name + '/',
                                       'save_case': 'off',
                                       'parameters': {'u_inf': u_inf}}

    settings = dict()
    settings['NonLinearDynamicPrescribedStep'] = {'print_info': 'on',
                                                  'max_iterations': 950,
                                                  'delta_curved': 1e-6,
                                                  'min_delta': 1e-8,
                                                  'newmark_damp': 5e-4,
                                                  'gravity_on': 'on',
                                                  'gravity': 9.81,
                                                  'num_steps': 1,
                                                  'dt': dt}
    
    settings['StepUvlm'] = {'print_info': 'on',
                            'horseshoe': 'off',
                            'num_cores': 4,
                            'n_rollup': 100,
                            'convection_scheme': 2,
                            'rollup_dt': dt,
                            'rollup_aic_refresh': 1,
                            'rollup_tolerance': 1e-4,
                            'velocity_field_generator': 'SteadyVelocityField',
                            'velocity_field_input': {'u_inf': u_inf,
                                                     'u_inf_direction': [1., 0., 0.]},
                            'rho': rho,
                            'n_time_steps': 1,
                            'dt': dt,
                            'gamma_dot_filtering': 3,
                            'vortex_radius': 1e-10}

    settings['DynamicCoupled'] = {'print_info': 'on',
                                  'structural_substeps': 10,
                                  'dynamic_relaxation': 'on',
                                  'clean_up_previous_solution': 'on',
                                  'structural_solver': 'NonLinearDynamicPrescribedStep',
                                  'structural_solver_settings': settings['NonLinearDynamicPrescribedStep'],
                                  'aero_solver': 'StepUvlm',
                                  'aero_solver_settings': settings['StepUvlm'],
                                  'fsi_substeps': 200,
                                  'fsi_tolerance': 1e-6,
                                  'relaxation_factor': 0.2,
                                  'minimum_steps': 1,
                                  'relaxation_steps': 150,
                                  'final_relaxation_factor': 0.0,
                                  'n_time_steps': 1,
                                  'dt': dt,
                                  'include_unsteady_force_contribution': 'off',
                                  'postprocessors': [],
                                  'postprocessors_settings': {'BeamLoads': {'folder': route_test_dir + output_folder,
                                                                            'csv_output': 'off'},
                                                              'BeamPlot': {'folder': route_test_dir + output_folder,
                                                                           'include_rbm': 'on',
                                                                           'include_applied_forces': 'on'},
                                                              'StallCheck': {},
                                                              'AerogridPlot': {
                                                                  'u_inf': u_inf,
                                                                  'folder': route_test_dir + output_folder,
                                                                  'include_rbm': 'on',
                                                                  'include_applied_forces': 'on',
                                                                  'minus_m_star': 0},
                                                            }}
    
    pazy.config['DynamicCoupled'] = settings['DynamicCoupled']
    pazy.config.write()

    sharpy.sharpy_main.main(['', pazy.case_route + '/' + pazy.case_name + '.sharpy'])


if __name__== '__main__':
    from datetime import datetime
    # u_inf_vec = np.linspace(10, 90, 81)

    u_inf_vec = np.linspace(30, 60, 7)
    alpha = 5.0
    gravity_on = False
    skin_on = True

    M = 16
    N = 1
    Ms = 16
    # M = 6
    # N = 1
    # Ms = 5

    batch_log = 'batch_log_alpha{:04g}'.format(alpha*100)

    with open('./{:s}.txt'.format(batch_log), 'w') as f:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write('SHARPy launch - START\n')
        f.write("date and time = %s\n\n" % dt_string)

    for i, u_inf in enumerate(u_inf_vec):
        print('RUNNING SHARPY %f %f\n' % (alpha, u_inf))
        case_name = 'pazy_uinf{:04g}_alpha{:04g}'.format(u_inf*10, alpha*100)
        try:
            generate_pazy(u_inf, case_name, output_folder='/output/test_pazy_M{:g}N{:g}Ms{:g}_alpha{:04g}_skin{:g}/'.format(M, N, Ms, alpha*100, skin_on),
                          cases_subfolder='/test_M{:g}N{:g}Ms{:g}_skin{:g}/'.format(M, N, Ms, skin_on),
                          M=M, N=N, Ms=Ms, alpha=alpha,
                          gravity_on=gravity_on,
                          skin_on=skin_on)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open('./{:s}.txt'.format(batch_log), 'a') as f:
                f.write('%s Ran case %i :::: u_inf = %f\n\n' % (dt_string, i, u_inf))
        except AssertionError:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open('./{:s}.txt'.format(batch_log), 'a') as f:
                f.write('%s ERROR RUNNING case %f\n\n' % (dt_string, u_inf))


