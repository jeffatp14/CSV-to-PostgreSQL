# CSV-to-PostgreSQL
This repository contains ETL pipeline for CSV-to-PostgreSQL by **Jeffa Triana Putra**.
currently fit for movies dataset

## 1. Data Modeling
Based on given datasets about ratings and movie information in  `.csv` format, writer designed ERD for conceptual, logical, and physical data model.
In the given datasets, there are 9 column, named MOVIES,YEAR,GENRE,RATING,ONE-LINE,STARS,VOTES,RunTime, and Gross. Writer decomposed the datasets into fact table, dimensional tables, and junction tables. **Fact table** contains measureable fields (year,rating,votes,runtime) and necessary information such as movie name and one-line. **Dimensional table** separated into 4 tables, which contains additional description of the fact table such as: stars, directors, and genre. Junction table will be needed as some of the table relation include **many-to-many relationship**, such as one movie can contain many genre and a particular genre can be in many movies.

### Conceptual data model
shows which table relate to each other
![alt text](https://github.com/jeffatp14/CadITDataEngTest/blob/main/data_modelling/conceptual_data%20model.jpeg)

### Logical data model
shows attribute of each table
![alt text](https://github.com/jeffatp14/CadITDataEngTest/blob/main/data_modelling/logical_data%20model.jpeg)

### Physical data model
shows detailed attribute of each table such as implemented table name, and its column type
![alt text](https://github.com/jeffatp14/CadITDataEngTest/blob/main/data_modelling/physical_data%20model.jpeg)

## 2. Database creation
Writer created a schema named movies_dw that contains 8 tables from data modeling before. Table creation query script can be accessed in `create_table_query` folder and table result can be seen in `tables` folder.

## 3. CSV Extractor (csv-postgres)
CSV Extractor is an ETL tool, it extract CSV from local files and store it in a postgres sink (currently available for this sink). 
There are 2 folders and one `main.py` program to make the process works. 
1. `csv_etl`
   This folder contain modules/function to extract, transform, and load csv file.
   - `config.py` : store all config variable from yaml file.
   - `cleaner.py` : clean initial raw data from extra spaces, inconsistent order, etc. (Currently only compatible for the given dataset/movies.csv).
   - `extractor.py` : contain a function to extract desired column from CSV and insert data function.
   - `transformer.py` : transform and clean duplicate for column that contain list, make it rows.
   - `postgres_sink` : endpoint of extractor, contain connection function to postgres database.
2. `configs`
   This folder contain all config file in yaml, template:
   ```
     columns:
    - column1
    - column2

    sink:
      host: postgres host
      port: postgres port
      username: postgres username
      password: postgres password
      database: database name
      schema: schema name
      method: insertion method
      table: table name
   
      dim_table: (optional for junction table), which dimensional table to join
      join_col: (optional for junction table), join on which column
   ```
   By specifying those variable in config files, the ETL can be delegated into multiple task for scheduling (e.g via Airflow) or in this program, writer use loop to run the task automatically. There are 3 type of insertion method: `extract` for direct extract without further transformation, `transform` transform list into rows, and `junction_sql` to handle the junction table.
   
3. `main.py`
   The main program for running the ETL. It will run ETL based on earlier configs setup.
4. Program Flow
   `main.py` will access all necessary classes, functions, or attribute from csv_etl module.
   - extract the raw files and put it in the cleaner function to clean and remove initial duplicate, it will produce raw dataframe necessary for further manipulation
   - In the main program, will loop through config files to run all the wanted ETL for every table: fact, dim, and junction.
   - Config method extract used for fact table, its column did not require any transformation
   - Config method transform used for dim table, because stars and genre is a list in one row, it will be transformed to be row for each element, and then eliminate the duplicate
   - Config method junction_sql used for junction table, as the junction table need id from other table, we have to use query to select necessary column and insert to the junction table.
   
## 4. Query
Both query scripts and its results can be accessed in `query_results` folder.
