import socket, random, csv, threading, os, time

block = threading.Lock()
L_FLAG = True


def sendmsg(sock, data):

    sock.send(data.encode())


def recvmsg(sock, bt):
    data = sock.recv(bt).decode()
    return data


socket.socket.sendmsg = sendmsg
socket.socket.recvmsg = recvmsg


def logging(*data):
    data = ' '.join((str(item) for item in data))
    global block, L_FLAG
    if L_FLAG:
        with block:
            print(data)
            with open("log.txt", 'a+') as file:
                file.write(data + '\n')



logging("Запуск сервера")
sock = socket.socket()

port = 9090

while True:
    try:
        sock.bind(('', port))
        logging(f"Порт {port}")
        break
    except OSError as oserr:
        logging(f"порт {port} недоступен")
        port = random.randint(1024, 65535)

sock.listen(0)
logging("Начало прослушивания порта")


def listening(conn, addr):
    global users_list, block, history
    logins = "logins.csv"
    try:
        with block:
            with open(logins, 'a+', newline='') as login:
                login.seek(0, 0)
                reader = csv.reader(login, delimiter=';')
                for row in reader:
                    if row[0] == addr[0]:
                        password = row[2]
                        name = row[1]
                        break
                else:
                    conn.sendmsg("Введите Ваше имя")
                    name = conn.recvmsg(1024)
                    conn.sendmsg("Введите пароль")
                    password = conn.recvmsg(1024)
                    writer = csv.writer(login, delimiter=';')
                    writer.writerow([addr[0], name, password])

        while True:
            conn.sendmsg("Введите пароль для начала диалога")
            password1 = conn.recvmsg(1024)
            if password1 == password:
                conn.sendmsg((f"Начинаем наше общение,{name}"))
                break
            else:
                conn.sendmsg("Неверный пароль")
        while True:
            data = conn.recvmsg(1024)
            logging(name, " : ", data)
            with block:
                with open(history, "a+") as file:
                    file.write(name + ": " + data + "\n")
            for conn1 in users_list:
                if conn1 != conn:
                    conn1.sendmsg(name + ": " + data)

    except:
        users_list.remove(conn)
        raise


def connecting():
    global users_list, CON_FLAG
    while True:
        if CON_FLAG:
            conn, addr = sock.accept()
            logging(f"Подключение клиента {addr}")
            users_list.append(conn)
            threading.Thread(target=listening, args=(conn, addr), daemon=True).start()


users_list = []
CON_FLAG = True
history = f"history_{time.time()}.txt"
threading.Thread(target=connecting, daemon=True).start()

while True:
    text = input()
    if text == "выключить":
        break
    elif text == "показывать логи":
        L_FLAG = True
    elif text == "не показывать логи":
        L_FLAG = False
    elif text == "очистить логи":
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        with block:
            with open("log.txt", "w"):
                pass
    elif text == "очистка файла идентификации":
        with block:
            with open("logins.csv", "w"):
                pass
    elif text == "включить паузу":
        CON_FLAG = False
    elif text == "выключить паузу":
        CON_FLAG = True
logging("Остановка сервера")