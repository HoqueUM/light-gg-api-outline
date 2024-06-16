import json
import re
from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from fake_useragent import UserAgent
disable_warnings(InsecureRequestWarning)

def json_factory(item_id, export_json=False):
    ua = str(UserAgent().random)
    headers = {'User-Agent': ua}
    url = f"https://www.light.gg/db/items/{item_id}/"
    html = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(html.text, 'html.parser')
    scripts = soup.find_all('script')

    script = scripts[18].string

    match = re.search(r'var rollData = (.*?);', script, re.DOTALL)
    rollData_string = match.group(1)
    split = rollData_string.split('ItemDefs: ')[1].split(',"Localization":{}}')
    final = split[0] + '}'

    rollData = json.loads(final)
    
    if export_json:
        with open(f'{item_id}_rollData.json', 'w') as f:
            json.dump(rollData, f, indent=4)
    
    return rollData