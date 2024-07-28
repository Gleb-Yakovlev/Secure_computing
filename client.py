from tkinter import*
import os
import socket
import threading
import RSA
import bits
import Elgamal
import time
import random
import sys

pid = os.getpid()
vOpenKey = []
validator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.bind(('localhost', 0))
print("client_socket port = ", client_socket.getsockname()[1])
window = Tk()

mArray = []
adressArray = []

stopFlag = True
validConnectFlag = True
agentConnectFlag = True
try:
    validator_socket.connect(('localhost', 12345))
except:
    print("The validator server is turned off")
    valid = Label(window, text="The validator server is turned off", font=("Arial Bold", 10))
    valid.pack(anchor=NW)
    validConnectFlag = False

try: 
    agent_socket.connect(('localhost', 23456))
except:
    print("The agent server is turned off")
    agent = Label(window, text="The agent server is turned off", font=("Arial Bold", 10))
    agent.pack(anchor=NW)
    agentConnectFlag = False
    

def Ready_for_the_election():
    print("Ready_for_the_election")
    validator_socket.send(("I want to vote"+"|SEP|"+str(pid)+"|SEP|"+str(client_socket.getsockname()[1])).encode())
    access = validator_socket.recv(1024)
    access = access.decode()
    access = res_mes(access, "|SEP|")
    if access[0]== "You can":
        global vOpenKey
        vOpenKey = list(map(int, access[1].split(";")))
        textL.configure(text = "Enter your value->")
        readyToElection.pack_forget()
        ballot.pack(anchor=CENTER)
        enterBallot.pack(anchor=CENTER)


    elif access[0] == "You don't have access":
        textL.configure(text = "You don't have access")

def Send_the_result():
    print("Send_the_result")
    
    ballot.pack_forget()
    enterBallot.pack_forget()
    textL.configure(text = "The voice is accepted, please wait, do not turn off the application.")
    
    m = ballot.get()
    if m == "":
        m = 0
    else: m = int(ballot.get())
    r = RSA.genR(vOpenKey[1])
    print("r = ", r)
    mm = RSA.masking_the_message(m, r, vOpenKey)
    print("mm = ", mm)
    
    mm = ';'.join(map(str, mm))
    mm += "|SEP|" + str(pid)
    print(mm)
    validator_socket.send(mm.encode())
    sig = validator_socket.recv(1024)
    sig = list(map(int, sig.decode().split(";")))
    print("sig =", sig)
    dem = RSA.demasking_message(sig, r, vOpenKey[1])
    print("dem = ", dem)
    mmm = RSA.get_message(dem, vOpenKey)
    print("mmm = ", mmm)
    if str(m) == str(mmm):
        print("sig all right")
    
    
    agent_socket.send("Request for a open key".encode())
    aOpenKey = agent_socket.recv(1024)
    aOpenKey = aOpenKey.decode()
    aOpenKey = list(map(int, aOpenKey.split(";")))
    print("aOpenKey = ", aOpenKey)
    elgamA, elgamB = Elgamal.get_encrypted_message(dem, aOpenKey)
    print("elgamM = " ,elgamA, elgamB)
    toAgentM = ((';'.join(map(str, elgamA))) +"|SEP|"+ (';'.join(map(str, elgamB))))
    mArray.append(toAgentM)
    print("toAgentM = ", toAgentM)
    threading.Thread(target=waiting_agent).start()


def waiting_agent():
    global agent_socket
    global stopFlag
    while stopFlag:
        print("waiting_agent = ", agent_socket)
        data = agent_socket.recv(1024)
        data = data.decode()
        print("Time is over", mArray, sys.getsizeof(mArray))
        print("data", data)
        if data == "Time is over":
            print("send mess to agent")
            string = '|SS|'.join(map(str, mArray))
            agent_socket.send(string.encode())
        else:
            print("give answer")
            textL.configure(text = "Answer = " + data)
            stopFlag = False
            agent_socket.close()
        
def validate(new_value):
    return new_value == "" or new_value.isnumeric()

def res_mes(mes, sep):
    return list(map(str, mes.split(sep)))

#server Space

def send_item(socket, item):
    socket.send(item.encode())

def send_array_to_agent():
    for item in mArray:
        send_item(agent_socket, item)
    mArray.clear()

def client_space(cl_socket, addr):
    data = cl_socket.recv(1024)
    data = data.decode()
    mArray.append(data)
    cl_socket.close()

def request_for_adresses():
    global adressArray
    adressArray.clear()
    validator_socket.send(("Request for addresses").encode())
    data = validator_socket.recv(1024)
    data = data.decode()
    adressArray = list(map(int, data.split(";")))
    if adressArray.count(int(client_socket.getsockname()[1])) > 0:
        adressArray.remove(int(client_socket.getsockname()[1]))
    
    
  
def send_func():
    global stopFlag
    while stopFlag:
        rand = random.randint(0, 1)
        if rand:
                if mArray:
                    request_for_adresses()
                    if adressArray:
                        mI = random.randrange(len(mArray))
                        mI = mArray.pop(mI)
                        aI = random.choice(adressArray)
                        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        cs.connect(('localhost', int(aI)))
                        send_item(cs, mI)
                        cs.close()
                        print("mArray = ", mArray)
        time.sleep(5)
        
        
def listen_func():
    print("Client listen....")
    client_socket.listen(10)
    while stopFlag:
        cl_socket, addr = client_socket.accept()
        print(f"The connection is established with {addr}")
        threading.Thread(target=client_space, args=(cl_socket, addr)).start()
        
threading.Thread(target=listen_func).start()
threading.Thread(target=send_func).start()
#server Space

window.title("Secure computing: elector")

pidL = Label(window, text="User ID = " + str(pid), font=("Arial Bold", 10))
pidL.pack(anchor=NE)

head = Label(window, text="Hello, take part in secure computing", font=("Arial Bold", 15))
head.pack(pady=20)

textL = Label(window, text="Click on the button when you are ready to vote", font=("Arial Bold", 12))
textL.pack(pady=20)

readyToElection = Button(window, text="Ready", command=(threading.Thread(target=Ready_for_the_election).start))
if validConnectFlag:
    readyToElection['state'] = 'normal'
else:
    readyToElection['state'] = 'disabled'
readyToElection.pack(pady=20)

vcmd = (window.register(validate), "%P")
ballot = Entry(window, width=10, validate='key', validatecommand=vcmd)
enterBallot = Button(window, text="Accept", command=(threading.Thread(target=Send_the_result).start))
if agentConnectFlag:
    enterBallot['state'] = 'normal'
else:
    enterBallot['state'] = 'disabled'
window.mainloop()

stopFlag = False
os.kill(pid, 9)