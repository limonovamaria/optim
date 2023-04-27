import numpy as np
from optim import nelder_mead
import matplotlib.pyplot as plt
from matplotlib import cm

print("список:")
my_list = [1, 2, 3]
print(id(my_list), my_list)
my_list *= 2
print(id(my_list), my_list)
a = my_list.pop()
print(id(my_list), my_list)
print(id(a), a)

print("\nмассив numpy:")
my_array = np.array([1, 3, 4, 2, 8])
print(id(my_array), my_array)
my_array *= 2
print(id(my_array), my_array)
b = np.delete(my_array, range(2))
print(id(b), b)
print(id(my_array), my_array)

take_first = lambda ar, n: (ar[n:], ar[:n])

new_array, my_array = take_first(my_array, 2)
print(id(my_array), my_array)
print(id(new_array), new_array)


X = np.array(np.linspace(0, 4, 50))
Y = np.array(np.linspace(0, 4, 50))
X, Y = np.meshgrid(X, Y)
Z_targ = X + Y
Z = X+Y+X*Y*1000

levels = np.linspace(np.min(Z_targ), np.max(Z_targ), 16)
fig, ax = plt.subplots()#subplot_kw={"projection": "3d"})
# ax.plot_surface(X, Y, Z)#, vmin=Z.min() * 2)#, cmap=cm.Blues)
# ax.contourf(X, Y, Z, cmap=cm.coolwarm)\
CS = ax.contour(X, Y, Z, levels=levels)
plt.clabel(CS, inline=1, fontsize=10)
plt.show()