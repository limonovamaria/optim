import numpy as np
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
