# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.7
RUN python3 -m pip install pipenv

EXPOSE 80
WORKDIR /number-bot

COPY bot.py .
COPY secrets/ ./secrets
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

CMD ["pipenv", "run", "python3","bot.py"]
