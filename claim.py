import requests
import random
import os
import colorama
from colorama import Fore, Style, init as colorama_init
import time
import json
import sys

colorama_init(autoreset=True)

cool_blue = Fore.BLUE + Style.BRIGHT
cool_green = Fore.GREEN + Style.BRIGHT
cool_red = Fore.RED + Style.BRIGHT

os.system('cls' if os.name == 'nt' else 'clear')

header = f"""
{cool_blue}============================================
{cool_blue}       GENSHIN CODE EXTRACTOR
{cool_blue}============================================
"""

print(header)

with open('proxies.json', 'r') as proxies_file:
    proxies_data = json.load(proxies_file)

proxies = proxies_data.get('proxies', [])

def print_progress(iteration, total, prefix='', suffix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()

def claim_code(token, claimer_link, proxy):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "cookie": "__dcfduid=6f575b70191f11ed97da1f757024d5d7; __sdcfduid=6f575b71191f11ed97da1f757024d5d71201146a0fe8b2af2c79af28e32aea073ecc34c95ace9556676f8372725bf8a8;",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImvuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE0MTAyMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

    try:
        response = requests.post(claimer_link, headers=headers, proxies={"http": proxy})
        if response.status_code == 204:
            print(cool_green + "Code Claimed Successfully")
        else:
            print(cool_red + "Code Claiming Failed")

    except Exception as e:
        print(cool_red + "Error Claiming Code:", str(e))

def genshin_code_extractor():
    tokens_file = 'tokens.txt'
    codes_file = 'codes.txt'
    claimer_link = "https://discord.com/api/v9/outbound-promotions/1138162966638907422/claim"

    try:
        with open(tokens_file, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(cool_red + "Tokens file not found.")
        return

    if not lines:
        print(cool_red + "No Tokens Left")
        os.system('pause')
        return

    print(cool_blue + "Claiming Genshin Impact Gift Pack Bundle Codes...\n")

    total_tokens = len(lines)
    start_time = time.time()

    for i, line in enumerate(lines, start=1):
        token = line.split(':')[-1]  
        claim_code(token, claimer_link, random.choice(proxies))  # Randomly select a proxy
        url = 'https://discord.com/api/v9/users/@me/outbound-promotions/codes?locale=en-GB'
        headers = {
            'authorization': token,
        }

        try:
            response = requests.get(url, headers=headers).json()
            print(response)

            if response:
                for item in response:
                    if 'outbound_title' in item['promotion'] and item['promotion']['outbound_title'] == "Genshin Impact Gift Pack Bundle\n":
                        code = item['code']
                        with open(codes_file, 'a') as the_file:
                            the_file.write(code + '\n')
                        print(cool_green + f"Code Found -> {code}")

            elapsed_time = time.time() - start_time
            print_progress(i, total_tokens, prefix=f"{cool_blue}Progress:", suffix=f"Time Elapsed: {elapsed_time:.2f} seconds", length=30)

        except Exception as e:
            print(cool_red + "Error:", str(e))

    with open(tokens_file, 'w') as f:
        f.write('\n'.join(lines[1:]))

    print("\n" + cool_green + "Extraction Completed.")
    os.system('pause')

if __name__ == "__main__":
    genshin_code_extractor()

