# Scrapy Pub/Sub

`scrapy-pubsub` is a scrapy extension which writes crawled items to Cloud Pub/Sub. It is based on [Google's Python client for Cloud Pub/Sub](https://googleapis.dev/python/pubsub/latest/), and takes inspiration from Mikhail Korobov's [scrapy-kafka-export](https://github.com/TeamHG-Memex/scrapy-kafka-export).

## Install

PyPI package coming soon.

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
