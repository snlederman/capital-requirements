import numpy as np
from numpy import sqrt
from scipy.optimize import fsolve

b = 0
c = -4
a = 1

data = (a, b, c)

def resolvente(x, *data):
	a, b, c = data
	return - x + (-b - sqrt( b**2 - 4 * a * c) / (2 * a))

x0 = -0.1

#a = resolvente(a0, *data)

x = fsolve(resolvente, x0, args=data)

for i in range(0, 11, 2):
	print(i)

print ("esto esta hecho por samuel")
