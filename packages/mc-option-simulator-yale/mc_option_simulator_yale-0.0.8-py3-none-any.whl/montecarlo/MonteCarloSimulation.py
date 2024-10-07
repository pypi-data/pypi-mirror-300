import random
import math
import scipy.stats

RISK_FREE_INTEREST = .03969 # 10 year treasury
DELTA_TIME = 1 # time to exp / TIME
TIME = 1 # in years
STEPS_N = 252

class MonteCarloSimulation:
    def __init__(self, stock_value, strike, volatility, steps, simulations):
        self.stock_value = stock_value
        self.risk_free_interest = RISK_FREE_INTEREST 
        self.strike = strike 
        self.sigma = volatility 
        self.delta_time = TIME/STEPS_N 
        self.T = TIME
        self.steps = steps
        self.simulations = simulations
        self.payoffs = []

    def Geometric_Brownian_Motion(self, option_type="call"):
        st_delta_t_sum = self.stock_value
        for _ in range(self.steps):
        
            gaussian = random.gauss(0, 1)
            exponent = ((self.risk_free_interest - 0.5 * self.sigma ** 2) 
                        * self.delta_time + self.sigma * math.sqrt(self.delta_time) * gaussian)

            st_delta_t_sum = st_delta_t_sum * math.exp(exponent)
            yield (_, st_delta_t_sum)  

        if option_type  == "call".lower():
            payoff = max(st_delta_t_sum - self.strike, 0)
        elif option_type == "put".lower():
            payoff = max(self.strike - st_delta_t_sum, 0)
        else:
            raise ValueError 
        self.payoffs.append(payoff)

        # option_price = math.exp(-self.risk_free_interest * self.T) * payoff
        # return option_price


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


def main():
    sim = MonteCarloSimulation(45, 46, .013, 252, 1000)
    sim.Geometric_Brownian_Motion()

if __name__ == "__main__":
    main()