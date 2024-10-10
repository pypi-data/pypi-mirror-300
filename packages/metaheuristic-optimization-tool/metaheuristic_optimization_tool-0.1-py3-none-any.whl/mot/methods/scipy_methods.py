import scipy.optimize as opt
from .method import Method
from math import floor

# from tabulate import tabulate
import matplotlib.pyplot as plt
import multiprocessing as mp
from functools import partial
import signal
import numpy as np
import sys
import os

import uuid

class scipy_optimize(Method):
    name = "Scipy optimization"

    def __init__(self):
        Method.__init__(self)

    def search(self, Perturber, Fitter, algorithm='differntial_evolution', maxiter=100, record=True,
               report=True, plot_parameters=False, store=False):
        self.Fitter = Fitter
        self.file_name = algorithm+'.csv'
        self.Perturber = Perturber

        self.uniq_id = str(uuid.uuid4())
        f = open(self.file_name, 'w')
        try:
            metric_list = [x.name for x in self.Fitter.function]
        except:
            metric_list = list(range(len(self.Fitter.function)))

        input_list = Perturber.v_label
        self.iter_n = 0
        column_header = ['Iteration'] + list(input_list) + list(metric_list) + ['fitness']
        f.write(','.join(column_header))
        f.write('\n')
        f.close()

        Nproc = mp.cpu_count()
        pool = mp.Pool(processes=Nproc)
        Fitter.normalize_weight()

        input_dict = {}
        for indx, val in enumerate(Perturber.v_label):
            input_dict[val] = {'unit': Perturber.v_unit[indx],
                               'min': Perturber.v_min[indx],
                               'max': Perturber.v_max[indx],
                               'step': Perturber.v_step[indx],
                               'integer': Perturber.integer[indx]}
        initial_guess = []
        bounds = []
        for key, val in input_dict.items():
            initial_guess.append((val['min'] + val['max']) / 2)
            bounds.append((val['min'], val['max']))

        # get constraint functions
        cons_list = []
        cons_dict_list = []
        for indx, val in enumerate(input_list):
            min_fcn = lambda x : x[indx]-Perturber.v_min[indx]
            max_fcn = lambda x : Perturber.v_max[indx] - x[indx]
            # min constraint function
            cons_list.append(min_fcn)
            cons_list.append(max_fcn)

            cons_dict_list.append({'type': 'ineq', 'fun': min_fcn})
            cons_dict_list.append({'type': 'ineq', 'fun': max_fcn})



        algorithms = ['fmin_slsqp', 'differential_evolution',
                      'basinhopping', 'brute', 'fmin_cobyla']

        if algorithm not in algorithms:
            print('Parameter algorithm has to be one of these:\n')
            print(algorithms)
            raise ValueError()
        if algorithm == 'fmin_slsqp':
            opt.fmin_slsqp(self.obj_fcn, initial_guess, bounds=bounds)
            return
        elif algorithm == 'differential_evolution':
            opt.differential_evolution(self.obj_fcn, bounds, maxiter=maxiter, atol=1e-4)
            return
        elif algorithm == 'basinhopping':
            opt.basinhopping(self.obj_fcn, initial_guess, niter=maxiter,
                             minimizer_kwargs={'constraints': cons_dict_list})
            return
        elif algorithm == 'brute':
            opt.brute(self.obj_fcn, ranges=bounds, Ns=maxiter)
        elif algorithm == 'fmin_cobyla':
            opt.fmin_cobyla(self.obj_fcn, initial_guess, cons=cons_list)
        else:
            print('SOMETHING IS WRONG!! ')
            raise ValueError()


    def obj_fcn(self, x):
        
        # run simulation
        for sim in self.Fitter.simulation:
            sim(x, self.uniq_id)

        score_list, fit = self.get_fit()
        
        # since the optimization functions require positive values
        # and they seek for minimum values
        obj = len(score_list) - fit
        print('\n')
        print('x:', x)
        print('score_list:', score_list)
        print('fit:', fit)
        print('ultimate_obj_score:', obj)
        print('\n')
        score_list = [str(score) for score in score_list]
        self.iter_n += 1
        row = [self.iter_n] + list(x) + list(score_list) + [obj]
        row = [str(val) for val in row] 
        with open(self.file_name, 'a') as f:
            f.write(','.join(row))
            f.write('\n')
        
        return obj


    def get_fit(self):
        # get metrics
        score_list = []
        fit = 0.0
        vio_hard = 0.0
        vio_penalty = 0.0

        # for every score, sum up the fitness
        for indx, val in enumerate(self.Fitter.function):
            score = val(self.uniq_id)
            score_list.append(score)
            if score >= self.Fitter.limit_max[indx]:
                if self.Fitter.limit_hard[indx]:
                    vio_hard -= self.violate_max(score, indx)
                else:
                    vio_penalty -= self.violate_max(score, indx)
            elif score <= self.Fitter.limit_min[indx]:
                if self.Fitter.limit_hard[indx]:
                    vio_hard -= self.violate_min(score, indx)
                else:
                    vio_penalty -= self.violate_min(score, indx)

            # compute fitness
            fit_add = (score - self.Fitter.norm_min[indx]) * self.Fitter.weight[indx] / (self.Fitter.norm_step[indx]) 
            fit += fit_add

        if vio_hard != 0.0: return score_list,vio_hard
        elif vio_penalty != 0.0:
            print('violated penalty\n')
            return score_list,fit*(1.0+vio_penalty/2)

        self.uniq_id = str(uuid.uuid4())
        return score_list, fit


    def violate_max(self, score, indx):
        # calculates how much 
        return ((score - self.Fitter.limit_max[i] / (self.Fitter.norm_max[indx] - self.Fitter.limit_max[i])))

    def violate_min(self, score, indx):
        return ((self.Fitter.limit_min[indx] - score) / (self.Fitter.limit_min[indx] - self.Fitter.norm_min[indx]))
