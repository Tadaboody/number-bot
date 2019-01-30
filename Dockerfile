# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6

EXPOSE 80
WORKDIR /number-bot

COPY bot.py .
COPY requirements.txt .
COPY secrets/ ./secrets

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "bot.py"]