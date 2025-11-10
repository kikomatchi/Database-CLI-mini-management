import pandas as pd
from connection import get_engine, get_connection

def show_available_tables():
    engine = get_engine()
    query = "SHOW TABLES;"
    tables = pd.read_sql_query(query, engine)
    if tables.empty:
        print("\nNo tables found in database.")
        return[]
    tables_col = tables.columns[0]
    tables_list = tables[tables_col].tolist()
    print(f"\nAvailable Tables: ")
    for i in tables_list:
        print(f"-{i}")
    return tables_list

def show_table_columns(table_name):
    engine = get_engine()
    query = f"SHOW COLUMNS FROM {table_name};"
    try:
        columns = pd.read_sql_query(query, engine)
        if columns.empty:
            print(f"\nNo Columns found in '{table_name}'.")
            return[]
        print(f"\nColumns in table '{table_name}':")
        for _,row in columns.iterrows():
            print(f"- {row['Field']} ({row['Type']})")
        return columns['Field'].tolist()
    except Exception as e:
        print(f"\n Error reading columns from '{table_name}': {e}")
        return[]
    
def insert_row(table_name, data: dict):
    if not data:
        print("No data provided to insert.")
        return
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    values = tuple(data.values())
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        print(f"Row inserted successfully into '{table_name}'.")
    except Exception as e:
        print(f"Error inserting row into '{table_name}':", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_row(table_name, record_id, data: dict, id_column="id"):
    if not data:
        print("No fields to update.")
        return
    fields = ", ".join([f"{col} = %s" for col in data.keys()])
    values = list(data.values())
    values.append(record_id)
    query = f"UPDATE {table_name} SET {fields} WHERE {id_column} = %s"
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        conn.commit()
        print(f"Row in '{table_name}' updated successfully.")
    except Exception as e:
        print(f"Error updating row in '{table_name}':", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
