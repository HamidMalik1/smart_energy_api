'''
Created on 10.05.2021
Provides the SolarEdge API data of Uni of Oulu
'''
import csv
import time
from datetime import datetime, timedelta

import MySQLdb
import pandas as pd
import solaredge
import schedule

from .config import CONFIG, MYSQL_CONNECTION
from . import solaredge_api



POWER_OUTPUT = CONFIG['csv']['solar_edge_power']

SOLAR_EDGE_CONFIG = CONFIG['solar_edge']

SITE_ID = SOLAR_EDGE_CONFIG['site_id']



def insert_overview(conn, overview_result):
    """Insert a overview line to DB"""
    query = "INSERT INTO solaredge_overview_api(lastupdatetime, lifetimedata, " \
        "lastyearenergy, lastmonthenergy,lastdayenergy, currentpower )  VALUES (%s,%s,%s,%s,%s,%s)"
    cur = conn.cursor()
    cur.executemany(query, [(overview_result['lastupdatetime'], overview_result['lifetimedata'],
        overview_result['lastyearenergy'], overview_result['lastmonthenergy'],
        overview_result['lastdayenergy'], overview_result['currentpower'])])
    conn.escape_string(query)
    conn.commit()


def overview():
    """Fetch and commit to DB"""
    overview_result = solaredge_api.overview.site_overview()

    conn = MySQLdb.connect(**MYSQL_CONNECTION, db="smartmetering")
    insert_overview(conn, overview_result)


def _days():
    today = datetime.today().strftime('%Y-%m-%d')

    yesterday = datetime.now() - timedelta(1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

    # Edit this date range as you see fit
    # If querying at the maximum resolution of 15 minute intervals, the API is limited to queries
    # of a month at a time This script queries one day at a time, with a one-second pause per day
    # that is polite but probably not necessary

    day_list = pd.date_range(start=yesterday, end=today)
    return day_list.strftime('%Y-%m-%d')


def fetch_df(api_cb, api_field_name, df_unit, days, time_unit=None):
    df_list = []
    for day in days:
        temp = api_cb(SITE_ID, day + ' 00:00:00', day + ' 23:59:59', \
            time_unit=time_unit)
        temp_df = pd.DataFrame(temp[api_field_name]['meters'][0]['values'])
        df_list.append(temp_df)
        time.sleep(1)
    df = pd.concat(df_list)
    df.columns = ['date', df_unit]
    return df


def merge_dfs(*dfs):
    print(*dfs)
    return pd.merge(*dfs)


def write_merged(csv_file, merged):
    """Write merged dfs to a .csv"""
    merged.to_csv(csv_file, index=False)


def insert_power(conn, row):
    """Insert a power row to DB"""
    query = "INSERT INTO energy_power_production(date ,energy ,power) " \
        "VALUES (%s,%s,%s)"
    cur = conn.cursor()
    cur.executemany(query, [(row['date'], row['energy'], row['power'])])

    conn.escape_string(query)
    conn.commit()


def insert_from_csv(conn, csv_file):
    """Insert rows from a .csv"""
    with open(csv_file) as f:
        rows = csv.DictReader(f, delimiter=',')
        for row in rows:
            insert_power(conn, row)
    conn.commit()


def cleanup_repeating(conn):
    """Cleanup previously written duplicate entries from DB"""
    # Add auto_increment in energy_production table to avoid repeating values.
    sql_delete_query = "DELETE n1 FROM energy_power_production n1," \
        " energy_power_production n2 " \
        "WHERE n1.ID < n2.ID AND n1.date = n2.date "
    cur = conn.cursor()
    cur.execute(sql_delete_query)
    conn.commit()
    print('number of rows deleted', cur.rowcount)


def energy_and_power():
    """Fetch and commit to DB"""
    api = solaredge.Solaredge(SOLAR_EDGE_CONFIG['api_key'])
    days = _days()

    energy_df = fetch_df(api.get_energy_details, 'energyDetails', 'energy', days,
        time_unit='QUARTER_OF_AN_HOUR')
    power_df = fetch_df(api.get_power_details, 'powerDetails', 'power', days)

    write_merged(POWER_OUTPUT, merge_dfs(energy_df, power_df))

    conn = MySQLdb.connect(**MYSQL_CONNECTION, db="smartmetering")
    
    insert_from_csv(conn, POWER_OUTPUT)
    cleanup_repeating(conn)
