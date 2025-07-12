import yaml
import os
from pathlib import Path
class Config:
    def __init__ (self, config_path):
       
        with open(config_path) as f:
            config = yaml.safe_load(f)

        #Load sink config
        self.sink_config = config.get('sink', {})

        #Sensitive information
        # self.sink_config['username'] = os.getenv('username')
        # self.sink_config['password'] = os.getenv('password')
        self.username = self.sink_config.get("username")
        self.password = self.sink_config.get("password")

        #Server connection
        self.host=self.sink_config.get("host")
        self.port=self.sink_config.get("port")

        #Database connection
        self.database= self.sink_config.get("database")
        self.schema= self.sink_config.get("schema")
        self.table= self.sink_config.get("table")

        #Method selection
        self.method= self.sink_config.get("method")
        self.join_col = self.sink_config.get("join_col")
        # self.join_col = config.get('join_col')

        self.dim_table= self.sink_config.get("dim_table")

        #Load column config
        self.columns= config.get('columns', [])

