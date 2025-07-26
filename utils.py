from deep_translator import GoogleTranslator

import re


def translate_text(text, target_lang='te'):
    result = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return result


def extract_keywords(text):
    keywords = []
    # Simple patterns to look for
    keywords += re.findall(r'\bfestival\b|\bdress\b|\bfood\b|\bsweets\b|\brace\b', text, re.IGNORECASE)
    return list(set(keywords))
