import re

def clean_markdown(text: str, config: dict = None, apply_all: bool = True) -> str:
    if not text:
        return text

    if config is None:
        config = {}
    if apply_all and not config:
        return clean_all(text)

    if config.get("code_block", apply_all):
        text = clean_code_block(text)
    if config.get("code_inline", apply_all):
        text = clean_code_inline(text)
    if config.get("headers", apply_all):
        text = clean_headers(text)
    if config.get("bold", apply_all):
        text = clean_bold(text)
    if config.get("italics", apply_all):
        text = clean_italics(text)
    if config.get("strikethrough", apply_all):
        text = clean_strikethrough(text)
    if config.get("blockquotes", apply_all):
        text = clean_blockquotes(text)

    return text


def clean_code_block(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    return text
    
def clean_code_inline(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'`[^`]*`', '', text)
    return text


def clean_headers(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    return text

def clean_bold(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'(\*\*|__)(.*?)\1', r'\2', text)
    return text


def clean_italics(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'(\*|_)(.*?)\1', r'\2', text)
    return text


def clean_strikethrough(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    return text


def clean_blockquotes(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'^\s*>\s*', '', text, flags=re.MULTILINE)
    return text


def clean_all(text: str) -> str:
    if not text:
        return text
    text = clean_code_block(text)
    text = clean_code_inline(text)
    text = clean_headers(text)
    text = clean_bold(text)
    text = clean_italics(text)
    text = clean_strikethrough(text)
    text = clean_blockquotes(text)
    return text


