import random as rd

def prover(x, g, p):
    r = rd.randint(1,100)
    C = g**r
    e = yield C
    t = e*x + r
    yield t