# Energy_Weather Forecast FMI for Uni of Oulu PV production 
Updated every three hours. 

Within this Nordic collaboration, the Finnish Meteorological Institute has begun calculating in MEPS sets (MetCoOp Ensemble Prediction System), which means conducting eight forecast runs at once instead of just a single run. The set system represents a probability forecasting system where several slightly differing forecasts are run simultaneously. The system then produces a forecast as well as an estimate on its uncertainty.
So the fractiles in the PV forecast, and how narrowly or widely they are distributed depend on how the individual forecasts in MEPS behave. The idea is that the spread becomes larger in cases when the predicted weather conditions are more uncertain (due to atmospheric dynamics). 



# SolarEgde Monitoring Server API 
Provides all the API's for Solaredge monitoring service
Including Energy, Power and other useful data for solar production at Uni of Oulu



# Data visualization
The graphic representation of data is shown using Grafana 
Energy_Weather.json and local snapshot : http://localhost:3000/dashboard/snapshot/c1gHvcH1f6tp1SPP4sZGc2rxARGe5MC5 


# Running with pipenv
You need Python 3.9 and `pip`. The project dependencies are managed with Pipenv.

These commands are run in the repository root:

```sh
cd smart_energy_api
```

1. Install pipenv:

```sh
pip install --user pipenv
```

2. Install project dependencies:

```sh
pipenv install
```

For this to succeed you'll need to be able to run the build for a oython module known as 'mysqlclient'. Read more: <https://github.com/PyMySQL/mysqlclient/>

3. Create a local configuration file based on the example

```sh
cp config.toml.example config.toml
```

4. Source the virtual environment:

```sh
pipenv shell
```

You'll also need a MySQL-server, in a development setting you can spin up one with:

```sh
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
```



# Linting with pylint

After preparing the pipenv environment please run:

```sh
pylint src/
```
