# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:30:58 2020

@author: Mohan
"""

import numpy as np
import moption.options as options
from scipy.stats import norm  


def div_adj(option):
    return np.exp(-option.q*option.t)

def vol_adj(option):
    return option.sigma*np.sqrt(option.t)

def discount(option):
    return np.exp(-option.r*option.t)
    
    
def d(option):
    """
    Return the d1, d2 in Black Sholes Model`

    :param option: the option characteristics
    :type option: VanillaOption
    """
    cost_rate = option.r - option.q
    intrinsic_part = np.log(option.S/option.K)
    time_part = (cost_rate + 0.5*option.sigma**2)*option.t
    nominator = intrinsic_part + time_part
    d1 = nominator/vol_adj(option)
    d2 = d1 - vol_adj(option)
    
    return d1, d2


def _type_helper(option_port, func):
    """
    Help relevant functions to do different operations based on the input type.
    To be used in an outer function, would call the inner function.

    Parameters
    ----------
    option_port : object in the option.py module
        The input to the outer function.
    func : function
        The inner function to call.

    """
    if isinstance(option_port, options.VanillaOption):
        return func(option_port)
    if isinstance(option_port, options.Portfolio):
        return np.sum([func(opt)* option_port.share[i]
                       for i, opt in enumerate(option_port.option)])
    
    
def pricing(option_port):
    def pricing_helper(option):
        if option.t == 0:
            return option.final_payoff(option.S)
            
        d1, d2 = d(option)
        forward_price = option.S*div_adj(option)/discount(option)
        stock_part = forward_price*norm.cdf(d1)
        cash_part = option.K*norm.cdf(d2)
        call_price = (stock_part - cash_part)*discount(option)
        if option.put == False:
            return call_price
        else:
            return call_price - (forward_price-option.K)*discount(option)
        
    return _type_helper(option_port, pricing_helper)


def delta(option_port):
    def delta_helper(option):
        if option.put:
            return div_adj(option)*(norm.cdf(d(option)[0])-1)
        else:
            return div_adj(option)*norm.cdf(d(option)[0])
    
    return _type_helper(option_port, delta_helper)

def gamma(option_port):
    def gamma_helper(option):
        return div_adj(option)*norm.pdf(d(option)[0])/(option.S*vol_adj(option))
    
    return _type_helper(option_port, gamma_helper)
    
def theta(option_port):
    def theta_helper(option):
        d1, d2 = d(option)
        stock_part = -div_adj(option)*option.S*norm.pdf(d1)* \
            option.sigma/(2*np.sqrt(option.t))
        div_part = option.q*option.S*div_adj(option)
        cash_part = option.r*option.K*discount(option)
        if option.put:
            return stock_part-norm.cdf(-d1)*div_part+norm.cdf(-d2)*cash_part
        else:
            return stock_part+norm.cdf(d1)*div_part-norm.cdf(d2)*cash_part
    
    return _type_helper(option_port, theta_helper)
        
def vega(option_port):
    def vega_helper(option):
        return norm.pdf(d(option)[0])*option.S*np.sqrt(option.t)*div_adj(option)
    
    return _type_helper(option_port, vega_helper)
    
def rho(option_port):
    def rho_helper(option):
        fac = option.K*option.t*discount(option)
        if option.put:
            return fac*(norm.cdf(d(option)[1])-1)
        else:
            return fac*norm.cdf(d(option)[1])
        
    return _type_helper(option_port, rho_helper)

def speed(option_port):
    def speed_helper(option):
        fac = d(option)[0]/vol_adj(option)
        return -gamma(option)*(1+fac)/option.S
    
    return _type_helper(option_port, speed_helper)
       
def vanna(option_port):
    def vanna_helper(option):
        return -div_adj(option)*d(option)[1]*norm.pdf(d(option)[0])/option.sigma
    
    return _type_helper(option_port, vanna_helper)
    
def volga(option_port):
    def volga_helper(option):
        d1, d2 = d(option)
        numerator_nodiv = d1*d2*norm.pdf(d1)*option.S*np.sqrt(option.t)
        return div_adj(option)*numerator_nodiv/option.sigma
    
    return _type_helper(option_port, volga_helper)

def charm(option_port):
    def charm_helper(option):
        d1, d2 = d(option)
        tmp = -d2/(2*option.t)+(option.r-option.q)/vol_adj(option)
        tmp = tmp*norm.pdf(d1)
        if option.put:
            return div_adj(option)*(option.q*norm.cdf(-d1)+tmp)
        else:
            return div_adj(option)*(-option.q*norm.cdf(d1)+tmp)
        
    return _type_helper(option_port, charm_helper)
    
def color(option_port):
    def color_helper(option):
        d1, d2 = d(option)
        fac1 = (1-d1*d2)/(2*option.t)
        fac2 = d1*(option.r-option.q)/vol_adj(option)
        return gamma(option)*(option.q+fac1+fac2)
    
    return _type_helper(option_port, color_helper)

def zomma(option_port):
    def zomma_helper(option):
        d1, d2 = d(option)
        return gamma(option)*(d1*d2-1)/option.sigma
    
    return _type_helper(option_port, zomma_helper)

def phi(option_port):
    def phi_helper(option):
        d1, _ = d(option)
        fac = option.t*option.S*div_adj(option)
        if option.put:
            return fac*norm.cdf(-d1)
        else:
            return -fac*norm.cdf(d1)
    
    return _type_helper(option_port, phi_helper)

def greeks(option_port):

    return {'Delta': delta(option_port),
            'Gamma': gamma(option_port),
            'Theta': theta(option_port),
            'Vega': vega(option_port),
            'Rho': rho(option_port),
            'Speed': speed(option_port),
            'Vanna': vanna(option_port),
            'Volga': volga(option_port),
            'Charm': charm(option_port),
            'Color': color(option_port),
            'Zomma': zomma(option_port),
            'Phi': phi(option_port)}
    
