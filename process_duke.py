import scipy.io as sio
import numpy as np
import pdb
from itertools import groupby

A = sio.loadmat('ground_truth/trainval')
A = A['trainData']

print(np.shape(A))

# build histogram
x_edges = range(1, 10, 1)
y_edges = range(1, 7142, 1)

hist = np.histogram2d(A[:, 0], A[:, 1], bins=(x_edges, y_edges))
# print(hist)

# sort by person id (camera id, frame #) data
A = A[np.lexsort((A[:, 2], A[:, 0], A[:, 1]))]

# from http://vision.cs.duke.edu/DukeMTMC/details.html
cam_offsets = [5542, 3606, 27243, 31181, 0, 22401, 18967, 46765]
num_cams = len(cam_offsets)

# adjust frame #s
for i in range(0, np.shape(A)[0]):
	cam_id = (int)(A[i][0]) - 1
	A[i][2] += cam_offsets[cam_id]

# sort by frame id (camera id)
ind = np.lexsort((A[:, 0], A[:, 2],))
A = A[ind]

# init people list
people = [[] for i in range(0, 7141)]

# build people list
for i in range(0, np.shape(A)[0]):
	people[(int)(A[i][1])].append(A[i][0])

# group by camera id
for i in range(0, len(people)):
	people[i] = [x[0] for x in groupby(people[i])]

# print(people)

# init camera matrix
matrix = np.zeros((num_cams, num_cams))

# compute camera matrix
for i in range(0, len(people)):
	for j in range(0, len(people[i]) - 1):
		cam_1 = (int)(people[i][j]) - 1
		cam_2 = (int)(people[i][j+1]) - 1
		matrix[cam_1][cam_2] += 1

print(matrix)