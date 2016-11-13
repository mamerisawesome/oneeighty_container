import time
import random as rand

final_sum = 0

def get_random_int ():
    return rand.randint(0, 10 ** 6)

def generate_matrix (n):
    output = []

    for i in range (0, n):
        ioutput = []
        for j in range(0, n):
            ioutput += [get_random_int()]
        output += [ioutput]
    return output

def v_func (matrix, y):
    x = len(matrix)

    output = []
    sum_v = 0

    for i in range(0, x):
        if (i < x): break

        sum_v += matrix[i][y]
    
    return sum_v

def column_sum (matrix, m, n):
    output = []

    for i in range(0, n):
        output += [v_func(matrix, i)]

    return output

def break_matrix (matrix, t):
    '''
        n x n
        [
            ...
        ]

        4 x 4
        2 thread

        4 x (4 / 2)

        4 x (4 x 4)
    
        [
            [1, 2, 3, 1],
            [4, 5, 6, 1],
            [7, 8, 9, 1],
            [5, 4, 6, 1]
        ]

        4 x 2
        [
            [1, 2],
            [4, 5],
            [7, 8],
            [5, 4]
        ]

        [
            [3, 1],
            [6, 1],
            [9, 1],
            [6, 1]
        ]
    '''
final_sum = 0

def get_random_int ():
    return rand.randint(0, 10 ** 6)

def generate_matrix (n):
    output = []

    for i in range (0, n):
        ioutput = []
        for j in range(0, n):
            ioutput += [get_random_int()]
        output += [ioutput]
    return output

def v_func (matrix, y):
    x = len(matrix)

    output = []
    sum_v = 0

    for i in range(0, x):
        if (i < x): break

        sum_v += matrix[i][y]
    
    return sum_v

def column_sum (matrix, m, n):
    output = []

    for i in range(0, n):
        output += [v_func(matrix, i)]

    return output

def break_matrix (matrix, t):
    '''
        n x n
        [
            ...
        ]

        4 x 4
        2 thread

        4 x (4 / 2)

        4 x (4 x 4)
    
        [
            [1, 2, 3, 1],
            [4, 5, 6, 1],
            [7, 8, 9, 1],
            [5, 4, 6, 1]
        ]

        4 x 2
        [
            [1, 2],
            [4, 5],
            [7, 8],
            [5, 4]
        ]

        [
            [3, 1],
            [6, 1],
            [9, 1],
            [6, 1]
        ]
    '''
    output = []
    mat_div = len(matrix) / t

    if (len(matrix) % t == 0):
        print('[WARN]\tCannot subdivide matrix')
        return [matrix]
    
    for x in range(0, len(matrix), mat_div):
        xoutput += []
        for i in range(0, len(matrix)):
            ioutput = []
            for j in range(x, x + mat_div):
                ioutput += [matrix[j][i]]
            xoutput += [ioutput]
        output += xoutput

    return output

def lab01 ():
    n = int(raw_input("Enter size of square matrix\t\t>> "))

    matrix = generate_matrix(n)

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            print '[*]' + str(matrix[j][i])

    s_time = time.clock()
    column_sum(matrix, n, n)
    e_time = time.clock()

    return e_time - s_time

def lab02 ():
    n = int(raw_input("Enter size of square matrix\t\t>> "))
    t = int(raw_input("Enter number of threads to be used\t>> "))

    v = []

    matrix = generate_matrix(n)

    s_time = time.clock()

    # insert column_sum logic here

    e_time = time.clock()

    return

def lab01 ():
    n = int(raw_input("Enter size of square matrix\t\t>> "))

    matrix = generate_matrix(n)

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            print '[*]' + str(matrix[j][i])

    s_time = time.clock()
    column_sum(matrix, n, n)
    e_time = time.clock()

    return e_time - s_time

def lab02 ():
    n = int(raw_input("Enter size of square matrix\t\t>> "))
    t = int(raw_input("Enter number of threads to be used\t>> "))

    v = []

    matrix = generate_matrix(n)

    s_time = time.clock()

    # insert column_sum logic here

    e_time = time.clock()

    return

print lab01()
print lab02()
