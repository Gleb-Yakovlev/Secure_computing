import os
import random
import mod


def write_new_arr(arr, lenght):
    dir = os.path.dirname(os.path.abspath(__file__))
    myFile = open(dir + "\\" + str(lenght) + ".txt", "w+")
    for i in arr:
        myFile.write(str(i)+'\n')
    myFile.close


def read_arr(name):
    dir = os.path.dirname(os.path.abspath(__file__))
    myFile = open(dir + "\\" + name, "r")
    arr = []
    while True:
        line = myFile.readline()
        if not line:
            break
        arr.append(int(line))
    return arr


def miller_rabin(n, lenght):
    t = n - 1
    s = 0
    while (t % 2 == 0):
        t /= 2
        s += 1
    for i in range(0, lenght, 1):
        a = random.randint(2, n-2)
        x = mod.exponentiation_modulo(a, t, n)
        if (x == 1 or x == n-1):
            continue
        for j in range(1, s, 1):
            x = mod.exponentiation_modulo(x, 2, n)
            if x == 1: return False
            if x == n-1: break
        if x != n-1: return False
    return True

def its_prime(num, lenght):
    if num == 0 or num == 1:
        return False
    simpArr = read_arr("simplePrimeN.txt")
    for i in simpArr:
        if num == i:
            return True
        if num % i == 0:
            return False
    if not miller_rabin(num, lenght): return False
    return True


def create_prime_list(lenght):
    arr = []
    for i in range((2**lenght), (2**(lenght+1)), 1):
        if (its_prime(i, lenght)):
            arr.append(i)
            #print(arr)
    write_new_arr(arr, lenght)


def findFile(name):
    dir = os.path.dirname(os.path.abspath(__file__))
    for files in os.walk(dir):
        if name in files[2]:
            return True
    return False


def get_prime_number(lenght):
    if (findFile(str(lenght)+".txt")):
        arr = read_arr(str(lenght)+".txt")
        return random.choice(arr)
    else:
        create_prime_list(lenght)
        get_prime_number(lenght)
    return 1

def get_big_prime_numb(lenght):
    lenght -= 1 
    r = random.randint((2**lenght), (2**(lenght+1))-1,)
    oldR = r
    right = True
    while(its_prime(r, lenght) != True):
        if right:
            r += 1
        else:
            r -=1
        if r == 2**(lenght+1)-1: 
            right = False
            r = oldR
    return r

#print(get_big_prime_numb(23))
# beg = time.time()
# print(get_big_prime_numb(18))
# end = time.time()
# print("Time = ", end-beg)

# beg = time.time()
# print(get_prime_number(18))
# end = time.time()
# print("Time = ", end-beg)
