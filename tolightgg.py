import requests
import json

url = 'https://www.light.gg/god-roll/roll-appraiser/data/?v=063024cachebust2'

response = requests.get(url).json()

interested = response['Weapons']['568611922']

with open('god_roll.json', 'w') as f:
    json.dump(interested, f, indent=4)