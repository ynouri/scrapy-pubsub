"""Tests for the Scrapy Pub/Sub extension"""
from scrapy_pubsub import PubSubItemExporter


def test_object():
    """Test that the class can be instantiated."""
    obj = PubSubItemExporter()
    assert obj
