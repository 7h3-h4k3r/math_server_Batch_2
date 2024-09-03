import subprocess
import threading
import socket 
from colorama import Fore, Back, Style
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

class OutputThreadUser(threading.Thread):
    def __init__(self,conn,proc):
        threading.Thread.__init__(self)
        self.conn = conn
        self.proc = proc
    def run(self):
        while self.proc.poll() is None:
            try:
                self.conn.sendall(self.proc.stdout.readline())
            except:
                pass

class HandleIncomingThread(threading.Thread):
    def __init__(self,conn,add):
        threading.Thread.__init__(self)
        self.conn = conn 
        self.add = add
    def run(self):
        print(Fore.RED + "Incoming connection New {} {}".format(self.add[0],self.add[1]))
        self.conn.sendall("\t\t ꜱɪᴍᴘʟᴇ ᴍᴀᴛʜ ꜱᴇʀᴠᴇʀ ʙʏ ʟᴀᴛʜᴘ (ʙᴀᴛᴄʜ 2)\n".encode())
        proc = subprocess.Popen(['bc'],stderr=subprocess.STDOUT,stdout=subprocess.PIPE,stdin= subprocess.PIPE)
        outputTh = OutputThreadUser(self.conn,proc)
        outputTh.start()
        while proc.poll() is None:
            data = self.conn.recv(1024)
            try:
                if not data:
                    break
                data = data.decode().strip()
                query = data + '\n'
                proc.stdin.write(query.encode())
                proc.stdin.flush()
            except:
                pass
host= ''
port = 9090
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((host,port))
server.listen()
print("Listening port {} ".format(port))
while True:
   conn,add = server.accept()
   server_thread = HandleIncomingThread(conn,add)
   server_thread.start()
server.close()