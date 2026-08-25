FROM python:3.10-slim
WORKDIR /app
COPY data_provider-multiprocess/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY config/ config/
COPY utils/ utils/
COPY data_provider-multiprocess/ .
CMD ["python", "main.py"]
