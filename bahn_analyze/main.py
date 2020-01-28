import pandas as pd
import h5py


# df1 = pd.read_parquet('data/trainstop_changes_part000_ids_1-5000000.parquet')
# df1.to_hdf('data/trainstop_changes_all.hdf5', 'w')


#%%
df2 = pd.read_parquet('data/trainstop_changes_part001_ids_5000001-10000000.parquet')
df2.to_hdf('data/trainstop_changes_all.hdf5', 'a')

#%%
import vaex.hdf5
#df = vaex.from_arrow_table('data/trainstop_changes_part000_ids_1-5000000.parquet')
df = vaex.from_pandas(df1)
#%%
df.export_hdf5('data/trainstop_changes_part001_ids_5000001-10000000.hdf5')

#%%
import vaex.hdf5
df_test = vaex.open('data/trainstop_changes_all.hdf5')

