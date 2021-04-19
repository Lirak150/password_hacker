import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 9090        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                print("empty")
                break
            elif data.decode() == "az":# replace "az" for other target passwords
                print("yes")
                conn.send("Connection success!".encode())
            else:
                print("no")
                conn.send("Wrong password!".encode())