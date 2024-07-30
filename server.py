## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
##      ░▒▓████████▓▒░  ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓██████████████▓▒░                ##
##         ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░               ##
##         ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░               ##
##         ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░               ##
##         ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░               ##
##         ░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██▓▒░        ##
##         ░▒▓█▓▒░▒▓██▓▒░░▒▓█████████████▓▒░░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██▓▒░        ##
##                                                                                     ##
## ----------------------------------------------------------------------------------- ##

import notify2
import socket
import sys
import os

ICON_PATH   = "icon.png"
INTERFACE   = "0.0.0.0"
PORT        = 22349
BUFFER_SIZE = 2 << 10

BLACK_LIST  = []

def notif_action(notif, action, data=None):
    print(notif)
    print(action)
    print(data)

def send_notification(message: str, origin: str):
    n = notify2.Notification(f"Message from {origin}", message, ICON_PATH)

    print(f"Just sent notif")

    n.add_action("accept", "Accept", notif_action)
    n.add_action("refuse", "Refuse", notif_action)
    n.add_action("block", "Block", notif_action)

    n.send(block=True)

def main(argv: list[str]) -> int:
    global BLACK_LIST

    notify2.init("T.W.M.")

    s = socket.socket()
    s.bind((INTERFACE, PORT))
    s.listen(5)

    print(f"Listening on port {PORT}")

    running = True

    while running:
        try:
            c, (ip, _) = s.accept()
            print(f"{ip} just connected")
            if ip in BLACK_LIST:
                print(f"But he is blacklisted. Bye !")
                c.close()
                continue
            data = c.recv(BUFFER_SIZE).decode()
            print(f"He just sent a {len(data)} bytes long message.")
            send_notification(data, ip)
            c.close()

        except KeyboardInterrupt:
            running = False

        except Exception as e:
            print(e)

    s.close()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))