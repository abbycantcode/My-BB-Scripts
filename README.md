# My-BB-Scripts
This repository contains that I use personally in by bug-bounty workflow

## sort_subdomains.py:
- This script sorts huge list of subdomains(multiple root-domains) from a file to new files belonging to a particular root-domain with their name on it.
- For example: all subdomains belonging to 'google.com' will be added to a file named 'google.com.txt'.
- This can be later be used to do domain specific recon or alt/perm using regulator where we can only provide one domain file at a time, plus easy to organise as well. 
- Usage: `python3 sort_subdomains.py subs.txt -t 10`
