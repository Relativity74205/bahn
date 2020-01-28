import os

import pandas as pd
import vaex

files = os.listdir('data')
files = [file for file in files if '.parquet' in file]

for file in sorted(files):
    print(f'reading parquet file {file} to pandas df')
    df_chunk = pd.read_parquet(f'data/{file}')
    print(f'converting to vaex df: {file}')
    vaex_chunk = vaex.from_pandas(df_chunk, copy_index=False)
    new_filename = file.split('.')[0]
    export_path = f'data_hdf5/{new_filename}.hdf5'
    print(f'exporting to hdf5: {file}')
    vaex_chunk.export_hdf5(export_path)

df = vaex.open('data_hdf5/trainstop_changes_part*')
df.export_hdf5('data_hdf5/Final.hdf5')
