'''
Created on 10.05.2021
Provides the SolarEdge API data of Uni of Oulu
'''
import time
from datetime import datetime, timedelta

import MySQLdb
import pandas as pd
import solaredge

from .config import CONFIG, MYSQL_CONNECTION
from . import solaredge_api



SOLAR_EDGE_CONFIG = CONFIG['solar_edge']

SITE_ID = SOLAR_EDGE_CONFIG['site_id']



def insert_overview(conn, overview_result):
    """Insert an overview line to DB"""
    query = 'INSERT INTO solaredge_overview_api(lastupdatetime, lifetimedata, ' \
        'lastyearenergy, lastmonthenergy,lastdayenergy, currentpower )  VALUES (%s,%s,%s,%s,%s,%s)'
    cur = conn.cursor()
    params = [
        overview_result['lastupdatetime'], overview_result['lifetimedata'],
        overview_result['lastyearenergy'], overview_result['lastmonthenergy'],
        overview_result['lastdayenergy'], overview_result['currentpower']
    ]
    params = [conn.escape_string(str(param)) for param in params]
    cur.executemany(query, [tuple(params)])
    if cur.rowcount < 1:
        raise RuntimeError("Nothing was inserted")
    conn.commit()


def overview():
    """Fetch and commit to DB"""
    overview_result = solaredge_api.overview.site_overview()

    conn = MySQLdb.connect(**MYSQL_CONNECTION, db='smartmetering')
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


def fetch_df(api_cb, api_field_name, df_unit, days, kwargs={}):
    df_list = []
    for day in days:
        temp = api_cb(SITE_ID, day + ' 00:00:00', day + ' 23:59:59', \
            **kwargs)
        temp_df = pd.DataFrame(temp[api_field_name]['meters'][0]['values'])
        df_list.append(temp_df)
        time.sleep(1)
    df = pd.concat(df_list)
    df.columns = ['date', df_unit]
    return df


def merge_dataframes(*dfs):
    return pd.merge(*dfs)


def replace_one(conn, row):
    """Replace an energy and power record to DB, date is the unique key"""
    query = 'REPLACE INTO energy_power_production(date, energy, power) ' \
        'VALUES (%s,%s,%s)'
    cur = conn.cursor()
    params = [
        row['energy'],
        row['power']
    ]
    params = [conn.escape_string(str(param)) for param in params]
    params = [row['date']] + params
    cur.executemany(query, [tuple(params)])
    if cur.rowcount < 1:
        raise RuntimeError("Nothing was inserted")


def replace_records(conn, rows):
    for _, row in rows.iterrows():
        replace_one(conn, row)
    conn.commit()


def energy_and_power():
    """Fetch and commit to DB"""
    api = solaredge.Solaredge(SOLAR_EDGE_CONFIG['api_key'])
    days = _days()

    energy_df = fetch_df(api.get_energy_details, 'energyDetails', 'energy', days,
        kwargs={'time_unit': 'QUARTER_OF_AN_HOUR'})
    power_df = fetch_df(api.get_power_details, 'powerDetails', 'power', days)

    conn = MySQLdb.connect(**MYSQL_CONNECTION, db='smartmetering')
    replace_records(conn, merge_dataframes(energy_df, power_df))
    print('done')
