import socket
from User import User
import threading

# VAR
HOST = "0.0.0.0"
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

# users
users = []

# Envia pra todos os usuários
def broadcast(text_msg):
    for user in users:
        if user.nickname in text_msg:
            pass
        else:
            user.clientObj.send(text_msg.encode())

def session_mng(user: User):
    while True:
        try:
            text_msg = user.clientObj.recv(1024).decode("utf-8")
            broadcast(f"{user.nickname}:{text_msg}")
        except:
            print(f"{user.nickname} disconnected.")
            users.remove(user)
            user.clientObj.close()
            break

server.listen()
print("---SERVER IS ONLINE!---")
while True:
    # Pega os dados do cliente que se conectou.
    clientObj, dataClient = server.accept()

    clientObj.send("NICK".encode())
    nickname = clientObj.recv(1024).decode('utf-8')
    print(f"CLIENT {nickname} CONNECT: {dataClient}")
    user : User = User(clientObj, nickname, None)
    users.append(user)
    clientObj.send(f"Welcome {nickname}".encode())

    threadSession = threading.Thread(target=session_mng, args=(user,))
    threadSession.start()