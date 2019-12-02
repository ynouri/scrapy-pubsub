"""
Runs a Scrapy crawler with the PubSubItemPipeline.

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
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.settings import Settings
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists
from tests.settings import PUBSUB_PROJECT_ID, PUBSUB_TOPIC


class MockSpider(Spider):
    """Mock spider used for the integration test."""

    name = "mock-spider"
    allowed_domains = ["toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response):
        """Parse quotes from toscrape.com"""
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }


def _settings():
    """Scrapy settings instantiated from tests/settings.py."""
    settings = Settings()
    settings_module_path = "tests.settings"
    settings.setmodule(settings_module_path, priority="project")
    return settings


def test_settings_are_read():
    """Test if the Scrapy settings are correctly read."""
    settings = _settings()
    item_pipelines = settings.getdict("ITEM_PIPELINES")
    project_id = settings.get("PUBSUB_PROJECT_ID")
    topic = settings.get("PUBSUB_TOPIC")
    assert item_pipelines == {"scrapy_pubsub.PubSubItemPipeline": 100}
    assert project_id == PUBSUB_PROJECT_ID
    assert topic == PUBSUB_TOPIC


def test_crawler(monkeypatch):
    """Test that the crawler process publishes to Pub/Sub."""
    monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "localhost:8085")
    monkeypatch.setenv("PUBSUB_PROJECT_ID", "test-project")
    _create_topic()
    _start_crawler_process()


def _create_topic():
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC)
        publisher.create_topic(topic_path)
    except AlreadyExists:
        pass


def _start_crawler_process():
    """Start a crawler process."""
    process = CrawlerProcess(_settings())
    process.crawl(MockSpider)
    process.start()


if __name__ == "__main__":
    _create_topic()
    _start_crawler_process()
