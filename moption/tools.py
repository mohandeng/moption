# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 08:43:01 2020

@author: Mohan
"""

from moption.black_sholes import options
import numpy as np

    
    

def scenario_analysis(option_port, target_func, variable = 'S',
                      vrange = []):
    """
    Calculate the value of a target function given a series of scenarios.

    Parameters
    ----------
    option_port : option object or array of option objects
        The option position to be valued.
    target_func : function
        The function used to get the value of the option position.
    variable : str, optional
        The parameter in the option used to describe the situation changes.
        Must be one of 'S', 'K', 'sigma', 't', 'r', 'q'. The default is 'S'.
    vrange : array of float, optional
        The values that 'variable' take. The default is np.array().

    Returns
    -------
    The array of function values in different scenarios.
    
    ############# to do: example and test
    """
    res = [target_func(option_port.set_param(param = variable, 
                       new_value = value)) for value in vrange]
    return np.array(res)
    
