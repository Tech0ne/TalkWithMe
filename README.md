# TalkWithMe
Sample application used as "talk with me !". Connect to the port using the provided client, or use netcat and follow the protocol to chat. As easy as that ! Will support plain text messages, b64 and RSA encryption.


If you were asking, default port number comes from : (int(hex(ord("T")) + hex(ord("W")) + hex(ord("M"))) % 65536) ;)