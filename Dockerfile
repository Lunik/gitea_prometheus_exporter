FROM python:alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY api api
COPY prometheus-exporter.py .
COPY config.yml.exemple config.yml

EXPOSE 9100

CMD ["python3", "prometheus-exporter.py"]