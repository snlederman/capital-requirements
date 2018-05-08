import csv
import pandas as pd
import timeit
from scipy.stats import norm, multivariate_normal
import numpy as np
from scipy.optimize import fsolve

start = timeit.default_timer()


with open('/users/samuelledermansardi/PycharmProjects/Tesis/capital-requirements/data/default.csv', newline='') as f:
    reader = csv.reader(f)
    data = {'year':[], 'Dt':[], 'Nt':[]}
    for row in reader:
        data['year'].append(int(row[0]))
        data['Dt'].append(int(row[1]))
        data['Nt'].append(int(row[2]))

df_data = pd.DataFrame(data=data).sort_values('year')

P1 = sum(df_data.Dt / df_data.Nt) / len(df_data.year)
P2 = sum((df_data.Dt * (1 - df_data.Dt)) / (df_data.Nt * (1 - df_data.Nt))) / len(df_data.year)

d = norm.ppf(P1)

x = np.array([d, d])
rho = 0.30708572
cov = np.array([[1, rho], [rho, 1]])
mean = np.array([0,0])

#print(multivariate_normal.cdf(x, mean, cov))
print(P2)

def fun(rho, *args):
    d, mean = args
    x = np.array([d, d])
    mean = np.array([0,0])
    cov = np.array([[1, rho], [rho, 1]])
    return P2 - multivariate_normal.cdf(x, mean, cov)

x0 = 0
rho = fsolve(fun, x0, args=(d,mean))
x = np.array([d, d])
cov = np.array([[1, rho], [rho, 1]])
mean = np.array([0,0])

print(multivariate_normal.cdf(x, mean, cov))


stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in {} seconds".format(execution_time))