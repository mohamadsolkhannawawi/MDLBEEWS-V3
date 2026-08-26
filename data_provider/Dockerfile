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

COPY data_provider/requirements.txt requirements.txt
RUN python -m pip install --retries 5 --timeout 60 --index-url https://pypi.org/simple --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY config/ config/
COPY utils/ utils/
COPY data_provider/ .

EXPOSE 8101

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8101')" || exit 1

CMD ["python", "main.py"]