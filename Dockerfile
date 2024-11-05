# Fase 1: Build
FROM python:3.12-slim as build

RUN apt-get update -y \
    && apt-get install -y build-essential libpq-dev git \
    && pip install virtualenv \
    && virtualenv /opt/demorepo/venv 

COPY . /demorepo
WORKDIR /demorepo

RUN . /opt/demorepo/venv/bin/activate \
    && pip install -r requirements.txt
    

# Fase 2: Runtime
FROM python:3.12-slim

RUN apt-get update -y \
    && apt-get install -y libpq5 postgresql-client \
    && apt-get clean \
    && groupadd -g 5000 -r wsuser \
    && useradd -r -M -u 5000 -g wsuser wsuser

COPY --from=build /demorepo /opt/demorepo
COPY --from=build /opt/demorepo/venv /opt/demorepo/venv

WORKDIR /opt/demorepo

ENV PATH="/opt/demorepo/venv/bin:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:/opt/demorepo"

USER wsuser:wsuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
