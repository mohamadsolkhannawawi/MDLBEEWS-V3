FROM python:3.10.14-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_INDEX_URL=https://pypi.org/simple \
    PIP_EXTRA_INDEX_URL='' \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    HTTP_PROXY='' \
    HTTPS_PROXY='' \
    http_proxy='' \
    https_proxy='' \
    NO_PROXY='*' \
    no_proxy='*'

COPY p_wave_detector/requirements.txt requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install --no-cache-dir --retries 5 --timeout 60 --index-url https://pypi.org/simple --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY p_wave_detector/ .

EXPOSE 8102

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8102')" || exit 1

CMD ["python", "main.py"]