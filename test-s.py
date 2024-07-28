import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 12345))

server_socket.listen(10)

print("Сервер запущен и ожидает подключения...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключение установлено с {addr}")

    data = client_socket.recv(1024)
    number = int(data.decode())

    result = math.pow(number, 2)

    client_socket.send(str(result).encode())

    client_socket.close()
