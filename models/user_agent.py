from parse import get_page
from bs4 import BeautifulSoup
import os


class UserAgent:
    def __init__(self):
        self.path = os.path.dirname(__file__) + "\\.."

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
            'accept': '*/*'}
        self.url = "https://seolik.ru/user-agents-list"
        self.name_file = "\\User agent.txt"
        self.name_dir = "\\User agent"
        self.page = None

    def parse(self):
        if os.path.exists(self.path + self.name_dir) is not True:
            os.mkdir(self.path + self.name_dir)

        if os.path.isfile(self.path + self.name_dir + self.name_file) is not True:
            self.page = get_page(self.url, self.headers)
            self.create_file_user_agent()

    def create_file_user_agent(self):
        list_user_agent = (BeautifulSoup(self.page, "lxml").find("div", class_="table-responsive")).find_all("tr")
        with open(self.path + self.name_dir + self.name_file, "w+") as file:
            for i in list_user_agent:
                file.write(i.find_all("td")[1].text + "\n")
