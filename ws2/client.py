import socket
import sys

HOST = "localhost"
PORT = 12345

def eprint(message):
    print(message, file = sys.stderr)

def main():
    try:
        host = socket.gethostbyname(HOST)
        port = PORT
        with socket.create_connection((host, port), timeout=5) as conn:
            data = conn.recv(4096)
            while data != b"":
                sys.stdout.write(data.decode("utf-8"))
                sys.stdout.flush()
                data = conn.recv(4096)
    except socket.timeout:
        eprint("error: connection timed out")
    except ConnectionRefusedError:
        eprint("error: connection refused")


if __name__ == "__main__":
    main()
