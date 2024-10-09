import logging
import unittest

from src.ai_models.ai_tools import AITools, QuestionAnswerModel

logger = logging.getLogger("__question_answer__")
logger.setLevel(logging.INFO)


class TestQuestionAnswer(unittest.TestCase):
    def test_question_answer_health(self):
        for model in QuestionAnswerModel:
            self.assertTrue(AITools.question_answer_health(model))
