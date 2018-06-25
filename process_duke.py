import scipy.io as sio
import numpy as np
import pdb
from itertools import groupby
import operator as op
import pprint

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

# sort by frame # (camera id)
ind = np.lexsort((A[:, 0], A[:, 2],))
A = A[ind]

# build people list
people = [[] for i in range(0, 7141)]

for i in range(0, np.shape(A)[0]):
	people[(int)(A[i][1])].append(A[i][0])

# group by camera id
for i in range(0, len(people)):
	people[i] = [x[0] for x in groupby(people[i])]

# print(people)

# find most popular trajectories
trajs = {}

for i in range(0, len(people)):
	t = tuple(people[i])
	if t in trajs:
		trajs[t] = trajs[t] + 1
	else:
		trajs[t] = 1

trajs = sorted(trajs.items(), key=op.itemgetter(1), reverse=True)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(trajs[:11])

# compute camera matrix
matrix = np.zeros((num_cams, num_cams))

for i in range(0, len(people)):
	for j in range(0, len(people[i]) - 1):
		cam_1 = (int)(people[i][j]) - 1
		cam_2 = (int)(people[i][j+1]) - 1
		matrix[cam_1][cam_2] += 1

print(matrix)

# build people list, II
people = [[] for i in range(0, 7141)]

for i in range(0, np.shape(A)[0]):
	people[(int)(A[i][1])].append(A[i])

# compute camera matrix_t
times = [0.1, 0.2, 0.5, 1.0, 2.0, 10.0, 150.0]
fpm = 60 * 60
matrix_t = np.zeros((len(times), num_cams, num_cams))

for i in range(0, len(people)):
	for j in range(0, len(people[i]) - 1):
		cam_1 = (int)(people[i][j][0]) - 1
		cam_2 = (int)(people[i][j+1][0]) - 1
		if cam_1 == cam_2:
			continue
		frame_1 = people[i][j][2]
		frame_2 = people[i][j+1][2]
		for idx, t in enumerate(times):
			if frame_2 - frame_1 < (fpm * t):
				matrix_t[idx][cam_1][cam_2] += 1

for i in range(0, len(matrix_t)):
	print('Time (min.): ', times[i])
	np.set_printoptions()
	print(matrix_t[i])
	for j in range(0, len(matrix_t[i])):
		row_sum = sum(matrix_t[i][j])
		if row_sum != 0:
			matrix_t[i][j] /= row_sum
			matrix_t[i][j] *= 100.
	np.set_printoptions(formatter={'float': lambda x: "%06s" % "{0:2.2f}".format(x)})
	print(matrix_t[i])
