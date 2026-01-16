"""
話術提取器
"""
from typing import Optional
from .gemini_client import GeminiClient
import config


class PhraseExtractor:
    """從文件中提取話術和術語"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client = GeminiClient(api_key, model)
        self.categories = config.CATEGORIES

    def extract(self, content: str) -> str:
        """
        從內容中提取話術

        Args:
            content: 文件內容（已解析的純文字）

        Returns:
            Markdown 格式的結構化話術
        """
        print("🤖 正在使用 Gemini 分析文件...")
        result = self.client.extract_phrases(content, self.categories)
        print("✅ 話術提煉完成")
        return result

    def merge_with_existing(self, existing_kb: str, new_content: str) -> str:
        """
        將新內容與現有知識庫合併

        Args:
            existing_kb: 現有知識庫內容
            new_content: 新提煉的內容

        Returns:
            合併後的知識庫
        """
        if not existing_kb or existing_kb.strip() == "":
            return new_content

        print("🔄 正在合併與去重...")
        merged = self.client.compare_and_deduplicate(existing_kb, new_content)
        print("✅ 合併完成")
        return merged
