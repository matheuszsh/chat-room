import socket
import threading
from pynput import keyboard
import time
from os import _exit

stop_thread = threading.Event()
thread_lock = threading.Lock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("x00:00---Welcome the net :D---x00:00")
nickname = input("nickname:").upper()
serverIp = input("server ip:")

def main():

    thread_lock.acquire()
    client.connect((serverIp, 5050))
    # Criando o objeto <socket client>
    while not stop_thread.is_set():
        try:
            sever_msg = client.recv(1024).decode("utf-8")
            if sever_msg == "NICK":
                print("Send nick")
                client.send(nickname.encode())
            else:
                print(sever_msg)
        except:
            print("!!! <> Lost Connection <> !!!")
            client.close()
    thread_lock.release()

def write():
    while not stop_thread.is_set():
        text_msg = input("")
        client.send(text_msg.encode())

def on_press_key(key):
    if key == keyboard.Key.esc:
        print("you leave on the session...")
        time.sleep(1)
        stop_thread.set()
        _exit(0)
    
        
        

run_main = threading.Thread(target=main)
run_main.start()

run_write = threading.Thread(target=write)
run_write.start()

with keyboard.Listener(on_press=on_press_key) as listener:
    listener.join()



