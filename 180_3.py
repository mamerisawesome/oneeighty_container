import time
import random as rand
import thread
import json
import numpy
import multiprocessing
import threading
import psutil

final_vector = []

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

def lab01 ():
    n = int(raw_input("Enter size of square matrix\t\t>> "))

    matrix = generate_matrix(n)

    s_time = time.clock()
    column_sum(matrix, n, n)
    e_time = time.clock()

    return e_time - s_time

def lab02 ():
    global final_vector

    final_vector = []
    n = int(raw_input("Enter size of square matrix\t\t>> "))
    t = int(raw_input("Enter number of threads to be used\t>> "))

    v = []
    thread_group = []

    matrix = generate_matrix(n)
    submat = break_matrix(matrix, t)
    t = len(submat)

    for i in range(0, n):
        final_vector += [0]
        thread_group += [0]

    s_time = time.clock()

    for i in range(0, t):
        params = json.dumps((submat[i], n, n/t, i))
        thread_group[i] = threading.Thread(target=column_sum, name='t' + str(i), args=([str(params), True]))
        thread_group[i].start()
        thread_group[i].join()

    e_time = time.clock()

    return e_time - s_time

def lab03 ():
    global final_vector

    cpus_count = multiprocessing.cpu_count()

    final_vector = []
    n = int(raw_input('Enter size of square matrix\t\t>> '))
    t = int(raw_input('Enter number of threads to be used\t>> '))

    v = []
    thread_group = []

    matrix = generate_matrix(n)
    submat = break_matrix(matrix, t)
    t = len(submat)

    s_time = time.time()

    # create and execute threads
    for i in range(0, t):
        thread_group += [multiprocessing.Process(target=column_sum, name='t' + str(i), args=(submat[i], n, n/t, i, True))]
        cpu_num = int(str(i % cpus_count)[0])
        psutil.Process(pid=thread_group[i].pid).set_cpu_affinity([cpu_num])

        thread_group[i].start()

    # make sure that all threads are done executing
    for i in range(0, t):
        thread_group[i].join()

    e_time = time.time()

    return e_time - s_time

time_e = lab03()
print 'Time elapsed:', time_e