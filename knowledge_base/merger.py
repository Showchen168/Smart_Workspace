"""
知識庫合併器 - 支援增量更新
"""
import os
from datetime import datetime


class KnowledgeBaseMerger:
    """管理知識庫的增量更新與合併"""

    def __init__(self, output_path: str):
        self.output_path = output_path

    def load_existing(self) -> str:
        """載入現有知識庫"""
        if os.path.exists(self.output_path):
            with open(self.output_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def save(self, content: str, source_file: str):
        """
        儲存知識庫

        Args:
            content: 知識庫內容
            source_file: 來源文件名稱
        """
        # 添加更新日誌
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = self._generate_header(source_file, timestamp)

        # 檢查內容是否已有 header
        if not content.startswith('# '):
            final_content = f"{header}\n\n{content}"
        else:
            final_content = content

        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✅ 知識庫已儲存至: {self.output_path}")

    def append_update_log(self, source_file: str):
        """在知識庫中追加更新紀錄"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if os.path.exists(self.output_path):
            with open(self.output_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 在文件開頭添加更新紀錄
            log_entry = f"\n> 📝 更新時間: {timestamp} | 來源: {source_file}\n"

            # 找到 metadata 區域並插入
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    content = f"{parts[0]}---{parts[1]}---{log_entry}{parts[2]}"
            else:
                content = log_entry + content

            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _generate_header(self, source_file: str, timestamp: str) -> str:
        """生成知識庫標頭"""
        header = f"""---
metadata:
  title: 專案知識庫
  last_updated: {timestamp}
  source: {source_file}
  format: Dify Knowledge Base (Markdown)
---

# 專案知識庫

> 📚 本知識庫由 AI 自動分析報告文件生成，用於 Dify 知識庫系統
>
> 最後更新: {timestamp}
> 來源文件: {source_file}

---
"""
        return header
