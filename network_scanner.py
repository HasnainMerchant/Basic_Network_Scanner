import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor


ip_addresses = []
ports = []

#Function To Scan Single Port
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect_ex(ip, port)
            return f"Port {port} on {ip} is open"
    except:
        return f"Port {port} on {ip} is closed"

#Function To Scan Multiple Ports on A Single IP Address
def scan_ip(ip, ports):
    results = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in ports]
        for future in futures:
            results.append(future.result())
        return results

#Function To Scan Multiple IP Addresses
def scan_network(ip_addresses, ports):
    all_results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scan_ip, ip, ports): ip for ip in ip_addresses}
        for future in futures:
            ip = futures[future]
            all_results[ip] = future.result()
    return all_results
        

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

def print_scan_results(results):
    for ip, result in results.items():
        print(f"Results for {ip}:")
        for res in result:
            print(res)

#Main Function
if __name__ == "__main__":
    #Function To Fill The Queue with Ports for efficient Threading
    def fill_queue(port_list):
        for port in port_list:
            ports.append(port)

    print_header()
    ip_address = input('Enter IP Address / Addresses - ')
    if ip_address == '':
        print("[-] Enter An IP Address")
        exit()
    else:
        for ip in ipaddress.IPv4Network(ip_address, strict=False):
            ip_addresses.append(str(ip))
    print_options()
    option = input('Enter Option - ')

    if option == '1':
        fill_queue(range(1, 65536))
        print(ports)
    elif option == '2':
        input_ports = input('Enter Port Numbers (seperated by comma) - ')
        fill_queue(input_ports.split(','))
        print(ports)
    elif option == '3':
        fill_queue([20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 119, 123, 143, 161, 194, 443, 546, 547])
        print(ports)
    else:
        print("[-] Enter Correct Options")
        exit()
    
    results = scan_network(ip_addresses, ports)
    print_scan_results(results)