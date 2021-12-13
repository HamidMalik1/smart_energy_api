import schedule

from smart_energy_api import bcdc_fmi
from smart_energy_api import energy_and_power

if __name__ == "__main__":
    schedule.every(180).minutes.do(bcdc_fmi.job)
    schedule.every(5).minutes.do(energy_and_power.overview)
    schedule.every(15).minutes.do(energy_and_power.energy_and_power)

    while True:
        schedule.run_pending()
