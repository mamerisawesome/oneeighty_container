#!/usr/bin/env python
import time
import random as rand
import thread
import json
import numpy
import multiprocessing
import threading
import psutil

def get_random_int ():
    return rand.randint(0, 10 ** 1)

def generate_matrix (n):
    output = numpy.random.randint(0, 10 ** 1, size=(n, n))
    print '[DONE]\tGenerated matrix of random integers'
    return output

def column_sum (matrix, m, n, index=0, parallel=False):
    if (parallel):
        global final_vector

    output = []

    for i in range(0, m):
        sum_v = 0
        for j in range(0, n):
            sum_v += int(matrix[i][j])
        output += [sum_v]

    if (parallel):
        for i in range(0, len(output)):
            final_vector += [output[i]]

    return output

def break_matrix (matrix, t):
    output = []
    mat_div = len(matrix) / t

    if (t == 1):
        print '[WARN]\tReturn matrix as only one thread is to be used'
        return [matrix]

    if (len(matrix) % t != 0):
        print '[WARN]\tCannot subdivide matrix'
        return [matrix]

    output = numpy.hsplit(matrix, t)

    print '[DONE]\tBroken down input matrix'

    return output

from mpi4py import MPI
import numpy
import sys

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

final_vector = None
sendbuf = None

if rank == 0:
    sendbuf = generate_matrix(mat_size)
    sendbuf = break_matrix(sendbuf, size - 1)
    final_vector = []
    for i in range(0, size-1):
      print "[0] Sending to " + str(i)
      recvbuf = comm.send({
        data: sendbuf[i],
        size: 
      }, dest=i+1, tag=i+1)
else:
    while not comm.Iprobe(source=0, tag=rank):
        print "[" + str(rank) + "] Listening to root"
        time.sleep(1)
    recvbuf = comm.recv(source=0, tag=rank)
    column_sum(recvbuf, )

comm.bcast(recvbuf, root=0)

