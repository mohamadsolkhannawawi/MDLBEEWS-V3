FROM python:3.10-slim-buster

WORKDIR /app

COPY load_balancer/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY load_balancer/ .

EXPOSE 8104

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8104')" || exit 1

CMD ["python", "main.py"]