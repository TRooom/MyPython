import socket
import re
from collections import deque

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def parse(string,port):
    dir = ""
    i = 11
    while string[i] != " ":
        dir += str(string[i])
        i+=1
    dirs = {"up" : -256, "down" : 256, "right" : 1,"left":-1 }
    new_port = port + dirs[dir]
    passw = re.findall("[0-9a-z]+$", string)[0]
    if len(passw) != 30:
        print(passw)
    return new_port, passw

def parse_answ(string,port):
    print(string)
    if string.split("\n")[0] != "Next step":
        print(string)
    nodes = [parse(x, port) for x in string.split("\n")[1:]]
    return nodes


def get_data(port, pasw):
    d = ""
    while True:
        try:
            global soc
            soc.connect(("46.101.195.72", port))
            soc.send(pasw.encode())
            d = soc.recv(1024)
            break
        except:
            soc.close()
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            continue
    return d

d1 = get_data(1024,"3k8bbz032mrap75c8iz8tmi7f4ou00").decode()

datas_len = set()
visited = set()
visited.add((1024,"3k8bbz032mrap75c8iz8tmi7f4ou00"))
prev = (1024,"3k8bbz032mrap75c8iz8tmi7f4ou00")
opened = deque()
opened.extend(parse_answ(d1, 1024))
while len(opened) != 0:
    next = opened.popleft()
    visited.add(next)
    data = get_data(next[0], next[1]).decode()
    new_open = parse_answ(data, next[0])
    for x in new_open:
        if x not in visited:
            opened.append(x)
    #print("v{} o{}  d{}".format(len(visited), len(opened), len(data)))
    if len(visited) > 500 and len(data) not in datas_len:
        pass#print("asdjfklsdjklsjadfkljf" + "     " + data)
    datas_len.add(len(data))







