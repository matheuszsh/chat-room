import socket
from User import User
import threading
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

SHARED_KEY = os.getenv("SHARED_KEY")

cipher = Fernet(SHARED_KEY.encode())

# VAR
HOST = "0.0.0.0"
PORT = 80

stop_thread = threading.Event()

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
            encrypted_msg = cipher.encrypt(text_msg.encode())
            user.clientObj.send(encrypted_msg)

def session_mng(user: User):
    while not stop_thread.is_set():
        try:
            encrypted_msg = user.clientObj.recv(1024)
            decrypted_msg = cipher.decrypt(encrypted_msg).decode("utf-8")
            broadcast(f"{user.nickname}:{decrypted_msg}")
        
        except KeyboardInterrupt:
            print("here")
            stop_thread.set()
            user.clientObj.close()
        
        except:
            print(f"{user.nickname} disconnected.")
            users.remove(user)
            user.clientObj.close()
            break

server.listen()
print("---SERVER IS ONLINE!---")
while not stop_thread.is_set():
    # Pega os dados do cliente que se conectou.
    try:
        clientObj, dataClient = server.accept()

        clientObj.send(cipher.encrypt("NICK".encode()))
        nickname = clientObj.recv(1024)
        decrypted_nickname = cipher.decrypt(nickname).decode('utf-8')
        print(f"CLIENT {decrypted_nickname} CONNECT: {dataClient}")
        user : User = User(clientObj, decrypted_nickname, None)
        users.append(user)
        default_msg = cipher.encrypt(f"Welcome {decrypted_nickname}".encode())
        clientObj.send(default_msg)
        
        
        threadSession = threading.Thread(target=session_mng, args=(user,))
        threadSession.start()
    except KeyboardInterrupt:
        stop_thread.set()
        server.close()
        threadSession.join()
    