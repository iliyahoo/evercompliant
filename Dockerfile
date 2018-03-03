FROM python:3.6.4-alpine3.6

RUN pip install tweepy pymongo

COPY hashtags_streamer.py /opt/

ENTRYPOINT ["/opt/hashtags_streamer.py"]
