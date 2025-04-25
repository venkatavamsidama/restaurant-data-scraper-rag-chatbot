from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.settings import PROXIES
import random

def get_webdriver() -> webdriver.Chrome:
    opts = Options()
    opts.add_argument('--headless')
    if PROXIES:
        proxy = random.choice(PROXIES)
        opts.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(options=opts)