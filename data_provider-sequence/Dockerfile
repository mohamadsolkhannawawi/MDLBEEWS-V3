FROM python:3.10-slim-buster
WORKDIR /app
COPY data_provider-sequence/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY config/ config/
COPY utils/ utils/
COPY data_provider-sequence/ .
CMD ["python", "main.py"]
