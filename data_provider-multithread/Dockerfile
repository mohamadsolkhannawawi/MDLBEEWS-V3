FROM python:3.10.14-slim-bullseye
WORKDIR /app
COPY data_provider-multithread/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY config/ config/
COPY utils/ utils/
COPY data_provider-multithread/ .
CMD ["python", "main.py"]
