# TODO: account for half stars, description, misc items, individual pages, perks, mods, and other stats
from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)

ranks = ['Common', 'Uncommon', 'Rare', 'Legendary', 'Exotic', 'Basic', 'Currency', 'Unknown']
armor = ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor', 'Class Item']

url = "https://www.light.gg/db/category/20/armor/"
ua = str(UserAgent().random)
headers = {'User-Agent': ua}
html = requests.get(url, headers=headers, verify=False)

soup = BeautifulSoup(html.text, 'html.parser')

rows = soup.find_all('div', class_='item-row')
names = []
item_json = {}
things = []

row = rows[1].find_all('div')

# this is for weapons
#print(row[0]) # usless
#print(row[1]) # id and image
#print(row[2]) # rarity and name
#print(row[3]) # kind of useless, we can get this info elsewhere
#print(row[4]) # item class, if any
#print(row[5]) # rarity
#print(row[6]) # damage type, slot
#print(row[7]) # item type
#print(row[8]) # info on stats
#print(row[9]) # number of stars
#print(row[10]) # PVE stat
#print(row[11]) # PVP stat

# this is for armor
#print(row[0]) # usless
#print(row[1]) # id and image
#print(row[2]) # rarity and name, # kind of useless, we can get this info elsewhere
#print(row[3])# kind of useless, we can get this info elsewhere 
#print(row[4]) # rarity
#print(row[5]) # Slot
#print(row[6]) # armor type
#print(row[7]) # info on stats
#print(row[8]) # number of stars
#print(row[9]) # PVE stat
#print(row[10]) # PVP Stats


class RowMethods:
    def __init__(self, row):
        self.row = row

    def is_weapon(self):
        return len(self.row) == 12

    def get_item_id(self):
        return self.row[1].get('data-id')

    def get_item_img(self):
        if self.is_weapon():
            return self.row[1].find('img').get('src')
        else:
            return self.row[1].find('img', class_='corner-watermark').get('src')

    def get_item_name(self):
        return self.row[2].find('a').text.strip()

    def get_item_class(self):
        if self.is_weapon():
            return self.row[4].text.strip()
        else:
            return None

    def get_item_rarity(self):
        if self.is_weapon():
            return self.row[5].text.strip()
        else:
            return self.row[4].text.strip()

    def get_item_damage_type(self):
        if self.is_weapon():
            return self.row[6].text.strip()
        else:
            return None

    def get_item_slot(self):
        if self.is_weapon():
            return self.row[6].find('img').get('title')
        else:
            return self.row[5].text.strip()

    def get_item_type(self):
        if self.is_weapon():
            return self.row[7].text.strip()
        else:
            return self.row[6].text.strip()

    def get_number_of_stars(self):
        if self.is_weapon():
            return len(self.row[9].find_all('i', class_='fa fa-star'))
        else:
            return len(self.row[8].find_all('i', class_='fa fa-star'))

    def get_item_pve(self):
        if self.is_weapon():
            return self.row[10].text.strip()
        else:
            return self.row[9].text.strip()

    def get_item_pvp(self):
        if self.is_weapon():
            return self.row[11].text.strip()
        else:
            return self.row[10].text.strip()

    def create_weapon_json(self):
        return {
            'id': self.get_item_id(),
            'img': self.get_item_img(),
            'name': self.get_item_name(),
            'class': self.get_item_class(),
            'rarity': self.get_item_rarity(),
            'damage_type': self.get_item_damage_type(),
            'slot': self.get_item_slot(),
            'type': self.get_item_type(),
            'stars': self.get_number_of_stars(),
            'pve': self.get_item_pve(),
            'pvp': self.get_item_pvp()
        }

    def create_armor_json(self):
        return {
            'id': self.get_item_id(),
            'img': self.get_item_img(),
            'name': self.get_item_name(),
            'rarity': self.get_item_rarity(),
            'slot': self.get_item_slot(),
            'type': self.get_item_type(),
            'stars': self.get_number_of_stars(),
            'pve': self.get_item_pve(),
            'pvp': self.get_item_pvp()
        }

    def create_json(self):
        if self.is_weapon():
            return self.create_weapon_json()
        else:
            return self.create_armor_json()