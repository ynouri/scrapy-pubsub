# Scrapy Pub/Sub

Scrapy extension which writes crawled items to Cloud Pub/Sub.

## Tests

[Cloud Pub/Sub emulator](https://cloud.google.com/pubsub/docs/emulator) provided by Google is used.

```
docker pull openjdk:latest
docker run -it openjdk:latest /bin/bash

```

## Github actions

- https://github.com/GoogleCloudPlatform/github-actions/tree/master/setup-gcloud
- https://github.com/actions/setup-java
