# for benchmarking
import time

# for dataset
import random as rand

# for data processing
import numpy
import json

# for multithreading
import multiprocessing
from multiprocessing import Manager, Value

# for core-affinity
import psutil

# for socket
import socket
import sys

# for interface
import flask

final_vector = []
comp_flag = 0
fa = []

def get_random_int ():
    return rand.randint(0, 10 ** 1)

def generate_matrix (n):
    output = numpy.random.randint(0, 10 ** 1, size=(n, n))
    print '[DONE]\tGenerated matrix of random integers'
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

def read_conf ():
    file = open('CONF.txt')

    fd = file.read()
    fa = fd.split('\n')
    for i in range(0, len(fa)):
        fa[i] = fa[i].split(' ')
        fa[i][1] = int(fa[i][1])

    file.close()

    return fa

def update_conf (fa, addr):
    for i in range(0, len(fa)):
        if (fa[i][0] == addr):
            fa[i] = ['0', 0]
            break
    
    return fa

def get_credentials ():
    s = int(sys.argv[1])
    # s = int(raw_input('Enter status of the instance\t\t>> '))
    if (not(s == 0 or s == 1)):
        print '[ERRR] Cannot identify if client or server'
        sys.exit(1)

    p = int(sys.argv[2])
    # p = int(raw_input('Enter port number\t\t\t>> '))

    return (s, p)

def set_credentials (p):
    sock = socket.socket()
    host = sock.getsockname()[0]
    port = p
    return (sock, host, p)

def send_data (fa, comp_flag, i, p, matrix):
    sock, host, port = set_credentials(p)
    try:
        sock.bind((fa.value[i][0], fa.value[i][1]))
    except:
        print '[ERR] Client can\'t connect'
        return '[ERR] Client can\'t connect'

    sock.listen(5)
    c, addr = sock.accept()

    print '[ CLIENT ', i, ' ] ', 'Got connection from', addr
    if (addr[0] == fa.value[i][0]):
        if (len(matrix) == 1):
            data = json.dumps(matrix[0].tolist())
        else:
            data = json.dumps(matrix[i].tolist())

        fa.value = update_conf(fa.value, addr[0])

        c.sendall(str(len(data)) + '|' + data)
        c.close()

        comp_flag.value += 1
        return (comp_flag.value, fa.value)
    else:
        c.sendall('ERRNULLCLIENT')
        c.close

        comp_flag.value += 1
        return 'ERRNULLCLIENT'

def start_server (p, fa):
    n = int(sys.argv[3])
    
    matrix = generate_matrix(n)
    matrix = break_matrix(matrix, len(fa))
    
    time_before = time.clock()
    time_after = 0

    fa = Manager().Value('0', fa)
    comp_flag = Manager().Value('0', 0)
    for i in range(0, len(fa.value)):
        proc = multiprocessing.Process(target=send_data, args=(fa, comp_flag, i, p, matrix))
        cpu_num = int(str(i % multiprocessing.cpu_count())[0])
        psutil.Process(pid=proc.pid).set_cpu_affinity([cpu_num])

        proc.start()
                
    while True:
        if (comp_flag.value == len(fa.value)):
            time_after = time.clock()
            print '[DONE] Matrix sent to all clients'
            print '[DONE] Closing server now'
            return (time_after - time_before)

def start_client (sock):
    time_before = time.clock()    
    raw_data = ''
    while 1:
        recvd = sock.recv(1024 * 6)
        if (recvd == 'ERRNULLCLIENT'):
            print '[ERRR] Forbidden'
            sock.close()
            sys.exit(1)

        raw_data += recvd
        if (not recvd): break

    size = raw_data.split('|')[0]
    data = raw_data.split('|')[1]

    size = int(size)
    if (size != len(data)):
        print '[ERRR] Data loss'
        sock.close()
        return 0

    data = numpy.matrix(json.loads(data))
    time_after = time.clock()    
    print '[DONE] Data sent successfully'

    sock.close()
    return (time_after - time_before)

def lab04 ():
    global final_vector
    global fa
    cpus_count = multiprocessing.cpu_count()
    final_vector = []

    ### GET INPUT DATA
    s, p = get_credentials()

    ### GET CONFIGURATION
    fa = read_conf()

    ### IF SERVER
    if (s == 0): 
        return start_server(p, fa)

    ### IF CLIENT
    elif (s == 1):
        sock, host, port = set_credentials(p)
        sock.connect((host, port))
        return start_client(sock)

    #### IF ERROR
    print '[ERRR] You did something wrong'
    sock.close()
    sys.exit(1)

time_elapsed = lab04()
print 'Elapsed: ' + str(time_elapsed)