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
RUN chmod 755 /home/app/cron/*.sh
RUN apt-get update && apt-get -y install cron
COPY cron/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron-log.log
#RUN (crontab -l ; echo "* * * * * /home/app/cron/cron.sh  > /proc/1/fd/1 2>/proc/1/fd/2") | crontab -u root -

CMD ["cron", "-f"]