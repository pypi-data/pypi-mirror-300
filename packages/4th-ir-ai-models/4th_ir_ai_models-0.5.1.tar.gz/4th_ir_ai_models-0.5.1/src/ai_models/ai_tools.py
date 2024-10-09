import json
import os
from enum import Enum
from typing import Dict, List, Literal, Union

import requests


class ImageClassificationModel(Enum):
    """Defines AI Models that can be used"""

    clip_vit_base_patch32 = "https://image-class-openai-clip-vit.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    document_finetuned_rvlcdip = "https://image-c-document-finetuned.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    # vissl = ""
    # classy_vision = ""
    # resnet50_1 = ""
    # efficientnet_b1 = ""
    # facebook_levit = ""
    # mxnet_resnet50 = ""
    # vit_base_224 = ""
    # vit_base_384 = ""
    # vit_finetunned = ""
    # van_base = ""
    # deit_base = ""
    # clip_vit = ""
    # microsoft_dit = ""
    # swin_large = ""
    # zero_shot_clip_vit = ""
    # facebook_diet_base = ""
    # facebook_diet_small_distelled = ""
    # microsoft_dit_base = ""
    # microsoft_swin_base = ""
    # vit_base_bean = ""
    # zero_shot_openai_clip_vit = ""
    # inception_v3 = ""


class NamedEntityRecognitionModel(Enum):
    """Defines AI Models that can be used"""

    spacy = "https://text-named-er-spacy.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    # flair = ""
    # flair_2 = ""
    # bert_1 = ""
    # en_bert_nvidia = ""
    # bert_finedtuned = ""
    # biomedical_ner_all = ""
    # bent_pub = ""
    # flair_ner_multi = ""
    # ner_english_ontonotes_large = ""
    # spacy_ner = ""


class TextClassifyModel(Enum):
    """Defines AI Models that can be used"""

    bart_large_mnli = "https://text-classification-bart-large.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    bart = "https://text-classification-bart.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    # disbart_mnli_12_1 = ""
    # mnli_yahoo = ""
    # distilbert_base = ""
    # facebook_bart_large = ""
    # roberta = ""


class TextSummarizeModel(Enum):
    """Defines AI Models that can be used"""

    bert2bert_small = "https://text-summarization.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    # google_bigbird_1 = ""
    # fairseq = ""
    # meeting_summary_facebook = ""
    # pegasus = ""
    # t5_headline_generator = ""
    # mt5_multilingual = ""
    # bert_finetuned_cnn = ""
    # bart_large_cnn = ""
    # facebook_bart_large = ""
    # long_t5 = ""
    # base_finetuned_news = ""


class TextExtractionModel(Enum):
    TextUtility = "https://text-utility.ai-sandbox.ch"


class TextSentimentAnalysisModel(Enum):
    bert_multilingual = "https://text-sentiment-analysis.calmflower-186525cd.switzerlandnorth.azurecontainerapps.io"


class LargeLanguageModel(Enum):
    mistral = "https://mistral.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"


class TextComparisonModel(Enum):
    """Defines AI Models that can be used"""

    all_minilm = "https://text-comparison-minilm.calmflower-186525cd.switzerlandnorth.azurecontainerapps.io"
    all_mpnet_base = "https://text-comparison-mpnet.calmflower-186525cd.switzerlandnorth.azurecontainerapps.io"


class TextTranslateModel(Enum):
    """Defines AI Models that can be used"""

    # only works english -> another language
    Transformers = "https://text-translation-transformers.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"


class Language(Enum):
    English = "English"
    French = "French"
    Romanian = "Romanian"
    German = "German"


class QuestionAnswerModel(Enum):
    """Defines AI Models that can be used"""

    # RobertaBaseSquad2 = "https://tqa-roberta-base-squad2.icysmoke-f4846de1.switzerlandnorth.azurecontainerapps.io"
    IntelDynamicTinybert = "https://tqa-intel-dynamic-tinybert.agreeabledune-08a9cefb.switzerlandnorth.azurecontainerapps.io"
    DistilbertBaseCasedDistilledSquad = "https://tqa-distilbert-distilled-squad.blackdune-63837cff.switzerlandnorth.azurecontainerapps.io"


