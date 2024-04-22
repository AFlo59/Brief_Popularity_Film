#FROM ubuntu:latest
FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED 1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
# RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
WORKDIR $HOME

COPY requirements.txt $HOME
RUN python -m pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . $HOME

# chown all the files to the app user
# RUN chown -R app:app $HOME

# change to the app user
# USER app

# CRON
COPY --chmod=755 ./cron/prediction.sh /home/app/cron
COPY --chmod=755 ./cron/imdb_top10_movies.sh /home/app/cron
RUN apt-get update && apt-get -y install cron
COPY cron/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron-log.log
RUN touch /var/log/pred-log.log

CMD ["cron", "-f"]