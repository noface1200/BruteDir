import http.client
import urllib.parse
import os

def get(url):
    parsed_url = urllib.parse.urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)
    conn.request("GET", parsed_url.path or "/")
    response = conn.getresponse()

    if response.status == 301:
        new_url = response.getheader("Location")
        return get(new_url)
    else:
        return response

os.system('cls' if os.name == 'nt' else 'clear')
print("""
██████  ██████  ██    ██ ████████ ███████     ██████  ██ ██████  
██   ██ ██   ██ ██    ██    ██    ██          ██   ██ ██ ██   ██ 
██████  ██████  ██    ██    ██    █████       ██   ██ ██ ██████  
██   ██ ██   ██ ██    ██    ██    ██          ██   ██ ██ ██   ██ 
██████  ██   ██  ██████     ██    ███████     ██████  ██ ██   ██ 
""")

wordlist = []
input_target = input("URL: ").strip()
wordlist_file = input("WORDLIST: ").strip()

with open(wordlist_file, 'r') as file:
    for line in file:
        wordlist.append(line)

print()

for subpath in wordlist:
    url = input_target + r'/' + subpath
    e = get(url)

    # Assign status message based on the HTTP status code
    if 200 <= e.status < 300:
        status_message = "info"
    elif 400 <= e.status < 500:
        status_message = "warning"
    else:
        status_message = "error"

    # Print URL, status code, and message all on the same line
    print(f'{url} [{e.status}] {status_message}')