class AITools:
    """Client for communicating with AI Model APIs"""

    def __init__(self, api_key) -> None:
        self.api_key = api_key

    def image_classification(
        self,
        image_file: str,
        classes: Union[List[str], None] = None,
        model: ImageClassificationModel = ImageClassificationModel.clip_vit_base_patch32,
    ) -> str:
        """
        Performs image classification
        Args:
            model: the model used to process the image
            image_file: the path to the image file
            classes: list of possible classes (not applicable to all models)

        Returns:
            The label of the image
        """
        url = model.value + "/api/v1/classify"
        if classes:
            data = {"classes": ",".join(classes)}
        else:
            data = {}
        files = [
            (
                "file",
                (
                    os.path.basename(image_file),
                    open(image_file, "rb"),
                    "image/png",
                ),
            )
        ]
        headers = {"Api-Key": self.api_key}

        response = requests.post(
            url=url, data=data, files=files, headers=headers
        )
        print(response.json())

        label = response.json()["label"]

        return label

    def text_extraction(
        self,
        file: str,
        format: Literal["pdf", "image"] = "pdf",
        model: TextExtractionModel = TextExtractionModel.TextUtility,
    ) -> str:
        """
        Performs text extraction from images or pdfs
        Args:
            model: the model used to process the image/pdf
            file: the path to the image/pdf file
            format: the file format (pdf, image)

        Returns:
            The extracted text
        """
        url = model.value + "/api/v1/ocr/image"
        if format not in ["pdf", "image"]:
            raise ValueError("Format must be image or pdf")

        media_type = "application/pdf" if format == "pdf" else "image/png"
        field = "pdf_file" if format == "pdf" else "image_file"
        files = [
            (
                field,
                (
                    os.path.basename(file),
                    open(file, "rb"),
                    media_type,
                ),
            )
        ]
        headers = {"accept": "application/json", "Api-Key": self.api_key}

        response = requests.post(url=url, files=files, headers=headers)

        text = response.json()["text"]

        return text

    def named_entity_recognition(
        self,
        text: str,
        model: NamedEntityRecognitionModel = NamedEntityRecognitionModel.spacy,
    ) -> List[Dict[str, str]]:
        """
        Performs named entity recognition
        Args:
            model: the model used to process the text
            text: the text to be processed

        Returns:
            List of tuples containing the words and their tags
        """
        url = model.value + "/api/v1/classify"
        data = {"text": text}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        results = response.json()["result"]

        return results

    def classify_text(
        self,
        text: str,
        labels: Union[List[str], None] = None,
        model: TextClassifyModel = TextClassifyModel.bart_large_mnli,
    ) -> str:
        """
        Performs text classification
        Args:
            model: the model used to classify the text
            question: the text to be classified
            labels: list of possible labels

        Returns:
            The answer to the question
        """

        url = model.value + "/api/v1/classify"

        data = {"text": text, "labels": labels}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        answer = response.json()["label"]

        return answer

    def summarize_text(
        self,
        text: str,
        model: TextSummarizeModel = TextSummarizeModel.bert2bert_small,
    ) -> str:
        """
        Performs text summarization
        Args:
            model: the model used to summarize the text
            text: the text to be summarized

        Returns:
            The summarized text
        """
        url = model.value + "/api/v1/summarize"
        data = {"text": text}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        response = response.json()

        return response["result"]

    def sentiment_analysis(
        self,
        text: str,
        model: TextSentimentAnalysisModel = TextSentimentAnalysisModel.bert_multilingual,
    ) -> str:
        """
        Performs text sentiment analysis
        Args:
            model: the model used to analyse the text
            text: the text to be analysed

        Returns:
            The text sentiment
        """
        url = model.value + "/api/v1/classify"
        data = {"text": text}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        response = response.json()

        return response["label"]

    def large_language_model(
        self,
        text: str,
        model: LargeLanguageModel = LargeLanguageModel.mistral,
    ) -> str:
        """
        Large language model using mistral API
        Args:
            model: the model used for language processing
            text: the text to be interpreted

        Returns:
            The text
        """
        # url = model.value + "/api/v1/classify"
        url = (
            f"{model.value}/create_document_store_txt/?"
            f"llm_model=mistral&ocr_language=eng&chunk_size=1000&"
            f"chunk_overlap=20&batch_size=10&index_name=singul"
        )
        data = {"text_input": text}
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        response = response.json()

        return response["label"]

    def compare_text(
        self, model: TextComparisonModel, source: str, texts: List[str]
    ) -> str:
        """
        Performs text comparison
        Args:
            model: the model used to compare the text
            source: the sentence against which the others are compared
            texts: list of sentences to be compared

        Returns:
            The most similar sentence from texts
        """
        url = model.value + "/api/v1/compare"

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }
        body = {"source": source, "sentences": texts}

        response = requests.post(
            url=url, data=json.dumps(body), headers=headers
        )

        result = response.json().get("similar")

        return result

    def translate_text(
        self,
        text: str,
        conversion_language: Language = Language.French,
        source_language: Language = Language.English,
        model: TextTranslateModel = TextTranslateModel.Transformers,
    ) -> str:
        """
        Performs text translation
        Args:
            model: the model used to translate the text
            text: the text to be translated

        Returns:
            The translated text
        """
        url = model.value + "/api/v1/translate"

        data = {
            "text": text,
            "source_lang": source_language.value,
            "target_lang": conversion_language.value,
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        response = response.json()

        return response.get("translated_text")

    def question_answer(
        self,
        question: str,
        context: str,
        model: QuestionAnswerModel = QuestionAnswerModel.IntelDynamicTinybert,
    ) -> str:
        """
        Performs question answering
        Args:
            model: the model used to process the question
            question: the question asked
            context: the context of the question

        Returns:
            The answer to the question
        """
        url = model.value + "/api/v1/answer"
        data = {
            "question": question,
            "context": context,
            "context_type": "text",
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

        response = requests.post(
            url=url, data=json.dumps(data), headers=headers
        )

        answer = response.json()
        return answer.get("answer")

    @staticmethod
    def summarize_text_health(model: TextSummarizeModel) -> bool:
        """
        Tests the health of the Text Summarization API
        Args:
            model: the Text Summarize model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def sentiment_analysis_health(model: TextSentimentAnalysisModel) -> bool:
        """
        Tests the health of the Text Sentiment Analysis API
        Args:
            model: the Text Sentiment Analysis model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def classify_text_health(model: TextClassifyModel) -> bool:
        """
        Tests the health of the Text Classification API
        Args:
            model: the Text Classify model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def text_ner_health(model: NamedEntityRecognitionModel) -> bool:
        """
        Tests the health of the Named Entity Recognition API
        Args:
            model: the Named Entity Recognition model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def image_classification_health(model: ImageClassificationModel) -> bool:
        """
        Tests the health of the Image Classification API
        Args:
            model: the Image Classification model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def text_extraction_health(model: TextExtractionModel) -> bool:
        """
        Tests the health of the Text Extraction API
        Args:
            model: the Text Extraction model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def large_language_model_health(model: LargeLanguageModel) -> bool:
        """
        Tests the health of the Large Language Model API
        Args:
            model: the Large Language model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def compare_text_health(model: TextComparisonModel) -> bool:
        """
        Tests the health of the Text Comparison API
        Args:
            model: the Text Compare model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def translate_text_health(model: TextTranslateModel) -> bool:
        """
        Tests the health of the Text Translation API
        Args:
            model: the Text Translate model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/health"

        response = requests.get(url=url)

        return response.status_code == 200

    @staticmethod
    def question_answer_health(model: QuestionAnswerModel) -> bool:
        """
        Tests the health of the Question Answering API
        Args:
            model: the QA model
        Returns:
            True if API is responing correctly, else False
        """
        url = model.value + "/api/v1/health"

        response = requests.get(url=url)

        return response.status_code == 200
