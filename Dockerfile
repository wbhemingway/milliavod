FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY tests tests
COPY karma_vods.json karma_vods.json
COPY milliavod.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP milliavod.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
