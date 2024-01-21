FROM python:3.9-alpine

WORKDIR /app

COPY ../lab01/lab01_producer/requirements.txt .

RUN pip install -r requirements.txt

ADD ../lab01/lab01_producer/lab01_producer.py /app

CMD ["python", "lab01_producer.py"]