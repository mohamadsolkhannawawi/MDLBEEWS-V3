FROM python:3.10-slim-buster

WORKDIR /app

COPY data_provider/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY data_provider/ .

EXPOSE 8101

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8101')" || exit 1

CMD ["python", "main.py"]