import requests
import json

base_url = 'https://www.bungie.net'

def fetch_definition(path):
    full_url = f"{base_url}{path}"
    response = requests.get(full_url)
    return response.json()

manifest_url = 'https://www.bungie.net/Platform/Destiny2/Manifest/'
manifest_response = requests.get(manifest_url)
manifest = manifest_response.json()

item_definition_path = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyInventoryItemDefinition']
class_definition_path = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyClassDefinition']
damage_type_definition_path = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinyDamageTypeDefinition']
perk_definition_path = manifest['Response']['jsonWorldComponentContentPaths']['en']['DestinySandboxPerkDefinition']

item_definitions = fetch_definition(item_definition_path)
class_definitions = fetch_definition(class_definition_path)
damage_type_definitions = fetch_definition(damage_type_definition_path)
perk_definitions = fetch_definition(perk_definition_path)

items = {}
for hash_key, item in item_definitions.items():
    item_details = {
        'name': item['displayProperties']['name'],
        'description': item['displayProperties'].get('description', ''),
        'icon': item['displayProperties'].get('icon', ''),
        'itemType': item.get('itemTypeDisplayName', 'Unknown Type'),
        'classType': item.get('classType', -1),
        'damageType': item.get('defaultDamageType', -1),
        'perks': []
    }
    if 'sockets' in item:
        for socket_entry in item['sockets']['socketEntries']:
            if 'singleInitialItemHash' in socket_entry:
                perk_hash = socket_entry['singleInitialItemHash']
                if str(perk_hash) in perk_definitions:
                    item_details['perks'].append(perk_definitions[str(perk_hash)]['displayProperties']['name'])
    
    items[int(hash_key)] = item_details

class_names = {definition['hash']: definition['displayProperties']['name'] for definition in class_definitions.values()}
damage_type_names = {definition['hash']: definition['displayProperties']['name'] for definition in damage_type_definitions.values()}

for item in items.values():
    item['classType'] = class_names.get(item['classType'], 'Any Class')
    item['damageType'] = damage_type_names.get(item['damageType'], 'No Damage')

with open('destiny2_items.json', 'w') as json_file:
    json.dump(items, json_file, indent=4)

print("Item details have been successfully written to destiny2_items.json")
