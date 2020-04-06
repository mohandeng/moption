# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:28:27 2020

@author: Mohan 
"""

import numpy as np
import copy

class VanillaOption:
    """
    A vanilla European option with necessay parameters.
    
    :param S: underlying stock price
    :type S: float
    :param K: strike price
    :type K: float
    :param t: time to expiration in years
    :type t: float
    :param sigma: annualized stock volatility
    :type sigma: float
    :param r: risk-free interest rate, defalut to be 0
    :type r: float
    :param q: divident paying rate, default to be 0
    :type q: float    
    :param put: True if is an put option; default is False (a call)
    :type put: bool 
    
    :ivar S: underlying stock price
    :vartype S: float
    :ivar K: strike price
    :vartype K: float
    :ivar t: time to expiration in years
    :vartype t: float
    :ivar sigma: annualized stock volatility in percentage
    :vartype sigma: float
    :ivar r: risk-free interest rate in percentage
    :vartype r: float
    :ivar q: divident paying rate in percentage, default to be 0
    :vartype q: float    
    :ivar put: True if is an put option; default to be False (a call)
    :vartype put: bool  
    """
    
    def __init__(self, S, K, t, sigma, r=0, q=0, put=False):
        self.S = float(S)
        self.K = float(K)
        self.t = float(t)
        self.sigma = float(sigma)
        self.r = float(r)
        self.q = float(q)
        self.put = put
        
    def __eq__(self, other):
        """ Return true if two options have exactly same parameters
        """
        if self.S == other.S and self.K == other.K \
            and self.t == other.t and self.sigma == other.sigma \
                and self.r == other.r and self.q == other.q \
                    and self.put == other.put:
                        return True
        else:
            return False
                    
    def summary(self):
        """Print the key atrributes about the option.
        """
        if self.put:
            print("Put Option")
        else:
            print("Call Option")
        print("=================================")
        print("Underlying Price = ", self.S)
        print("Underlying Volatility = ", 100*self.sigma, "%")
        print("Strike Price = ", self.K)
        print("Time to Maturity = ", self.t, "years")
        print("Interest Rate = ", 100*self.r, "%")
        if self.q:
            print("Divident Paying Rate = ", 100*self.q, "%")

    def change_type(self, inplace = False):
        """
        Change the type(call versus put) of the option.

        Parameters
        ----------
        inplace : bool, optional
            Change the current object if it's Ture; 
            only return a new object if it's False. The default if is False.

        Returns
        -------
        VanillaOption
            The option after type change.

        """
        if inplace:
            self.put = not self.put
        
        return VanillaOption(self.S, self.K, self.t, self.sigma,
                          self.r, q = self.q, put = not self.put)
    
    def shock(self, S_shock = 0, K_shock = 0, t_shock = 0, sigma_shock = 0, 
          r_shock = 0, q_shock = 0, type_change = False, percentage = False, 
          inplace = False):
        """ Return an option given shocks in the parameter to an option.

        Parameters
        ----------
        option : VanillaOption 
            The original option.
        S_shock : float, optional
            The shock in the underlying price. The default is 0.
        K_shock : float, optional
            The shock in the strike price. The default is 0.
        t_shock : float, optional
            The shock in the time to maturity. The default is 0.
        sigma_shock : float, optional
            The shock in the volatility. The default is 0.
        r_shock : float, optional
            The shock in the interest rate. The default is 0.
        q_shock : float, optional
            The shock in the dividend rate. The default is 0.
        type_change : bool, optional
            Whether change the option type between put and call. 
            The default is False.
        percentage : bool, optional
            Whether the change in given in percentage. The default is False.
            If True, the shock means a percentage change. 
        inplace : bool, optional
            Whether change the original instance. The default is False.
            
        Returns
        -------
        new_option : VanillaOption
            The option after shocks.
        """          
        if percentage == False:
            new_option = VanillaOption(self.S + S_shock, self.K + K_shock,
                                  self.t + t_shock, self.sigma + sigma_shock,
                                  self.r + r_shock, self.q + q_shock,
                                  self.put) 
        else:
            new_option = VanillaOption(self.S * (1 + S_shock/100), 
                                  self.K * (1 + K_shock/100),
                                  self.t * (1 + t_shock/100), 
                                  self.sigma * (1 + sigma_shock/100),
                                  self.r * (1 + r_shock/100), 
                                  self.q * (1 + q_shock/100),
                                  self.put) 
            
        if type_change:
            new_option.change_type(inplace = True)
            
        if inplace:
            self.S, self.K, self.t, self.sigma, self.r, self.q, self.put \
                = new_option.S, new_option.K, new_option.t, new_option.sigma, \
                    new_option.r, new_option.q, new_option.put 
            
        return new_option
    
    def set_param(self, new_value, param = 'S', inplace = False):
        """
        Update a parameter of the option.

        Parameters
        ----------
        new_value : float
            The new value of the parameter.
        param : str, optional
            The parameter to be updated. The default is 'S'.
            Should be one of 'S', 'K', 't', 'sigma', 'r', 'q'.
        inplace : bool, optional
            Change the current object if it's Ture; 
            only return a new object if it's False. The default if is False.

        Returns
        -------
        VanillaOption
            The option after type change.
        """
        new_option = copy.copy(self)
        setattr(new_option, param, new_value)
        if inplace:
            self.S, self.K, self.t, self.sigma, self.r, self.q, self.put \
                = new_option.S, new_option.K, new_option.t, new_option.sigma, \
                    new_option.r, new_option.q, new_option.put 
        return new_option
    
    
    def final_payoff(self, s_final = None):
        """ Get the final payoff under different underlying prices.
        
        Parameters
        ----------
        s_final : array-like of float, optional
            The final underling prices used to calculate payoff. 
            The default is None. When this happen, use [0, 2K].

        Returns
        -------
        Array of float
            The final payoff under the given final underlying prices.

        """
        if s_final is None:
            s_final = np.linspace(0, 2*self.K, num = 100)
        if self.put:
            payoff = np.maximum(0, self.K - s_final) 
        else:
            payoff = np.maximum(s_final - self.K, 0)
            
        return np.array(payoff)
    



# portfolio class
class Portfolio:
    """
    A portfolio consists of option objects.
    
    :param option : the options in the portfolio.
    :type option: array_like, type of option object
    :param share: the number of shares, should be the same size of `options`. 
                    Default is None. If only give `options` with no
                    `shares`, would initialize it with a list of ones.
    :type share: array_like, type of int
    """
    
    def __init__(self, option, share = None):
        if share is None:
            share = np.ones(len(option))
        # delete the options with zero shares
        option = np.array(option)[np.array(share) != 0]
        share = np.array(share)[np.array(share) != 0]
        self.option, self.share = option, share
    
    def shock(self, S_shock = 0, K_shock = 0, t_shock = 0, sigma_shock = 0, 
              r_shock = 0, q_shock = 0, type_change = False, 
              percentage = False, inplace = False):
        
        new_options = [opt.shock(S_shock, K_shock, t_shock, sigma_shock, 
              r_shock, q_shock, type_change, percentage) 
                       for opt in self.option]

        if inplace:
            # not really inplace, should better optimize
            self = Portfolio(new_options, self.share)
            
        return Portfolio(new_options, self.share)

    def set_param(self, new_value, param = 'S', inplace = False):
        new_options = [opt.set_param(new_value, param, inplace) 
                       for opt in self.option]        
        if inplace:
            # not really inplace, should better optimize
            self = Portfolio(new_options, self.share)
            
        return Portfolio(new_options, self.share)
    
    def final_payoff(self, s_final = None):
        
        if s_final is None:
            k_max = np.max([opt.K for opt in self.option])
            s_final = np.linspace(0, 2*k_max, num = 100)
            
        
        payoff = np.array([opt.final_payoff(s_final)*self.share[i] for 
                            i, opt in enumerate(self.option)])

            
        return np.sum(payoff, axis = 0)
    
    def __neg__(self):
        """ Return the short position of the current portfolio
        """
        return Portfolio(self.option, -self.share)
    
    def __add__(self, other):
        """ Add two portfolio by combining the options in them; 
        add the number of shares if given an int/float
        """
        if type(other) is Portfolio:
            new_option = copy.deepcopy(self.option)
            new_share = copy.deepcopy(self.share)
            for j, opt_add in enumerate(other.option):
                for i, opt_exist in enumerate(new_option):
                    if opt_add == opt_exist:
                        # the option to add already exist
                        new_share[i] += other.share[j]
                        break
                if not (opt_add == opt_exist):
                    # if reach here the option to add doesn't exist
                    new_option = np.append(new_option, opt_add)
                    new_share = np.append(new_share, other.share[j])
            
            return Portfolio(new_option, new_share)
        
        elif type(other) in (int, float):
            return Portfolio(self.option, self.share + other)
        
        else:
            raise TypeError("Value to add must be a numeric or Portfolio object")        
    

    def __sub__(self, other):
        """ Combine the long position of the minuend and the short position of the subtrahend . 
        """
        return self + (-other)
    
    def __mul__(self, other):
        """ Multiply the number of shares by a number.
        """
        return Portfolio(self.option, self.share * other)
            
    def __rmul__(self, other):
        """ Multiply the number of shares by a number.
        """
        return Portfolio(self.option, self.share * other)
            

            
                    
                
        