import logging
import unittest

from src.ai_models.ai_tools import AITools, TextClassifyModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestTextClassify(unittest.TestCase):
    def test_classify_text_health(self):
        for model in TextClassifyModel:
            self.assertTrue(AITools.classify_text_health(model))
