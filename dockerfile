FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/
COPY src /app/src
COPY README.md /app/

RUN pip install --no-cache-dir --upgrade pip && pip install .

ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "mgt.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
