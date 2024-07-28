import socket
import threading
import Elgamal
import bits
import RSA
import time
import datetime

openKey, closeKey = Elgamal.getKeys(23)
print("openKey = ", openKey)
print("closeKey = ", closeKey)
vOpenKey = []
agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

finalArray = []
superFinalyArray = []

stopFlag = True

agent_socket.bind(('localhost', 23456))
agent_socket.listen(10)
print("Agent ready and listen...")

def user_work_space(client_socket, addr):
        try:
            data = client_socket.recv(1024)
        except:
            print("The client has disconnected")
            global socketArray
            socketArray.remove(client_socket)
            print("Remove ", client_socket)
            client_socket.close()
            return
        data = data.decode()
        res = []
        res = list(map(str, data.split("|SEP|")))
        if res[0] == "Give me the open key":
            threading.Thread(target=get_V_openKey).start()
        if res[0] == "Request for a open key":
            strOpenKey = ';'.join(map(str, openKey))
            client_socket.send(strOpenKey.encode())
        

def get_V_openKey():
    global vOpenKey

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    client_socket.send("Give me the open key".encode())
    vOpenKey = client_socket.recv(1024)
    vOpenKey = vOpenKey.decode()
    vOpenKey = list(map(int, vOpenKey.split(";")))
    print("vOpenKey = ", vOpenKey)

def Messaging(client_socket):
    global finalArray
    print("Messaging ", client_socket)
    client_socket.send("Time is over".encode())
    data = client_socket.recv(1024)
    data = data.decode()
    data = list(map(str, data.split("|SS|")))
    finalArray += data

def Send_a_reply(client_socket, rep):
    print("Send_a_reply ", client_socket, rep)
    client_socket.send(str(rep).encode())
    client_socket.close()

    
def Counting_the_results():
    global socketArray
    for i in socketArray:
        #print("send to ", i)
        threading.Thread(target=Messaging, args=(i,)).start()
    time.sleep(5)
    for i in finalArray:
        ab = list(map(str, i.split("|SEP|")))
        a = list(map(int, ab[0].split(";")))
        b = list(map(int, ab[1].split(";")))
        dm = Elgamal.get_decrypt_the_message(a, b, openKey, closeKey)
        m = RSA.get_message(dm, vOpenKey)
        #m = bits.int_to_text(m)
        print("I got m = ", m)
        superFinalyArray.append(int(m))
    answer = operation()
    for i in socketArray:
        threading.Thread(target=Send_a_reply, args=(i, answer, )).start()
    time.sleep(5)
    global stopFlag
    stopFlag = False
    
    
def operation():
    global superFinalyArray
    answer = 0
    for i in superFinalyArray:
        answer += i
    return answer

def We_are_waiting_for_the_end(time_dif):
    time.sleep(time_dif)
    Counting_the_results()

threading.Thread(target=get_V_openKey).start()

time_dif = 60*2
threading.Thread(target=We_are_waiting_for_the_end, args=(time_dif,)).start()

socketArray = []
while stopFlag:
    client_socket, addr = agent_socket.accept()
    socketArray.append(client_socket)
    print(f"The connection is established with {addr}")
    threading.Thread(target=user_work_space, args=(client_socket, addr)).start()
agent_socket.close()
    