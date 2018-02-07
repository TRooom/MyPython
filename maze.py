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
    print(string.split("\n")[0])
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
        except :
            soc.close()
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            continue
    return d

def explore():
    visited = set()
    opened = deque()
    tick =0
    opened.append((1024,"3k8bbz032mrap75c8iz8tmi7f4ou00"))
    opened, visited = load()
    while len(opened) != 0:
        next = opened.popleft()
        visited.add(next)
        data = get_data(next[0], next[1]).decode()
        new_open = parse_answ(data, next[0])
        for x in new_open:
            if x not in visited:
                opened.append(x)
        tick+=1
        if tick % 100 ==0:
            log(visited,opened)
            print(tick)

def log(visited, opened):
    log_file(visited,"visited")
    log_file(opened, "opened")


def log_file(collection, name):
    file = open(name,mode="w")
    lines = ["{0} {1}".format(x[0],x[1]) for x in collection]
    file.write("\r".join(lines))
    file.close()

def load():
    visited_file = open("visited",mode="r")
    visited = set()
    for x in visited_file.readlines():
        port = int(x.split(" ")[0])
        passw = x.replace("\n","").split(" ")[1]
        visited.add((port,passw))
    visited_file.close()
    opened_file = open("opened", mode="r")
    opened = deque()
    for x in opened_file.readlines():
        port = int(x.split(" ")[0])
        passw = x.replace("\n","").split(" ")[1]
        opened.append((port,passw))
    opened_file.close()
    return opened, visited




explore()

