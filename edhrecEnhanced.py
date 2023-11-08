# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 14:53:16 2023

@author: Charles-Alexis
"""
import data_striping as ds
import numpy as np

data_fetching = ds.DataFetchingCollection('collection/collection.xlsx','collection/nitpickingnerd_commander_list.xlsx')
# data_fetching.fetch_scryfall_collection()
# data_fetching.fetch_edhrec_collection()

# #%%
# data_fetching.plot_percent_usage_collection()

# ind = 0
# for perc in data_fetching.card_percent_usage:
#     if perc > 35:
#         print('Name: ' + data_fetching.collection_name_list[ind] + ' %: '+ "{:.2f}".format(perc))
#     ind += 1


#%%
data_fetching.get_most_compatibile_commander(collection=False)
data_fetching.possible_commander.sort(key = lambda x: x[2])
data_fetching.possible_commander[1500:-1]