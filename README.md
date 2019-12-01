# Scrapy Pub/Sub

Scrapy extension which writes crawled items to Cloud Pub/Sub.

## Tests

[Cloud Pub/Sub emulator](https://cloud.google.com/pubsub/docs/emulator) provided by Google is used for integration tests.

## Github workflow

The following Github actions are used:

- https://github.com/GoogleCloudPlatform/github-actions/tree/master/setup-gcloud
- https://github.com/actions/setup-java

For `setup-gcloud`, the creation of a dummy service account was necessary.

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
