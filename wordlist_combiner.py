import sys
import threading

if len(sys.argv) != 4:
    print("Usage: python wordlist_combiner.py user.txt pass.txt num_threads")
    sys.exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]
num_threads = int(sys.argv[3])
outfile = "combined-wordlist.txt"

words1 = []
with open(file1, "r") as f1:
    for line in f1:
        words1.append(line.strip())

words2 = []
with open(file2, "r") as f2:
    for line in f2:
        words2.append(line.strip())

lock = threading.Lock()

def write_permutations(words):
    with open(outfile, "a") as f_out:
        for word1 in words:
            for word2 in words2:
                line = "{}:{}\n".format(word1, word2)
                with lock:
                    f_out.write(line)

# Dividing the words into chunks for each thread
word_chunks = [words1[i::num_threads] for i in range(num_threads)]

threads = []
for chunk in word_chunks:
    thread = threading.Thread(target=write_permutations, args=(chunk,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
