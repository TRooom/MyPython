from collections import deque

def load():
    visited_file = open("visited",mode="r")
    visited = set()
    for x in visited_file.readlines():
        port = int(x.split(" ")[0])
        passw = x.split(" ")[1]
        visited.add((port,passw))
    visited_file.close()
    opened_file = open("opened", mode="r")
    opened = deque()
    for x in opened_file.readlines():
        port = int(x.split(" ")[0])
        passw = x.split(" ")[1]
        opened.append((port,passw))
    opened_file.close()
    return opened, visited

load()