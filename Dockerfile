# Fase 1: Build
FROM python:3.12-slim as build

RUN apt-get update -y \
    && apt-get install -y build-essential libpq-dev git

COPY . /demorepo
WORKDIR /demorepo

RUN pip install -r requirements.txt

# Fase 2: Runtime
FROM python:3.12-slim

RUN apt-get update -y \
    && apt-get install -y libpq5 postgresql-client \
    && apt-get clean \
    && groupadd -g 5000 -r wsuser \
    && useradd -r -M -u 5000 -g wsuser wsuser

# Copiar solo las dependencias necesarias
COPY --from=build /demorepo /opt/demorepo

WORKDIR /opt/demorepo

# Instalar las dependencias en la fase final
RUN pip install --no-cache-dir -r /opt/demorepo/requirements.txt

USER wsuser:wsuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
