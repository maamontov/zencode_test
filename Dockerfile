FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /zenart_api
COPY requirements.txt /zenart_api/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /zenart_api/
