#!/usr/bin/env python
import time
import random as rand
import numpy

def get_random_int ():
    return rand.randint(0, 10 ** 1)

def generate_matrix (n):
    output = numpy.random.randint(0, 10 ** 1, size=(n, n))
    print '[DONE]\tGenerated matrix of random integers'
    return output

def column_sum (matrix, m, n):
    return numpy.sum(matrix, axis=0)

def row_sum (matrix, m, n):
    return numpy.sum(matrix, axis=0)

def mat_mult (matrix, other_mat):
    return numpy.dot(matrix, other_mat)
    # return numpy.multiply(matrix, other_mat)

def break_matrix (matrix, t):
    output = []
    mat_div = len(matrix) / t

    if (t == 1):
        print '[WARN]\tReturn matrix as only one slave is to be used'
        return [matrix]

    output = numpy.array_split(matrix, t)

    print '[DONE]\tBroken down input matrix'

    return output

from mpi4py import MPI
import numpy
import sys

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
mat_size = int(sys.argv[1])
samp_vector = numpy.random.randint(0, 10 ** 1, size=(mat_size, 1))

if rank == 0:
    data = generate_matrix(mat_size)
    chunks = break_matrix(data, size)
    t = time.time()
    data = comm.scatter(chunks, root=0)
else:
    data = comm.scatter(None, root=0)

data = mat_mult(data, samp_vector)
if rank == 0: 
    mat_res = comm.gather(data, root=0)
    for i in range(0, len(mat_res)):
      mat_res[i] = row_sum(mat_res[i], len(mat_res), len(mat_res[i]))
    print "[TIME] " + str(time.time() - t)
else:
    mat_res = comm.gather(data, root=0)
