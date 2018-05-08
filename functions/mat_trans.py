from numpy import zeros
import csv
import datetime
import pandas as pd
import timeit
from scipy.linalg import expm

start = timeit.default_timer()

def n_date(date):
    '''
    :param date: Un str con una fecha correspondiente.
    :return: Tipo datetime con los dias, meses y anos correspondiente.
    '''
    date = date.split('/')
    return datetime.date(day=int(date[1]), month=int(date[0]), year=int(date[2]))

def n_calif(C):
    '''
    :param C: Un str con el tipo de calificacion.
    :return: Retorna un int con la clase de calificacion correspondiente
    '''
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

def country_id(id):
    '''
    :param id: id de tipo str y corresponde a un pais.
    :return: Un str con el nombre del pais correspondiente.
    '''
    COUNTRY = ['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'El Salvador',
               'Guatemala', 'Hoduras', 'Mexico', 'Panama', 'Paraguay', 'Peru', 'Republica Dominicana', 'Uruguay',
               'Venezuela']
    return COUNTRY[int(id) - 1]

def int_y(to, data):
    '''
    :param to: tiempo inicial.
    :param data: Un dataframe de prestarios en el tiempo de la clase i.
    :return: La integral de los prestarios en la clase i en el tiempo s.
        - Se inicializa y.
        - Se itera en el tiempo en un rango de to a tf.
        - Se filtra la data que esta en el rango definido, y luego se obtiene la cantidad de prestatarios en dicho rango.
        - Finalmente se devuelve la sumataria de y.
    '''
    y = []
    for t in range(to, max(data['tf']) + 1):
        y.append(data[(data['to'] < t) & (data['tf'] >= t)].count().country)
    return sum(y)

'''
    - Se abre el documento, guardado en la carpeta de data.
    - Se crea una variable reader que contiene toda la informacion del documento.
    - Se crea un diccionario con los valores de cada columna.
    - Se ejecuta un for para ir tomando los valores contenido en reader.
'''
with open('/users/samuelledermansardi/PycharmProjects/Tesis/capital-requirements/data/data.csv', newline='') as f:
    reader = csv.reader(f)
    data = {'id':[], 'rating':[], 'date':[]}
    for row in reader:
        data['id'].append(int(row[0]))
        data['date'].append(row[1])
        data['rating'].append(row[2])

data['country'] = list(map(country_id, data['id']))  # Crea una llave con nos nombres de los paises segun su id.
data['rating_id'] = list(map(n_calif, data['rating']))  # Crea una llave con las clases de calificaciones.
data['date'] = list(map(n_date, data['date']))  # Se modifica la llave date de tipo str a datetime.

df_data = pd.DataFrame(data=data).sort_values('date')  # Creo un dataframe con la data original y lo ordeno por date.

st = min(df_data['date'])  # Tomo el start time, o tiempo de inicio de la muestra.
ft = max(df_data['date'])  # Tomo el finish time, o tiempo final de la muestra.
'''
    Tomo los date y los resto con el start time para tener un to (tiempo inicio) 
    con respecto al primer tiempo en nuestra muestra.
'''
df_data['to'] = list(map(lambda x: (x - st).days, df_data['date']))

'''
    Cantidad de clases para transiciones.
'''
N_id = len(df_data.drop_duplicates(['rating_id'])['rating_id'].values)
N = zeros((N_id, N_id))  # Inicio mi matrix N como una matrix de ceros tamano N_id, N_id.

'''
    Creacion de la matrix de transiciones de prestarios de la clase i a la clase j; donde i y j puede tomar N_id clases.
    - Itero entre los prestatarios.
    - Luego filtro la data de dicho prestario, y tomo un array con sus distintas clases.
    - Itero entre las clases - 1, ya que el ultimo no tiene transcicion.
    -  Luego se incrementa la posicion de N, donde se hayo una transicion de clase i a j.
'''
for country in df_data.drop_duplicates(['country'])['country'].values:
    rate = df_data[df_data.country == country]['rating_id'].values
    for i in range(len(rate)-1):
        N[rate[i]-1][rate[i+1]-1] += 1

'''
    Cantidad de prestatarios.
'''
N_country = len(df_data.drop_duplicates(['country'])['country'].values)
'''
    Se registra la duracion de los prestarios en cada clase.
        - Se itera entre los distintos prestatarios.
        - Luego de cada prestario se itera en sus tiempos de inicio en cada clase.
        - Se crea una condicion donde hay un booleano new que nos dice si estamos 
        en un prestario nuevo.
        - Si el prestario es nuevo, se toma el punto to como aux.
        - Si no se toma el punto to y se resta el aux, que es el punto anterior,
        dandonos la duracion.
        - Se toma el to del siguiente y se le asigna al tf del anterior.
        - Se toma el to como aux para la proxima iteracion.
        - Para la ultima iteracion se toma el to y se resta con respecto a la 
        diferencia que hay entre el tiempo final y el tiempo inicial.
        - Y para el tiempo final se toma el ultimo el ultimo tiempo.
        
'''
df_data.sort_values(['id','date'])
dt = [] # Duracion.
tf = [] # Tiempo final.
for i in range(1, N_country + 1):
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

df_data['dt'] = pd.Series(data=dt)  # Se agrega una columna dt (duracion) al dataframe.
df_data['tf'] = pd.Series(data=tf)  # Se agrega una columna tf (tiempo final) al dataframe

'''
    Creacion de la cantidad de prestatarios en la clase i.
        - Se itera entre las distintas clase.
        - Se toma el menor tiempo inicial.
        - Se ejecuta la funcion int_y para tener la integracion por cada clase.
'''
Y = []  # Inicializo el array de Y
# Tomo los valores de las clases, ordenadas crecientemente.
rate = df_data.drop_duplicates(['rating_id']).sort_values('rating_id')['rating_id'].values
for i in rate:
    to = min(df_data[df_data['rating_id'] == i]['to'])
    Y.append(int_y(to, df_data[df_data['rating_id'] == i]))


'''
    Se calcula la matrix generadora.
        - Se itera entre el numero de clase.
        - Cada fila se divide entre Yi, llamado tasa de transicion.
        - La digonal corresponde a la sumatoria negativa de cada fila.
        - Se hace el elemento [i,i], igual a cero para que no afecte en la sumatoria.
        - La ultima fila es igual a cero, debido a que es un estado absorbente.
'''

for i in range(N_id - 1):
    N[i] = N[i] / Y[i]
    N[i][i] = 0
    N[i][i] = -sum(N[i])
else:
    N[N_id - 1] = N[N_id - 1] * 0

'''
    Calculo de la matrix de transicion.
        - Se multiplica por 365 para obtener la matrix generadora en agnos.
        - Se aplica la funcion exponecial a la matrix N y se multiplica por 100 para obtenerla en probabilidades.
'''
N = N * 365
Mt = expm(N)*100
print(Mt)

stop = timeit.default_timer()
execution_time = stop - start
print("Program Executed in {} seconds".format(execution_time))