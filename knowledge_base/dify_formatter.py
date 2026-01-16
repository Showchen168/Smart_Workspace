"""
Dify 格式化器
"""


class DifyFormatter:
    """將提煉的內容格式化為 Dify 友善格式"""

    @staticmethod
    def format(content: str) -> str:
        """
        格式化內容為 Dify 知識庫格式

        Args:
            content: AI 提煉的原始內容

        Returns:
            格式化後的 Markdown 內容
        """
        # Gemini 已經輸出 Markdown 格式，這裡做基本檢查和優化
        formatted = content.strip()

        # 確保有適當的段落間距
        formatted = formatted.replace('\n\n\n', '\n\n')

        # 添加分隔線增強可讀性
        formatted = DifyFormatter._add_section_dividers(formatted)

        return formatted

    @staticmethod
    def _add_section_dividers(content: str) -> str:
        """在主要區塊間添加分隔線"""
        lines = content.split('\n')
        result = []

        for i, line in enumerate(lines):
            result.append(line)

            # 在大標題（## ）後添加分隔線
            if line.startswith('## ') and i < len(lines) - 1:
                if not lines[i + 1].startswith('---'):
                    result.append('')

        return '\n'.join(result)

    @staticmethod
    def add_qa_format(term: str, definition: str, context: str = "") -> str:
        """
        生成 Q&A 格式（方便 Dify 檢索）

        Args:
            term: 術語或話術
            definition: 定義或說明
            context: 使用場景（可選）

        Returns:
            Q&A 格式的 Markdown
        """
        qa = f"""
Q: {term}是什麼？/ 如何使用「{term}」？

A: {definition}
"""
        if context:
            qa += f"\n**使用場景**: {context}\n"

        return qa

    @staticmethod
    def create_index(categories: list) -> str:
        """
        創建目錄索引

        Args:
            categories: 分類列表

        Returns:
            Markdown 格式的目錄
        """
        index = "## 📑 目錄\n\n"
        for i, category in enumerate(categories, 1):
            index += f"{i}. [{category}](#{category})\n"

        return index + "\n---\n\n"
