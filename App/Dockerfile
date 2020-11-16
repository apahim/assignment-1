FROM        centos/python-36-centos7

WORKDIR     /cloudy

COPY        . ./

RUN         pip install .

ENTRYPOINT  ["./entrypoint.sh"]
