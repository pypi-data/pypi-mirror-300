import random
import math
import scipy.stats
import constants as c

class MonteCarloSimulation:
    def __init__(self, stock_value, strike, volatility):
        self.stock_value = stock_value
        self.risk_free_interest = c.RISK_FREE_INTEREST 
        self.strike = strike 
        self.sigma = volatility 
        self.delta_time = c.DELTA_TIME 
        self.T = c.TIME

    def Geometric_Brownian_Motion(self, option_type="call"):
        gaussian = random.gauss(0, 1)
        exponent = ((self.risk_free_interest - 0.5 * self.sigma ** 2) 
                    * self.delta_time + self.sigma * math.sqrt(self.delta_time) * gaussian)

        st_delta_t = self.stock_value * math.exp(exponent)

        if option_type  == "call".lower():
            payoff = max(st_delta_t - self.strike, 0)
        elif option_type == "put".lower():
            payoff = max(self.strike - st_delta_t, 0)
        else:
            raise ValueError    
        
        option_price = math.exp(-self.risk_free_interest * self.T) * payoff
        return option_price

    def Black_Scholes(self, option_type="call".lower()):
        N = scipy.stats.norm.cdf

        d1 = (math.log(self.stock_value / self.strike) + (self.risk_free_interest 
            + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))
        d2 = d1 - self.sigma * math.sqrt(self.T)

        if option_type == "call".lower():
            cost = self.stock_value * N(d1) - self.strike * math.exp(-self.risk_free_interest * self.T) * N(d2)
        elif option_type == "put".lower():
            cost = self.strike * math.exp(-self.risk_free_interest * self.T) * N(-d2) - self.stock_value * N(-d1)
        else:
            raise ValueError
        
        return cost