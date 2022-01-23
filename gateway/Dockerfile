FROM python:3.10

WORKDIR /gateway

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9090

CMD [ "python3", "gateway.py"]
