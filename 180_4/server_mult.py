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

def start_server (sock, matrix):
    time_before = time.clock()
    time_after = 0

    sock.listen(5)

    n = int(sys.argv[3])
    matrix = generate_matrix(n)

    # matrix = break_matrix(matrix, len(fa))

    print '[EXEC] Listening'

    while True:
        c, addr = sock.accept()
        print 'Got connection from', addr

        s_flag = 0
        data = json.dumps(matrix.tolist())

        c.sendall(str(len(data)) + '|' + data)
        c.close()

        s_flag = 1
                
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
        sock, host, port = set_credentials(p)
        print '[CRED] Host:', host
        print '[CRED] Port:', port
        sock.bind((host, port))
        return start_server(sock, fa)

    ### IF CLIENT
    elif (s == 1):
        for i in range(0, len(fa)):
            sock, host, port = set_credentials(fa[i][1])
            # host = fa[i][0]

            print sock, host, port

            sock.connect((host, port))
            start_client(sock)
        
        return "[DONE] Listening to server"

    #### IF ERROR
    print '[ERRR] You did something wrong'
    sock.close()
    sys.exit(1)

time_elapsed = lab04()
print 'Elapsed: ' + str(time_elapsed)