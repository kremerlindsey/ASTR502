# week of jan 12

import lightkurve as lk
import numpy as np
import pandas as pd

filename = '/Users/lindseykremer/Downloads/ASTR502_Mega_Target_List.csv'
data = pd.read_csv(filename)

tic_id_list = data['tic_id']

stars_found = []

for star in tic_id_list:
    search = lk.search_lightcurve(star, mission = "K2")
    
