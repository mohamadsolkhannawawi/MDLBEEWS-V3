FROM python:3.10.14-bullseye

WORKDIR /app

COPY fast_api/requirements.txt requirements.txt
RUN python -m pip install --upgrade "pip>=24.2,<25"
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY fast_api/ .

EXPOSE 3333 8108

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3333/health')" || exit 1

CMD ["python", "main.py"]