import scipy.io as sio
import numpy as np

A = sio.loadmat('ground_truth/trainval')
A = A['trainData']

print(np.shape(A))

x_edges = range(1, 10, 1)
y_edges = range(1, 7142, 1)

hist = np.histogram2d(A[:, 0], A[:, 1], bins=(x_edges, y_edges))
print(hist)