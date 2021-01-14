FROM python:alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

######### FIX #########

COPY patch/py-gitea_user-get-orgs.diff /tmp/py-gitea_user-get-orgs.diff

RUN apk add -u --no-cache --virtual build-utils patch \
  && unix2dos /tmp/py-gitea_user-get-orgs.diff \
  && patch --binary -u /usr/local/lib/python3.9/site-packages/gitea/gitea.py -i /tmp/py-gitea_user-get-orgs.diff \
  && apk del build-utils

######### FIX #########

COPY api api
COPY prometheus-exporter.py .
COPY config.yml.exemple config.yml

EXPOSE 9100

CMD ["python3", "prometheus-exporter.py"]