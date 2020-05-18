FROM python:3

RUN pip install lastversion gitpython termcolor

COPY src/main.py /usr/bin/main.py
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
