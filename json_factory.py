# TODO: armor is different. this will need to be adjust for armor.
import json
import re
from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)
from SiteMethods import GetItem

def json_factory(item_id, export_json=False, is_name=False):
    ua = str(UserAgent().random)
    headers = {'User-Agent': ua}
    if is_name:
        item = GetItem()
        id = item.get_id_by_name(item_id)
        url = f"https://www.light.gg/db/items/{id}/"
    else:
        url = f"https://www.light.gg/db/items/{item_id}/"
    html = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(html.text, 'html.parser')
    scripts = soup.find_all('script')

    script = scripts[18].string

    match = re.search(r'var rollData = (.*?);', script, re.DOTALL)
    rollData_string = match.group(1)
    presplit = rollData_string.split('ItemDefs: ')[0].split('Raw:')[1]
    
    presplit = presplit.rstrip().rstrip(',')
    data = json.loads(presplit)
    
    if export_json:
        with open(f'{item_id}_rollData.json', 'w') as f:
            json.dump(data, f, indent=4)
    
    return data