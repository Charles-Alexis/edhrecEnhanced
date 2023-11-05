# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:53:16 2023

@author: Charles-Alexis
"""

import requests
import xlrd
import pandas as pd
import time

dataframe = pd.read_excel('collection/test_100.xlsx')
name_list = list()
card_data = list()

for name in dataframe['Card Name']:
    name_list.append(name.replace(' ','-').replace(',','').lower())

counter = 0
nbr_of_card = len(name_list)

time_start = time.time()
scryfall_base_url = 'https://api.scryfall.com/cards/named?exact='
for card_name in name_list:
    response = requests.get(scryfall_base_url + card_name)
    counter += 1
    if response.status_code == 200:
        card_data.append(response.json())
    if response.status_code != 200:
        print('Probleme with card: ' + card_name)
    if counter%100 == 0:
        print('Percent completed: ' + "{:.2f}".format(counter/nbr_of_card*100) +' in ' + "{:.2f}".format(time.time() - time_start))
 
possible_commander = list()
for data in card_data:
    if 'Legendary Creature' in data['type_line']:# and '//' not in data['type_line']:
        possible_commander.append([data['name'],data])
 
### CREATING TYPE ARRAYS
creatures = list()
for data in card_data:
    if 'Creature' in data['type_line']:
        creatures.append([data['name'],data])
        
instants = list()
for data in card_data:
    if 'Instant' in data['type_line']:
        instants.append([data['name'],data])
        
sorceries = list()
for data in card_data:
    if 'Sorcery' in data['type_line']:
        sorceries.append([data['name'],data])
        
battles = list()
for data in card_data:
    if 'Battle' in data['type_line']:
        battles.append([data['name'],data])
        
lands = list()
for data in card_data:
    if 'Land' in data['type_line']:
        lands.append([data['name'],data])
        
enchantments = list()
for data in card_data:
    if 'Enchantment' in data['type_line']:
        enchantments.append([data['name'],data])
        
artifacts = list()
for data in card_data:
    if 'Artifact' in data['type_line']:
        artifacts.append([data['name'],data])
        
planeswalkers = list()
for data in card_data:
    if 'Planeswalker' in data['type_line']:
        planeswalkers.append([data['name'],data])

### CHECKING SYNERGIES
base_url = 'https://json.edhrec.com/pages/'
response = requests.get(base_url + 'cards/explore.json')

# debug = response.json()['container']['json_dict']['cardlists']