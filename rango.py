import requests
import sys
import re
import os

def print_banner(num_cidrs):
    banner = f"""
    ######################################################
    #                                                    #
    #              IP Range Status Checker               #
    #                                                    #
    #            Muestra IP - Status Code - Ok/Error     #
    #                                                    #
    ######################################################
    #                                                    #
    #                Hecho por Murphy                    #
    #                                                    #
    ######################################################
    Total CIDRs identificados: {num_cidrs}
    """
    print(banner)

def post_ip_range(input_file, output_file):
    url = "https://ipgen.hasarin.com/iprange"
    headers = {
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not?A_Brand";v="99", "Chromium";v="130"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://ipgen.hasarin.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://ipgen.hasarin.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }

    ip_pattern = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')  # Pattern to match IPs only
    log_file = f"{os.path.splitext(input_file)[0]}.log"  # Log file name based on input file name

    # Contar los CIDRs en el archivo de entrada
    num_cidrs = sum(1 for line in open(input_file) if '/' in line)
    print_banner(num_cidrs)
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(log_file, 'w') as log:
        for count, line in enumerate(infile, start=1):
            line = line.strip()
            if '/' not in line:
                continue

            ip, mask = line.split('/')
            data = {
                "ipstart": "",
                "ipend": "",
                "iprangetype": "cidr",
                "ipcidr": ip,
                "mask": mask
            }
            
            response = requests.post(url, headers=headers, data=data)
            status_message = f"{count}. {ip}/{mask} {response.status_code} {'Ok' if response.ok else 'Error'}"
            print(status_message)  # Print status message on screen
            log.write(status_message + "\n")  # Write status message to the log file

            if response.ok:
                # Extract only the IPs from the response content
                ips = ip_pattern.findall(response.text)
                for extracted_ip in ips:
                    outfile.write(extracted_ip + "\n")

    return num_cidrs

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        post_ip_range(input_file, output_file)
