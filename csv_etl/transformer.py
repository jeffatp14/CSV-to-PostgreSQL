import pandas as pd
import ast
class Transform:
    def __init__(self):
        pass
    '''
    used for transforming wide data to long
    '''
    def transform_list_to_row(self, data:pd.DataFrame, column_names):
        col_list = []
        for col in column_names:
            col_list.append(col)
        cols = ','.join(col_list)
          # Drop rows where the column is null or empty
        data = data.dropna(subset=[cols])
        data = data[data[cols].str.strip().astype(bool)]  # remove empty strings

        # Remove leading/trailing quotes and whitespace
        data[cols] = data[cols].str.replace('"', '', regex=False).str.strip()

        # Split the values by comma
        data[cols] = data[cols].str.split(',')

        # Explode the list into individual rows
        df_exploded = data.explode(cols)

        # Clean up whitespace again and drop empty strings
        df_exploded[cols] = df_exploded[cols].str.strip()
        df_exploded = df_exploded[df_exploded[cols] != ""]

        # Drop duplicates and sort
        df_cleaned = df_exploded[[cols]].drop_duplicates().sort_values(by=cols).reset_index(drop=True)

        return df_cleaned
      
    def insert_junction_from_query(self, cursor, raw_table, dim_table, junction_table, join_col, fact_id_col, dim_id_col):

            query = f"""
            INSERT INTO movies_dw.{junction_table} ({fact_id_col}, {dim_id_col})
            SELECT
                f.{fact_id_col},
                d.{dim_id_col}
            FROM movies_dw.{raw_table} f
            JOIN LATERAL unnest(string_to_array(f.{join_col}, ',')) AS g({join_col}_name) ON true
            JOIN movies_dw.{dim_table} d
                ON TRIM(g.{join_col}_name) = d.{join_col}
                ON CONFLICT DO NOTHING;
            """
       
            cursor.execute(query)


      
