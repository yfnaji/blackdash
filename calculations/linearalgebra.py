import numpy as np
from math import sqrt


def laguerre_matrix(payoffs, bases):
    
    matrix = []
    for i in range(len(payoffs)):
        row = []
        for j in range(bases):

            if j == 0:
                row.append(1.0)
            elif j == 1:
                row.append(1.0 - payoffs[i])
            else:
                L = (2 * (j - 1) + 1 - payoffs[i]) * row[j-1]
                L -= (j - 1) * row[j-2]
                L /= j
                row.append(L)
        matrix.append(row)
    return np.array(matrix)


def matrix_multiply(A, B):

    matrix = []
    rows, mult, cols = A.shape[0], 1 if B.shape[0] == 1 else A.shape[1], B.shape[1]

    for i in range(rows):
        row = []
        for j in range(cols):
            entry = 0
            for s in range(mult):
                entry += A[i, s] * B[s, j]
            row.append(entry)
        matrix.append(row)
    return np.array(matrix)

def matrix_multiply_vector(A, b):
    
    vector = []

    for i in range(A.shape[0]):
        entry = 0
        for j in range(len(b)):
            entry += A[i, j] * b[j]
        vector.append(entry)

    return np.array(vector)


def dot_product(a, b):
    dot = 0.0
    for i in range(len(a)):
        dot += a[i] * b[i]
    return dot

def normalize_vector(a):
    norm = 0
    for i in range(len(a)):
        norm += a[i] ** 2
    return a / sqrt(norm)

def QR_decomposition(A):

    Q = np.array([[0 for x in range(A.shape[0])] for y in range(A.shape[0])], dtype=float)
    R = np.array([[0 for x in range(A.shape[0])] for y in range(A.shape[0])], dtype=float)
    for i in range(A.shape[0]):
        e = A[:, i]
        for j in range(i):
            e = e - dot_product(e, Q[:, j]) * Q[:, j]
        e = normalize_vector(e)
        Q[:,i] = e 

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if j >= i:
                R[i, j] = dot_product(Q[:, i], A[:, j])
    return Q, R

def upper_triangular_inverse(A):
    n = A.shape[0]
    x = np.array([0 for x in range(n)])
    Inv = np.array([[0 for x in range(n)] for y in range(n)])
    entry = 0.0

    for r in range(n - 1, -1, -1):
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                entry += A[i, j] * x[j]
            if i == r:
                entry = (1.0 / A[i, i]) * (1.0 - entry)
            else:
                entry = - (1.0 / A[i, i]) * entry
            
            x[i] = entry
            entry = 0.0
        Inv[:, r] = x

    return Inv

def transpose(A):
    
    n, m = A.shape
    B = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            B[i, j] = A[j, i]
    return B
