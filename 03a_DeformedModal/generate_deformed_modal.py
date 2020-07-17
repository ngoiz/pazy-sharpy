import numpy as np
import os
import unittest
from pazy_wing_model import PazyWing
import sharpy.sharpy_main
import sharpy.utils.algebra as algebra


# Problem Set up
def generate_pazy(u_inf, case_name, output_folder='/output/', cases_subfolder='', **kwargs):
    # u_inf = 60
    alpha_deg = kwargs.get('alpha', 0.)
    rho = 1.225
    num_modes = 16
    gravity_on = kwargs.get('gravity_on', True)
    skin_on = kwargs.get('skin_on', False)

    # Lattice Discretisation
    M = kwargs.get('M', 4)
    N = kwargs.get('N', 32)
    M_star_fact = kwargs.get('Ms', 10)

    route_test_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    # SHARPy nonlinear reference solution
    case_route = route_test_dir + '/cases/' + cases_subfolder + '/' + case_name
    if not os.path.exists(case_route):
        os.makedirs(case_route)

    model_settings = {'skin_on': skin_on,
                      'discretisation_method': 'michigan',
                      'num_elem': 2,
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
             'Modal',
             'SaveParametricCase'
             ],
        'case': pazy.case_name, 'route': pazy.case_route,
        'write_screen': 'on', 'write_log': 'on',
        'save_settings': 'on',
        'log_folder': route_test_dir + output_folder + pazy.case_name + '/',
        'log_file': pazy.case_name + '.log'}

    pazy.config['BeamLoader'] = {
                                'unsteady': 'off',
                                'orientation': algebra.euler2quat([0, alpha_deg * np.pi/180, 0])}

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
        'horseshoe': 'on',
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
            'horseshoe': 'on',
            'num_cores': 4,
            'n_rollup': 0,
            'rollup_dt': dt,
            'rollup_aic_refresh': 1,
            'rollup_tolerance': 1e-4,
            'velocity_field_generator': 'SteadyVelocityField',
            'velocity_field_input': {
                'u_inf': u_inf,
                'u_inf_direction': u_inf_direction},
            'vortex_radius': 1e-9},
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

    pazy.config['WriteVariablesTime'] = {'folder': route_test_dir + output_folder,
                                       'structure_variables': ['pos'],
                                         'cleanup_old_solution': 'on',
                                       'structure_nodes': list(range(0, pazy.structure.n_node//2))}

    pazy.config['Modal'] = {'folder': route_test_dir + output_folder,
                            'NumLambda': 20,
                            'rigid_body_modes': 'off',
                            'print_matrices': 'on',
                            'keep_linear_matrices': 'off',
                            'write_dat': 'on',
                            'continuous_eigenvalues': 'off',
                            'write_modes_vtk': 'on',
                            'use_undamped_modes': 'on'}

    pazy.config['SaveParametricCase'] = {'folder': route_test_dir + output_folder + pazy.case_name + '/',
                                         'save_case': 'off',
                                         'parameters': {'u_inf': u_inf}}
    pazy.config.write()

    print('Running {}'.format(pazy.case_route + '/' + pazy.case_name + '.sharpy'))
    sharpy.sharpy_main.main(['', pazy.case_route + '/' + pazy.case_name + '.sharpy'])


if __name__ == '__main__':
    from datetime import datetime

    u_inf_vec = np.linspace(1, 60, 60)

    alpha = 7
    gravity_on = False
    skin_on = False

    M = 16
    N = 64
    Ms = 1

    batch_log = 'batch_log_alpha{:04g}'.format(alpha * 100)

    with open('./{:s}.txt'.format(batch_log), 'w') as f:
        # dd/mm/YY H:M:S
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f.write('SHARPy launch - START\n')
        f.write("date and time = %s\n\n" % dt_string)

    for i, u_inf in enumerate(u_inf_vec):
        print('RUNNING SHARPY %f\n' % u_inf)
        case_name = 'pazi_uinf{:04g}_alpha{:04g}'.format(u_inf * 10, alpha * 100)
        try:
            generate_pazy(u_inf, case_name,
                          output_folder='/output/pazy_um1{:g}N{:g}Ms{:g}_alpha{:04g}_skin{}/'.format(M, N, Ms,
                                                                                                     alpha * 100,
                                                                                                     skin_on),
                          cases_subfolder='/M{:g}N{:g}Ms{:g}/'.format(M, N, Ms),
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


