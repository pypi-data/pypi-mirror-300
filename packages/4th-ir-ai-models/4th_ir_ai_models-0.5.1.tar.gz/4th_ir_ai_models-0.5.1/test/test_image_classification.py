import logging
import unittest

from src.ai_models.ai_tools import AITools, ImageClassificationModel

logger = logging.getLogger("__image_classification__")
logger.setLevel(logging.INFO)


class TestImageClassification(unittest.TestCase):
    def test_image_classification_health(self):
        for model in ImageClassificationModel:
            self.assertTrue(AITools.image_classification_health(model))
