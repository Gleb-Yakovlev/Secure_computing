import socket
import random
import threading
import time

array = []
for i in range(0, 5, 1):
    array.append(random.randint(0, 100))
print("The original array = ", array)

clientArray = []

to_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
to_client_socket.bind(('localhost', 0))
to_client_socket.listen(10)


to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
to_server_socket.connect(('localhost', 12345))

def send_to_server_port():
    to_server_socket.send(str(to_client_socket.getsockname()[1]).encode())

def listen_client():
    while True:
        s, a = to_client_socket.accept()
        print(f"EST: {a}")
        data = s.recv(1024)
        number = int(data.decode())
        array.append(number)
        s.close()

def send_array():
    while True:
        time.sleep(5)
        to_server_socket.send("Give".encode())
        data = to_server_socket.recv(1024)
        data = data.decode()
        

threading.Thread(target=listen_client).start()
threading.Thread(target=send_array).start()

