from bs4 import BeautifulSoup
from parse import get_page, check_proxy
import os


class Proxy:
    def __init__(self):
        self.path = os.path.dirname(__file__) + "\\.."
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
            'accept': '*/*'}
        self.url = ["https://hidemy.name/ru/proxy-list/?maxtime=1400&type=h&anon=34&start=#list",
                    "https://advanced.name/freeproxy?type=&page=1"]
        self.name_file = "\\proxy.txt"
        self.name_dir = "\\Proxy"
        self.page = None
        self.invalid_proxy = []
        self.valid_proxy = []

    def parse(self):
        if os.path.exists(self.path + self.name_dir) is not True:
            os.mkdir(self.path + self.name_dir)

        if os.path.isfile(self.path + self.name_dir + self.name_file) is not True:
            open(self.path + self.name_dir + self.name_file, "w")

        # parse proxy from site hidemy
        self.page = get_page(self.url[0].replace("start=", "start=0"), self.headers)
        if self.page is not None:
            quantity_page = len((BeautifulSoup(self.page, 'lxml').find("div", class_="pagination")).find_all("li")) - 1
            for i in range(quantity_page):
                if self.page is not None:
                    self.write_proxy_from_hidemy()
                self.page = get_page(self.url[0].replace("start=", "start=" + str(64 * (i + 1))), self.headers)

        self.check_proxy()

    def write_proxy_from_hidemy(self):
        list_proxy = (BeautifulSoup(self.page, "lxml").find("table")).find_all("tr")
        del list_proxy[0]
        for tr in list_proxy:
            ip = tr.find_all("td")
            self.invalid_proxy.append(self.get_ip(ip[4].text.lower(), ip[0].text, ip[1].text))

    @staticmethod
    def get_ip(protocol: str, ip: str, port: str):
        result = {}
        if protocol == "http":
            result["http"] = ip + ":" + port
        return result

    def check_proxy(self):
        for ip in self.invalid_proxy:
            operation = check_proxy(ip)
            if operation:
                self.valid_proxy.append(ip)
