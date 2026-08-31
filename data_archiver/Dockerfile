FROM python:3.10-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    HTTP_PROXY='' \
    HTTPS_PROXY='' \
    http_proxy='' \
    https_proxy='' \
    NO_PROXY='*' \
    no_proxy='*'

COPY data_archiver/requirements.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip
  RUN python -m pip install --no-cache-dir --no-compile --retries 10 --timeout 120 --index-url https://pypi.org/simple --trusted-host pypi.org --trusted-host files.pythonhosted.org --only-binary=:all: --no-deps obspy==1.4.1
  RUN python -m pip install --no-cache-dir --no-compile --retries 10 --timeout 120 --index-url https://pypi.org/simple --trusted-host pypi.org --trusted-host files.pythonhosted.org --only-binary=:all: scipy lxml matplotlib sqlalchemy requests decorator
RUN python -m pip install "setuptools<60.0.0" wheel
RUN python -m pip install "numpy<1.25.0" wheel
  RUN python -m pip install --no-cache-dir --no-compile --retries 10 --timeout 120 --index-url https://pypi.org/simple --trusted-host pypi.org --trusted-host files.pythonhosted.org --only-binary=:all: -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY data_archiver/ .

EXPOSE 8106

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8106')" || exit 1

CMD ["python", "main.py"]
