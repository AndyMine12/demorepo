# Fase 1: Build
FROM python:3.12-slim as build

RUN apt-get update -y \
    && apt-get install -y build-essential libpq-dev git \
    && pip install virtualenv

RUN virtualenv /opt/demorepo/venv
ENV VIRTUAL_ENV=/opt/demorepo/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY . /demorepo

WORKDIR /demorepo


RUN pip install -r /practica3/Scripts/requirements.txt


FROM python:3.12-slim


COPY --from=build /opt/demorepo /opt/demorepo


RUN apt-get update -y \
    && apt-get install -y libpq5 postgresql-client \
    && apt-get clean \
    && groupadd -g 5000 -r wsuser \
    && useradd -r -M -u 5000 -g wsuser wsuser \
    && chown -R wsuser:wsuser /opt/demorepo


ENV VIRTUAL_ENV=/opt/demorepo/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN pip install --no-cache-dir --upgrade pip


RUN pip install --no-cache-dir -r /opt/demorepo/practica3/requirements.txt


WORKDIR /opt/demorepo


USER wsuser:wsuser


EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
