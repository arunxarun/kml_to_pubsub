FROM python:2.7

COPY ./src /src

WORKDIR /src

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]
