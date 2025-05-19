# napravimo resetku 
# vjerojatnost da je setac u celiji i: P_i = m/n gdje je m onoliko koliko ih je u toj celiji
# round(x+xmin)/deltax = i
# round(y+ymin)/deltay = j
# dis(i,j)= dis(1,j)+1
# za ispis: x = i*deltax-xmin y = j*deltay-ymin... delte su sirina celije

import random
import numpy as np
import matplotlib.pyplot as plt
import math

xuk = []
yuk = []
x = []
y = []

for i in range(-400, 400):
    xuk.append(i)
    yuk.append(i)

def entropija():
    for j in range(len(xuk)):
        x.append(random.random())
        y.append(random.random())

        
