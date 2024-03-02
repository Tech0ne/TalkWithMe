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

ICON_PATH = "icon.png"

SAVE_PATH = "client_infos.json"

RSA_LENGTH = 10

INTERFACE = "0.0.0.0"
PORT = 22349
BUFFER_SIZE = 2 << 10

IMPORTANT_TIMEOUT = 5 * 60 # important message timeout

CLIENT_RSA_KEYS = {}

CLIENT_WRITING = []
CLIENT_WAITING = []

import notifypy
import socket
import json
import enum
import rsa
import os

class Urgency(enum.Enum):
    NORMAL = 0
    IMPORTANT = 1
    CRITICAL = 2

class Message:
    def __init__(self, client: socket.socket, message: bytes):
        self.client = client
        self.message = message
        # Message form :
        # size;urgency;identifier;b64_message
        # where size = len(identifier) + len(message) + 1
        # urgency = "NORMAL", "IMPORTANT", "CRITICAL"
        #   (server will only accept RSA important and critical)
        #   (server will only allow 1 important message every )
        # identifier = md5(personal value to identify itself)
        # will be paired with the IP to identify a client
        #
        # SPECIAL MESSAGES :
        # size;urgency;RSA;b64_encoded_rsa_pub_key
        # size;urgency;B64;b64_encoded_message
        # 
        # Note : if the message does not follow this syntax (check done by looking if everything befor the first ';' is an int),
        #   this will be counted as a NORMAL with no identifier, and will be read until '\n' is encountered

        self.size = -1
        self.urgency = Urgency.NORMAL
        self.identifier = ""
        self.cut_message()
    
    def cut_message(self):
        if self.message.count(b';') != 3:
            self.size = len(self.message)
            while self.message[-1] != '\n':
                self.message += self.client.recv(BUFFER_SIZE)
            self.size = len(self.message)



def send_notification(title, message):
    n = notifypy.Notify()
    n.title = title
    n.message = message
    n.icon = ICON_PATH
    n.application_name = "T.W.M."

    n.send()

def rsa_new_keys():
    return rsa.newkeys(2 << RSA_LENGTH)

def load_clients():
    global CLIENT_RSA_KEYS
    if os.path.isfile(SAVE_PATH):
        try:
            CLIENT_RSA_KEYS = json.load(open(SAVE_PATH, 'r'))
        except:
            pass

def save_clients():
    global CLIENT_RSA_KEYS
    json.dump(CLIENT_RSA_KEYS, open(SAVE_PATH, 'w+'), indent=4)

def main():
    load_clients()




## ----------------------------------------------------------------------------------- ##
##                                                                                     ##
## MIT License                                                                         ##
## Copyright (c) 2024 Tech0ne                                                          ##
##                                                                                     ##
## Permission is hereby granted, free of charge, to any person obtaining a copy        ##
## of this software and associated documentation files (the "Software"), to deal       ##
## in the Software without restriction, including without limitation the rights        ##
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell           ##
## copies of the Software, and to permit persons to whom the Software is               ##
## furnished to do so, subject to the following conditions:                            ##
##                                                                                     ##
## The above copyright notice and this permission notice shall be included in all      ##
## copies or substantial portions of the Software.                                     ##
##                                                                                     ##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR          ##
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,            ##
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE         ##
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER              ##
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,       ##
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE       ##
## SOFTWARE.                                                                           ##
##                                                                                     ##
## ----------------------------------------------------------------------------------- ##