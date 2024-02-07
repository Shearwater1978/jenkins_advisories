FROM python:3.11-slim

MAINTAINER uglykoyote@gmail.com

ENV HOW_DEEP_ITEMS_LOOK_BACK=1
ENV LOOKING_DAYS=365
ENV SENSITIVE_PLUGINS='kubernetes'

RUN pip install --upgrade pip

RUN useradd -ms /bin/bash sentinel

USER sentinel
WORKDIR /tmp/
COPY --chown=sentinel:sentinel app/requirements.txt .
RUN pip install --user -r requirements.txt

WORKDIR /opt/
COPY --chown=sentinel:sentinel app/rss_feed_reader.py .

ENTRYPOINT ["python", "rss_feed_reader.py"]