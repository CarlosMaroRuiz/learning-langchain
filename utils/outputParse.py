from langchain_core.output_parsers.transform import BaseTransformOutputParser
from .clean_md import clean_markdown

class CleanMarkdownParser(BaseTransformOutputParser[str]):
    config: dict = {}
    apply_all: bool = True
    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True

    @property
    def _type(self) -> str:
        return "clean_markdown_parser"

    def parse(self, text: str) -> str:
        return clean_markdown(text, config=self.config, apply_all=self.apply_all)
