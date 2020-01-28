import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = {'url': 'sqlite:///database.db'}

engine = create_engine(DB_URL['url'], echo=False)
con = engine.connect()

fname_base = 'trainstop_changes'

amount_ids = 114058833
iterate_size = 5000000
min_ids = range(1, amount_ids, iterate_size)
max_ids = range(iterate_size, amount_ids+iterate_size, iterate_size)
for i, (min_id, max_id) in enumerate(zip(min_ids, max_ids)):
    max_id = min(amount_ids, max_id)
    part = str(i).zfill(3)
    stmt = "SELECT * FROM trainstops_changes WHERE change_id >= :min_id AND change_id <= :max_id"
    params_dict = {'min_id': min_id,
                   'max_id': max_id}

    fname = f'{fname_base}_part{part}_ids_{min_id}-{max_id}'
    print(f'params_dict {params_dict}; fname {fname}')
    data = pd.read_sql_query(text(stmt), con, params=params_dict)
    print(data.shape)
    data.to_parquet(f'{fname}.parquet')
    i = i + 1

