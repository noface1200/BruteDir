import requests
import time
from colorama import Fore, Back, Style, init
init()


banner = rf"""
 {Fore.WHITE} ____             _      {Fore.YELLOW} ____  _      
 {Fore.WHITE}| __ ) _ __ _   _| |_ ___{Fore.YELLOW}|  _ \(_)_ __ 
 {Fore.WHITE}|  _ \| '__| | | | __/ _ {Fore.YELLOW}\ | | | | '__|
 {Fore.WHITE}| |_) | |  | |_| | ||  __{Fore.YELLOW}/ |_| | | |   
 {Fore.WHITE}|____/|_|   \__,_|\__\___{Fore.YELLOW}|____/|_|_|  

  {Fore.WHITE} Recommand:

  {Fore.YELLOW} Thread should be 1 

  {Fore.YELLOW} And make Sure the URL have no scheme!
"""
print(banner)

Input_Target = input(Fore.WHITE+"URL: ")
Input_wordlist = input(Fore.WHITE+"Wordlist: ")
Input_thread = int(input(Fore.WHITE+"Threads: "))  


if not Input_Target.startswith(('http://', 'https://')):
    Input_Target = 'http://' + Input_Target


with open(Input_wordlist, "r") as WL:
    for word in WL:
        word = word.strip() 
        url = f"{Input_Target}/{word}"  

        reply = requests.get(url)
        if reply.status_code == 200:
            print(Fore.GREEN+f"[~] Found: {url}")
        elif reply.status_code == 404:
            print(Fore.RED+f"[!] Cannot Find: {url}")
        else:
            print(Fore.YELLOW+f"[?] Status {reply.status_code} for {url}")

        time.sleep(Input_thread)  

input("Click Enter To Exit")
