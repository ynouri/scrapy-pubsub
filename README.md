# Scrapy Pub/Sub

`scrapy-pubsub` is a scrapy extension which writes crawled items to Cloud Pub/Sub.

It is based on [Google's Python client for Cloud Pub/Sub](https://googleapis.dev/python/pubsub/latest/).

## Install

PyPI package coming soon.

## How to use

Coming soon.

## Design

There were at least 4 different approaches possible for integrating Cloud Pub/Sub within the Scrapy framework and APIs.

| Approach           | Examples                                                                                                                                     | Pros                                                                                                                                                                                                                                                                                 | Cons                                                                                                                                                                                                                                                                                   |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1/ Item Exporter   | - [SQLite item exporter](https://github.com/RockyZ/Scrapy-sqlite-item-exporter) <br> - Native item exporters such as `JsonLinesItemExporter` | - Pub/Sub is an alternative way to export items, so `ItemExporter` sounds like the right interface for it.                                                                                                                                                                           | - `ItemExporter` objects are coupled to a `FeedExporter` which works with a file. In the case of Pub/Sub, we don't have a file. <br> - Scrapy native `ItemExporters` are closer to formatters (to JSON, JSON lines, XMLs...) which is orthogonal to the persistence medium (see below) |
| 2/ Storage Backend | - Native storage backends such as `StdoutFeedStorage`                                                                                        | - Pub/Sub could be seen as an alternative storage method, indepedently from the way the item are "exported", ie formatted. One could use either `JsonLinesItemExporter`, `XmlItemExporter`, or a even a custom item exporter and persist the items to the Pub/Sub "backend storage". | - The backend storage concept means that Pub/Sub should be seen as a file and provide a file interface <br> - Some item exporters write beginning and end tags to a file (e.g. `JsonItemExporter`) which would trigger sending incorrect messages to Pub/Sub.                          |
| 3/ Extension       | - [Kafka exporter extension](https://github.com/TeamHG-Memex/scrapy-kafka-export) <br> - Native extensions such as `FeedExport`              | - Simple <br> - Decoupled from `FeedExport`: one can publish to Pub/Sub but also write to a file <br> - This approach has previously been used for a Kafka extension, which should be very similar to Pub/Sub.                                                                       | - Can't reuse different item exporters <br> - Need to handle signals logic                                                                                                                                                                                                             |
| 4/ Item Pipeline   | - [MongoDB pipeline example](https://docs.scrapy.org/en/latest/topics/item-pipeline.html)                                                    | - Simple & decoupled like extensions <br> - It appears that signals are already handled for item pipelines, as opposed to extensions <br> - The MongoDB example from the official documentation indicates this would be the way to follow                                            | - Can't reuse different item exporters                                                                                                                                                                                                                                                 |

The Item Pipeline approach (4/) has been chosen for a first version.

## Reference

### Scrapy documentation

- [Item exporters](https://docs.scrapy.org/en/latest/topics/exporters.html)
- [Feed exports](https://docs.scrapy.org/en/latest/topics/feed-exports.html)
- [Extensions](https://docs.scrapy.org/en/latest/topics/extensions.html)
- [Core API](https://docs.scrapy.org/en/latest/topics/api.html)
- [Run from a script](https://docs.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script)

### Scrapy community contributions

- [Scrapy Kafka exporter extension](https://github.com/TeamHG-Memex/scrapy-kafka-export)
- [Scrapy SQLite item exporter](https://github.com/RockyZ/Scrapy-sqlite-item-exporter)

### Stack overflow

- [How to create a custom Scrapy item exporter?](https://stackoverflow.com/questions/33290876/how-to-create-custom-scrapy-item-exporter)

## Tests

Google's [Cloud Pub/Sub emulator](https://cloud.google.com/pubsub/docs/emulator) is used for integration tests.

## CI

The following Github actions are used:

- [setup-gcloud](https://github.com/GoogleCloudPlatform/github-actions/tree/master/setup-gcloud)
- [setup-java](https://github.com/actions/setup-java)

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

## Development

To install the dependencies:

```
pip install -e .[dev]
```
