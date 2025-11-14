FROM python:3.10

WORKDIR /app

COPY server.py .

RUN pip install flask

CMD ["python3", "server.py"]
