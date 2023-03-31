import argparse
import re

# Define the regexes to filter out words
regexes = [
    r"[\!(,%]",  # Ignore noisy characters
    r".{100,}",  # Ignore lines with more than 100 characters (overly specific)
    r"[0-9]{4,}",  # Ignore lines with 4 or more consecutive digits (likely an id)
    r"[0-9]{3,}$",  # Ignore lines where the last 3 or more characters are digits (likely an id)
    r"[a-z0-9]{32}",  # Likely MD5 hash or similar
    r"[0-9]+[A-Z0-9]{5,}",  # Number followed by 5 or more numbers and uppercase letters (almost all noise)
    r"\/.*\/.*\/.*\/.*\/.*\/.*\/.*\/.*\/.*\/",  # Ignore lines more than 9 directories deep (overly specific)
    r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}",  # Ignore UUIDs
    r"[0-9]+[a-zA-Z]+[0-9]+[a-zA-Z]+[0-9]+",  # Ignore multiple numbers and letters mixed together (likely noise)
    r"\.(png|jpg|jpeg|gif|svg|bmp|ttf|avif|wav|mp4|aac|ajax|css|all|woff|woff2)$",  # Ignore low value filetypes
    r"^$",  # Ignores blank lines
]

# Set up the command line argument parser
parser = argparse.ArgumentParser(description="Clean a wordlist file.")
parser.add_argument("input_file", metavar="input_file", help="The input file to clean.")

# Parse the command line arguments
args = parser.parse_args()

# Get the input file name from the command line arguments
input_file = args.input_file

print(f"[+] Cleaning {input_file}")
with open(input_file, "r") as f:
    original_words = f.readlines()

original_size = len(original_words)

# Remove words that match the regexes
filtered_words = []
for word in original_words:
    word = word.strip()
    skip_word = False
    for regex in regexes:
        if re.search(regex, word):
            skip_word = True
            break
    if not skip_word:
        filtered_words.append(word)

# Sort and remove duplicates
filtered_words = sorted(list(set(filtered_words)))

# Write cleaned words to a new file
output_file = input_file + "_cleaned"
with open(output_file, "w") as f:
    f.write("\n".join(filtered_words))

new_size = len(filtered_words)
removed = original_size - new_size

print(f"[-] Removed {removed} lines")
print(f"[+] Wordlist is now {new_size} lines")
print("[+] Done")
