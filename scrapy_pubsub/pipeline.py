"""Scrapy Item Pipeline for Cloud Pub/Sub"""
# pylint: disable=too-few-public-methods
import logging
import json
from google.cloud import pubsub_v1
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class PubSubItemPipeline:
    """Cloud Pub/Sub Item Exporter"""

    def __init__(self, project_id, topic):
        """Init"""
        self.project_id = project_id
        self.topic = topic
        self.publisher = None
        self.topic_path = None
        self.futures = []

    @classmethod
    def from_crawler(cls, crawler):
        """Create a PubSubItemPipeline using the crawler settings."""
        settings = crawler.settings
        project_id = settings.get("PUBSUB_PROJECT_ID")
        topic = settings.get("PUBSUB_TOPIC")
        if project_id is None or topic is None:
            logger.error("Missing configuration for scrapy_pubsub")
            raise NotConfigured
        return cls(project_id, topic)

    def open_spider(self, _):
        """Creater the Pub/Sub client."""
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            self.project_id, self.topic
        )

    def close_spider(self, _):
        """Ensure that all futures returned with a result."""
        for future in self.futures:
            future.result()

    # pylint: disable=no-self-use
    def process_item(self, item, _):
        """Publish a scraped item to Pub/Sub"""
        data = json.dumps(item).encode("utf-8")
        logger.debug(f"Publishing to Pub/Sub topic {self.topic}.")
        future = self.publisher.publish(self.topic_path, data)
        self.futures.append(future)
        return item
