from astropy.table import Table
import pandas as pd
import numpy as np

mega_list = pd.read_csv('/Users/lindseykremer/Downloads/ASTR502_Mega_Target_List.csv')            # read in mega target list from class

### Kounkel ###

# mega_list['ticid'] = mega_list['tic_id'].str.replace('TIC', '', regex=False).astype('Int64')    # replace the letters in the mega target list's cells with empty space so they can be read as integers                                                                                                # the first in parentheses is what you want removed  

# kounkel = Table.read('https://content.cld.iop.org/journals/1538-3881/164/4/137/revision1/ajac866dt1_mrt.txt', format = 'ascii.cds').to_pandas()
#                                                                                                 # read in the source using its link    
# print('catalogue read in done')
# print(kounkel.columns)
# print(mega_list.columns)

# mega_with_kounkel = mega_list.merge(kounkel[['TIC', 'Period']], 
#                                     left_on='ticid', 
#                                     right_on='TIC').drop_duplicates(subset='tic_id')

# print("Kounkel =", len(mega_with_kounkel), "matches")

### Fetherolf ###

# mega_list['ticid'] = mega_list['tic_id'].str.replace('TIC', '', regex=False).astype('Int64')    # replace the letters in the mega target list's cells with empty space so they can be read as integers
#                                                                                                 # the first in parentheses is what you want removed  

# fetherholf = Table.read('https://content.cld.iop.org/journals/0067-0049/268/1/4/revision1/apjsacdee5t1_mrt.txt', format = 'ascii.cds').to_pandas()
#                                                                                                 # read in the source using its link    
# print('catalogue read in done')
# print(fetherholf.columns)
# print(mega_list.columns)

# mega_with_fetherholf = mega_list.merge(fetherholf[['TIC', 'P']], 
#                                     left_on='ticid', 
#                                     right_on='TIC').drop_duplicates(subset='tic_id')

# print("Fetherholf =", len(mega_with_fetherholf), "matches")

### Lu ###

# mega_list['gaiadr3'] = mega_list['gaia_dr3_id'].str.replace('Gaia DR3', '', regex=False).astype('Int64')    # replace the letters in the mega target list's cells with empty space so they can be read as integers
#                                                                                                 # the first in parentheses is what you want removed  

# lu = Table.read('https://content.cld.iop.org/journals/1538-3881/164/6/251/revision1/ajac9beet1_mrt.txt', format = 'ascii.cds').to_pandas()
#                                                                                                 # read in the source using its link    
# print('catalogue read in done')
# print(lu.columns)
# print(mega_list.columns)

# mega_with_lu = mega_list.merge(lu[['EDR3', 'Prot']], 
#                                     left_on='gaiadr3', 
#                                     right_on='EDR3').drop_duplicates(subset='gaia_dr3_id')

# print("Lu =", len(mega_with_lu), "matches")

### Holcomb ###

# mega_list['ticid'] = mega_list['tic_id'].str.replace('TIC', '', regex=False).astype('Int64')    # replace the letters in the mega target list's cells with empty space so they can be read as integers
#                                                                                                 # the first in parentheses is what you want removed  

# holcomb = Table.read('/Users/lindseykremer/Downloads/spinspotter_by_star.csv').to_pandas()
#                                                                                                 # read in the source using its link    
# print('catalogue read in done')
# print(holcomb.columns)
# print(mega_list.columns)

# mega_with_holcomb = mega_list.merge(holcomb[['TICID', 'Prot']], 
#                                     left_on='ticid', 
#                                     right_on='TICID').drop_duplicates(subset='tic_id')

# print("Holcomb =", len(mega_with_holcomb), "matches")

### Colman ###

mega_list['ticid'] = mega_list['tic_id'].str.replace('TIC', '', regex=False).astype('Int64')    # replace the letters in the mega target list's cells with empty space so they can be read as integers
                                
mega_list = mega_list.drop_duplicates(subset = 'ticid')                                                                # the first in parentheses is what you want removed  

colman = np.loadtxt('/Users/lindseykremer/Downloads/fig12.dat 2', 
                    usecols = (0,4))
                                                            # read in the source using its link    
TIC = colman[:, 0].astype(int)
Prot = colman[:, 1]

matches = mega_list['ticid'].isin(TIC)
number = len(matches)
print('Colman =', number)

# print('catalogue read in done')
# print(colman.columns)
# print(mega_list.columns)

# mega_with_colman = mega_list.merge(colman[['TIC', 'Prot']], 
#                                     left_on='ticid', 
#                                     right_on='TIC').drop_duplicates(subset='tic_id')

# print("Colman =", len(mega_with_colman), "matches")


