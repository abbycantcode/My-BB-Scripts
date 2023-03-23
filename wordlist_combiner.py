import sys

if len(sys.argv) != 3:
    print("Usage: python script.py file1.txt file2.txt")
    sys.exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]
outfile = "combined-wordlist.txt"

words1 = []
with open(file1, "r") as f1:
    for line in f1:
        words1.append(line.strip())

words2 = []
with open(file2, "r") as f2:
    for line in f2:
        words2.append(line.strip())

with open(outfile, "w") as f_out:
    for word1 in words1:
        for word2 in words2:
            f_out.write("{}:{}\n".format(word1, word2))
