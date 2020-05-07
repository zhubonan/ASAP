#!/usr/bin/python3
import argparse
import os
import sys
import json

import numpy as np
from asaplib.data import ASAPXYZ
from asaplib.hypers import universal_soap_hyper


def main(fxyz, prefix):
    """

    Test if computing descriptors is working.

    Parameters
    ----------
    fxyz: string giving location of xyz file
    prefix: string giving the filename prefix
    """

    # read frames
    asapxyz = ASAPXYZ(fxyz)

    peratom = True
    tag = 'test'

    soap_js = {'soap1': {'type': 'SOAP',
                       'cutoff': 2.0, 
                      'n': 2, 'l': 2,
                      'atom_gaussian_width': 0.2, 
                      'rbf': 'gto', 'crossover': False}}

    k2_js = { 'lmbtr-k2': {'type': 'LMBTR_K2',
         'k2':{
        "geometry": {"function": "distance"},
        "grid": {"min": 0, "max": 2, "n": 10, "sigma": 0.1},
        "weighting": {"function": "exponential", "scale": 0.5, "cutoff": 1e-3}},
         'periodic': False,
         'normalization': "l2_each"}}

    kernel_js = {}
    kernel_js[1] = {'kernel_type': 'moment_sum',  
                              'zeta': 1,
                              'element_wise': False}
    kernel_js[2] = {'kernel_type': 'sum',  
                              'element_wise': True}

    desc_spec_js = {'test_soap':{'atomic_descriptor':  soap_js, 'kernel_function': kernel_js},
                   'test_k2':{'atomic_descriptor':  k2_js, 'kernel_function': kernel_js}}

    # compute the descripitors
    asapxyz.compute_global_descriptors(desc_spec_js, [], peratom, tag)

    asapxyz.write(prefix)
    asapxyz.save_descriptor_state(tag)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-fxyz', type=str, required=True, help='Location of xyz file')
    parser.add_argument('--prefix', type=str, default='ASAP', help='Filename prefix')
    args = parser.parse_args()
    main(args.fxyz, args.prefix)