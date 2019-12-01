"""Scrapy settings for integration test."""

FEED_EXPORTERS = {
    "pubsub": "scrapy_pubsub.PubSubItemExporter",
}

PUBSUB_PROJECT_ID = "test-project"
PUBSUB_TOPIC = "test-topic"
