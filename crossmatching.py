from astropy.table import Table
import pandas as pd

kounkel = Table.read('https://cdsarc.cds.unistra.fr/ftp/J/AJ/164/137/table1.dat', readme='https://cdsarc.cds.unistra.fr/ftp/J/AJ/164/137/ReadMe', format='ascii.cds').to_pandas()

mega_list = pd.read_csv('/Users/lindseykremer/Downloads/ASTR502_Mega_Target_List.csv')

mega_with_kounkel = mega_list.merge(kounkel[['RAdeg', 'DEdeg']], left_on='ra', right_on='RAdeg').drop_duplicates(subset='ra')