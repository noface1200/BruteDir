import http.client
import urllib.parse
import os
import time

def get(url, retries=5, backoff_factor=2):
    parsed_url = urllib.parse.urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("GET", parsed_url.path or "/")
    response = conn.getresponse()

    if response.status == 302:
        new_url = response.getheader("Location")
        print(f"Redirecting to {new_url}...")
        return get(new_url)

    if response.status == 429:
        retry_after = response.getheader("Retry-After")
        if retry_after:
            try:
                retry_after_seconds = int(retry_after)
                print(f"Rate limited. Retrying in {retry_after_seconds} seconds...")
                time.sleep(retry_after_seconds)
            except ValueError:
                print(f"Rate limited. Retry after {retry_after}. Please wait...")
                time.sleep(60)
            return get(url)
        else:
            if retries > 0:
                wait_time = backoff_factor ** (5 - retries)
                print(f"Rate limited. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                return get(url, retries=retries-1)

    return response

os.system('cls' if os.name == 'nt' else 'clear')

print("""
██████  ██████  ██    ██ ████████ ███████     ██████  ██ ██████  
██   ██ ██   ██ ██    ██    ██    ██          ██   ██ ██ ██   ██ 
██████  ██████  ██    ██    ██    █████       ██   ██ ██ ██████  
██   ██ ██   ██ ██    ██    ██    ██          ██   ██ ██ ██   ██ 
██████  ██   ██  ██████     ██    ███████     ██████  ██ ██   ██ 
""")

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

wordlist = []
input_target = input("URL: ").strip()
wordlist_file = input("WORDLIST: ").strip()

with open(wordlist_file, 'r') as file:
    for line in file:
        wordlist.append(line.strip())

print()

for subpath in wordlist:
    subpath = subpath.strip("/")
    url = input_target.rstrip("/") + '/' + subpath
    e = get(url)

    if 200 <= e.status < 300:
        status_message = f"{GREEN}info{RESET}"
    elif 400 <= e.status < 500:
        status_message = f"{YELLOW}warning{RESET}"
    elif e.status == 429:
        status_message = f"{RED}rate-limited{RESET}"
    elif e.status == 302:
        status_message = f"{YELLOW}redirect{RESET}"
    else:
        status_message = f"{RED}error{RESET}"

    print(f'{url} [{e.status}] {status_message}', end="")
    print()
