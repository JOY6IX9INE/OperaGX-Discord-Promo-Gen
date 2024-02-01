import requests, time
import concurrent.futures
import os, uuid, ctypes
from random import choice
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

os.system('cls' if os.name == 'nt' else 'clear')

class Counter:
    count = 0

class PromoGenerator:
    red = '\x1b[31m(-)\x1b[0m'
    blue = '\x1b[34m(+)\x1b[0m'
    green = '\x1b[32m(+)\x1b[0m'
    yellow = '\x1b[33m(!)\x1b[0m'

    def __init__(self, proxy=None):
        self.proxy = proxy
        self.session = self.create_session()

    def create_session(self):
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def generate_promo(self):
        url = "https://api.discord.gx.games/v1/direct-fulfillment"
        headers={
            'authority': 'api.discord.gx.games',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.opera.com',
            'referer': 'https://www.opera.com/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera GX";v="106"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
        }

        data = {
            "partnerUserId": str(uuid.uuid4())
        }

        try:
            if self.proxy:
                formatted_proxy = f"http://{self.proxy}"
                response = self.session.post(url, json=data, headers=headers, proxies={'http': formatted_proxy, 'https': formatted_proxy}, timeout=5)
            else:
                response = self.session.post(url, json=data, headers=headers, timeout=5)

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    Counter.count += 1
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Opera Gx Promo Gen | Made With <3 By Joy | Generated : {Counter.count}")
                    link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
                    with open("promos.txt", "a") as f:
                        f.write(f"{link}\n")
                    print(f"{self.get_timestamp()} {self.green} Generated Promo Link : {link}")
            elif response.status_code == 429:
                print(f"{self.get_timestamp()} {self.yellow} You Are Being Rate-limited!")
            else:
                print(f"{self.get_timestamp()} {self.red} Request Failed : {response.status_code}")
        except Exception as e:
            print(f"{self.get_timestamp()} {self.red} Request Failed : {e}")

    @staticmethod
    def get_timestamp():
        time_idk = time.strftime('%H:%M:%S')
        return f'[\x1b[90m{time_idk}\x1b[0m]'

class PromoManager:
    def __init__(self):
        self.num_threads = int(input(f"{PromoGenerator.get_timestamp()} {PromoGenerator.blue} Enter Number Of Threads : "))
        with open("proxies.txt") as f:
            self.proxies = f.read().splitlines()

    def start_gen(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = {executor.submit(self.generate_promo): i for i in range(self.num_threads)}
            try:
                concurrent.futures.wait(futures)
            except KeyboardInterrupt:
                for future in concurrent.futures.as_completed(futures):
                    future.result()

    def generate_promo(self):
        proxy = choice(self.proxies) if self.proxies else None
        generator = PromoGenerator(proxy)
        while True:
            generator.generate_promo()

if __name__ == "__main__":
    manager = PromoManager()
    manager.start_gen()
