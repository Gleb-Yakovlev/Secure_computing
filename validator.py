import socket
import RSA
import threading

openKey, closeKey = RSA.getKeys(11)
print("keys = ", openKey, closeKey)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 12345))

approvedList = []
adressList = []

server_socket.listen(10)
print("Validator ready and listen...")

def approved(res):
    print(f"{res[1]} allowed to vote")
    approvedList.append(res[1])
    adressList.append(res[2])
    print("adressList = ", adressList)
    client_socket.send(("You can" + "|SEP|" + str(openKey[0])+";"+str(openKey[1])).encode())

def signature(res):
    print(f"{addr} in approvedList")
    m = list(map(int, res.split(";")))
    print("m", m)
    s = RSA.creating_a_signature(m, closeKey)
    s = ';'.join(map(str, s))
    client_socket.send(s.encode())
    
def update_approved_list():
    print("update_approved_list")

def user_work_space(client_socket, addr):
    address = 0
    while True:
        try:
            data = client_socket.recv(1024)
        except:
            print("The client has disconnected")
            client_socket.close()
            global adressList
            print("adressList = ", adressList)
            print("address = ", address)
            adressList.remove(address)
            break
        data = data.decode()
        res = []
        res = list(map(str, data.split("|SEP|"))) 

        print(res)
        print("approvedList = ", approvedList)
        print("adressList = ", adressList)
        if res[0] == "Request for addresses":
            strA = ';'.join(map(str, adressList))
            client_socket.send(strA.encode())
        
        elif res[0] == "Give me the open key":
            client_socket.send((str(openKey[0])+";"+str(openKey[1])).encode())
            client_socket.close()
            break
        elif res[0] == 'I want to vote' and res[1] not in approvedList:
            address = res[2]
            approved(res)
        elif res[1] in approvedList:
            signature(res[0])

while True:
    client_socket, addr = server_socket.accept()
    print(f"The connection is established with {addr}")
    threading.Thread(target=user_work_space, args=(client_socket, addr)).start()

