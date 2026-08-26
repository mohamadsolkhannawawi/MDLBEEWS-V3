FROM python:3.10.14-bullseye

WORKDIR /app

COPY loc_mag_detector/requirements.txt requirements.txt
RUN python -m pip install --upgrade "pip>=24.2,<25"
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY loc_mag_detector/ .

EXPOSE 8105

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8105')" || exit 1

CMD ["python", "main.py"]