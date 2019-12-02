"""Pub/Sub config helper for the crawler integration test."""
import uuid
from scrapy.settings import Settings
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists
from tests.settings import PUBSUB_PROJECT_ID, PUBSUB_TOPIC

PUBSUB_SUBSCRIPTION = "test-subscription"


class PubSubConfiguration:
    """Pub/Sub configuration helper class."""

    def __init__(self):
        """
        A unique ID is generated for each test - to avoid reusing the same
        topic or subscription.
        """
        self.id_ = str(uuid.uuid4())
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.create_topic()
        self.create_subscription()

    @property
    def topic(self):
        """Topic name including the unique ID"""
        return f"{PUBSUB_TOPIC}-{self.id_}"

    @property
    def subscription(self):
        """Subscription name including the unique ID"""
        return f"{PUBSUB_SUBSCRIPTION}-{self.id_}"

    def create_topic(self):
        """Create the topic"""
        topic_path = self.publisher.topic_path(PUBSUB_PROJECT_ID, self.topic)
        try:
            self.publisher.create_topic(topic_path)
        except AlreadyExists:
            pass
        return topic_path

    def create_subscription(self):
        """Create the subscription"""
        self.sub_path = self.subscriber.subscription_path(
            PUBSUB_PROJECT_ID, self.subscription
        )
        topic_path = self.subscriber.topic_path(PUBSUB_PROJECT_ID, self.topic)
        try:
            self.subscriber.create_subscription(self.sub_path, topic_path)
        except AlreadyExists:
            pass

    def scrapy_settings(self):
        """Scrapy settings instantiated from tests/settings.py"""
        settings = Settings()
        settings_module_path = "tests.settings"
        settings.setmodule(settings_module_path, priority="project")
        # We replace the topic name by the one generated with the UUID
        settings.set("PUBSUB_TOPIC", self.topic, priority="project")
        return settings
