from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)

ranks = ['Common', 'Uncommon', 'Rare', 'Legendary', 'Exotic', 'Basic', 'Currency', 'Unknown']
armor = ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor', 'Class Item']

url = "https://www.light.gg/db/all/"
ua = str(UserAgent().random)
headers = {'User-Agent': ua}
html = requests.get(url, headers=headers, verify=False)

soup = BeautifulSoup(html.text, 'html.parser')

rows = soup.find_all('div', class_='item-row')
names = []
item_json = {}
things = []

row = rows[2].find_all('div')

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

# TODO: make a method to create a json from the info found above
def create_json_from_row(row):
    return


# method to get name and rarity
for rank in ranks:
    for row in rows:
        item_name_element = row.find('a', class_=f'text-{rank.lower()}')
        if item_name_element:
            item_name = item_name_element.text.strip()
            if item_name:
                item_json[item_name] = {"Rarity": rank}
    