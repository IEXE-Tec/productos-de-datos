FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN apt-get update && \
    apt-get install libgomp1 && \
    pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
