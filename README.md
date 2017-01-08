# What is Matterllo ?
Simple integration between Trello and Mattermost: send Trello activity notifications to Mattermost channels

![matterllo_logo](matterllo.png)

# Quick Start
## Common part
[**Here**](COMMON.md)

## Heroku based install
* If you are not familiar with Python ecosystem, use this method.

[**Here**](HEROKU.md)

## Linux web server install
[**Here**](LINUX.md)

## Docker install
### old version
[**Here**](https://hub.docker.com/r/joinville/matterllo/)

### new version (django UI)

To use this project with docker:

```
docker build -t matterllo .
docker run -d --name matterllo -p 8000:8000 -e TRELLO_APIKEY=<apikey> -e TRELLO_TOKEN=<token> -v data:/usr/src/app/data matterllo
docker exec matterllo python manage.py loaddata admin
```

Or with docker-compose:

```
version: '2'

services:
  bridge:
    build: .
    ports:
      - 8000:8000
    volumes:
      - ./data:/usr/src/app/data
    environment:
      - TRELLO_APIKEY=<APIKEY>
      - TRELLO_TOKEN=<TOKEN>

networks:
  default:
    external:
      name: main
```