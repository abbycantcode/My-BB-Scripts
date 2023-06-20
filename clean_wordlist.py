import argparse
import re
from tqdm import tqdm

# Define the regexes to filter out words
regexes = [
    # regex patterns...
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
