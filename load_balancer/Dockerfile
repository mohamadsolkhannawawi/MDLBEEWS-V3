FROM python:3.10.14-bullseye

WORKDIR /app

COPY load_balancer/requirements.txt requirements.txt
RUN python -m pip install --upgrade "pip>=24.2,<25"
RUN python -m pip install "setuptools<60.0.0" wheel
RUN python -m pip install "numpy<1.25.0" wheel
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY load_balancer/ .

EXPOSE 8103

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8103')" || exit 1

CMD ["python", "main.py"]
