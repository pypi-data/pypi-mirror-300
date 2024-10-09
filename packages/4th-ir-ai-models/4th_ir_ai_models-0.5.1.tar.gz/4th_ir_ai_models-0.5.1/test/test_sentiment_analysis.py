import logging
import unittest

from src.ai_models.ai_tools import AITools, TextSentimentAnalysisModel

logger = logging.getLogger("__sentiment_analysis__")
logger.setLevel(logging.INFO)


class TestSentimentAnalysis(unittest.TestCase):
    def test_sentiment_analysis_health(self):
        for model in TextSentimentAnalysisModel:
            self.assertTrue(AITools.sentiment_analysis_health(model))
