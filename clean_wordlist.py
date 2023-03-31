import argparse
import re

# Define the regexes to filter out patterns
regexes = [
    r"^[^A-Za-z0-9]+$", # Ignore a line containing only special characters
    r"[\!(,%]",  # Ignore noisy characters
    r"\b\d{1,2}/\d{1,2}\b", # Ignoring date like things
    r"^\d{2,}$", # Ignoring if only numbers are present
    r"&&{2,}",  # Ignore consecutive ampersand symbols
    r"(=){2,}", # Ignore consecutive or more equals to sign
    r"^\+.*", # Ignore lines that starts with '+' symbol
    r"\);\*/", # Ignore this, some nuances I've found when curating target specific wordlist
    r"^'\+.*", # Ignore this pattern
    r".{100,}",  # Ignore lines with more than 100 characters (overly specific)
    r"[0-9]{4,}",  # Ignore lines with 4 or more consecutive digits (likely an id)
    r"[0-9]{3,}$",  # Ignore lines where the last 3 or more characters are digits (likely an id)
    r"[a-z0-9]{32}",  # Likely MD5 hash or similar
    r"[0-9]+[A-Z0-9]{5,}",  # Number followed by 5 or more numbers and uppercase letters (almost all noise)
    r"\/.*\/.*\/.*\/.*\/.*\/.*\/",  # Ignore lines more than 6 directories deep (overly specific)
    r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}",  # Ignore UUIDs
    r"[0-9]+[a-zA-Z]+[0-9]+[a-zA-Z]+[0-9]+",  # Ignore multiple numbers and letters mixed together (likely noise)
    r"^[,.;:'\"\[\]\|\-_=+\)\(\*\^\%\$\#\@\!\`\~]", # Ignore lines starting with these special characters
    r"^(?:%2C|%2E|%3B|%3A|%27|%22|%5B|%7B|%5D|%7D|%7C|%5C|%2D|%5F|%3D|%2B|%29|%28|%2A|%5E|%25|%24|%23|%40|%21|%60|%7E)", # Ignores URl Encoded version of the above characters(also only if it is present at the start of the line)
    r"\.(png|jpg|jpeg|gif|svg|bmp|ttf|avif|wav|mp4|aac|ajax|css|all|JPG|JPEG|PNG|CSS|woff|woff2)$",  # Ignore low value filetypes
    r"&[#\w]*;(,|\.|;|:|'|\"|\[|\{|\}|\]|\||\\|\-|_|=|\+|\)|\(|\*|\^|%|\$|#|@|!|~)", # Ignore HTML Encoded version of the special characters if they are present at the start.
    r"&[a-zA-Z]+;", # Ignore XML Encoded characters
    r"^$",  # Ignores blank lines
    r"^[^A-Za-z0-9\s]", # Ignore Lines starting with special characters
]

# Setting up the command line argument parser
parser = argparse.ArgumentParser(description="Clean a wordlist file.")
parser.add_argument("input_file", metavar="input_file", help="The input file to clean.")

# Parsing the command line arguments
args = parser.parse_args()

# Getting the input file name from the command line arguments
input_file = args.input_file

print(f"[+] Cleaning {input_file}")
with open(input_file, "r") as f:
    original_words = f.readlines()

original_size = len(original_words)

# Removing words that match the regexes
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

# Sorting and removing duplicates
filtered_words = sorted(list(set(filtered_words)))

# Writing cleaned words to a new file
output_file = input_file + "_cleaned"
with open(output_file, "w") as f:
    f.write("\n".join(filtered_words))

new_size = len(filtered_words)
removed = original_size - new_size

print(f"[-] Removed {removed} lines")
print(f"[+] Wordlist is now {new_size} lines")
print("[+] Done")
