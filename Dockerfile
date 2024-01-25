FROM python:3.10.7-slim-buster
COPY case_creator /app/case_creator
COPY diseases.csv /app/
COPY connexions.csv /app/
COPY main.py /app/

RUN apt-get update && \
    apt-get -y install \
    gcc \
    git \
    curl \
    vim \
    build-essential \
    libpq-dev \
    wget \
    libcurl4-openssl-dev \
    libssl-dev \
    libgnutls28-dev \
    mime-support \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    unzip \
    python-pytest \
    && apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app/
