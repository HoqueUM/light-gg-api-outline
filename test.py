from json_factory import json_factory
import requests

base_url = 'https://www.bungie.net'
maybe = json_factory('The Last Word', export_json=False, is_name=True)
manifest_url = 'https://www.bungie.net/Platform/Destiny2/Manifest/'
manifest_response = requests.get(manifest_url)
manifest = manifest_response.json()

print(manifest['Response']['jsonWorldComponentContentPaths']['en'].keys())
damage_types = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyDamageTypeDefinition']
response = requests.get(f"{base_url}{damage_types}")
hashes = response.json().keys()
damage_types_dict = {}

for id in hashes:
    damage_types_dict[id] = response.json()[id]['displayProperties']['name']

# DestinyDamageTypeDefinition -> self explanatory
# DestinyInventoryItemDefinition -> literally every item. enter the hash to find a list of item stuff. 
# DestinyItemTierTypeDefinition -> this is the rarity of the item.
# we will look into this later.


'''
inventory_item = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyInventoryItemLiteDefinition']
response = requests.get(f"{base_url}{inventory_item}")
hashes = response.json().keys()
print(response.json()['1364093401'])
'''
inventory_item = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinySandboxPerkDefinition']
response = requests.get(f"{base_url}{inventory_item}")
hashes = response.json().keys()
