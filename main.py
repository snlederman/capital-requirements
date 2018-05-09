#from functions.mat_trans import mt
from functions.moment_method import correlation
import csv

############################################ DATA ######################################################################
'''
    - Se abre el documento, guardado en la carpeta de data.
    - Se crea una variable reader que contiene toda la informacion del documento.
    - Se crea un diccionario con los valores de cada columna.
    - Se ejecuta un for para ir tomando los valores contenido en reader.
'''
with open('data/data.csv', newline='') as f:
    reader = csv.reader(f)
    data = {'id':[], 'rating':[], 'date':[]}
    for row in reader:
        data['id'].append(int(row[0]))
        data['date'].append(row[1])
        data['rating'].append(row[2])
data_mt = data

with open('data/default.csv', newline='') as f:
    reader = csv.reader(f)
    data = {'year':[], 'Dt':[], 'Nt':[]}
    for row in reader:
        data['year'].append(int(row[0]))
        data['Dt'].append(int(row[1]))
        data['Nt'].append(int(row[2]))
data_mm = data

'''
 Loss Given Default.
 Perdidas Dado el Incumplimiento.
'''
LGD = 45
'''
 Expoture At Default
 Exposicion ante el incumplimiento
'''
EAD = 100

############################################ MODEL #####################################################################
#Mt = mt(data_mt)
rho = correlation(data_mm, DEBUG=True)






