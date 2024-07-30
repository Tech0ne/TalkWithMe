FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3 python3-pip python3-gi python3-dbus
RUN useradd user

RUN chown user:user /app/

RUN pip3 install notify2 dbus-python

USER user

COPY server.py /app/server.py
COPY icon.png /app/icon.png

CMD [ "python3", "/app/server.py" ]