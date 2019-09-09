import sys
import socket
import time
from datetime import datetime
from threading import Thread, current_thread
from datetime import datetime

BIND_HOST = "127.0.0.1"
BIND_PORT = 12345

def dbg(message):
    print("%s [thread=%s] %s" % (datetime.now().isoformat(), current_thread().name, message), file=sys.stderr)

def on_connection(conn, remote_addr):
    host, _ = remote_addr
    dbg("accept work")
    dbg("remote address: %s" % host)
    for i in range(5):
        message = b"Hello %s" % str(datetime.now().isoformat()).encode()
        dbg("send message %s (%s out of 5)" % (message, i + 1))
        conn.send(message)
        time.sleep(3)
    dbg("closing connection")
    conn.close()

def main():
    current_thread().name = "main"
    acceptor = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
    # Set SO_REUSEADDR for faster rebinds
    acceptor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    acceptor.bind((BIND_HOST, BIND_PORT))
    acceptor.listen()
    dbg("bound socket to %s:%s" % (BIND_HOST, BIND_PORT))
    thread_counter = 0
    while True:
        try:
            conn, remote_addr = acceptor.accept()
            thread_counter += 1
            thread = Thread(target = on_connection, args = (conn, remote_addr), name = "worker-%s" % thread_counter)
            # Stop the thread when the main thread exits
            thread.daemon = True
            thread.start()
        except KeyboardInterrupt:
            print()
            break
    dbg("releasing socket...")
    acceptor.close()
    dbg("exiting")

if __name__ == "__main__":
    main()