import socket, threading

def sendmsg(sock, data):
    sock.send(data.encode())

def recvmsg(sock, bt):
    data = sock.recv(bt).decode()
    return data

socket.socket.sendmsg = sendmsg
socket.socket.recvmsg = recvmsg

def recieving():
    while True:
        data = sock.recvmsg(1024)
        with block:
            print(data)


block = threading.Lock()
sock = socket.socket()
sock.setblocking(1)

host = 'localhost'
print("Введите номер порта")
port = int(input())
print("Выполняется соединение с сервером")
sock.connect((host, port))
print("Соединено с сервером установлено")

threading.Thread(target = recieving, daemon = True).start()
while True:
    msg = input()
    sock.sendmsg(msg)
    if msg == "выход":
        break

print("Разрыв соединения с сервером")


sock.close()