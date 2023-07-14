import os
import sys
import requests
import concurrent.futures
from tqdm import tqdm
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Function to download a file from a given URL
def download_file(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        filename = os.path.basename(urlparse(url).path)
        filename, file_extension = os.path.splitext(filename)

        # Generate a unique filename
        counter = 1
        while os.path.exists(os.path.join('downloaded-js', filename + f'_{counter}' + file_extension)):
            counter += 1

        filename = filename + f'_{counter}' + file_extension
        filepath = os.path.join('downloaded-js', filename)

        with open(filepath, 'wb') as f:
            f.write(response.content)

        return url

# Create the 'downloaded-js' folder if it doesn't exist
if not os.path.exists('downloaded-js'):
    os.makedirs('downloaded-js')

# Check if the file argument is provided
if len(sys.argv) < 2:
    print('Please provide a file with URLs as an argument.')
    sys.exit(1)

# Get the file path from command-line arguments
file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(file_path):
    print(f'File "{file_path}" does not exist.')
    sys.exit(1)

# Read the URLs from the file
with open(file_path, 'r') as f:
    urls = f.read().splitlines()

# Create a progress bar
progress_bar = tqdm(total=len(urls), desc='Downloading', unit='file(s)')

# Function to update the progress bar
def update_progress_bar(url):
    progress_bar.update()

# Download files using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Submit download tasks to the executor
    futures = [executor.submit(download_file, url) for url in urls]

    # Process completed tasks as they finish
    for future in concurrent.futures.as_completed(futures):
        url = future.result()
        if url:
            update_progress_bar(url)

progress_bar.close()
print('All files downloaded successfully.')
