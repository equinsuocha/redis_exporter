FROM python:3.7.1
# set python env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install package
COPY . ./usr/src/redis_exporter/
RUN /usr/local/bin/python3.7 -m pip install -r ./usr/src/redis_exporter/requirements.txt
RUN /usr/local/bin/python3.7 -m pip install ./usr/src/redis_exporter

COPY ./docker/settings_docker.yaml /etc/redis_exporter/redis_exporter.yaml
RUN chmod a+x ./usr/src/redis_exporter/docker/entrypoint.sh

CMD ./usr/src/redis_exporter/docker/entrypoint.sh
