from astropy.table import Table
import pandas as pd

### Kounkel ###

mega_list = pd.read_csv('/Users/lindseykremer/Downloads/ASTR502_Mega_Target_List.csv')          # read in mega target list from class
mega_list['ticid'] = mega_list['tic_id'].str.replace('TIC', '', regex=False).astype('Int64')    # replace the letters in the mega target list's cells with empty space so they can be read as integers
                                                                                                # the first in parentheses is what you want removed  

kounkel = Table.read('https://content.cld.iop.org/journals/1538-3881/164/4/137/revision1/ajac866dt1_mrt.txt', format = 'ascii.cds').to_pandas()
                                                                                                # read in the source using its link    
print('catalogue read in done')
print(kounkel.columns)
print(mega_list.columns)

mega_with_kounkel = mega_list.merge(kounkel[['TIC', 'Period']], 
                                    left_on='ticid', 
                                    right_on='TIC').drop_duplicates(subset='tic_id')

print("Kounkel =", len(mega_with_kounkel), "matches")