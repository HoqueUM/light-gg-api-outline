from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)
from RowMethods import RowMethods

ua = str(UserAgent().random)
headers = {'User-Agent': ua}

def soup_generator(var, is_id=False):
    if is_id:
        url = f"https://www.light.gg/db/item/{var}/"
    else:
        url = f"https://www.light.gg/db/search/?q={var}"
    html = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def get_item_by_id(id):
    soup = soup_generator(id, is_id=True)
    return soup 
def get_item_by_name(name):
    name = name.replace(' ', '%20')
    soup = soup_generator(name, is_id=False)
    rows = soup.find_all('div', class_='item-row')
    row = rows[1].find_all('div')
    methods = RowMethods(row)
    return  get_item_by_id(methods.get_item_id())


print(get_item_by_name('The Last Word') == get_item_by_id(1364093401))