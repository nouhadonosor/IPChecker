import json
import socks

from dns import reversename, resolver

from pingscanner import PingScanner
from portscanner import PortScanner

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return None

def save_json(obj, filename):
    try:
        with open(filename, 'w+') as f:
            json.dump(obj, f, indent=4, sort_keys=True)
        return True
    except:
        return None


def main():
    proxy_filename = 'proxy.json'
    proxy = load_json(proxy_filename)

    if proxy:
        while True:
            if proxy['proxy_type'] == 1:
                proxy_type = 'SOCKS4'
            elif proxy['proxy_type'] == 2:
                proxy_type = 'SOCKS5'
            else:
                proxy_type = 'HTTP'
            proxy_addr = proxy['proxy_addr']
            proxy_port = proxy['proxy_port']
            proxy_username = proxy['proxy_username']
            proxy_password = proxy['proxy_password']

            sel = input(f'Using proxy:\
            \nType: {proxy_type}\
            \nAddress: {proxy_addr}\
            \nPort: {proxy_port}\
            \nUsername: {proxy_username}\
            \nPassword: {proxy_password}\
            \nContinue(y/n)?')
            if sel == 'y':
                break
            elif sel == 'n':
                proxy = None
                break
    if not proxy:
        proxy = {}
        proxy_type_inp = input('Enter proxy type (SOCKS5, SOCKS4, HTTP):')
        if proxy_type_inp == 'SOCKS5':
            proxy_type = socks.SOCKS5
        elif proxy_type_inp == 'SOCKS4':
            proxy_type = socks.SOCKS4
        elif proxy_type_inp == 'HTTP':
            proxy_type = socks.HTTP
        else:
            proxy_type = None
        proxy['proxy_type'] =       proxy_type
        proxy['proxy_addr'] =       input('Enter proxy address (ex. 127.0.0.1):')
        proxy['proxy_port'] =       input('Enter proxy port (ex. 9050):')
        proxy['proxy_username'] =   input('Enter proxy username (ex. user123):')
        proxy['proxy_password'] =   input('Enter proxy password (ex. ilovetomatoes):')

        save_json(proxy, proxy_filename)
        

    rng = input("Enter ip range: ")
    min_port = int(input("Enter minimum port: "))
    max_port = int(input("Enter maximum port: "))
    print('Scanning for alive hosts...')
    ips = PingScanner(rng).scan()
    if len(ips) > 0:
        print(f'\nGot {len(ips)} alive hosts!')
        for ip in ips:
            print(ip)
        print('\nScanning alive hosts for ports:')
    else:
        print(f'\nAlive hosts not found.')
    ips_dict = {}
    for ip in ips:
        print(f'\nScanning {ip}:')
        ips_dict[ip] = {}
        try:
            rev_name = reversename.from_address(ip)
        except:
            rev_name = None
        try:
            reversed_dns = str(resolver.query(rev_name, "PTR")[0]) or None
        except:
            reversed_dns = None

        print(f'Reversed DNS: {reversed_dns}')
        ips_dict[ip]['reversed_dns'] = reversed_dns
        prt_scnr = PortScanner(ip, min_port=min_port, max_port=max_port)
        prt_scnr.set_proxy(**proxy)
        ips_dict[ip]['ports'] = prt_scnr.scan()
    print()

    with open('output.json', 'w+') as f:
        json.dump(ips_dict, f, indent=4, sort_keys=True)

    input('Done!')

if __name__ == '__main__':
    main()