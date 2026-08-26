FROM python:3.10-slim-buster

WORKDIR /app

COPY p_wave_detector_load_balance/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY p_wave_detector_load_balance/ .

EXPOSE 8004 8103

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8004/health')" || exit 1

CMD ["python", "main.py"]