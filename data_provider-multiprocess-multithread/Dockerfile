FROM python:3.10.14-bullseye
WORKDIR /app
COPY data_provider-multiprocess-multithread/requirements.txt requirements.txt
RUN python -m pip install --upgrade "pip>=24.2,<25"
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY config/ config/
COPY utils/ utils/
COPY data_provider-multiprocess-multithread/ .
CMD ["python", "main.py"]
