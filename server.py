import json
import socket
import random
import datetime
import hashlib
import sys

#SERVER LOG: [current time as Year-month-day-hour-minute-second] [MESSAGE]
def server_log(msg):
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print("SERVER LOG: {} {}".format(time,msg))

def get_handler(request,accounts,session_timeout):
    pass

def auth(username,password,accounts):
    if username not in accounts:
        return False
    correct_password,salt = accounts[username]
    h = hashlib.sha256()
    h.update((password+salt).encode())
    return h.hexdigest() == correct_password
    

def post_handler(msg,accounts,session_timeout,conn):
    method,uri,version,headers,body = msg
    if "username" not in headers or "password" not in headers:
        server_log("LOGIN FAILED")
        conn.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())
        return
    username,password = headers["username"],headers["password"]
    if not auth(username,password,accounts):
        server_log("LOGIN FAILED: {} : {}".format(username,password))
        conn.send("HTTP/1.0 200 OK\r\n\r\nLogin Failed!".encode())
        return
    session_id = hex(random.randint(0,2**64 - 1))
    #TODO: add session id to session table
    server_log("LOGIN SUCCESSFUL: {} : {}".format(username,password))
    response = "HTTP/1.0 200 OK\r\nSet-Cookie: sessionID={}\r\n\r\nLogged in!".format(session_id)
    conn.send(response.encode())
     
def http_parser(request):
    request = request.split("\r\n")
    method,uri,version = request[0].split(" ")
    headers = {}
    for header in request[1:]:
        if header == "":
            break
        key,value = header.split(": ")
        headers[key] = value
    body = request[-1]
    return method,uri,version,headers,body

def server(ip,port,accounts,session_timeout,rootdir):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen()
    while 1:
        conn,addr = s.accept()
        msg = http_parser(conn.recv(1024).decode())      
        method,uri,version,headers,body = msg
        if method == "POST" and uri == "/":
            post_handler(msg,accounts,session_timeout,conn)
        elif method == "GET":
            conn.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())
            pass
        else: 
            #maybe server log if not passing testcases later
            conn.send("HTTP/1.0 501 Not Implemented\r\n\r\n".encode())
            pass
        conn.close()
    s.close()

def main():
    ip,port,accountsfile,session_timeout,rootdir = sys.argv[1:]
    port = int(port)
    session_timeout = int(session_timeout)
    accounts = json.load(open(accountsfile))
    server(ip,port,accounts,session_timeout,rootdir)

if __name__ == "__main__":
    main()