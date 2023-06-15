import numpy
from math import sqrt


def initialize_brownian_bridge(n_simulations, drift, volatility, maturity_time):
    
    X = numpy.zeros(n_simulations, dtype=float)
    for i in range(n_simulations):
        X[i] = ((drift - 0.5 * volatility ** 2) * maturity_time)
        X[i] += volatility * sqrt(maturity_time) * numpy.random.randn(1)[0]
    
    return X

def brownian_bridge(X, volatility, t_now, t_prev):
    try:
        for i in range(len(X)):
            X[i] = X[i] * (t_now / t_prev)
            X[i] += volatility * sqrt(t_now * (t_prev - t_now) / t_prev) * numpy.random.randn(1)[0]
    except ValueError:
        import pdb; pdb.set_trace
        pass
    
    return X