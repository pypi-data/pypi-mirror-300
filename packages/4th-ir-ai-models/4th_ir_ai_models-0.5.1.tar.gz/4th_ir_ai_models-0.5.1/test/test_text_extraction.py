import logging
import unittest

from src.ai_models.ai_tools import AITools, TextExtractionModel

logger = logging.getLogger("__text_extraction__")
logger.setLevel(logging.INFO)


class TestTextExtraction(unittest.TestCase):
    def test_text_extraction_health(self):
        for model in TextExtractionModel:
            self.assertTrue(AITools.text_extraction_health(model))
