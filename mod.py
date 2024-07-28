import primeNumb

def gcd(num1, num2):
    while num1 != 0 and num2 != 0:
        if num1 >= num2:
            num1 %= num2
        else:
            num2 %= num1
    return num1 or num2


def lcm(a, b):
    return (a*b)/gcd(a, b)


def it_mutually_simple(n1, n2):
    if n1*n2 == lcm(n1, n2):
        return True
    else:
        return False

def create_a_mutually_prime_number(n):
    r = primeNumb.get_big_prime_numb(n.bit_length())
    while (not it_mutually_simple(r, n)):
        r = primeNumb.get_big_prime_numb(n.bit_length())
    return r

# def the_primitive_root(m):
#     '''
#     get m return g like
#     g**y(m) = 1 (mod m)
#     and 
#     g**l != 1 (mod m), 1 <= l < y(m)
#     '''
#     while True:
#         g = create_a_mutually_prime_number(m)
    
    
def primRoots(p):

    for g in range(2, p):
        if power_mod(g, p-1, p) == 1:
            primitive_root = True
            for j in range(1, p-1):
                if power_mod(g, j, p) == 1:
                    primitive_root = False
                    break
            if primitive_root:
                return g

    return None  # Примитивный корень не найден

def power_mod(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def extended_euclidean_algorithm(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_euclidean_algorithm(b % a, a)
        return (g, y - (b // a) * x, x)

def exponentiation_modulo(b, n, m):
    '''
    (b**n)%m
    '''
    return pow(int(b), int(n), int(m))
    # nn = 1
    # for i in range(1, n+1, 1):
    #     nn = (b*nn) % m
    # return nn


# def exponentiation_modulo(args):
#     '''
#     (b**n)%m
#     '''
#     b = args[0]
#     n = args[1]
#     m = args[2]
#     nn = 1
#     for i in range(1, n+1, 1):
#         nn = (b*nn) % m
#     return nn






import time
import numpy as np
import math
# def Exponentiation(args):

#     return a**b

def module(args):
    a = args[0]
    b = args[1]
    c = args[2]
    return pow(a, b, c)


def my_power(args):
    a = args[0]
    n = args[1]
    if n % 2 == 0:
        return (a**2)**(n/2)
    if n % 2 != 0:
        return a*pow(a, n-1)
    return a

def test1(args):
    a = args[0]
    b = args[1]
    c = args[2]
    return (a * b) % c

def test2(args):
    a = args[0]
    b = args[1]
    c = args[2]
    return pow(a*b, 1, c)

def timer(f, *arg):
    start = time.time()
    a = f(arg)
    end = time.time()
    print("Time is = ", end-start)
    return a

#timer(test2, 2843440, 2842440)
#timer(test1, 2843440, 2842440)
#print("a = ", timer(test2, 2843440, 2842440, 7988798798))
#print("a = ", timer(test1, 2843440, 2842440, 7988798798))

#primRoots(2555809)

#  #MOD = 1000000007
#     """
#     Returns the result of a^b i.e. a**b
#     We assume that a >= 1 and b >= 0

#     Remember two things!
#      - Divide power by 2 and multiply base to itself (if the power is even)
#      - Decrement power by 1 to make it even and then follow the first step
#     """
#     base = args[0]
#     power = args[1]
#     result = 1
#     while power > 0:
#         # If power is odd
#         if power % 2 == 1:
#             result = (result * base)

#         # Divide the power by 2
#         power = power // 2
#         # Multiply base to itself
#         base = (base * base)

#     return result