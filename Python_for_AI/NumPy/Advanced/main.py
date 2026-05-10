import numpy as np
import numpy.ma as ma

a = np.array([1, 2, 3])
b = np.array([[4], [5]])
print(a + b)
c = np.random.random((1, 4, 7, 2, 4))
d = np.random.random((7, 4, 1, 1, 1))
print(c + d)
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(a[np.newaxis, :, 1])
print(a[[True, False, True]])

a = np.arange(12).reshape(3, 4)
for row in a:
    for element in row:
        print(element, end=" ")
for element in np.nditer(a, order="F"):
    print(element, end="/")

with np.nditer(a, op_flags=["readwrite"]) as it:
    for element in it:
        element[...] = element**2

print(a)


arr = np.array([1, 2, 3, np.nan, 4, np.inf])
print(arr)
masked_arr = ma.masked_array(arr, mask=[0, 0, 0, 1, 0, 1])
print(masked_arr.mean())
print(masked_arr)
print(ma.masked_less(arr, 4))
print(ma.masked_where(arr % 2 == 0, arr))

A = np.array([[1, 2], [3, 4]])

B = np.array([[0, 5], [10, 15]])
C = np.array([[None, None], [None, None]])

C[0, 0] = A[0, 0] * B[0, 0] + A[0, 1] * B[1, 0]
C[0, 1] = A[0, 0] * B[0, 1] + A[0, 1] * B[1, 1]
C[1, 0] = A[1, 0] * B[0, 0] + A[1, 1] * B[1, 0]
C[1, 1] = A[1, 0] * B[0, 1] + A[1, 1] * B[1, 1]
print(C)
print(np.matmul(A, B))
print(A @ B)
arr = np.array([1, 2, "BVB"])
print(arr.dtype)
