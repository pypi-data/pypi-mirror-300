import logging
import unittest

from src.ai_models.ai_tools import AITools, TextTranslateModel

logger = logging.getLogger("__text_translate__")
logger.setLevel(logging.INFO)


class TestTextTranslate(unittest.TestCase):
    def test_translate_text_health(self):
        for model in TextTranslateModel:
            self.assertTrue(AITools.translate_text_health(model))
