"""
Integration test: runs a Scrapy crawler with the PubSubItemPipeline. The
PubSubItemPipeline publishes to a Pub/Sub emulator running locally. The results
are read back from Pub/Sub and verified.

To run locally the Google Cloud Pub/Sub emulator use:
```
export PUBSUB_EMULATOR_HOST=localhost:8085
export PUBSUB_PROJECT_ID=test-project
gcloud beta emulators pubsub start \
    --project=${PUBSUB_PROJECT_ID} \
    --host-port=${PUBSUB_EMULATOR_HOST}
```
"""
# pylint: disable=redefined-outer-name
import json
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import pytest
from tests.pubsub_config import PubSubConfiguration


class MockSpider(Spider):
    """Mock spider used for the integration test."""

    name = "mock-spider"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        """Parse quotes from toscrape.com"""
        # TODO: actually mock toscrape.com responses
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }


@pytest.fixture(scope="module")
def pubsub():
    """Pub/Sub config fixture."""
    return PubSubConfiguration()


@pytest.fixture(scope="module")
def settings(pubsub):
    """Settings fixture."""
    return pubsub.scrapy_settings()


def test_settings_are_read(settings):
    """Test if the Scrapy settings are correctly read."""
    item_pipelines = settings.getdict("ITEM_PIPELINES")
    project_id = settings.get("PUBSUB_PROJECT_ID")
    topic = settings.get("PUBSUB_TOPIC")
    assert item_pipelines == {"scrapy_pubsub.PubSubItemPipeline": 100}
    assert project_id == "test-project"
    assert "test-topic" in topic


def test_crawler(pubsub, settings):
    """Test that the crawler process publishes to Pub/Sub."""
    # Crawl
    process = CrawlerProcess(settings)
    process.crawl(MockSpider)
    process.start()
    # Synchronously pull results from subscription
    response = pubsub.subscriber.pull(pubsub.sub_path, max_messages=100)
    msgs = response.received_messages
    data = [json.loads(msg.message.data.decode("utf-8")) for msg in msgs]
    ack_ids = [msg.ack_id for msg in msgs]
    pubsub.subscriber.acknowledge(pubsub.sub_path, ack_ids)
    assert len(data) == 10
    assert data[0] == {
        "author": "Albert Einstein",
        "tags": ["change", "deep-thoughts", "thinking", "world"],
        "text": (
            "“The world as we have created it is a process of our thinking. It"
            " cannot be changed without changing our thinking.”"
        ),
    }
