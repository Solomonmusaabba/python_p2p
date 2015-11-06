import threading
import server_client_base as scb 
import socket


class Client(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__(host_ip, port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host_ip, port))

        th = threading.Thread(target=self.recv_handler, kwargs={'sock':self.s})
        th.start()

    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            if not msg:
                break
            self.msg_queue.put(msg)

    def send_msg(self, msg):
        if not msg:
            return
        self.s.sendall(msg.encode())
        
    def destroy(self):
        self.s.close()
