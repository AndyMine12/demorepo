FROM python:3.12-slim as build

RUN apt-get update -y \
    && apt-get install -y build-essential libpq-dev git \
    && pip install virtualenv \
    && virtualenv /opt/cn_p2_simple_ws/venv \
    && . /opt/cn_p2_simple_ws/venv/bin/activate \
    && pip install gunicorn

COPY . /demorepo

WORKDIR /demorepo

RUN . /opt/demorepo/venv/bin/activate \
    && pip install .

FROM python:3.12-slim

COPY --from=build /opt/demorepo /opt/demorepo
COPY entrypoint.sh /bin/entrypoint.sh

RUN apt-get update -y \
    && apt-get install -y libpq5 postgresql-client \
    && apt-get clean \
    && groupadd -g 5000 -r wsuser \
    && useradd -r -M -u 5000 -g wsuser wsuser \
    && chown -R wsuser:wsuser /opt/demorepo \
    && chmod +x /bin/entrypoint.sh
    

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/cn_p2_simple_ws
USER wsuser:wsuser

EXPOSE 8000
ENTRYPOINT ["entrypoint.sh"]

