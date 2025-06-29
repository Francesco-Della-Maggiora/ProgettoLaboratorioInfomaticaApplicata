FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV MPLCONFIGDIR=/tmp/mplconfig

COPY app/ ./

RUN groupadd -r appuser && useradd -r -g appuser appuser \
  && mkdir -p /app/generated \
  && chown -R appuser:appuser /app \
  && chmod -R u+rwX /app
USER appuser


EXPOSE 5000
CMD ["python3", "app.py"]
