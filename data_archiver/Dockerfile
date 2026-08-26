FROM python:3.10.14-slim-bullseye

WORKDIR /app

COPY data_archiver/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY data_archiver/ .

EXPOSE 8106

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8106')" || exit 1

CMD ["python", "main.py"]