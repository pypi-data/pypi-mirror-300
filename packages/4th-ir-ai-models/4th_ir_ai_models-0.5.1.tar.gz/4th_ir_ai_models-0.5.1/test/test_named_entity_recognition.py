import logging
import unittest

from src.ai_models.ai_tools import AITools, NamedEntityRecognitionModel

logger = logging.getLogger("__NER__")
logger.setLevel(logging.INFO)


class TestNER(unittest.TestCase):
    def test_ner_health(self):
        for model in NamedEntityRecognitionModel:
            self.assertTrue(AITools.text_ner_health(model))
