import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect(("212.193.68.254", 60005))
soc.send("[                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ]\n".encode())

data = soc.recv(2048) + soc.recv(2048)
print(data.decode().replace(" ","0"))
soc.close()


