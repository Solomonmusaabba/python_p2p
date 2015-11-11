from errno import EBADF

import threading
import server_client_base as scb 
import socket


class Client(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__()

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((host_ip, port))

        th = threading.Thread(target=self.recv_handler, kwargs={'sock':self._s})
        th.start()

    def recv_handler(self, sock):
        while True:
            try:
                msg = sock.recv(1024)
                msg = msg.decode()
                if not msg:
                    self._msg_queue.put("SYSTEM: Host is disconnected.") 
                    self.destroy()
                    break

                self._msg_queue.put(msg)
            except Exception as e:
                if e.errno == EBADF: 
                    # User closed the program
                    break

                self._msg_queue.put("SYSTEM: " + repr(e))

    def send_msg(self, msg):
        if not msg:
            return

        try:
            if self._s is not None:
                self._s.sendall(msg.encode())
            else:
                self._msg_queue.put(msg)
        except Exception as e:
            self._msg_queue.put("SYSTEM: " + repr(e))
        
    def destroy(self):
        if self._s is not None:
            self._s.close()
            self._s = None
