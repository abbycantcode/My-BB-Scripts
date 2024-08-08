import subprocess
import os
import concurrent.futures
import logging
from collections import defaultdict
import argparse
from datetime import datetime
from xml.etree import ElementTree as ET

# Set up logging
logging.basicConfig(filename='nmap_scan.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run nmap scans based on IP:Port input and combine the results.')
    parser.add_argument('-i', '--input', type=str, default='naabu_results.txt', help='Input file with IP:Port data')
    parser.add_argument('-o', '--output', type=str, default='nmap-out', help='Output directory for nmap results')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of threads for parallel execution')
    return parser.parse_args()

def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    logging.info(f"Output directory '{output_dir}' is ready.")

def parse_file(file_path):
    ip_ports = defaultdict(list)
    try:
        with open(file_path, "r") as file:
            for line in file:
                ip, port = line.strip().split(":")
                ip_ports[ip].append(port)
        logging.info(f"Parsed {len(ip_ports)} unique IPs from file.")
    except Exception as e:
        logging.error(f"Failed to parse file: {e}")
        raise
    return ip_ports

def run_nmap(ip, ports, output_dir):
    ports_str = ",".join(ports)
    output_file = os.path.join(output_dir, f"nmap_out_{ip}.xml")
    nmap_command = ["nmap", "-sV", "-Pn", "-p", ports_str, "-oX", output_file, ip]
    
    try:
        logging.info(f"Running command: {' '.join(nmap_command)}")
        subprocess.run(nmap_command, check=True)
        logging.info(f"Completed scan for {ip}. Output saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run nmap for {ip}: {e}")

def combine_nmap_xml_files(output_dir, combined_filename="nmap_out.xml"):
    combined_root = None
    xml_files = [f for f in os.listdir(output_dir) if f.startswith("nmap_out_") and f.endswith(".xml")]

    for xml_file in xml_files:
        file_path = os.path.join(output_dir, xml_file)
        
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            if combined_root is None:
                combined_root = ET.Element(root.tag, root.attrib)
                for child in list(root):
                    combined_root.append(child)
            else:
                for child in list(root):
                    combined_root.append(child)

        except ET.ParseError as e:
            logging.error(f"Error parsing {file_path}: {e}")
    
    if combined_root is not None:
        combined_tree = ET.ElementTree(combined_root)
        combined_output_path = os.path.join(output_dir, combined_filename)
        combined_tree.write(combined_output_path)
        logging.info(f"Combined XML saved to {combined_output_path}")
    else:
        logging.warning("No valid XML files found to combine.")

def main():
    args = parse_arguments()
    
    # Generate a unique timestamped directory for each run
    timestamped_dir = os.path.join(args.output, datetime.now().strftime('%Y%m%d_%H%M%S'))
    create_output_directory(timestamped_dir)
    
    ip_ports = parse_file(args.input)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(run_nmap, ip, ports, timestamped_dir) for ip, ports in ip_ports.items()]
        concurrent.futures.wait(futures)
    
    logging.info("All nmap scans completed. Starting to combine XML files.")
    combine_nmap_xml_files(timestamped_dir)
    logging.info("All tasks completed successfully.")

if __name__ == "__main__":
    main()
