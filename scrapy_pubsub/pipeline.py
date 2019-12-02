"""Scrapy Item Pipeline for Cloud Pub/Sub"""
# pylint: disable=too-few-public-methods
import logging
from scrapy.exceptions import NotConfigured

logger = logging.getLogger(__name__)


class PubSubItemPipeline:
    """Cloud Pub/Sub Item Exporter"""

    def __init__(self, project_id, topic):
        """Init"""
        self.project_id = project_id
        self.topic = topic

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

    def open_spider(self, spider):
        """Open the Pub/Sub topic"""

    def close_spider(self, spider):
        """Close the Pub/Sub topic"""

    # pylint: disable=no-self-use
    def process_item(self, item, _):
        """Publish a scraped item to Pub/Sub"""
        print("Item processed!!!!")
        return item
