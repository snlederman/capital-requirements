from numpy import matrix, zeros
import csv
import datetime
import pandas as pd
import timeit

start = timeit.default_timer()



with open('data.csv', newline='') as f:
    reader = csv.reader(f)
    data = {'id':[], 'rating':[], 'date':[]}
    for row in reader:
        data['id'].append(row[0])
        data['rating'].append(row[2])
        data['date'].append(row[1])

def n_date(date):
    date = date.split('/')
    return datetime.date(day=int(date[1]), month=int(date[0]), year=int(date[2]))

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
data['date'] = list(map(n_date, data['date']))
data['id'] = list(map(int, data['id']))
df_data = pd.DataFrame(data=data).sort_values('date')

st = min(df_data['date'])
ft = max(df_data['date'])
df_data['to'] = list(map(lambda x: (x - st).days, df_data['date']))


def m_generator():
    A = zeros((17, 17))
    pass


# Creamos la matrix Ns_t = df_data.sort_values('date')['date'][0]
#f_t = df_data.sort_values('date')['date'][-1]
id = 0
rate = {}

id_data = df_data.sort_values(['id','date'])
'''
for i in range(len(data['id'])):
    if data['id'][i] != id:
        id = data['id'][i]
        rate[str(id)] = []
        rate['dt_' + str(id)] = []

    rate[str(id)].append(data['rating_id'][i])
    if i == len(data['id'])-1:
        rate['dt_' + str(id)].append(ft - id_data['date'][i])
    else:
        rate['dt_' + str(id)].append(id_data['date'][i + 1] - id_data['date'][i])

'''
N = zeros((8, 8))


for country in df_data.drop_duplicates(['country'])['country'].values:
    rate = df_data[df_data.country == country]['rating_id'].values
    for i in range(len(rate)-1):
        N[rate[i]-1][rate[i+1]-1] += 1
print(N)



"""
# Creamos Yi
rate = {}
time_country = {}


for i in range(len(data['rating'])):
    time_country = {}
    if not n_calif(data['rating'][i]) in rate:
        rate[n_calif(data['rating'][i])] = []
    time_country[data['id'][i]] = n_date(data['date'][i])
    rate[n_calif(data['rating'][i])].append(time_country)

Y = {}
for key in rate.keys():
    Y[key] = len(rate[key])


print(rate[3])
print(Y[3])
"""

dt = []
tf = []
for i in range(1,18):
    new = True
    for data in df_data[df_data['id']==i]['to']:
        if new:
            aux = data
            new = False
        else:
            dt.append(data - aux)
            tf.append(data)
            aux = data
    dt.append((ft - st).days - aux)
    tf.append((ft - st).days)



df_data['dt'] = pd.Series(data=dt)
df_data['tf'] = pd.Series(data=tf)

#print(df_data[df_data['rating_id']==5][['to','dt','tf']])
#print(df_data[df_data['id']==1][df_data['rating_id']==5][['rating','to','dt','tf']])
#print(ft)
#acum = datetime.timedelta(5804)
#print()
#print(df_data.as_matrix(['to','tf']))
#for dt in df_data.iteritems(['to','tf']):
#    print(dt)

def Int_Y(to, data):
    Y = []
    for t in range(to,max(data['tf'])+1):
        Y.append(data[(data['to'] < t) & (data['tf'] >= t)].count().country)
    return sum(Y)


Y = []
rate = df_data.drop_duplicates(['rating_id']).sort_values('rating_id')['rating_id'].values
print(rate)
for i in rate:
    to = min(df_data[df_data['rating_id'] == i]['to'])
    Y.append(Int_Y(to, df_data[df_data['rating_id'] == i]))

for i in range(7):
    N[i] = N[i]/Y[i]
    N[i][i] = 0
    N[i][i] = -sum(N[i])
else:
    N[7] = N[7]*0

print(N*365)

stop = timeit.default_timer()
execution_time = stop - start

print("Program Executed in {} seconds".format(execution_time))