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

def is_weapon(row):
    return len(row) == 12

def get_item_id(row):
    return row[1].get('data-id')

def get_item_img(row):
    if (is_weapon(row)):
        return row[1].find('img').get('src')
    else:
        return row[1].find('img', class_='corner-watermark').get('src')

def get_item_name(row):
    return row[2].find('a').text.strip()

def get_item_class(row):
    if is_weapon(row):
        return row[4].text.strip()
    else:
        return None

def get_item_rarity(row):
    if is_weapon(row):
        return row[5].text.strip()
    else:
        return row[4].text.strip()

def get_item_damage_type(row):
    if is_weapon(row):
        return row[6].text.strip()
    else:
        return None

def get_item_slot(row):
    if is_weapon(row):
        return row[6].find('img').get('title')
    else:
        return row[5].text.strip()

def get_item_type(row):
    if is_weapon(row):
        return row[7].text.strip()
    else:
        return row[6].text.strip()

def get_number_of_stars(row):
    if is_weapon(row):
        return len(row[9].find_all('i', class_='fa fa-star'))
    else:
        return len(row[8].find_all('i', class_='fa fa-star'))

def get_item_pve(row):
    if is_weapon(row):
        return row[10].text.strip()
    else:
        return row[9].text.strip()

def get_item_pvp(row):
    if is_weapon(row):
        return row[11].text.strip()
    else:
        return row[10].text.strip()

def create_weapon_json_from_row(row):
    item = {
        'id': get_item_id(row),
        'img': get_item_img(row),
        'name': get_item_name(row),
        'class': get_item_class(row),
        'rarity': get_item_rarity(row),
        'damage_type': get_item_damage_type(row),
        'slot': get_item_slot(row),
        'type': get_item_type(row),
        'stars': get_number_of_stars(row),
        'pve': get_item_pve(row),
        'pvp': get_item_pvp(row)
    }
    return item

def create_armor_json_from_row(row):
    item = {
        'id': get_item_id(row),
        'img': get_item_img(row),
        'name': get_item_name(row),
        'rarity': get_item_rarity(row),
        'slot': get_item_slot(row),
        'type': get_item_type(row),
        'stars': get_number_of_stars(row),
        'pve': get_item_pve(row),
        'pvp': get_item_pvp(row)
    }
    return item

def create_json_from_row(row):
    if is_weapon(row):
        return create_weapon_json_from_row(row)
    else:
        return create_armor_json_from_row(row)

