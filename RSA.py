import bits
import mod
from primeNumb import primeNumb


def findE(eler):
    ferma = [3, 17]
    for i in ferma:
        if mod.it_mutually_simple(i, eler):
            return i
    return 0


def findD(phi_n, e):
    gcd, x, y = mod.extended_euclidean_algorithm(e, phi_n)

    if gcd != 1:
        print("e and phi(n) must be mutually simple")

    d = x % phi_n
    return d


def getKeys(lenght):
    
    p, q = genPQ(lenght)
    n = p*q
    eler = (p-1)*(q-1)
    e = findE(eler)
    while e == 0:
        p, q = genPQ(lenght)
        n = p*q
        eler = (p-1)*(q-1)
        e = findE(eler)
    
    d = findD(eler, e)
    openKey = [e, n]
    closeKey = [d, n]
    return openKey, closeKey


def RSA_get_encrypted_message(openKey, m):
    '''
    get message, string to array int
    '''
    
    if type(m) is int:
        return (m**openKey[0])%openKey[1]
    
    if type(m) is str:
        arr = bits.text_to_int(m)
        shifrArr = []
        for item in arr:
            shifrArr.append((item**openKey[0]) % openKey[1])
        return shifrArr


def RSA_decrypt_the_message(closeKey, shifrArr):
    if type(shifrArr) is int:
        return mod.exponentiation_modulo(shifrArr, closeKey[0], closeKey[1])
    
    if type(shifrArr) is list:
        deShifrArr = []
        for item in shifrArr:
            deShifrArr.append(mod.exponentiation_modulo(
                item, closeKey[0], closeKey[1]))
        mText = bits.int_to_text(deShifrArr)
        return mText


def genPQ(lenght):
    p = primeNumb.get_big_prime_numb(lenght)
    q = primeNumb.get_big_prime_numb(lenght)
    while p == q:
        q = primeNumb.get_big_prime_numb(lenght)
    return p, q


def genR(n):
    r = primeNumb.get_big_prime_numb(n.bit_length())
    while (not mod.it_mutually_simple(r, n)):
        r = primeNumb.get_big_prime_numb(n.bit_length())
    return r


def masking_the_message(m, r, openKey):
    '''
    m' = m*r**e mod n 
    '''
    m = bits.text_to_int(str(m))
    shifrArr = []
    for item in m:
        shifrArr.append(
            item * mod.exponentiation_modulo(r, openKey[0], openKey[1])% openKey[1] ) 
    return shifrArr


def creating_a_signature(mm, closeKey):
    '''
    s' = m'**d mod p
    '''
    deShifrArr = []
    for item in mm:
        deShifrArr.append(mod.exponentiation_modulo(
            item, closeKey[0], closeKey[1]))
    return deShifrArr


def demasking_message(mm, r, p):
    '''
    s = s'*r**-1 mod p
    '''
    s = []
    gcd, x, y = mod.extended_euclidean_algorithm(r, p)
    x = x % p
    for item in mm:
        s.append((item * x)%p)  
    return s

def get_message(m, openKey):
    getM = []
    for item in m:
        getM.append(mod.exponentiation_modulo(item, openKey[0], openKey[1]))
    getM = bits.int_to_text(getM)
    return getM


# m = "Hello world!"
# print("Message = ", m)
# openKey, closeKey = getKeys(11)
# print("openKey = ", openKey)
# print("closeKey = ", closeKey)
# # shifrArr = RSA_get_encrypted_message(openKey, m)
# # print("Encrypted message = ", shifrArr)
# # deshifrArr = RSA_decrypt_the_message(closeKey, shifrArr)
# # print("Decrypted message = ", deshifrArr)

# r = genR(openKey[1])
# print("R = ", r)
# shifrArr = masking_the_message(m, r, openKey)
# print("Masking message = ", shifrArr)
# sigMessage = creating_a_signature(shifrArr, closeKey)
# print("Signed message = ", sigMessage)
# demM = demasking_message(sigMessage, r, openKey[1])
# print("The unmasking message = ", demM)
# gettedMessage = get_message(demM, openKey)
# print("The original message = " + m + "; The received message = ", gettedMessage)


# print("p = ", p)
# print("q = ", q)
# eler = (p-1)*(q-1)
# print("eler = ", eler)
# e = findE(eler)
# print("e = ", e)
# d = findD(eler, e)
# print("d = ", d)


# def exponentiation_modulo(b, n, m):
#     '''
#     (b**n)%m
#     '''
#     nn = 1
#     for i in range(1, n+1, 1):
#         nn = (b*nn) % m
#     return nn

# def RSA_get_encrypted_message_int(openKey, m):
#     '''get int return int'''
#     return (m**openKey[0])%openKey[1]

# def RSA_decrypt_the_message_int(closeKey, m):
#     '''get int return int'''
#     return mod.exponentiation_modulo(m, closeKey[0], closeKey[1])
# def gcd(num1, num2):
#     while num1 != 0 and num2 != 0:
#         if num1 >= num2:
#             num1 %= num2
#         else:
#             num2 %= num1
#     return num1 or num2


# def lcm(a, b):
#     return (a*b)/gcd(a, b)


# def it_mutually_simple(n1, n2):
#     if n1*n2 == lcm(n1, n2):
#         return True
#     else:
#         return False


# def extended_euclidean_algorithm(a, b):
#     if a == 0:
#         return (b, 0, 1)
#     else:
#         g, x, y = extended_euclidean_algorithm(b % a, a)
#         return (g, y - (b // a) * x, x)


# print("p = ", p)
#     print("q = ", q)
#     print("eler = ", eler)
#     print("e = ", e)
#     print("d = ", d)
#     print("Open Key = {", e, ";", n, "}")
#     print("Close Key = {", d, ";", n, "}")

# bit = bits.text_to_bit(m)
# print("text to bit = ", bit)

# text = bits.bit_to_text(bit)
# print("bit tot text = ", text)

    # deShifrArr.append((item**d)%n)

# arr = []
# for i in range(0, len(str(m)), lenN):
#     arr.append(int(str(m)[:lenN]))
#     if len(str(m)) >= lenN:
#         m = int(str(m)[lenN:])
#     print(m)
# print(arr)

# input("Press Enter to continue...")
