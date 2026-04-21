from astropy.table import Table
import pandas as pd
import numpy as np

# read mega list
mega_list = pd.read_csv('/Users/lindseykremer/Downloads/ASTR502_Mega_Target_List.csv')

# clean IDs ONCE (don’t repeat this every section)
mega_list['ticid'] = mega_list['tic_id'].str.replace('TIC', '', regex=False).astype('Int64')
mega_list['gaiadr3'] = mega_list['gaia_dr3_id'].str.replace('Gaia DR3', '', regex=False).astype('Int64')

all_results = []   # <-- collect everything here

### Kounkel ###
kounkel = Table.read(
    'https://content.cld.iop.org/journals/1538-3881/164/4/137/revision1/ajac866dt1_mrt.txt',
    format='ascii.cds'
).to_pandas()

mega_with_kounkel = mega_list.merge(
    kounkel[['TIC', 'Period']],
    left_on='ticid',
    right_on='TIC'
).drop_duplicates(subset='tic_id')

kounkel_out = mega_with_kounkel[['ticid', 'Period']].copy()
kounkel_out['source'] = 'Kounkel'
kounkel_out = kounkel_out.rename(columns={'Period': 'Prot'})

all_results.append(kounkel_out)

print("Kounkel =", len(kounkel_out))


### Fetherolf ###
fetherholf = Table.read(
    'https://content.cld.iop.org/journals/0067-0049/268/1/4/revision1/apjsacdee5t1_mrt.txt',
    format='ascii.cds'
).to_pandas()

mega_with_fetherholf = mega_list.merge(
    fetherholf[['TIC', 'P']],
    left_on='ticid',
    right_on='TIC'
).drop_duplicates(subset='tic_id')

fetherholf_out = mega_with_fetherholf[['ticid', 'P']].copy()
fetherholf_out['source'] = 'Fetherolf'
fetherholf_out = fetherholf_out.rename(columns={'P': 'Prot'})

all_results.append(fetherholf_out)

print("Fetherolf =", len(fetherholf_out))


### Lu ###
lu = Table.read(
    'https://content.cld.iop.org/journals/1538-3881/164/6/251/revision1/ajac9beet1_mrt.txt',
    format='ascii.cds'
).to_pandas()

mega_with_lu = mega_list.merge(
    lu[['EDR3', 'Prot']],
    left_on='gaiadr3',
    right_on='EDR3'
).drop_duplicates(subset='gaia_dr3_id')

lu_out = mega_with_lu[['ticid', 'Prot']].copy()
lu_out['source'] = 'Lu'

all_results.append(lu_out)

print("Lu =", len(lu_out))


### Holcomb ###
holcomb = pd.read_csv('/Users/lindseykremer/Downloads/spinspotter_by_star.csv')

mega_with_holcomb = mega_list.merge(
    holcomb[['TICID', 'Prot']],
    left_on='ticid',
    right_on='TICID'
).drop_duplicates(subset='tic_id')

holcomb_out = mega_with_holcomb[['ticid', 'Prot']].copy()
holcomb_out['source'] = 'Holcomb'

all_results.append(holcomb_out)

print("Holcomb =", len(holcomb_out))


### Colman ###
colman = np.loadtxt('/Users/lindseykremer/Downloads/fig12.dat 2', usecols=(0, 4))

colman_df = pd.DataFrame({
    'ticid': colman[:, 0].astype(int),
    'Prot': colman[:, 1]
})

mega_with_colman = mega_list.merge(
    colman_df,
    on='ticid'
).drop_duplicates(subset='tic_id')

colman_out = mega_with_colman[['ticid', 'Prot']].copy()
colman_out['source'] = 'Colman'

all_results.append(colman_out)

print("Colman =", len(colman_out))


### COMBINE EVERYTHING ###
final_df = pd.concat(all_results, ignore_index=True)

# optional: remove duplicates if same TIC+Prot appears multiple times
final_df = final_df.drop_duplicates()

# save to CSV
final_df.to_csv('/Users/lindseykremer/Downloads/all_rotation_periods.csv', index=False)

print("Saved", len(final_df), "total rows to CSV")