# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 22:42:52 2023

@author: Charles-Alexis
"""

import requests

class DataStrip:
    def __init__(self):
        self.edhrec_base_url = 'https://json.edhrec.com/pages/cards/'
        self.edhrec_debug_splitcard_url = 'https://json.edhrec.com/pages'
    
    def get_percent_deck(self,card_name):
        response = requests.get(self.edhrec_base_url + card_name+'.json')
        if response.status_code != 200:
            print('ERROR LOADING CARD')
            
        try:
            deck_line = response.json()['container']['json_dict']['card']['label']
            strip_deck_line = deck_line.replace(' ','').replace('decks','').replace('In','').replace('of','')
        except:
            response = requests.get(self.edhrec_debug_splitcard_url + response.json()['redirect']+'.json')
            deck_line = response.json()['container']['json_dict']['card']['label']
            strip_deck_line = deck_line.replace(' ','').replace('decks','').replace('In','').replace('of','')

        strip_param = [0,0,0]
        for char in strip_deck_line:
            if char == '\n':
                strip_param[0] = strip_param[2]
            if char == '%':
                strip_param[1] = strip_param[2]+1
                break
            strip_param[2] +=1
        
        nbr_of_deck = strip_deck_line[0:strip_param[0]]
        total_deck = strip_deck_line[strip_param[1]:len(strip_deck_line)]
        
        return 100*(float(nbr_of_deck)/float(total_deck))