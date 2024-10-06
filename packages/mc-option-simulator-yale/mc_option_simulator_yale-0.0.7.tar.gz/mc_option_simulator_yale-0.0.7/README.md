# Monte Carlo

[Monte Carlo Simulator ](https://github.com/yalehacks)

# setup

pip install using:

```
pip install mc-option-simulator-yale
```

import the module using:

```
from montecarlo.MonteCarloSimulation import MonteCarloSimulation
```

classes: $\\$

```python
class MonteCarloSimulation:
```

Methods belong to MonteCarloSimulation

```python
def __init__(self, stock_value, strike, volatility):
        self.stock_value = stock_value
        self.risk_free_interest = RISK_FREE_INTEREST
        self.strike = strike
        self.sigma = volatility
        self.delta_time = DELTA_TIME
        self.T = TIME
```

```python
def Geometric_Brownian_Motion(self, option_type="call")
```

```python
def Black_Scholes(self, option_type="call".lower())
```

Full class and method details omitted, refer to the code to see full implementation.
