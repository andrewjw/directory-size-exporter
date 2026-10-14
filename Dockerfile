FROM python:3.14.8-slim

ARG VERSION

COPY . /exporter

RUN pip install -r /exporter/requirements.txt

ENTRYPOINT ["/exporter/bin/directory-size-exporter"]
CMD []