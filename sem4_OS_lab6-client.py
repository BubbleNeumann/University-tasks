import sys
import socket
import select

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTextEdit, QVBoxLayout, QPushButton, QMessageBox

# globals
app = QApplication(sys.argv)
window = QWidget()
HOST = '127.0.0.1'  # The server's hostname or IP address   
PORT = 65432  # The port used by the server
text_area = QTextEdit(parent=window)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def msg_is_valid(msg) -> bool:
    for c in msg:
        if (ord(c) >= ord('a') and ord(c) <= ord('z')) or (ord(c) >= ord('A') and ord(c) <= ord('Z') or (ord(c) >= ord('0') and ord(c) <= ord('9'))):
            continue
        else:
            return False
    return True

def send() -> None:

    try:
        ready_to_read, ready_to_write, in_error = select.select([s], [], [s], 0)
    except select.error:
        s.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
        s.close()
        print('connection error')
        sys.exit()

    if len(ready_to_read) == 0 and len(ready_to_write) == 0 and len(in_error) == 0:
        msg = text_area.toPlainText()
        text_area.clear()
        if msg == 'ex':
            s.sendall(msg.encode(encoding='UTF-8', errors='ignore'))
            sys.exit()
        else:
            if not msg_is_valid(msg):
                notif = QMessageBox();
                notif.setText('some letters might not be supported')
                notif.exec_()
            else:
                msg = encrypte(msg).encode(encoding='UTF-8', errors='ignore')
                s.sendall(msg)
    else:
        print('connection error')
        sys.exit()


def encrypte(msg: str) -> str:
    KEY = 3
    MOD = 26
    if KEY >= MOD:
         KEY %= MOD

    encrypted_msg = ''

    for ch in msg:
        c = ord(ch)
        if c >= ord('a') and c <= ord('z'):	
            if c + KEY <= ord('z'):
                encrypted_msg += chr(c + KEY)
            else:
                encrypted_msg += chr(ord('a') - (ord('z') - c + 1) + KEY)
        elif c >= ord('A') and c <= ord('Z'):
            if c + KEY <= ord('Z'):
                encrypted_msg += chr(c + KEY)
            else:
                encrypted_msg += chr(ord('A') - (ord('Z') - c + 1) + KEY)
        else:
            encrypted_msg += ch

    return encrypted_msg


def main() -> None:
    layout = QVBoxLayout()
    window.setWindowTitle('client')
    window.setGeometry(1000, 1000, 600, 500)
    connection_msg = QLabel('\tserver is not connected', parent=window)
    send_button = QPushButton("Send")
    fff_button = QPushButton("fff")
    send_button.clicked.connect(send)

    layout.addWidget(connection_msg)
    
    layout.addWidget(text_area)
    layout.addWidget(send_button)
    layout.addWidget(fff_button)
    window.setLayout(layout)
    window.show()
    

    s.connect((HOST, PORT))
    connection_msg.setText('\tserver connected')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()