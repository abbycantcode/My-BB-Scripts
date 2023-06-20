import argparse
import re
from tqdm import tqdm

# Define the regexes to filter out words
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
    r"[A-Z]{5,}", # 5 or more consecutive capital characters which are usually junk or of no use
    r"\b(\d+|xx)\.html\b", # Some more spam endpoints filtered
    r"^\w+(?:[-+]\w+){2,}$", # Location spams
    r"\b[a-zA-Z0-9-]*\d[a-zA-Z0-9-]*\.[a-zA-Z]+\b" # Spammy subdomains
]

# Set up the command line argument parser
parser = argparse.ArgumentParser(description="Clean a wordlist file.")
parser.add_argument("input_file", metavar="input_file", help="The input file to clean.")

# Parse the command line arguments
args = parser.parse_args()

# Get the input file name from the command line arguments
input_file = args.input_file

print(f"[+] Cleaning {input_file}")

# Step 1: Count the number of lines in the input file
with open(input_file, "r") as f:
    original_size = sum(1 for _ in f)

# Step 2: Create a progress bar with the total number of lines
progress_bar = tqdm(total=original_size)

# Step 3: Process the lines in the input file and filter out unwanted words
filtered_words = []
with open(input_file, "r") as f:
    for line in f:
        line = line.strip()
        skip_word = False
        for regex in regexes:
            if re.search(regex, line):
                skip_word = True
                break
        if not skip_word:
            filtered_words.append(line)
        progress_bar.update(1)  # Update the progress bar for each line processed

# Step 4: Close the progress bar
progress_bar.close()

# Step 5: Sort and remove duplicates from the filtered words
filtered_words = sorted(set(filtered_words))

# Step 6: Write cleaned words to a new file
output_file = input_file + "_cleaned"
with open(output_file, "w") as f:
    f.write("\n".join(filtered_words))

new_size = len(filtered_words)
removed = original_size - new_size

print(f"[-] Removed {removed} lines")
print(f"[+] Wordlist is now {new_size} lines")
print("[+] Done")
