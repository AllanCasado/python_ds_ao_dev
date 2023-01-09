import pandas as pd
from sqlalchemy import create_engine

conn = create_engine('sqlite:///database_hm.sqlite', echo=False)
df = pd.read_sql_query(f"SELECT * FROM showroom", conn)
print(df.tail())
print(df.shape)