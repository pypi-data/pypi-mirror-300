import logging
import unittest

from src.ai_models.ai_tools import AITools, TextSummarizeModel

logger = logging.getLogger("__text_summarize__")
logger.setLevel(logging.INFO)


class TestTextSummarize(unittest.TestCase):
    def test_summarize_text_health(self):
        for model in TextSummarizeModel:
            self.assertTrue(AITools.summarize_text_health(model))
