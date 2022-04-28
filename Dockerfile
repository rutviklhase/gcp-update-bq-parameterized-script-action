FROM python:3

LABEL 'com.github.actions.name' = 'GCP Big Query update parameterized script'
LABEL 'com.github.actions.description' = 'Update GCP Big Query parameterized sql scripts'

LABEL version = '0.1.0'
LABEL repository = 'https://github.com/GeneralMills/gcp-bq-update-parameterized-script'
LABEL maintainer = 'Kapil Kumar Trivedi'

COPY requirements.txt /requirements.txt
RUN pip3 --version; pip3 install -U pip; pip3 --version
RUN pip install -r /requirements.txt


COPY src/bigquery_update_parameterized_script.py /bigquery_update_parameterized_script.py

# Executes python file when the Docker container starts up
# CMD ['/bin/ls', '-l', '/bin/sh/python*']

ENTRYPOINT ["python", "/bigquery_update_parameterized_script.py"]
