# Scrapy Pub/Sub

`scrapy-pubsub` is a scrapy extension which writes crawled items to Cloud Pub/Sub.

It is based on [Google's Python client for Cloud Pub/Sub](https://googleapis.dev/python/pubsub/latest/).

## Install

PyPI package coming soon.

## Reference

### Scrapy documentation

- [Item exporters](https://docs.scrapy.org/en/latest/topics/exporters.html)
- [Feed exports](https://docs.scrapy.org/en/latest/topics/feed-exports.html)
- [Extensions](https://docs.scrapy.org/en/latest/topics/extensions.html)
- [Core API](https://docs.scrapy.org/en/latest/topics/api.html)
- [Run from a script](https://docs.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script)

### Community item exporters

- [Scrapy Kafka item exporter](https://github.com/TeamHG-Memex/scrapy-kafka-export)
- [Scrapy SQLite item exporter](https://github.com/RockyZ/Scrapy-sqlite-item-exporter)

### Stack overflow

- [How to create a custom Scrapy item exporter?](https://stackoverflow.com/questions/33290876/how-to-create-custom-scrapy-item-exporter)

## Tests

Google's [Cloud Pub/Sub emulator](https://cloud.google.com/pubsub/docs/emulator) is used for integration tests.

## CI

The following Github actions are used:

- https://github.com/GoogleCloudPlatform/github-actions/tree/master/setup-gcloud
- https://github.com/actions/setup-java

For `setup-gcloud`, the creation of a dummy service account was necessary. The following steps were used:

```bash
# Create account
SERVICE_ACCOUNT=scrapy-pubsub-github-workflow
gcloud iam service-accounts create ${SERVICE_ACCOUNT}

# Check no roles have been given
PROJECT=xyz
gcloud projects get-iam-policy ${PROJECT} \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:${SERVICE_ACCOUNT}"

# Create key
gcloud iam service-accounts keys create ./key.json \
  --iam-account ${SERVICE_ACCOUNT}@${PROJECT}.iam.gserviceaccount.com \
  --key-file-type=json
cat key.json | base64
```
