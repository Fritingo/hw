import random as rd

def verifier(C, y, g, p):
    e = rd.randint(1,100)
    t = yield e

    if (g**t == (y**e)*C):
        accept = 1
    else:
        accept = 0

    yield accept