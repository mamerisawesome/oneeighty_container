# for benchmarking
import time

# for dataset
import random as rand

# for data processing
import numpy
import json

# for multithreading
import multiprocessing

# for core-affinity
import psutil

# for socket
import socket
import sys

# for interface
import flask

final_vector = []

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

def get_credentails ():
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
    host = socket.gethostname()
    port = p
    return (sock, host, p)

def start_server (p, fa):
    n = int(sys.argv[3])
    # n = int(raw_input('Enter size of square matrix\t\t>> '))
    
    matrix = generate_matrix(n)
    matrix = break_matrix(matrix, len(fa))
    
    time_before = time.clock()
    time_after = 0

    comp_flag = 0
    while True:
        for i in range(0, len(fa)):
            sock, host, port = set_credentials(p)
            sock.bind((fa[i][0], fa[i][1]))
            sock.listen(5)
            c, addr = sock.accept()

            s_flag = 0
            print '[ CLIENT ', i, ' ] ', 'Got connection from', addr
            if (addr[0] == fa[i][0]):
                if (len(matrix) == 1):
                    data = json.dumps(matrix[0].tolist())
                else:
                    data = json.dumps(matrix[i].tolist())

                fa = update_conf(fa, addr[0])

                c.sendall(str(len(data)) + '|' + data)
                c.close()

                s_flag = 1
                comp_flag += 1
                
                if (comp_flag == len(fa)):
                    time_after = time.clock()
                    print '[DONE] Matrix sent to all clients'
                    print '[DONE] Closing server now'
                    c.close()
                    return (time_after - time_before)
                    
                break

        if (s_flag == 0):
            c.sendall('ERRNULLCLIENT')
            c.close

        s_flag = 0

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
    cpus_count = multiprocessing.cpu_count()
    final_vector = []

    ### GET INPUT DATA
    s, p = get_credentails()

    ### GET CONFIGURATION
    fa = read_conf()

    ### IF SERVER
    if (s == 0): 
        ### SET CREDENTIALS
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