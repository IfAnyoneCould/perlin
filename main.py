from test import *
import matplotlib.pyplot as plt
import numpy as np


array = np.empty((100,100))

for x in range(100):
    for y in range(100):
        mult = 1/25
        val = Perlin(x*mult,y*mult)
        array[x,y] = val.Perlin()

plt.imshow(array, cmap = 'gray')
plt.gca().invert_yaxis()
plt.show()


