# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:53:16 2023

@author: Charles-Alexis
"""

import requests
import xlrd
import pandas as pd
import time
from unidecode import unidecode

### LAYOUT TO WATCH: SPLIT, ADVENTURE

dataframe = pd.read_excel('collection/collection.xlsx')
name_list = list()
card_data = list()

for name in dataframe['Card Name']:
    name_list.append(unidecode(name.replace(' ','-').replace('!','').replace('?','').replace(',','').lower().partition('-//-')[0]))

counter = 0
nbr_of_card = len(name_list)

print('Number of Cards to Fetch: '+ str(nbr_of_card))

time_start = time.time()
scryfall_base_url = 'https://api.scryfall.com/cards/named?exact='
for card_name in name_list:
    response = requests.get(scryfall_base_url + card_name)
    counter += 1
    
    if response.status_code == 200:
        card_data.append(response.json())
    if response.status_code != 200:
        print('Probleme with card: ' + card_name)
        
    if counter%250 == 0:
        timing = time.time() - time_start
        print('%: ' + "{:.2f}".format(counter/nbr_of_card*100) +' in ' + "{:.2f}".format(timing) + ' Fetched card: ' +str(counter) + ' Estimated to end: ' +str(((timing*nbr_of_card)/counter)-timing ))

print('%: ' + "{:.2f}".format(counter/nbr_of_card*100) +' in ' + "{:.2f}".format(time.time() - time_start) + ' Fetched card: ' +str(counter))

possible_commander = list()
for data in card_data:
    if 'Legendary Creature' in data['type_line']:
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

### PRINTING STATS        
print('COLLECTION STATS')
print('Possible commanders: '+str(len(possible_commander)))
print('Creatures: '+str(len(creatures)))
print('Instants: '+str(len(instants)))
print('Sorceries: '+str(len(sorceries)))
print('Artifacts: '+str(len(artifacts)))
print('Enchantments: '+str(len(enchantments)))
print('Planeswalkers: '+str(len(planeswalkers)))
print('Battles: '+str(len(battles)))
print('Lands: '+str(len(lands)))

#%%
import data_striping as ds
import numpy as np
### CHECKING SYNERGIES

percent_array = np.zeros(len(name_list))
data_strip = ds.DataStrip()

time_debut = time.time()
for ind in range(len(name_list)):
    percent_array[ind] = data_strip.get_percent_deck(name_list[ind])
    if ind%250 == 0:
        print(ind)
    
print('Get percent Data in: ' + str(time.time()- time_debut))
















