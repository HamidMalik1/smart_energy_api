FROM python:3.9-buster

WORKDIR /var/smart_energy_api

COPY smart_energy_api/ /usr/src/smart_energy_api/smart_energy_api/
COPY main.py /usr/src/smart_energy_api

COPY Pipfile* /var/smart_energy_api


# you can mount config with:
# --volume config.toml:/var/smart_energy_api/config.toml:ro

RUN apt-get update \
  && apt-get install -y python3-dev \
     default-libmysqlclient-dev build-essential

RUN pip install --no-cache-dir pipenv
RUN pipenv install --site-packages

CMD ["pipenv", "run", "python", "/usr/src/smart_energy_api/main.py"]