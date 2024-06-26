from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)
from RowMethods import RowMethods

ua = str(UserAgent().random)
headers = {'User-Agent': ua}



class GetItem():
    def __init__(self):
        self.soup = None
    
    def soup_generator(self, var, is_id=False):
        if is_id:
            url = f"https://www.light.gg/db/items/{var}/"
        else:
            url = f"https://www.light.gg/db/search/?q={var}"
        html = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup

    def get_item_by_id(self, id):
        self.soup = self.soup_generator(id, is_id=True)
        return self.soup 
    
    def get_item_by_name(self, name):
        name = name.replace(' ', '%20')
        id = self.get_id_by_name(name)
        return  self.get_item_by_id(id)
    
    def get_item(self, item):
            if item.isdigit():
                return self.get_item_by_id(item)  
            else:
                return self.get_item_by_name(item)  
    
    def get_name_by_id(self, id):
        soup = self.soup_generator(id, is_id=True)
        div = soup.find('div', class_='item')
        title = div.find('h2').get_text(strip=True)
        return title
    
    def get_id_by_name(self, name):
        soup = self.soup_generator(name, is_id=False)
        rows = soup.find_all('div', class_='item-row')
        row = rows[1].find_all('div')
        methods = RowMethods(row)
        return methods.get_item_id()

    def get_item_name(self):
        return self.soup


items = GetItem()

name = items.get_name_by_id('1364093401')

print(name)

item = items.get_item('The Last Word')
#print(item)
divs = item.find('div', class_='body-content')

#print(len(sub_divs))
