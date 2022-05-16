import sys
import os
import socket
from threading import Thread 

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from datetime import datetime


# globals
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
FILE_NAME = 'log.txt'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def update_log(msg: str) -> None:
    current_time = datetime.now().strftime('%H:%M:%S')
    file = open(FILE_NAME, 'a')
    file.write(current_time + ' ' + msg + '\n')
    file.close()

def decrypte(msg: str) -> str:
    KEY = 3
    MOD = 26  
    if KEY >= MOD:
        KEY %= MOD

    decrypted_msg = ''
    
    for ch in msg:
        c = ord(ch)
        if c >= ord('a') and c <= ord('z'):
            if c - KEY <= ord('z'):
                decrypted_msg += chr(c - KEY)
            else:
                decrypted_msg += chr(ord('z') + (c - ord('a') + 1) - KEY)
		
        elif c >= ord('A') and c <= ord('Z'):
            if c - KEY <= 'Z':
                decrypted_msg += chr(c - KEY)
            else:
                decrypted_msg += chr(ord('Z') + (c - ord('A') + 1) - KEY)	
        else:
            decrypted_msg += ch
    
    return decrypted_msg

def upd(label) -> None:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    label_text = ''
        
    while True: 
        data = conn.recv(1024)  
        if data == b'ex' or not data:
            s.close()
            os._exit(0)                     
        decrypted_msg = decrypte(data.decode(errors='ignore'))        
        update_log(decrypted_msg)
        label_text += data.decode(errors='ignore') + ' -> ' + decrypted_msg + '\n'
        label.setText(label_text)

   
    

def main() -> None:
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()    
    window.setWindowTitle('server')
    window.setGeometry(1000, 1000, 600, 500)
    connection_msg = QLabel('', parent=window)
    connection_msg.setAlignment(Qt.AlignTop)
    layout.addWidget(connection_msg)
    window.setLayout(layout)
    window.show()

   
    th = Thread(target=upd, args=(connection_msg,))
    th.start()

    sys.exit(app.exec_())



if __name__ == "__main__":    
    main()
