import pandas as pd
import timeit
from scipy.stats import norm, multivariate_normal
import numpy as np
from scipy.optimize import fsolve

def fun(rho, *args):
    d, P2 = args
    x = np.array([d, d])
    mean = np.array([0, 0])
    cov = np.array([[1, rho], [rho, 1]])
    return P2 - multivariate_normal.cdf(x, mean, cov)

def correlation(data, DEBUG=False):
    start = timeit.default_timer()

    df_data = pd.DataFrame(data=data).sort_values('year') # Creamos un DataFrame y lo ordenamos por agno.

    '''
        Calculamos los momentos para utilizarlo en la estimacion de la correlacion.
            - P1: momento 1
            - P2: momento 2
    '''
    P1 = sum(df_data.Dt / df_data.Nt) / len(df_data.year)
    P2 = sum((df_data.Dt * (1 - df_data.Dt)) / (df_data.Nt * (1 - df_data.Nt))) / len(df_data.year)

    '''
        d: La inversa de una funcion de distribucion acumulada de una normal estandar.
    '''
    d = norm.ppf(P1)

    rho = fsolve(fun, x0=0, args=(d, P2))

    countries = {'Argentina':[], 'Bolivia':[], 'Brasil':[], 'Chile':[], 'Colombia':[],
    'Costa Rica':[], 'Ecuador':[], 'El Salvador':[], 'Guatemala':[],
    'Hoduras':[], 'Mexico':[], 'Panama':[], 'Paraguay':[], 'Peru':[],
    'Republica Dominicana':[], 'Uruguay':[],
    'Venezuela':[]}
    for i in range(10 ** 6):
        for country in countries.keys():
            countries[country].append(np.sqrt(rho) * np.random.normal(0, 1) + np.sqrt(1 - rho) * np.random.normal(0, 1))

    df_sol = pd.DataFrame(data=countries)
    print(df_sol)

    stop = timeit.default_timer()
    execution_time = stop - start

    if DEBUG:
        print(multivariate_normal.cdf(x=np.array([d, d]), mean = np.array([0,0]), cov=np.array([[1, rho], [rho, 1]])))
        print(P2)
        print("moment_method Program Executed in {} seconds".format(execution_time))

    return rho