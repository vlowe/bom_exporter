# Purpose
Create a Docker container for a Raspberry Pi which queries the [Bureau of Meterology](http://www.bom.gov.au) for weather measurements at [Observatory Hill](http://www.bom.gov.au/fwo/IDN60901/IDN60901.94768.json) and [Sydney Airport](http://www.bom.gov.au/fwo/IDN60801/IDN60801.94767.json).

# To build and run this container
```
docker build --tag bom_exporter .
docker run -p 8000:8000 bom_exporter:latest
```

# To get just the docker image
Visit the docker image [here](https://hub.docker.com/r/vickilowe/bom_exporter)

Example `docker-compose.yml` config:

```yml
version: '3.4'
services:
  bom_exporter:
    image: vickilowe/bom_exporter
    restart: always
    command: [
      "--urls",
      "http://www.bom.gov.au/fwo/IDN60801/IDN60801.94767.json",
    ]
    ports:
    - "8000:8000"
```

Example `prometheus.yml`:

```yml
scrape_configs:
  - job_name: 'bom_exporter'
    static_configs:
      - targets: ['hostname:8000']
```
