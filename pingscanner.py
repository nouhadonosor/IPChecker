import os
import platform
import ipaddress
import threading
import re
from multiprocessing.pool import ThreadPool

from datetime import datetime


class PingScanner:
    def __init__(self, ip_range_str):
        self.__lock = threading.Lock()
        self.__ip_range = ipaddress.IPv4Network(ip_range_str)
        self.__alive_ips = []
        self.__echoes = 1
        self.__timeout = 100
        os_name = platform.system()
        if (os_name == "Windows"):
            self.__ping_command = f"ping -n {self.__echoes} -w {self.__timeout} "
        elif (os_name == "Linux"):
            self.__ping_command = f"ping -c {self.__echoes} -i {self.__timeout} "
        else :
            self.__ping_command = f"ping -c {self.__echoes} -i {self.__timeout} "

    def __ip_gen(self, ip_range):
        for ip in ipaddress.IPv4Network(self.__ip_range):
            yield str(ip)

    def __thread_func(self, host):
        #print(addr, end='\r')
        comm = self.__ping_command + host
        response = os.popen(comm)
    
        for line in response.readlines():
            
            #if (line.count("TTL")):
            if re.search('ttl', line, re.IGNORECASE):
                with self.__lock:
                    self.__alive_ips.append(host)
                #print (addr, "is up!")
                break

    def __wrapper(self, host):
        self.__thread_func(host)

    def scan(self):
        p = ThreadPool(100)
        p.map(self.__wrapper, self.__ip_gen(self.__ip_range))

        p.close()
        p.join()
        return self.__alive_ips


