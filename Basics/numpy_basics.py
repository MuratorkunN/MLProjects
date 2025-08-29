import numpy as np

my_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

my_array = np.array(my_list)
print(my_list)
print(my_array)
print(type(my_array))

print(my_array.dtype)
print(my_array.shape)
print(my_array.size)
print(my_array.itemsize)
print(my_array.nbytes)
print(my_array.ndim)

print(my_array[0:2, 0:2])
print(my_array[0:2, 0:999])

new_array = my_array.copy()
new_array[0, 0] = 0
print(new_array)

new_array = my_array + 2
print(new_array)

new_array = my_array ** 2
print(new_array)

new_array += my_array
print(new_array)

print(np.sum(my_array))
print(np.sum(my_array, axis=0))
print(np.sum(my_array, axis=1))

print(my_array.T)
print(np.linalg.matrix_rank(my_array))
print(np.linalg.det(my_array))

print(my_array > 4)
print(my_array[my_array > 4])

