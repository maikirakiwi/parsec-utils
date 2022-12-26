import socket, os, sys, datetime, logging

# Server
def Server():
    #listen_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    #listen_socket.bind("[[\\.\pipe\]]discord-ipc-0")
    #listen_socket.listen(1)

    dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_socket.connect_ex(('192.168.1.200', 32767))

    while True:
        with open(r"\\.\pipe\discord-ipc-0", "rb+", buffering=0) as pipe:
            data = pipe.read(1024)
            logging.info(f"[{datetime.datetime.now()}] RPC Data Captured")
        try:
            #data = rpc_data.recv(1024)
            dest_socket.send(data)
        except (KeyboardInterrupt, SystemExit):
            dest_socket.close()
            logging.info("[{datetime.datetime.now()}] RPC Sockets Terminated (KBI)")
            raise
        finally:
            dest_socket.close()
            logging.info("[{datetime.datetime.now()}] RPC Sockets Terminated")

def Client():
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_socket.bind(('localhost', 32767))
    recv_socket.listen(1)

    sendRPC_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sendRPC_socket.connect(f"{os.environ['TMPDIR']}/discord-ipc-0")
    
    while True:
        rpc_data, addr = recv_socket.accept()
        logging.info(f"[{datetime.datetime.now()}] RPC Data Received from {addr}")
        try:
            data = recv_socket.recv(1024)
            sendRPC_socket.send(data)
        except (KeyboardInterrupt, SystemExit):
            recv_socket.close()
            sendRPC_socket.close()
            logging.info("[{datetime.datetime.now()}] RPC Sockets Terminated (KBI)")
            raise
        finally:
            recv_socket.close()
            sendRPC_socket.close()
            logging.info("[{datetime.datetime.now()}] RPC Sockets Terminated")

if __name__ == "__main__":
    match sys.platform:
        case "win32":
            Server()
        case "darwin":
            Client()
        case _:
            print("Unsupported platform")
            sys.exit(1)
