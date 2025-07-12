from pathlib import Path
from csv_etl.cleaner import Cleaner
from csv_etl.transformer import Transform
from csv_etl.postgres_sink import Postgres
from csv_etl.extractor import extract_col
from csv_etl.config import Config


if __name__ == "__main__":
    import pandas as pd

    extracted_file = Path(__file__).parent / "movies.csv"
    config_folder = Path(__file__).parent /  "configs"
    config_files = list(config_folder.glob("*.yml"))

    transform=Transform()

    #Clean data first
    cleaner = Cleaner()
    raw_rows = cleaner.clean_raw(extracted_file)
    clean_data = [cleaner.parse_raw(row) for row in raw_rows[1:] if cleaner.parse_raw(row)]
    raw_df = cleaner.remove_duplicate(clean_data)
    print(raw_df)

    for config_file in config_files:

        config = Config(config_file)
        client = Postgres(config.sink_config)

        print(f"Running job for: {config_file.name} : {config.table}")

        if config.method == 'extract':
            selected_df = extract_col(raw_df, config.columns)
            client.load(selected_df)
        elif config.method == 'transform':
            selected_df = transform.transform_list_to_row(raw_df, config.columns)
            client.load(selected_df)
        elif config.method == 'junction_sql':
            client = Postgres(config.sink_config)
            transform.insert_junction_from_query(
                client.cursor,
                raw_table='raw_movies',
                dim_table=config.dim_table,  
                junction_table=config.table,  
                join_col=config.join_col,  
                fact_id_col=config.columns[0],
                dim_id_col=config.columns[1]
            )
        else:
            raise ValueError(f"Unknown method: {config.method}, file = {config_file.name}")

        client.connection.commit()
        client.close_connection()
 
