from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from requests_toolbelt.multipart.encoder import MultipartEncoder
from settings.urls import Urls
import http.client
import time
import requests


http.client._MAXHEADERS = 1000


def check_proxy(ip_string):
    response = requests.get("https://icanhazip.com/", proxies=ip_string)
    if response.status_code == 200:
        return True
    else:
        return False


def get_page(url_string, user_agent=None, params=None):
    try:
        response = requests.get(
            url_string,
            headers=user_agent,
            params=params
        )
        if response.status_code == 200:
            return response.text
        else:
            pass
    except:
        return None


def get_driver(sleep):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(Urls.MAIN)
    time.sleep(sleep)
    return driver


def get_cookies(driver):
    list_cookies = driver.get_cookies()
    dict_cookies = {}
    for ldc in list_cookies:
        dict_cookies[ldc["name"]] = ldc["value"]
    return dict_cookies


def get_data(login, password):
    data = MultipartEncoder({
        'LoginPasswordAuthorizationLoadForm[login]': login,
        'LoginPasswordAuthorizationLoadForm[password]': password,
        'LoginPasswordAuthorizationLoadForm[token]': '',
    })
    return data


def get_headers(data, driver):
    headers = {
        'accept': '*/*',
        'user-agent': driver.execute_script("return navigator.userAgent;"),
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': data.content_type,
    }
    return headers


def authentication(data, cookies, headers):
    response = requests.post(Urls.AUTHORIZATIONS,
                             data=data,
                             cookies=cookies,
                             headers=headers)
    return response
