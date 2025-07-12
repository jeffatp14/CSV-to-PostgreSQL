from psycopg2 import extras
import pandas as pd

def extract_col(df: pd.DataFrame, column_names):
    return df[column_names]

def column_exists(cursor, schema, table, column):
    column_exists = """
    SELECT EXISTS (
        SELECT * FROM information_schema.columns
        WHERE table_schema='{schema}' 
        AND table_name='{table}'
        AND column_name='{column}')
        """.format(
            schema  = schema,
            table   = table,
            column  = column
    )
    cursor.execute(column_exists)
    column_exists = cursor.fetchone()[0]
    return column_exists

def insert_data(cursor, schema, table, df: pd.DataFrame):
    data = [tuple(None if pd.isna(v) else v for v in row) for row in df.to_numpy()]
    
    col_list = []
    for col in df.columns:
        col_list.append(col)
    
    # Check if all columns exist in table
    for col in col_list:    
        if not column_exists(cursor, schema, table, col):
            raise Exception(f"PSQL SINK - Column {col} doesn't exist, please add column to table first.")
            
    cols = ','.join(col_list)

    query = "INSERT INTO %s.%s(%s) VALUES %%s" % (schema, table, cols)
    extras.execute_values(cursor, query, data)
    
    return