'''
Created on 10.05.2021
Provides the Finnish Meteorological Institute (FMI) API data of Uni of Oulu
'''
import csv
import datetime as dt

import urllib.request
import MySQLdb

from .config import CONFIG, MYSQL_CONNECTION



# FIXME
ASSUME_DB_TIMEZONE = dt.timezone(-dt.timedelta(hours=2), "Europe/Helsinki")



def fetch(base_url):
    """List of lines from Ilmanet"""
    api_url_fmi = base_url + '/download.php?orderId=93173&id=127&type=solar&limit=1'

    # Ilmanet responds with Content-Type: text/csv; charset=utf-8
    # the first line is a header
    return urllib.request.urlopen(api_url_fmi)


def lines(fetched):
    """Iterable list of lines from Ilmanet"""
    return [line.decode('utf-8').rstrip() for line in fetched.readlines()]


def read_forecasts(lines):
    """Return a list of forecast dicts"""
    reader = csv.DictReader(lines)
    return list(reader)


def overwrite_ilmanet_date(forecast):
    """Overwrite forecast forecast_time with with a datetime instance"""
    date = dt.datetime.strptime(forecast['forecast_time'] + "00", '%Y-%m-%d %H:%M:%S%z')
    forecast['forecast_time'] = date


def parse_dates(forecasts):
    """Overwrite forecasts forecast_time with with a datetime instance"""
    [overwrite_ilmanet_date(forecast) for forecast in forecasts]


def replace_one(conn, line):
    """Replace a forecast line to DB, the unique key is forecast_time"""
    query = 'REPLACE INTO fmi_data(forecast_time, request_id, power_output_w, ' \
        'power_output_f0_w, power_output_f10_w, power_output_f25_w, ' \
        'power_output_f50_w, power_output_f75_w, power_output_f90_w, ' \
        'power_output_f100_w, system_temperature_c, nominal_output_efficiency, ' \
        'air_temperature_c, cloud_cover_total, ' \
        'cloud_cover_high, cloud_cover_medium, ' \
        'cloud_cover_low, system_radiation_global_wm2, ' \
        'system_radiation_direct_wm2, ' \
        'system_radiation_diffuse_wm2, radiation_global_wm2, '\
        'radiation_direct_wm2, radiation_diffuse_wm2 ) ' \
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,' \
        '%s,%s)'

    cur = conn.cursor()
    params = [
        line['request_id'], line['power_output_w'],
        line['power_output_f0_w'], line['power_output_f10_w'],
        line['power_output_f25_w'], line['power_output_f50_w'],
        line['power_output_f75_w'], line['power_output_f90_w'],
        line['power_output_f100_w'],
        line['system_temperature_c'], line['nominal_output_efficiency'],
        line['air_temperature_c'], line['cloud_cover_total'],
        line['cloud_cover_high'], line['cloud_cover_medium'],
        line['cloud_cover_low'], line['system_radiation_global_wm2'],
        line['system_radiation_direct_wm2'], line['system_radiation_diffuse_wm2'],
        line['radiation_global_wm2'], line['radiation_direct_wm2'],
        line['radiation_diffuse_wm2']
    ]
    params = [conn.escape_string(str(param)) for param in params]
    params = [line['forecast_time']] + params
    cur.executemany(query, [tuple(params)])
    if cur.rowcount < 1:
        raise RuntimeError("Nothing was inserted or replaced")


def replace(conn, forecasts):
    """Replace a list of forecast dicts"""
    for forecast in forecasts:
        replace_one(conn, forecast)
    conn.commit()


def job():
    """Fetch latest forecast and commit it to DB"""
    base_url = str(CONFIG['ilmanet']['url'])
    forecasts = read_forecasts(lines(fetch(base_url)))
    parse_dates(forecasts)
    conn = MySQLdb.connect(**MYSQL_CONNECTION, db='smartmetering')
    replace(conn, forecasts)
    print('done')
