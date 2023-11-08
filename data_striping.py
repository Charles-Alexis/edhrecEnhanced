# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 22:42:52 2023

@author: Charles-Alexis
"""

import requests
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from unidecode import unidecode

class DataFetchingCollection:
    def __init__(self, collection_path = '', commander_list_path = ''):
        ## PATH TO COLLECTION AND COMMANDER LIST
        self.collection_path = collection_path
        self.commander_list_path = commander_list_path
        
        ## NAME LIST
        self.collection_name_list = list()
        self.collection_name_list_with_duplicate = list()
        self.commanders_name_list = list()
        
        ## LOAD COLLECTION
        self.collection_data_frame = pd.read_excel(self.collection_path)
        self.load_collection()
        self.remove_duplicate_card()
        self.collection_size = len(self.collection_name_list)
        
        ## LOAD COMMANDER LIST
        self.commander_data_frame = pd.read_excel(self.commander_list_path)
        self.load_commander_list()
        self.nbr_of_possible_commander = len(self.commanders_name_list)
        
        ## SCRYFALL API
        self.scryfall_base_url = 'https://api.scryfall.com/cards/named?exact='
        self.scryfall_card_data = list()
        
        ## EDHREC API
        self.edhrec_base_url = 'https://json.edhrec.com/pages'
        self.edhrec_debug_splitcard_url = 'https://json.edhrec.com/pages'
        self.edhrec_card_data = list()
        
        ## PARAMS FOR PLOTING PERCENT AND COMPATIBILITY WITH COLLECTION
        self.card_percent_usage = np.zeros(len(self.collection_name_list))
        self.used_in_treshhold = 2 # IF CARD APPEARS IN LESS THEN used_in_treshhold% FOR COMMANDER, DONT SAVE IT
        self.big_dict_of_possible_commander = {}
        
        self.commanders_in_collection= list()
        self.possible_commander = list()
    
    def load_collection(self):
        for name in self.collection_data_frame['Card Name']:
            self.collection_name_list_with_duplicate.append(unidecode(name.replace(' ','-').replace('!','').replace('?','').replace(',','').lower().partition('-//-')[0]))

    def load_commander_list(self):
        for name in self.commander_data_frame['Commander']:
            self.commanders_name_list.append(unidecode(name.replace(' ','-').replace('!','').replace('?','').replace(',','').lower().partition('-//-')[0]))

    def remove_duplicate_card(self):
        self.collection_name_list = list(set(self.collection_name_list_with_duplicate))

    def fetch_edhrec_single(self,card_name):
        return requests.get(self.edhrec_base_url + '/cards/' +card_name+'.json')

    def fetch_edhrec_commander(self, card_name, themes=False):
        if themes:
            return requests.get(self.edhrec_base_url + '/commanders/' + card_name + '/' + themes + '.json')
        else:
            return requests.get(self.edhrec_base_url + '/commanders/' + card_name+'.json')
    
    def fetch_edhrec_collection(self):
        print('Number of Cards to Fetch from EDHREC: '+ str(self.collection_size))
        print('Estimated Time: '+"{:.2f}".format(self.collection_size*0.1)+'s')
    
        counter = 0
        time_start = time.time()
        for card_name in self.collection_name_list:
            response = self.fetch_edhrec_single(card_name)
            
            try:
                response.json()['container']['json_dict']['card']['label']
            except:
                print('Special layout card detected at: ' + str(counter))
                response = requests.get(self.edhrec_debug_splitcard_url + response.json()['redirect']+'.json')
            
            self.edhrec_card_data.append(response.json())
            
            counter += 1
            if counter%250 == 0:
                timing = time.time() - time_start
                print('%: ' + "{:.2f}".format(counter/self.collection_size*100) +' in ' + "{:.2f}".format(timing) + 's')
                print('# Fetched card: ' +str(counter) + ' Estimated to end: '+ "{:.2f}".format(((timing*self.collection_size)/counter)-timing) + 's')
            time.sleep(0.05) ### FOR NOT OVERLOADING
        print('Took: ' + "{:.2f}".format(time.time()-time_start)+'s to fetch all cards' )
    
    def get_percent_usage_data(self, resp):
        return (resp['container']['json_dict']['card']['num_decks']/resp['container']['json_dict']['card']['potential_decks'])*100
    
    def plot_percent_usage_collection(self):
        for ind in range(self.collection_size):
            self.card_percent_usage[ind] = self.get_percent_usage_data(self.edhrec_card_data[ind])
        plt.hist(self.card_percent_usage,1000)
        
    def fetch_scryfall_single(self, card_name):
        return requests.get(self.scryfall_base_url + card_name)

    def fetch_scryfall_collection(self):
        print('Number of Cards to Fetch from Scryfall: '+ str(self.collection_size))
        print('Estimated Time: '+"{:.2f}".format(self.collection_size*0.1)+'s')
        
        counter = 0
        time_start = time.time()
        for card_name in self.collection_name_list:
            response = self.fetch_scryfall_single(card_name)
            counter += 1
            if response.status_code == 200:
                self.scryfall_card_data.append(response.json())
            if response.status_code != 200:
                print('Probleme with card: ' + card_name)
            
            if counter%250 == 0:
                timing = time.time() - time_start
                print('%: ' + "{:.2f}".format(counter/self.collection_size*100) +' in ' + "{:.2f}".format(timing) + 's')
                print('# Fetched card: ' +str(counter) + ' Estimated to end: '+ "{:.2f}".format(((timing*self.collection_size)/counter)-timing) + 's')
            time.sleep(0.05) ### FOR NOT OVERLOADING
        print('Took: ' + "{:.2f}".format(time.time()-time_start)+'s to fetch all cards' )

    def get_most_played_in(self, resp):
        most_played_list = list()
        try :
            resp['container']['json_dict']['card']['banned']
        except KeyError:
            if resp['container']['json_dict']['cardlists'][0]['header'] == 'New Commanders':
                for new_commanders in resp['container']['json_dict']['cardlists'][0]['cardviews']:
                    if (float(new_commanders['num_decks'])/float(new_commanders['potential_decks'])*100) > self.used_in_treshhold:
                        most_played_list.append(new_commanders['sanitized_wo'])
                for commanders in resp['container']['json_dict']['cardlists'][1]['cardviews']:
                    if (float(commanders['num_decks'])/float(commanders['potential_decks'])*100) > self.used_in_treshhold:
                        most_played_list.append(commanders['sanitized_wo'])
            if resp['container']['json_dict']['cardlists'][0]['header'] == 'Commanders':
                for commanders in resp['container']['json_dict']['cardlists'][0]['cardviews']:
                    if (float(commanders['num_decks'])/float(commanders['potential_decks'])*100) > self.used_in_treshhold:
                        most_played_list.append(commanders['sanitized_wo'])
                
        return most_played_list
    
    def get_most_potential_commander_to_build(self):
        self.big_dict_of_possible_commander = {}
        counter = 0
        time_start = time.time()
        
        for cards in self.edhrec_card_data:
            most_used_list = self.get_most_played_in(cards)
            counter += 1
            for commanders in most_used_list:
                try:
                    self.big_dict_of_possible_commander[commanders] += 1
                except KeyError:
                    self.big_dict_of_possible_commander[commanders] = 1
                    
    def get_commander_compatibilities(self, commander_name, themes = False):
        commander_resp = self.fetch_edhrec_commander(commander_name, themes)
        commander_data = commander_resp.json()['container']['json_dict']['cardlists']
        total_card = 0
        compatible_card = 0
        
        for categories in commander_data:
            for cards in categories['cardviews']:
                if cards['sanitized_wo'] in self.collection_name_list:
                    compatible_card+=1
                total_card+=1
        print((float(compatible_card)/float(total_card))*100)
            
    def create_commander_list_from_collection(self):
        temp_list= list()
        for data in self.scryfall_card_data:
            if 'Legendary' in data['type_line'] and 'Creature' in data['type_line']:
                name = data['name'].replace(' ','-').replace('!','').replace('?','').replace(',','').lower().partition('-//-')[0]
                temp_list.append(name)
        self.possible_commander = list(set(temp_list))
                
    def get_most_compatibile_commander(self, collection = True):
        self.possible_commander= list()
        if collection:
            self.create_commander_list_from_collection()
            commander_list = self.possible_commander
        else:
            commander_list = self.commanders_name_list    
        
        ind = 1
        for commanders in commander_list:
            resp = self.fetch_edhrec_commander(commanders)
            print(commanders)
            if resp.status_code == 200:
                try:
                    commander_data = resp.json()['container']['json_dict']['cardlists']
                    total_card = 0
                    compatible_card = 0
                    for categories in commander_data:
                        for cards in categories['cardviews']:
                            if cards['sanitized_wo'] in self.collection_name_list:
                                compatible_card+=1
                            total_card+=1
                    self.possible_commander.append([ind, commanders,((float(compatible_card)/float(total_card))*100),compatible_card, total_card])
                    ind += 1
                except KeyError:
                    ind+=1
                
                
               
                
                
                
                
                
                
                
                
            
    
    
            
            
            