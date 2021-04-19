# write your code here
import sys
import diffrent_brute_force
import socket

ip_address = ""
port = 0


def start_program():
    arg_parse()
    with socket.socket() as client_socket:
        brute_force = diffrent_brute_force.TimeBasedVulnerabilityBruteForce(
            client_socket, ip_address, port)
        brute_force.brute_force()


def arg_parse():
    args = sys.argv
    global ip_address, port
    ip_address = args[1]
    port = int(args[2])


start_program()
