import socket
import ipaddress
from queue import Queue
import threading
import copy


open_ports = {}
unreachable_ip = []

def scan_network(ip_address, queue_port):
    queue_list = copy.copy(queue_port)
    thread_list = []
    def scan_port(port):
        try:
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Attempt to connect to the IP address and port
            sock.connect_ex((ip, port))
            sock.close()
            return True
        except:
            return False
    def worker(queue_list):
        while not len(queue_list) == 0:
            port = queue_list.pop(0)
            if scan_port(port):
                print(f'Port {port} is Open for IP {ip} !')
                open_ports[ip] = port
            else:
                unreachable_ip.append(ip)
    
    for ip in ipaddress.IPv4Network(ip_address):
        ip = str(ip)
        print(f"Scanning IP: {ip}")
        queue_list = copy.copy(queue_port)
        try:
            for t in range(100):
                thread = threading.Thread(target=worker, args=[queue_list])
                thread_list.append(thread)
            for thread in thread_list:
                thread.start()
            for thread in thread_list:
                thread.join()
            thread_list.clear()
        except KeyboardInterrupt:
            thread_list.clear()
            thread.join()

def print_header():
    # Get Ip Address Range From User
    print('========================================')
    print('            Network Scanner             ')
    print('========================================')

def print_options():
    # Define a list of ports to scan
    # Default is Scan common Port, get user specified ports or scan all ports
    print('''
        Port Scanning Options - 
          1. To Scan All Ports
          2. Enter Specific Port Numbers
          3. To Scan Common Ports
          ''')

def print_scan_results():
    print(open_ports)
    print(unreachable_ip)

#Main Function
if __name__ == "__main__":
    queue_ports = []

    #Function To Fill The Queue with Ports for efficient Threading
    def fill_queue(port_list):
        for port in port_list:
            queue_ports.append(port)

    print_header()
    ip_address = input('Enter IP Address / Addresses - ')
    if ip_address == '':
        print("[-] Enter An IP Address")
        exit()
    print_options()
    option = input('Enter Option - ')

    if option == '1':
        fill_queue(range(1, 65536))
    elif option == '2':
        ports = input('Enter Port Numbers (seperated by comma) - ')
        fill_queue(ports.split(','))
    elif option == '3':
        fill_queue([20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 119, 123, 143, 161, 194, 443, 546, 547])
    else:
        print("[-] Enter Correct Options")
        exit()
    
    scan_network(ip_address, queue_ports)
    print_scan_results()