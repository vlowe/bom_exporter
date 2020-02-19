# This can compile fine on my Mac x86_64 machine, and on Cloud Build thanks to cross-build-start.

FROM balenalib/raspberrypi3-python:3

# https://www.balena.io/docs/reference/base-images/base-images/#building-arm-containers-on-x86-machines
RUN [ "cross-build-start" ]

# RUN apt-get update && apt-get install python3-pip
RUN python -m pip install prometheus_client requests

# https://www.balena.io/docs/reference/base-images/base-images/#building-arm-containers-on-x86-machines
RUN [ "cross-build-end" ]

COPY bom_exporter.py /root
EXPOSE 8000
ENTRYPOINT ["python3", "/root/bom_exporter.py"]
