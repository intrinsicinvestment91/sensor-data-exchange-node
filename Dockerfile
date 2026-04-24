FROM python:3.12-slim

WORKDIR /app

# Install system deps for cryptography wheel
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Vendor copies of the two bitagent files SDEN needs at runtime
COPY bitagent/ /bitagent/

COPY sden/ ./sden/

ENV PYTHONPATH="/app:/bitagent"
ENV SDEN_HOST=0.0.0.0
ENV SDEN_PORT=8080

EXPOSE 8080

CMD ["python", "-m", "sden.main"]
