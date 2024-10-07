import os 
import pandas as pd 
from sqlalchemy import create_engine
import pymysql
import time 

HOST = os.environ.get('DK_DB_HOST', '')
PASSWORD = os.environ.get('DK_DB_PASSWORD', '')


def run_sql_query_from_file(file, conn, logger=None):
    """
    Read in a .sql file and gets the results in pandas DF 
    Inputs
    ------
        file: the file location (str)
        conn: Database Connection Object

    Outputs
    -------
        Dataframe containing result set 
    """
    with open(file, 'r') as f:
        query = f.read()

    start = time.time()
    df = pd.read_sql_query(query, conn)
    end = time.time()

    if logger:
        n_rows = df.shape[0]
        n_seconds = '{:.1f}'.format(end - start)
        logger.info(f"Queried from file: {file}, retrieved n_rows: {n_rows}, took {n_seconds}s.")

    return df


def create_connection(host=HOST,
                      user='akgoyal',
                      database='dk_nba',
                      password=PASSWORD):
    """
    Inputs
    ------
        host: string containing host name
        user: string for the user
        database: string for the database name
        password: string 

    Outputs
    -------
        Connection object
    """

    conn = create_engine('mysql+pymysql://' + user + ':' +
                         password + '@' + host + ':3306/' + database,
                         echo=False)
    return conn

def create_cursor(host=HOST,
                  user='akgoyal',
                  database='dk_nba',
                  password=PASSWORD):
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=database
    )
    return conn