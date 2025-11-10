import pandas as pd
from connection import get_engine

def read_table_(table_name):
    engine = get_engine()
    query = f"SELECT * FROM {table_name}"
    try:
        df = pd.read_sql(query, engine)
        print(f"Loaded {len(df)} rows from {table_name}")
    except Exception as e:
        print(f"Error reading table '{table_name}': {e}")
        df = pd.DataFrame()
    return df

def view_table(df, sort_by=None, ascending=True, limit=None):
    if sort_by and sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=ascending)
    if limit:
        df = df.head(limit)
    print(df)
    return df

def search_table(df, **filters):
    query_df = df.copy()
    for key, value in filters.items():
        if key not in query_df.columns:
            print(f"Columns '{key}' not found.-")
            continue
        if isinstance(value, list):
            query_df = query_df[query_df[key].isin(value)]
        elif isinstance(value, tuple):
            if len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
                query_df = query_df[(query_df[key] >= value[0]) & (query_df[key]<= value[1])]
            elif len(value) == 2 and isinstance(value[0], str) and isinstance(value[1], (int, float)):
                op, val = value
                if op == '>': query_df = query_df[query_df[key]>val]
                elif op =='<': query_df = query_df[query_df[key]<val]
                elif op =='>=': query_df = query_df[query_df[key]>=val]
                elif op == '<=': query_df = query_df[query_df[key]<=val]
                elif op =='!=': query_df = query_df[query_df[key]!=val]
                elif op == '==': query_df = query_df[query_df[key]==val]
        elif isinstance(value, str):
            query_df = query_df[query_df[key].astype(str).str.contains(value, case=False, na=False)]
        else:
            query_df = query_df[query_df[key] == value]
    print(f"Found {len(query_df)} matching rows.")
    return query_df

