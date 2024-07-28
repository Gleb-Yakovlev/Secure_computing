
import random
from primeNumb import primeNumb
import mod
import bits
import math


import time
def getKeys(n):
    '''
    return openKey[y, g, p]
           closeKey[x]
    '''
    p = primeNumb.get_big_prime_numb(n)
    g = mod.primRoots(p)
    x = random.randint(1, p-2)
    y = pow(g, x, p)
    openKey = [p, g, y]
    closeKey = x
    return openKey, closeKey

# def timer(f, *arg):
#     start = time.time()
#     a = f(arg)
#     end = time.time()
#     print("Time is = ", end-start)
#     return a


def get_encrypted_message(m, openKey):
    '''
    return a, b 
    a = (g**k) mod p
           b = M*(y**k) mod p
    '''
    p, g, y = openKey
    
    
    if type(m) is int:  
        k = random.randint(1, int(p)-1)
        while(mod.gcd(k, p-1) != 1):
            k = random.randint(1, int(p)-1)   
        a= pow(g, k, p)
        m * (pow(y, k, p))
        return a, b

    if type(m) is str:     
        m = bits.text_to_int(m)

    if type(m) is list:
        a = []
        b = []     
        for item in m:
            k = random.randint(1, int(p)-1)
            while(mod.gcd(k, p-1) != 1):
                k = random.randint(1, int(p)-1) 
            a.append(pow(g, k, p))
            b.append(item * (pow(y, k, p)))
        return a, b

def demasking_message_int(a, b, x, p):
    '''
    M = b*(a**x)**-1 mod p
    get b, a**x, p
    '''
    return b*pow(a, p-1-x, p)%p

def get_decrypt_the_message(a, b, openKey, closeKey):
    if type(a) is int and type(b) is int:    
        return(demasking_message_int(a, b, closeKey, openKey[0]))
    if type(b) is list:
        m = []
        for i in range(0, len(b), 1):
            m.append(demasking_message_int(a[i], b[i], closeKey, openKey[0]))
        return m


# p = [1 ,2 ,3 ,4 ]
# if type(p) is list:
#     print("asdasd")
# print(type(p))

# import RSA
# import time
# m = "123"
# print("m = ", m)

# sOK, sCK = RSA.getKeys(11)
# print("sOK = ", sOK)
# print("sCK = ", sCK)
# r = RSA.genR(sOK[1])
# shifrArr = RSA.masking_the_message(m, r, sOK)
# print("r = ", r)
# print("shfr arr = ", shifrArr)
# sigMessage = RSA.creating_a_signature(shifrArr, sCK)
# print("sig m = ", sigMessage)
# demM = RSA.demasking_message(sigMessage, r, sOK[1])
# print("Dem m = ", demM)
# gettedMessage = RSA.get_message(demM, sOK)
# print("gettedMessage = ", bits.int_to_text(gettedMessage))
# m = demM

# m = "Hello world!"
# print("The original message - ", m)
# bm = bits.text_to_int(m)
# openKey, closeKey = getKeys(22) 
# #print("openKey = [p, g, y]")
# print("openKey = ", openKey)
# #print("closeKey = [x]")
# print("closeKey = ", closeKey)
# a, b = get_encrypted_message(bm, openKey)
# print("a = ", a)
# print("b = ", b)
# mm = get_decrypt_the_message(a, b, openKey, closeKey)
# mm = bits.int_to_text(mm)
# print("Encrypted and decrypted message - ", mm)

#     print("mm = ", mm)
# for i in range(1,10, 1):
#     a, b = get_encrypted_message(m, openKey)
#     print("a = ", a)
#     print("b = ", b)
#     mm = get_decrypt_the_message(a, b, openKey, closeKey)

#     print("mm = ", mm)
    


    # roots = []
    # required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)

    # for g in range(1, modulo):
    #     actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
    #     #return g
    #     if required_set == actual_set:
    #         #roots.append(g)
    #         return g           
    # return roots