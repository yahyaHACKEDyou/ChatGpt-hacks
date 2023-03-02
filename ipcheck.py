import threading
import queue
import socket
import socks
import requests

def check_socks4_proxy(ip_address, port, q):
  # Set up the socks4 proxy using the ip_address and port
  socks.set_default_proxy(socks.SOCKS4, ip_address, port)
  socket.socket = socks.socksocket
  # Try to connect to a website using the socks4 proxy
  try:
    response = requests.get("http://www.google.com")
    if response.status_code == 200:
      # Add the IP address and port to the queue if they are a valid socks4 proxy
      q.put((ip_address, port))
  except (ConnectionError, RequestException):
    pass

# Read the list of IP addresses and ports from the "ip.txt" file
with open("ip.txt") as f:
  ip_addresses_ports = [line.strip().split(":") for line in f]

# Create a queue to store the working IP addresses and ports
q = queue.Queue()

# Keep track of the number of threads started
thread_count = 0

# Iterate through the list of IP addresses and ports
for ip_address, port in ip_addresses_ports:
  # Start a new thread to check the IP address and port
  thread = threading.Thread(target=check_socks4_proxy, args=(ip_address, int(port), q))
  thread.start()
  thread_count += 1

# Open the "ip_addresses.txt" file in write mode
with open("ip_addresses.txt", "w") as f:
  # Wait for all the threads to finish
  while thread_count > 0:
    # Check if there are any working IP addresses and ports in the queue
    if not q.empty():
      # Write the IP address and port to the "ip_addresses.txt" file
      ip_address, port = q.get()
      f.write(f"{ip_address},{port}\n")
      print(f"{ip_address}:{port} is a valid socks4 proxy")
    # Decrement the thread count if a thread has finished
    thread_count -= 1

