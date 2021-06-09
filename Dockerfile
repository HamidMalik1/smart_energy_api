FROM python:3.9-alpine

WORKDIR /var/smart_energy_api

COPY smart_energy_api/ /usr/src/smart_energy_api/smart_energy_api/
COPY main.py /usr/src/smart_energy_api

COPY Pipfile* /var/smart_energy_api


# you can mount config with:
# --volume settings.conf:/var/smart_energy_api/settings.conf:ro

RUN pip install --no-cache-dir pipenv
RUN pipenv install --system

CMD ["python", "/usr/src/smart_energy_api/main.py"]