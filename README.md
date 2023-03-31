# My-BB-Scripts
This repository contains one off scripts that I use personally in by bug-bounty workflow. These are simply some tasks that I have regularly come up while hunting bugs and doing stuff in terminal.

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

## wordlist_combiner.py
- This script is specifically used for making a combined-wordlist of `user:pass` for bruteforcing attack from a tool like `hydra`
  - It will have all the permutations of users and passwords from both files.
- Usage: python3 wordlist_combiner.py user.txt pass.txt num_threads
- The output of this will be in a new file `combined-wordlist.txt` in the format
```
user1:pass1
user1:pass2
user1:pass3
user2:pass1
user2:pass2
... so on
```

## wordlist_cleaner.py
- This script cleans a huge ass wordlist from noisy and unncessary things such as not useful file extensions which can be later used to create a new target specific wordlist or even permutations of it so we can do content discovery with it afterwards.
- Usage: `python3 wordlist_cleaner.py wordlist.txt`
- The output will be saved in a new file: `wordlist.txt_cleaned`
- This is a modified version of what @BonJarber made a few years back. You can check the original one here: [clean_wordlist.sh](https://github.com/BonJarber/SecUtils/blob/master/clean_wordlist/clean_wordlist.sh)
