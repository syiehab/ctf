from sympy import isprime
import random

while True:
    k = random.getrandbits(135)
    p = 6*k+1
    q = 12*k+1
    r = 18*k+1
    if isprime(p) and isprime(q) and isprime(r):
        n = p*q*r
        print(f'{n=}')
        print(f'{p=}')
        print(f'{q=}')
        print(f'{r=}')
        break