from typing import Tuple

import six
from google.cloud import translate_v2 as translate

translate_client = translate.Client()


def translate_text(target: str, text: str) -> Tuple[str, str]:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages

    Args:
        target The language to translate results into.
        text The text to translate.

    Returns:
        A tuple of the translated text and the detected language. (translated text, detected language)
    """

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    return result["translatedText"], result["detectedSourceLanguage"]
