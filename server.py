#!/usr/bin/env python3

import json
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse

from Crypto.PublicKey import RSA
from Crypto.Util.number import *

KEY_LENGTH = 512
EXP_LENGTH = 256
PASSWORD = b"dLzjWZ5gj/X+PZHv8+UeiQRK9zzOj/2Nf5CU90SSWtqEm3/jKpEK/o1QsSbTlYDuahgIVZbj"
PORT = 80
p = getPrime(KEY_LENGTH)
q = getPrime(KEY_LENGTH)


class Handler(SimpleHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200, "OK")
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        request = urlparse(s.path)
        path = request[2]
        query = request[4]
        if path == "/":
            send_index(s)
        elif path == "/public":
            send_public_key(s)
        elif path == "/generate":
            send_new_key_pair(s)
        elif path == "/key":
            send_get_key(s, query)
        else:
            s.send_response(404, "Not Found")
            s.send_header("Content-type", "text/html")
            s.end_headers()


def send_index(s):
    s.send_response(200, "OK")
    s.send_header("Content-type", "text/html")
    s.end_headers()
    s.wfile.write(b"<a href='/public'>Get server's public key</a><br>")
    s.wfile.write(b"<a href='/generate'>Generate new RSA key pair</a><br>")
    s.wfile.write(b"<a href='/key'>Get file key.txt (need admin permission)</a><br>")


def send_new_key_pair(s):
    s.send_response(200, "OK")
    s.send_header("Content-type", "text/plain")
    s.end_headers()
    s.wfile.write(key_to_string(generate_key_pair()).encode())


def send_public_key(s):
    s.send_response(200, "OK")
    s.send_header("Content-type", "text/plain")
    s.end_headers()
    s.wfile.write(key_to_string(server_key).encode())


def send_get_key(s, sign):
    if is_int(sign) and server_key.verify(PASSWORD, [int(sign), 0]):
        s.send_response(200, "OK")
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        s.wfile.write(key)
    else:
        s.send_response(403, "Forbidden")
        s.send_header("Content-type", "text/plain")
        s.end_headers()
        s.wfile.write(b"403 Forbidden")


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def generate_key_pair():
    p = getPrime(KEY_LENGTH)
    f = (p - 1) * (q - 1);
    e = getRandomInteger(EXP_LENGTH)
    while GCD(e, f) != 1:
        e = getRandomInteger(EXP_LENGTH)
    d = inverse(e, f)
    return RSA.construct([p * q, e, d])


def key_to_string(key):
    res = '### ';
    if key.has_private():
        res += 'PRIVATE'
    else:
        res += 'PUBLIC'
    res += ' RSA KEY ###\n'
    dic = {'n' : key.n, 'e' : key.e}
    if key.has_private():
        dic['d'] = key.d
    return res + json.dumps(dic)


def start_server(port):
    httpd = socketserver.TCPServer(("", port), Handler)
    httpd.serve_forever()


if __name__ == '__main__':
    with open('key.txt') as key_file:
        key = key_file.read().strip().encode()
    
    server_key = generate_key_pair()
    print(key_to_string(server_key))
    server_key = server_key.publickey()

    start_server(PORT)
