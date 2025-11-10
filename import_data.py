import pandas as pd
from connection import get_connection

def import_csv_to_table(csv_path, table_name):
    conn = get_connection()
    cursor = conn.cursor()

    df = pd.read_csv(csv_path)
    print(f"Reading {csv_path} — {len(df)} rows loaded.")

    for _, row in df.iterrows():
        placeholders = ", ".join(["%s"] * len(row))
        columns = ", ".join(row.index)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = tuple(row)
        try:
            cursor.execute(sql, values)
        except Exception as e:
            print(f"Inserting Data Error into {table_name}: {e}")

    conn.commit()
    print(f"Successfully imported {len(df)} rows into {table_name}.")
    conn.close()
