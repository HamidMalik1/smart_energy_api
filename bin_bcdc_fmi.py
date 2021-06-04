import schedule

from smart_energy_api import bcdc_fmi

if __name__ == "__main__":
    schedule.every(180).minutes.do(bcdc_fmi.job)

    while True:
        schedule.run_pending()
