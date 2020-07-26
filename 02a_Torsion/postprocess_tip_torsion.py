import sys
import os
sys.path.append('../lib/sharpy-analysis-tools/')
from batch.sets import Actual
import numpy as np
import sharpy.utils.algebra as algebra


def process_bending_results(path_to_folder, N, tip_load_vec, ref_b, file_name='/pazy_bending_{}/'):
    deflection_list = []
    for i in range(len(tip_load_vec)):
        variables_output_directory = path_to_folder + file_name.format(i) + '/WriteVariablesTime/'
        deflection = np.zeros((N, 3))
        crv = np.zeros((N, 3))
        for i_node in range(N):
            node_deflection_file = variables_output_directory + '/struct_pos_node{:g}.dat'.format(i_node)
            node_crv_file = variables_output_directory + '/struct_psi_node{:g}.dat'.format(i_node)
            try:
                deflection[i_node, :] = np.loadtxt(node_deflection_file)[1:]
                crv[i_node, :] = np.loadtxt(node_crv_file)[1:]
                deflection[i_node, :] += algebra.crv2rotation(crv[i_node, :]).dot(ref_b)
                end_of_iter = False
            except OSError:
                print(i, i_node)
                end_of_iter = True
                break
        if end_of_iter:
            break
        else:
            deflection_list.append(deflection)

    return deflection_list