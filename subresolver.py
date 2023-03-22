import threading
import argparse
import socket

# Defining function to resolve a domain to an IP address
def resolve_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return (domain, ip_address)
    except socket.gaierror:
        return None

# Defining function to process a batch of domains and resolve them to IP addresses
def process_batch(batch, results_file):
    for domain in batch:
        result = resolve_domain(domain)
        if result is not None:
            (domain, ip_address) = result
            with open(results_file, 'a') as f:
                f.write(domain + ',' + ip_address + '\n')

# Defining function to split the domains file into batches and process them in parallel
def resolve_domains(domains_file, num_threads=4):
    # Read the domains file into a list
    with open(domains_file) as f:
        domains = f.read().splitlines()

    # Creating a file to store the results
    results_file = 'resolved_domains.txt'
    with open(results_file, 'w') as f:
        pass

    # Starting a separate thread for each batch of domains
    batch_size = len(domains) // num_threads
    batches = [domains[i:i+batch_size] for i in range(0, len(domains), batch_size)]
    threads = []
    for batch in batches:
        thread = threading.Thread(target=process_batch, args=(batch, results_file))
        thread.start()
        threads.append(thread)

    # Waiting for all threads to finish
    for thread in threads:
        thread.join()

    # Reading the results file and extracting unique Domains and IP addresses
    with open(results_file) as f:
        lines = f.read().splitlines()
        domains_set = set()
        ip_addresses_set = set()
        for line in lines:
            domain, ip_address = line.split(',')
            domains_set.add(domain)
            ip_addresses_set.add(ip_address)

    # Writing unique domains to a file
    alive_domains_file = 'alive_domains.txt'
    with open(alive_domains_file, 'w') as f:
        for domain in domains_set:
            f.write(domain + '\n')

    # Writing unique IP addresses to a file
    ip_addresses_file = 'ip_addr.txt'
    with open(ip_addresses_file, 'w') as f:
        for ip_address in ip_addresses_set:
            f.write(ip_address + '\n')

# Parsing command-line arguments
parser = argparse.ArgumentParser(description='Resolve domains to IP addresses.')
parser.add_argument('domains_file', help='the file containing the domains to resolve')
parser.add_argument('-t', '--num_threads', type=int, default=4,
                    help='the number of threads to use (default: 4)')
args = parser.parse_args()

# Resolving the domains and extracting unique domains and IP addresses
resolve_domains(args.domains_file, num_threads=args.num_threads)
