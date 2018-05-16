import timeit
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.stats import norm, multivariate_normal, t

from functions.mat_trans import COUNTRIES

NUMERO_ITERACIONES = 10 ** 6


def fun(rho, *args):
    d, P2 = args
    x = np.array([d, d])
    mean = np.array([0, 0])
    cov = np.array([[1, rho], [rho, 1]])
    return P2 - multivariate_normal.cdf(x, mean, cov)


def _loss_cal(sqrt_ro, sqrt_1_rho, LGDxEAD, vals, z, epsilon, chi2_a):
    aux = 0
    i = 0
    for country in COUNTRIES:
        a = sqrt_ro * z + sqrt_1_rho * epsilon[i] / chi2_a
        if a <= vals[country]:
            aux += LGDxEAD
        i += 1
    return aux


def correlation(data, sol, LGD, EAD, DEBUG=False):
    start = timeit.default_timer()

    df_data = pd.DataFrame(data=data).sort_values('year')  # Creamos un DataFrame y lo ordenamos por agno.
    df_sol = pd.DataFrame(data=sol).sort_values('country')  # TODO: comentar
    """
        Calculamos los momentos para utilizarlo en la estimacion de la correlacion.
            - P1: momento 1
            - P2: momento 2
    """
    P1 = sum(df_data.Dt / df_data.Nt) / len(df_data.year)
    P2 = sum((df_data.Dt * (1 - df_data.Dt)) / (df_data.Nt * (1 - df_data.Nt))) / len(df_data.year)

    """
        d: La inversa de una funcion de distribucion acumulada de una normal estandar.
    """
    d = norm.ppf(P1)

    rho = fsolve(fun, x0=np.array(0), args=(d, P2))

    _loss_pool = Pool()
    sqrt_rho = np.sqrt(rho)
    sqrt_1_rho = np.sqrt(1 - rho)
    LGDxEAD = LGD * EAD

    vals = {}

    for country in COUNTRIES:
        vals[country] = df_sol[df_sol['country'] == country].d.values

    z = np.random.normal(0, 1, NUMERO_ITERACIONES)
    epsilon = np.random.normal(0, 1, (NUMERO_ITERACIONES, len(COUNTRIES)))
    alfa = 3
    chi2 = np.random.chisquare(alfa, NUMERO_ITERACIONES)
    chi2_a = list(map(lambda x: np.sqrt(x/alfa), chi2))

    loss = _loss_pool.starmap(_loss_cal,
                              [(sqrt_rho, sqrt_1_rho, LGDxEAD, vals, z[i], epsilon[i], chi2_a[i]) for i in
                               range(NUMERO_ITERACIONES)])

    loss.sort()
    plt.hist(loss)
    plt.show()
    stop = timeit.default_timer()
    execution_time = stop - start

    if DEBUG:
        """
        print(multivariate_normal.cdf(x=np.array([d, d]), mean = np.array([0,0]), cov=np.array([[1, rho], [rho, 1]])))
        print(P2)
        """
        print("moment_method Program Executed in {} seconds".format(execution_time))

    return rho


def correlation_manuel(data, sol, LGD, EAD, DEBUG=False):
    start = timeit.default_timer()

    df_data = pd.DataFrame(data=data).sort_values('year')  # Creamos un DataFrame y lo ordenamos por agno.
    df_sol = pd.DataFrame(data=sol).sort_values('country')  # TODO: comentar
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

    rho = fsolve(fun, x0=np.array(0), args=(d, P2))

    countries = {'Argentina': [], 'Bolivia': [], 'Brasil': [], 'Chile': [], 'Colombia': [],
                 'Costa Rica': [], 'Ecuador': [], 'El Salvador': [], 'Guatemala': [],
                 'Hoduras': [], 'Mexico': [], 'Panama': [], 'Paraguay': [], 'Peru': [],
                 'Republica Dominicana': [], 'Uruguay': [],
                 'Venezuela': []}
    loss = []
    for i in range(NUMERO_ITERACIONES):
        z = np.random.normal(0, 1)
        aux = 0
        for country in countries.keys():
            epsilon = np.random.normal(0, 1)
            a = np.sqrt(rho) * z + np.sqrt(1 - rho) * epsilon / np.sqrt()
            if a <= df_sol[df_sol['country'] == country].d.values:
                aux += LGD * EAD
        loss.append(aux)
    loss.sort()
    plt.hist(loss)
    plt.show()
    stop = timeit.default_timer()
    execution_time = stop - start

    if DEBUG:
        '''
        print(multivariate_normal.cdf(x=np.array([d, d]), mean = np.array([0,0]), cov=np.array([[1, rho], [rho, 1]])))
        print(P2)
        '''
        print("moment_method Program Executed in {} seconds".format(execution_time))

    return rho
