import datetime 
import time
import os
import inspect
import glob 
import pandas as pd


def get_current_chicago_time():
    """
    Returns datetime object of the current chicago time, needs to be adjusted during DST
    """
    return datetime.datetime.utcnow() - datetime.timedelta(hours=5)

def run_query(query, conn, has_game_date=True):
    start = time.time()
    df = pd.read_sql_query(query, conn)
    end = time.time()
    n = end - start 
    rows, cols = df.shape
    if has_game_date:
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    print(f'Returned {rows} rows, {cols} cols, took {n} seconds.')
    return df

def run_query_from_file(file, conn, has_game_date=True):
    """
    Input:
        file: str - name of file containing SQL query
        conn: SQLAlchemy object - database connection object
    Output:
        df: pandas Dataframe containing the queries output
    """
    s = time.time()
    with open(file, 'r') as f:
        q = f.read().strip()
    df = pd.read_sql_query(q, conn)
    if has_game_date:
        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    e = time.time()
    t = '{:.1f}'.format(e-s)

    print(f'Successfully Queried Data from {file}, took {t} seconds.')
    return df 


def write_to_db(df, table_name, conn):
    start = time.time()
    df.to_sql(table_name, conn, if_exists='append', index=False)
    end = time.time()
    rows, cols = df.shape
    n = end - start 
    print(f'Saved {rows} rows, {cols} cols to table {table_name}, took {n} seconds')


def get_todays_df(df, today_column='GAME_DATE'):
    return df[df[today_column].dt.date == datetime.date.today()]


def time_function(func):
    """
    Decorator that reports the execution time of a function
    """
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        t = '{:.1f}'.format(end-start)

        print(f'Function {func.__name__} took {t} seconds')
        return result
    return wrap


def time_function_simple(func):
    """
    Decorator that reports the execution time of a function
    """
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        t = '{:.1f}'.format(end-start)

        
        bound_args = inspect.signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        target_args = dict(bound_args.arguments)
        
        kv = ', '.join([f'{x[0]}={x[1]}' for x in list(zip(target_args.keys(), target_args.values()))])

        print(f'Function {func.__name__} took {t} seconds, ran with arguments {kv}')
        return result
    return wrap

def get_most_recent_file_from_directory(directory):
    """
    Input:
        directory: str - (i.e. '/Users/t2/Desktop')
    Output:
        str - fully-qualified filename, i.e. /Users/t2/Desktop/fantasy/GitDK/DraftKings/data/aggregated_data/2022-01-03_13:06:14.319307.csv
    """
    list_of_files = glob.glob(f'{directory}/*')
    return max(list_of_files, key=os.path.getctime)

def write_pandas_csv(df, file, index=False):
    rows, cols = df.shape
    start = time.time()
    df.to_csv(file, index=index)
    end = time.time()
    print(f"Saved {n} rows, {cols} cols to {file}, took {end-start} seconds")

def read_pandas_csv(file):
    start = time.time()
    df = pd.read_csv(file)
    end = time.time()
    rows, cols = df.shape 
    print(f"Read in {rows} rows and {cols} columns from file {file}, took {end-start} seconds")
    return df 

def find_latest_run(p):
    """
    Look in a log directory and return the latest file. all files must be in format:
         "%Y-%m-%d_%H:%M:%S.log"
    :param p: str - Path
    :return: most recent datetime object. If there are no files in the directory,
        this will default to January 4, 2005.
    """
    dates = []
    for file in os.listdir(p):
        with open(os.path.join(p, file), 'r') as f:
            x = f.read()
        # ignore empty file
        if len(x) == 0:
            continue

        date_info = file.split('.')[0]
        date = datetime.datetime.strptime(date_info, "%Y-%m-%d_%H:%M:%S")
        dates.append(date)

    if len(dates) == 0:
        # Default to arbitrary date, January 4, 2005
        return datetime.datetime(2005, 1, 4)

    most_recent = sorted(dates, reverse=True)[0]
    return most_recent