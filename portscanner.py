# Import the necessary modules for socket programming
from socket import socket, AF_INET, SOCK_STREAM, getservbyport
# Import the threading module for multi-threading
import threading
# Import the ipaddress module for working with IP addresses
import ipaddress
# Import the time module for timing purposes
import time

class PortScanner():
    # Initialize the class and set class variables
    def __init__(self, ip, first, last, num_threads=100):
        # The IP address to be scanned
        self.ip = ip
        # The first port number to start scanning
        self.first = first
        # The last port number to end scanning
        self.last = last
        # The number of threads to use for scanning
        self.num_threads = num_threads
        # A list of all the ports to be scanned
        self.ports = [p for p in range(first, last+1)]
        # A list of all the open ports
        self.open_ports = []
        # A lock to prevent data race while accessing shared data
        self.lock = threading.Lock()
        # A list of IP addresses that are not reachable
        self.notReach = []

    # Get the service running on a particular port
    def getService(self, port):
        try:
            # Use the getservbyport function to get the service name
            service = getservbyport(port, "tcp")
        except OSError:
            # If the service name is not found, set it to "Unknown"
            service = "Unknown"
        return service

    # Start the scan
    def start(self):
        # Initialize variables
        reachable = False
        notReachable = []
        # Loop through the ports, creating a list of threads
        for i in range(0, self.last - self.first + 1, self.num_threads):
            threads = [threading.Thread(target=self.scan, args=(self.ip, port)) for port in self.ports[i:i+self.num_threads]]
            # Start all the threads
            for t in threads:
                t.start()
            # Wait for all the threads to finish
            for t in threads:
                t.join()
        # If there are no open ports, add the IP address to the list of unreachable IPs
        if not self.open_ports:
            self.notReach.append(self.ip)
        else:
            reachable = True
            # Print the open ports for the reachable IP address
            print(f"\n[+] Scanning {self.ip} Ports...")            
            print("*"*64)
            print(*self.open_ports, sep="\n")
            print()
        
    # Scan a single port for the given IP address
    def scan(self, ip, port):
    # Create a socket object
        s = socket(AF_INET, SOCK_STREAM)
        # Set the timeout to 0.1 seconds
        s.settimeout(0.1)
        try:
            # Connect to the target host on the specified port
            s.connect((ip, port))
            # Get the service name running on the open port
            service = self.getService(port)
            # Acquire the lock to prevent multiple threads from accessing the open_ports list at the same time
            with self.lock:
                self.open_ports.append(f"[-] Port {port} for {ip} is open, Service is: {service}...")
        except:
        # In case of an error, do nothing
            pass
        # Close the socket
        s.close()