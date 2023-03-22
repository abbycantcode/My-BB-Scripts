import threading
import argparse

# A function to extract the root domain from a subdomain
def get_root_domain(subdomain):
    return '.'.join(subdomain.split('.')[-2:])

# A function to process a batch of subdomains and sort them by root domain
def process_batch(batch, domain_files):
    for subdomain in batch:
        root_domain = get_root_domain(subdomain)
        if root_domain in domain_files:
            with open(domain_files[root_domain], 'a') as f:
                f.write(subdomain + '\n')

# A function to split the subdomains file into batches and process them in parallel
def process_subdomains(subdomains_file, num_threads=4):
    # Read the subdomains file into a list
    with open(subdomains_file) as f:
        subdomains = f.read().splitlines()

    # Creating a dictionary to store the file handles for each root domain
    domain_files = {}

    # Starting a separate thread for each batch of subdomains
    batch_size = len(subdomains) // num_threads
    batches = [subdomains[i:i+batch_size] for i in range(0, len(subdomains), batch_size)]
    threads = []
    for batch in batches:
        for subdomain in batch:
            root_domain = get_root_domain(subdomain)
            if root_domain not in domain_files:
                domain_files[root_domain] = root_domain + '.txt'
                with open(domain_files[root_domain], 'w') as f:
                    pass
        thread = threading.Thread(target=process_batch, args=(batch, domain_files))
        thread.start()
        threads.append(thread)

    # Waiting for all threads to finish
    for thread in threads:
        thread.join()

# Parsing command-line arguments
parser = argparse.ArgumentParser(description='Sort subdomains by root domain.')
parser.add_argument('subdomains_file', help='the file containing the subdomains to sort')
parser.add_argument('-t', '--num_threads', type=int, default=4,
                    help='the number of threads to use (default: 4)')
args = parser.parse_args()

# Processing the subdomains file
process_subdomains(args.subdomains_file, num_threads=args.num_threads)
