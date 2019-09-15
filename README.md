# docker-taiga

This image is a complete rebuild from scratch for a production environment with ldap support. 
Some parts might be inspired by the original repositories of benhutchins 
(https://github.com/benhutchins/docker-taiga) and the fork of benyanke 
(https://github.com/benyanke/docker-taiga).

## Features

- All in one taiga container: taiga-front, taiga-back and taiga-events (no external services 
are included though, like PostgreSQL or RabbitMQ)
- Nginx built in to expose only one port
- LDAP-Authentication support (taiga-contrib-ldap-auth-ext)
- Nearly all configuration values are configurable via environment variables (see sample.env 
for all available options)
- Up-to-date (at least at the moment ^^)


## Requirements

- Webserver as reverse proxy to provide ssl capability or change the nginx config (taiga.conf)
and inject certificates to directly expose the container
- Postgresql as database server
- (optional) RabbitMQ & Redis for async operations and events (see taiga documentation for details)


## Docker configuration

### Docker hub

The image is available on docker hub: https://hub.docker.com/r/taiq/docker-taiga

Use `docker pull taiq/docker-taiga` to pull the image.

### Environment settings

In the `sample.env` file you can find all possible settings with their default values.
Some of them will be explained in the following section:

- `SECRET_KEY`: set to a random value to protect your sessions (important!)
- Database section: set all values according to your database
- `URL_SCHEME` & `URL_HOST`: set to the url that your taiga server is reachable (used by taiga-back)
- `FRONT_API_URL` & `FRONT_EVENTS_URL`: tell the frontend how it can reach the backend services (use 
https and wss for tls)

### Volumes

Bind the directory `/data` to a volume to not lose your data when redeploying the container.
The directory will contain all files created by taiga, like attachments.


## Notes about licensing

This is a community build and is not associated with Taiga.io. Only the files in this repository 
are subject to the repository license file (LICENSE) and not the built container. All packages of taiga 
(e.g. taiga-back) are subject of their respective licenses.

## Breaking/Important changes

### 4.2.13_3

- Uses python alpine as basis instead of buster-slim. Any related docker images will need to adjust their behavior.
- SECRET_KEY2 removed due to a misconception. SECRET_KEY2 was used for taiga-events which needs to be the same as SECRET_KEY from django. This is now corrected as there is only SECRET_KEY in use for both files now. If you used different keys taiga-events was not working and did not print any error messages.
- Fixed celery for async events. Due to another misconception the default configuration of taiga for celery was not loaded. This resultet in at least a broken async project export feature.
 