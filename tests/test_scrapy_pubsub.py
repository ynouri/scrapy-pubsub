"""Tests for the Scrapy Pub/Sub extension"""
from scrapy_pubsub.scrapy_pubsub import ScrapyPubSub


def test_object():
    """Test that the class can be instantiated."""
    obj = ScrapyPubSub()
    assert obj
