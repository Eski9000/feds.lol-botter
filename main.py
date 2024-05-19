import requests
from bs4 import BeautifulSoup
import threading
import os

os.system('title .gg/krush & cls')
def scrape_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    proxies = soup.get_text().split('\r\n')
    return proxies

def check_proxy(proxy, valid_proxies):
    try:
        response = requests.get("https://www.google.com", proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            print(f"\033[92mValid proxy found: {proxy}\033[0m")
            valid_proxies.append(proxy)
    except:
        print(f"\033[91mInvalid proxy: {proxy}\033[0m")

def checkandstart(biolink):
    valid_proxies = []
    proxies = scrape_proxies()

    threads = []
    for proxy in proxies:
        thread = threading.Thread(target=check_proxy, args=(proxy, valid_proxies))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"\033[94mTotal valid proxies: {len(valid_proxies)}\033[0m")
    if len(valid_proxies) > 0:
        start_view_bot(valid_proxies, biolink)
    else:
        print("\033[91mNo valid proxies found.\033[0m")

def make_request_with_proxy(proxy, biolink):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://feds.lol',
        'priority': 'u=1, i',
        'referer': 'https://feds.lol/luxury',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    json_data = {
        'biolink': biolink,
    }

    try:
        response = requests.post('https://feds.lol/api/biolink/manage/view', 
                                 headers=headers, 
                                 json=json_data,
                                 proxies={'http': proxy, 'https': proxy},
                                 timeout=10)
        
        print(f"\033[92mSent view > {biolink} with {proxy}\033[0m")
    except:
        print(f"\033[91mFailed to send view > {biolink} with {proxy}\033[0m")

def start_view_bot(valid_proxies, biolink):
    threads = []
    for proxy in valid_proxies:
        thread = threading.Thread(target=make_request_with_proxy, args=(proxy, biolink))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

biolink = input('\033[94mUser > \033[0m')

checkandstart(biolink)
