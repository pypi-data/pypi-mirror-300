import logging
import unittest

from src.ai_models.ai_tools import AITools, LargeLanguageModel

logger = logging.getLogger("__large_language_model__")
logger.setLevel(logging.INFO)


class TestLargeLanguageModel(unittest.TestCase):
    def test_large_language_model_health(self):
        for model in LargeLanguageModel:
            self.assertTrue(AITools.large_language_model_health(model))