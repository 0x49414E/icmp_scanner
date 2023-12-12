#!/usr/bin/env python3 

import argparse
import signal
from termcolor import colored
import subprocess
from concurrent.futures import ThreadPoolExecutor
import sys

def def_handler(sig,frame):
    print(colored("\n[!] Exiting...", "red"));
    sys.exit(1);

signal.signal(signal.SIGINT, def_handler) # CTRL+C

def validate_target(target):
    
    # 192.168.1.1-100

    if '-' not in target:
        if len(target.split('.')) == 4:
            return [target];
        else: 
            print(colored(f"\n[!] IP Format is invalid.", "red"));
            return None;
    else:
        target_splitted = target.split('.'); # ['192', '168', '1', '1-100']
        first_three_octets = '.'.join(target_splitted[:3]);
        start, end = target_splitted[3].split('-');
        return [f"{first_three_octets}.{i}" for i in range(int(start), int(end) + 1)];
        

def get_arguments():
    parser = argparse.ArgumentParser(description="Host Discovery Tool via ICMP Protocol");
    parser.add_argument("-t", "--target", required=True, help="Specify a host or a range of the network", dest="target");

    args = parser.parse_args();

    return args.target;

def host_discovery(target):
    try: 
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1,stdout=subprocess.DEVNULL);
        if ping.returncode == 0:
            print(colored(f"\n[+] Host {target} is active!", "green"));
    except subprocess.TimeoutExpired: 
        pass;

def main():
    target = get_arguments()
    targets = validate_target(target)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(host_discovery, targets)
   
if __name__ == "__main__":
    main()
