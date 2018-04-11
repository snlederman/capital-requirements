from numpy import matrix, zeros
import csv
import datetime
import pandas as pd

with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = {'id':[], 'rating':[], 'fecha':[]}
    for row in reader:
        data['id'].append(row[0])
        data['rating'].append(row[2])
        data['fecha'].append(row[1])

def n_fecha(fecha):
    fecha = fecha.split('/')
    return datetime.date(day=int(fecha[1]), month=int(fecha[0]), year=int(fecha[2]))

def n_calif(C):
    # Esta funcion retorna los numeros de
    # calificacion dependiendo de el tipo de
    # calificacion.

    if C == 'AAA':
        return 1
    elif C in ['AA+', 'AA-', 'AA']:
        return 2
    elif C in ['A+', 'A-', 'A']:
        return 3
    elif C in ['BBB+', 'BBB-', 'BBB']:
        return 4
    elif C in ['BB+', 'BB-', 'BB']:
        return 5
    elif C in ['B+', 'B-', 'B']:
        return 6
    elif C in ['CCC+', 'CCC-', 'CCC', 'CC', 'C']:
        return 7
    elif C == 'SD':
        return 8

def id_country(country):
    # Esta funcion asigna un identifiador a cada pais
    COUNTRY = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'El Salvador',
               'Guatemala', 'Hoduras', 'Mexico', 'Panama', 'Paraguay', 'Peru', 'Republica Dominicana', 'Uruguay',
               'Venezuela']
    return COUNTRY.index(country) + 1

def country_id(id):
    COUNTRY = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'El Salvador',
               'Guatemala', 'Hoduras', 'Mexico', 'Panama', 'Paraguay', 'Peru', 'Republica Dominicana', 'Uruguay',
               'Venezuela']
    return COUNTRY[int(id) - 1]

data['country'] = list(map(country_id, data['id']))
data['rating_id'] = list(map(n_calif, data['rating']))
data['fecha'] = list(map(n_fecha, data['fecha']))
data['id'] = list(map(int, data['id']))
df_data = pd.DataFrame(data=data).sort_values('fecha')

st = min(df_data['fecha'])
ft = max(df_data['fecha'])
df_data['fecha'] = list(map(lambda x: x - st, df_data['fecha']))


def m_generator():
    A = zeros((17, 17))
    pass


# Creamos la matrix Ns_t = df_data.sort_values('fecha')['fecha'][0]
#f_t = df_data.sort_values('fecha')['fecha'][-1]
id = 0
rate = {}

id_data = df_data.sort_values(['id','fecha'])

for i in range(len(data['id'])):
    if data['id'][i] != id:
        id = data['id'][i]
        rate[str(id)] = []
        rate['dt_' + str(id)] = []

    rate[str(id)].append(data['rating_id'][i])
    if i == len(data['id'])-1:
        rate['dt_' + str(id)].append(ft - id_data['fecha'][i])
    else:
        rate['dt_' + str(id)].append(id_data['fecha'][i + 1] - id_data['fecha'][i])


N = zeros((8, 8))
"""
for key in rate.keys():
    val = rate[key]
    for i in range(len(val)-1):
        N[val[i]-1][val[i+1]-1] += 1
"""


"""
# Creamos Yi
rate = {}
time_country = {}


for i in range(len(data['rating'])):
    time_country = {}
    if not n_calif(data['rating'][i]) in rate:
        rate[n_calif(data['rating'][i])] = []
    time_country[data['id'][i]] = n_fecha(data['fecha'][i])
    rate[n_calif(data['rating'][i])].append(time_country)

Y = {}
for key in rate.keys():
    Y[key] = len(rate[key])


print(rate[3])
print(Y[3])
"""


for data in df_data[df_data['id']==1]['fecha']:

    print(data)
#print(df_data[df_data['id']==1])
