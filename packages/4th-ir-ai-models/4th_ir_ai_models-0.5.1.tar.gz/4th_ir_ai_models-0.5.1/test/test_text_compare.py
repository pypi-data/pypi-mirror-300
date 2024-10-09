import logging
import unittest

from src.ai_models.ai_tools import AITools, TextComparisonModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestTextCompare(unittest.TestCase):
    def test_compare_text_health(self):
        for model in TextComparisonModel:
            self.assertTrue(AITools.compare_text_health(model))
