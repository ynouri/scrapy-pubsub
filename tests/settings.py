"""Scrapy settings for integration test."""

ITEM_PIPELINES = {"scrapy_pubsub.PubSubItemPipeline": 100}

PUBSUB_PROJECT_ID = "test-project"
PUBSUB_TOPIC = "test-topic"
