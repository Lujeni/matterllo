# syntax=docker/dockerfile:1.0.0-experimental
FROM python:3.7-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN --mount=type=ssh pip3 install --no-cache-dir -r requirements.txt

RUN groupadd -g 1000 matterllo && useradd -rm -d /home/matterllo -s /bin/bash -g matterllo -u 1000 matterllo

WORKDIR /home/matterllo
COPY --chown=matterllo:matterllo matterllo matterllo/
COPY --chown=matterllo:matterllo core core/
COPY --chown=matterllo:matterllo manage.py .
COPY --chown=matterllo:matterllo docker-entrypoint.sh .

EXPOSE 8000
USER 1000:1000
ENV PYTHONUNBUFFERED 1

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
