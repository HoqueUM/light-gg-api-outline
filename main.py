from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)

ranks = ['Common', 'Uncommon', 'Rare', 'Legendary', 'Exotic']
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
#print(row[2][3])
#print(row[2][4])
#print(row[2][5])
#print(row[2][6])
#print(row[2][7])
#print(row[2][8])
#print(row[2][9])
#print(row[2][10])
#print(row[2][11])


for rank in ranks:
    for row in rows:
        item_name_element = row.find('a', class_=f'text-{rank.lower()}')
        if item_name_element:
            item_name = item_name_element.text.strip()
            if item_name:
                item_json[item_name] = {"Rarity": rank}
    