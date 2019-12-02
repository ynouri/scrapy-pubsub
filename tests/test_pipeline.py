"""Unit tests for the Scrapy Pub/Sub item pipeline"""
from scrapy_pubsub import PubSubItemPipeline
from tests.settings import PUBSUB_PROJECT_ID, PUBSUB_TOPIC


# TODO: write unit tests by mocking Pub/Sub publisher
def test_object():
    """Test that the class can be instantiated."""
    obj = PubSubItemPipeline(PUBSUB_PROJECT_ID, PUBSUB_TOPIC)
    assert obj
