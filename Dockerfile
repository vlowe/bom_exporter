# This can compile fine on my Mac x86_64 machine. Maybe Docker's virtualizing it?

FROM arm32v6/alpine

RUN apk update && apk add python3
RUN python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip
RUN python3 -m pip install prometheus_client requests
COPY bom_exporter.py /root
EXPOSE 8000
ENTRYPOINT ["python3", "/root/bom_exporter.py"]
