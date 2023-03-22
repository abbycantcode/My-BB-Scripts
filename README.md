# My-BB-Scripts
This repository contains that I use personally in by bug-bounty workflow

## sort_subdomains.py:
- This script sorts huge list of subdomains(multiple root-domains) from a file to new files belonging to a particular root-domain with their name on it.
- For example: all subdomains belonging to 'google.com' will be added to a file named 'google.com.txt'.
- This can be later be used to do domain specific recon or alt/perm using regulator where we can only provide one domain file at a time, plus easy to organise as well. 
- Usage: `python3 sort_subdomains.py subs.txt -t 10`

## subresolver.py:
- This script takes a list of subdomains resolve it to see the alive ones and sort them out in different files.
- Usage: `python3 subresolver.py domains.txt -t 10`
- Resulting files will be:
  - `alive_domains.txt` -> Contains domain names that did resolve to an IP
  - `resolved_domains.txt` -> Resolved domains from the original list and their IP as a comma separated value
  - `ip_addr.txt` -> Unique IP address that the domains resolved to
