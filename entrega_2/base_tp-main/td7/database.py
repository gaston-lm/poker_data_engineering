import pandas as pd
from sqlalchemy import create_engine, text
import os

from td7.custom_types import Records
from td7.config import POSTGRES_CONN_STRING


class Database:
    """Class to interact with the database."""

    def __init__(self, conn_string=POSTGRES_CONN_STRING, sql_file_path=None):
        self.engine = create_engine(conn_string)
        self.connection = self.engine.connect()

        if sql_file_path:
            absolute_path = os.path.join(os.path.dirname(__file__), sql_file_path)
            self.run_sql_file(absolute_path)

    def run_select(self, sql: str) -> Records:
        """Runs a select query and returns dict records.

        Parameters
        ----------
        sql : str
            SELECT query to run.

        Returns
        -------
        Records
        """
        dataframe = pd.read_sql(sql, self.connection)
        return dataframe.to_dict(orient="records")

    def run_insert(self, records: Records, table: str):
        """Runs an insert statement from data to table.

        Parameters
        ----------
        records : Records
            Data to insert.
        table : str
            Table name to insert.
        """
        pd.DataFrame(records).to_sql(
            table, self.connection, if_exists="append", index=False
        )
    
    def run_sql_file(self, file_path: str):
        """Reads and executes SQL commands from a file.

        Parameters
        ----------
        file_path : str
            Path to the SQL file.
        """
        with open(file_path, 'r') as file:
            sql_commands = file.read()
        
        with self.connection.begin() as transaction:
            for command in sql_commands.split(';'):
                if command.strip():
                    self.connection.execute(text(command))

    def __del__(self):
        self.connection.close()