FROM python:3.11.9

ENV DOCKER_CONTAINER true

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
