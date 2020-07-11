import threading, socket, sys, time
#from queue import Queue
from multiprocessing.pool import ThreadPool
import socks
"""
socks.set_default_proxy(
        proxy_type=socks.SOCKS5, 
        addr="localhost",
        port=9050,
        rdns=None,
        username=None,
        password=None
    )
"""
class PortScanner:
    def __init__(self, host, min_port=1, max_port=65536):
        self.__lock = threading.Lock()

        self.__host = host
        self.__min_port = min_port
        self.__max_port = max_port
        self.__open_ports = []

        self.__proxy_type = None
        self.__proxy_addr = None
        self.__proxy_port = None
        self.__proxy_username = None
        self.__proxy_password = None
        

    def __thread_func(self, host, port):
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socks.socksocket()
        s.set_proxy(
            proxy_type=self.__proxy_type, 
            addr=self.__proxy_addr,
            port=self.__proxy_port,
            rdns=None,
            username=self.__proxy_username,
            password=self.__proxy_password
        )
        try:
            s.settimeout(5)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            con = s.connect((self.__host, port))
            with self.__lock:
                self.__open_ports.append(str(port))
                print('Port: ' + str(port) + ' is open')
            con.close()
        except Exception as e:
            pass

    def __wrapper(self, port):
        self.__thread_func(self.__host, port)

    def set_proxy(self, proxy_type, proxy_addr, proxy_port, proxy_username=None, proxy_password=None):
        self.__proxy_type = proxy_type
        self.__proxy_addr = proxy_addr
        self.__proxy_port = proxy_port
        self.__proxy_username = proxy_username
        self.__proxy_password = proxy_password

    def scan(self):
        
        p = ThreadPool(5000)
        p.map(self.__wrapper, range(self.__min_port, self.__max_port))

        p.close()
        p.join()
        return self.__open_ports

        
        
        
                    
        





