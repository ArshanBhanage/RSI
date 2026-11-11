FROM python:3.13-slim
RUN pip install --no-cache-dir duckdb==2.0.0 sqlglot==30.31.0
USER 65534:65534
WORKDIR /tmp
ENTRYPOINT ["python", "-I", "/authority/evaluate.py"]
