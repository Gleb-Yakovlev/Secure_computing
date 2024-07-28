
import random
from primeNumb import primeNumb
import mod
import bits
import math
import RSA


import time



def getKeys(n):
    '''
    return openKey[y, g, p]
           closeKey[x]
    '''
    n = n[0]
    
    p = primeNumb.get_big_prime_numb(n)
    #p = timer(primeNumb.get_big_prime_numb,n)
    g = mod.primRoots(p)
    #g = timer(mod.primRoots, p)
    x = random.randint(1, p-2)
    #y = (g**x)%p
    y = pow(g, x, p)
    openKey = [p, g, y]
    closeKey = x
    return openKey, closeKey

def timer(f, *arg):
    start = time.time()
    a = f(arg)
    end = time.time()
    print("Time is = ", end-start)
    return a


def get_encrypted_message(args):
    '''
    return a, b 
    a = (g**k) mod p
           b = M*(y**k) mod p
    '''
    m = args[0]
    openKey = args[1]
    
    p, g, y = openKey
    k = random.randint(1, int(p)-1)
    while(mod.gcd(k, p-1) != 1):
        k = random.randint(1, int(p)-1)
    
    if type(m) is int:     
        #a = (g**k) % p
        a= pow(g, k, p)
        #b = m * (y**k) % p
        m * (pow(y, k, p))
        return a, b

    if type(m) is str:     
        m = bits.text_to_int(m)

    if type(m) is list:
        start = time.time()
        #a = (g**k) % p
        a= pow(g, k, p)
        end = time.time()
        print("a = (g**k) % p = ", end-start)
        b = []     
        for item in m:
            #start = time.time()
            #b.append(item * (y**k) % p)
            b.append(item * (pow(y, k, p)))
            #end = time.time()
           # print("b.append(item * (y**k) % p) = ", end-start)
        return a, b

# def demasking_message_int(mm, r, p):
#     '''
#     M = b*(a**x)**-1 mod p
#     get b, a**x, p
#     '''
#     gcd, x, y = mod.extended_euclidean_algorithm(r, p)
#     x = x % p
#     # s = ((mm * x)%p)  
#     # return s


def demasking_message_int(a, b, x, p):
    '''
    M = b*(a**x)**-1 mod p
    get b, a**x, p
    '''
    
    return b*pow(a, p-1-x, p)%p

def get_decrypt_the_message(arg):
    a = arg[0]
    b= arg[1]
    openKey = arg[2]
    closeKey = arg[3]
    
    if type(a) is int and type(b) is int:    
        return(demasking_message_int(a, b, closeKey, openKey[0]))
    if type(b) is list:
        m = []
        for item in b:
            #m.append(demasking_message_int(item, pow(a, closeKey), openKey[0]))
            m.append(demasking_message_int(a, item, closeKey, openKey[0]))
        #print("M = ", m)
        return m


# p = [1 ,2 ,3 ,4 ]
# if type(p) is list:
#     print("asdasd")
# print(type(p))

# import RSA
# import time
#m = "123"
#print("m = ", m)
m = "9999"
sOK, sCK = RSA.getKeys(11)
print("sOK = ", sOK)
print("sCK = ", sCK)
r = RSA.genR(sOK[1])
shifrArr = RSA.masking_the_message(m, r, sOK)
print("r = ", r)
print("shfr arr = ", shifrArr)
sigMessage = RSA.creating_a_signature(shifrArr, sCK)
print("sig m = ", sigMessage)
demM = RSA.demasking_message(sigMessage, r, sOK[1])
print("Dem m = ", demM)
gettedMessage = RSA.get_message(demM, sOK)
print("gettedMessage = ", bits.int_to_text(gettedMessage))
m = demM

#m = "9999"
openKey, closeKey = timer(getKeys,22) 
print("openKey = [p, g, y]")
print("openKey = ", openKey)
print("closeKey = [x]")
print("closeKey = ", closeKey)
a, b = timer(get_encrypted_message, m, openKey)
print("a = ", a)
print("b = ", b)
mm = timer(get_decrypt_the_message, a, b, openKey, closeKey)
print("mm = ", mm)

gettedMessage = RSA.get_message(mm, sOK)
print("gettedMessage = ", bits.int_to_text(gettedMessage))

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