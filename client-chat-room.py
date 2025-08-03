import socket
import threading
import time
from sys import exit
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv() # carrega as variaveis de ambiente

SHARED_KEY = os.getenv("SHARED_KEY")

cipher = Fernet(SHARED_KEY.encode())

stop_thread = threading.Event()
start_send_client_msg_event = threading.Event()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    print("x00:00---Welcome to the net :D---x00:00")
    nickname = input("nickname:").upper()
    serverIp = input("server ip:")
    try:
        client.connect((serverIp, 80))
    except:
        print("\n</connection failure/>")
        exit(0)
except:
    exit(0)

def send_recv():
   
    # Criando o objeto <socket client>
    while not stop_thread.is_set():
        try:
            # Manda o nick do usuário para o servidor
            sever_msg = cipher.decrypt(client.recv(1024)).decode("utf-8") # NICK OR Broadcast
            if sever_msg == "NICK":
                print("Send nick")
                encrypted_nick = cipher.encrypt(nickname.encode())
                client.send(encrypted_nick)
                start_send_client_msg_event.set()
            else:
                # Recebe mensagem do broadcast
                print(sever_msg)
        except KeyboardInterrupt:
            print("thread 1 atictived")
            stop_thread.set()
        except:
            print("</connection failure/>")
            stop_thread.set()
            exit(0)



def send_client_msg():
    start_send_client_msg_event.wait()
    while not stop_thread.is_set():
        try:
            text_msg = input("")
            encrypted_msg = cipher.encrypt(text_msg.encode())
            client.send(encrypted_msg)

        except (EOFError, KeyboardInterrupt):
            print("[INFO] the user stopped the program.")
            stop_thread.set()
            client.close()
            break

        except Exception as e:
            print(f"[ERRO] message failed to send: {e}")
            stop_thread.set()
            client.close()
            break

try:
    run_send_recv = threading.Thread(target=send_recv)
    run_send_recv.start()

    run_send_client_msg = threading.Thread(target=send_client_msg)
    run_send_client_msg.start()

    run_send_recv.join()
    run_send_client_msg.join()

except KeyboardInterrupt:
    print("</program finished/>")
    stop_thread.set()
    exit(0)