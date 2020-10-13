import numpy as np
import os
import unittest
import cases.templates.flying_wings as wings
import sharpy.sharpy_main

# Problem Set up
def generate_pazy(u_inf, case_name, output_folder='/output/', cases_folder='', **kwargs):
    # u_inf = 60
    alpha_deg = kwargs.get('alpha', 0.)
    rho = 1.225
    num_modes = 16
    gravity_on = kwargs.get('gravity_on', True)

    # Lattice Discretisation
    M = kwargs.get('M', 4)
    N = kwargs.get('N', 32)
    M_star_fact = kwargs.get('Ms', 10)

    # SHARPy nonlinear reference solution
    ws = wings.PazyControlSurface(M=M,
                                  N=N,
                                  Mstar_fact=M_star_fact,
                                  u_inf=u_inf,
                                  alpha=alpha_deg,
                                  cs_deflection=[0, 0],
                                  rho=rho,
                                  sweep=0,
                                  physical_time=2.0,
                                  n_surfaces=2,
                                  route=cases_folder + '/' + case_name,
                                  case_name=case_name)

    ws.gust_intensity = 0.01
    ws.sigma = 1

    ws.control_surface_type = np.array([2])

    ws.clean_test_files()
    ws.update_derived_params()
    ws.set_default_config_dict()

    ws.generate_aero_file()
    ws.generate_fem_file()

    ws.config['SHARPy'] = {
        'flow':
            ['BeamLoader',
             'AerogridLoader',
             # 'NonLinearStatic',
             'StaticUvlm',
             'AerogridPlot',
             'BeamPlot',
             'WriteVariablesTime',
             'DynamicCoupled',
             ],
        'case': ws.case_name, 'route': ws.route,
        'write_screen': 'on', 'write_log': 'on',
        'save_settings': 'on',
        'log_folder': output_folder + '/' + ws.case_name + '/',
        'log_file': ws.case_name + '.log'}

    ws.config['BeamLoader'] = {
        'unsteady': 'off',
        'orientation': ws.quat}

    ws.config['AerogridLoader'] = {
        'unsteady': 'off',
        'aligned_grid': 'on',
        'mstar': ws.Mstar_fact * ws.M,
        'freestream_dir': ws.u_inf_direction,
        'wake_shape_generator': 'StraightWake',
        'wake_shape_generator_input': {'u_inf': ws.u_inf,
                                       'u_inf_direction': ws.u_inf_direction,
                                       'dt': ws.dt}}

    ws.config['StaticUvlm'] = {
        'rho': ws.rho,
        'velocity_field_generator': 'SteadyVelocityField',
        'velocity_field_input': {
            'u_inf': ws.u_inf,
            'u_inf_direction': ws.u_inf_direction},
        'rollup_dt': ws.dt,
        'print_info': 'on',
        'horseshoe': 'off',
        'num_cores': 4,
        'n_rollup': 0,
        'rollup_aic_refresh': 0,
        'vortex_radius': 1e-10,
        'rollup_tolerance': 1e-4}

    settings = dict()
    settings['NonLinearStatic'] = {'print_info': 'off',
                                   'max_iterations': 200,
                                   'num_load_steps': 5,
                                   'delta_curved': 1e-6,
                                   'min_delta': 1e-8,
                                   'gravity_on': gravity_on,
                                   'gravity': 9.81}

    ws.config['StaticCoupled'] = {
        'print_info': 'on',
        'max_iter': 200,
        'n_load_steps': 4,
        'tolerance': 1e-5,
        'relaxation_factor': 0.1,
        'aero_solver': 'StaticUvlm',
        'aero_solver_settings': {
            'rho': ws.rho,
            'print_info': 'off',
            'horseshoe': 'off',
            'num_cores': 4,
            'n_rollup': 0,
            'rollup_dt': ws.dt,
            'rollup_aic_refresh': 1,
            'rollup_tolerance': 1e-4,
            'velocity_field_generator': 'SteadyVelocityField',
            'velocity_field_input': {
                'u_inf': ws.u_inf,
                'u_inf_direction': ws.u_inf_direction},
            'vortex_radius': 1e-10},
        'structural_solver': 'NonLinearStatic',
        'structural_solver_settings': settings['NonLinearStatic']}

    ws.config['AerogridPlot'] = {'folder': output_folder,
                                 'include_rbm': 'off',
                                 'include_applied_forces': 'on',
                                 'minus_m_star': 0}

    ws.config['AeroForcesCalculator'] = {'folder': output_folder,
                                         'write_text_file': 'on',
                                         'text_file_name': ws.case_name + '_aeroforces.csv',
                                         'screen_output': 'on',
                                         'unsteady': 'off'}

    ws.config['BeamPlot'] = {'folder': output_folder,
                             'include_rbm': 'off',
                             'include_applied_forces': 'on'}

    ws.config['BeamCsvOutput'] = {'folder': output_folder,
                                  'output_pos': 'on',
                                  'output_psi': 'on',
                                  'screen_output': 'on'}

    ws.config['WriteVariablesTime'] = {'folder': output_folder,
                                       'structure_variables': ['pos'],
                                       'structure_nodes': list(range(0, ws.num_node_surf)),
                                       'cleanup_old_solution': 'on'}

    settings = dict()
    settings['NonLinearDynamicPrescribedStep'] = {'print_info': 'on',
                                                  'max_iterations': 950,
                                                  'delta_curved': 1e-2,
                                                  'min_delta': 1e-5,
                                                  'newmark_damp': 5e-2,
                                                  'gravity_on': 'on',
                                                  'gravity': 9.81,
                                                  'num_steps': ws.n_tstep,
                                                  'dt': ws.dt}

    settings['StepUvlm'] = {'print_info': 'on',
                            'horseshoe': 'off',
                            'num_cores': 4,
                            'n_rollup': 100,
                            'convection_scheme': 3,
                            'rollup_dt': ws.dt,
                            'rollup_aic_refresh': 1,
                            'rollup_tolerance': 1e-4,
                            'velocity_field_generator': 'SteadyVelocityField',
                            'velocity_field_input': {'u_inf': ws.u_inf*1,
                                                     'u_inf_direction': [1., 0., 0.]},
                            'rho': ws.rho,
                            'n_time_steps': ws.n_tstep,
                            'vortex_radius': 1e-10,
                            'dt': ws.dt,
                            'gamma_dot_filtering': 3}

    settings['DynamicCoupled'] = {'print_info': 'on',
                                  'structural_substeps': 0,
                                  'dynamic_relaxation': 'on',
                                  'clean_up_previous_solution': 'on',
                                  'structural_solver': 'NonLinearDynamicPrescribedStep',
                                  'structural_solver_settings': settings['NonLinearDynamicPrescribedStep'],
                                  'aero_solver': 'StepUvlm',
                                  'aero_solver_settings': settings['StepUvlm'],
                                  'fsi_substeps': 200,
                                  'fsi_tolerance': 1e-6,
                                  'relaxation_factor': ws.relaxation_factor,
                                  'minimum_steps': 1,
                                  'relaxation_steps': 150,
                                  'final_relaxation_factor': 0.0,
                                  'n_time_steps': ws.n_tstep,
                                  'dt': ws.dt,
                                  'include_unsteady_force_contribution': 'on',
                                  'steps_without_unsteady_force': 2,
                                  'postprocessors': ['AerogridPlot', 'BeamPlot', 'WriteVariablesTime'],
                                  'postprocessors_settings': {'BeamLoads': {'folder': output_folder,
                                                                            'csv_output': 'off'},
                                                              'BeamPlot': {'folder': output_folder,
                                                                           'include_rbm': 'on',
                                                                           'include_applied_forces': 'on'},
                                                              'StallCheck': {},
                                                              'AerogridPlot': {
                                                                  'u_inf': ws.u_inf,
                                                                  'folder': output_folder,
                                                                  'include_rbm': 'on',
                                                                  'include_applied_forces': 'on',
                                                                  'minus_m_star': 0},
                                                              'WriteVariablesTime': {
                                                                  'folder': output_folder,
                                                                  'structure_variables': ['pos', 'psi'],
                                                                  'structure_nodes': [ws.num_node_surf - 1,
                                                                                      ws.num_node_surf,
                                                                                      ws.num_node_surf + 1]},
                                                              'UDPout': {'receiver_hostnames': ['127.0.0.1'],
                                                                         'receiver_port': [65430],
                                                                         'structure_variables': ['pos'],
                                                                         'structure_nodes': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
                                                              }}

    ws.config['DynamicCoupled'] = settings['DynamicCoupled']

    ws.config.write()

    sharpy.sharpy_main.main(['', ws.route + ws.case_name + '.sharpy'])

if __name__== '__main__':
    from datetime import datetime

    u_inf_vec = [73]

    alpha = 4
    gravity_on = True

    M = 8
    N = 128
    Ms = 8

    batch_log = 'batch_log_alpha{:04g}'.format(alpha*100)

    with open('./{:s}.txt'.format(batch_log), 'w') as f:
        # dd/mm/YY H:M:S
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write('SHARPy launch - START\n')
        f.write("date and time = %s\n\n" % dt_string)

    for i, u_inf in enumerate(u_inf_vec):
        print('RUNNING SHARPY %f\n' % u_inf)
        case_name = 'pazy_uinf{:04g}_alpha{:04g}'.format(u_inf*10, alpha*100)
        try:
            generate_pazy(u_inf, case_name, output_folder='./output/OpenLoop_wake3_M{:g}N{:g}Ms{:g}_alpha{:04g}/'.format(M, N, Ms, alpha*100),
                          cases_folder='./cases/M{:g}N{:g}Ms{:g}wake3/'.format(M, N, Ms),
                          M=M, N=N, Ms=Ms, alpha=alpha,
                          gravity_on=gravity_on)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open('./{:s}.txt'.format(batch_log), 'a') as f:
                f.write('%s Ran case %i :::: u_inf = %f\n\n' % (dt_string, i, u_inf))
        except AssertionError:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open('./{:s}.txt'.format(batch_log), 'a') as f:
                f.write('%s ERROR RUNNING case %f\n\n' % (dt_string, u_inf))
