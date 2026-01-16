"""
內容分類器
"""
import config


class Classifier:
    """管理和應用分類系統"""

    def __init__(self):
        self.categories = config.CATEGORIES

    def get_categories(self) -> list:
        """獲取所有分類"""
        return self.categories

    def get_category_description(self) -> dict:
        """獲取每個分類的說明"""
        descriptions = {
            "專業術語庫": "技術術語、業務術語、產業專有名詞",
            "開場話術": "背景引入、問題陳述、目的說明",
            "數據陳述話術": "增長數據、對比數據、趨勢分析",
            "分析論證話術": "因果分析、SWOT分析、多角度分析",
            "轉折與強調": "轉折句型、強調重點、補充說明",
            "案例引用話術": "成功案例、失敗教訓、對標分析",
            "風險與挑戰": "風險識別、應對策略、限制說明",
            "建議與結論": "行動建議、總結陳述、下一步規劃",
            "問答對應": "常見問題、專業解答",
            "圖表說明話術": "圖表引入、數據解讀、視覺化描述",
            "會議簡報用語": "互動引導、時間管理、總結收尾",
            "郵件與文件慣用語": "正式開頭、禮貌用語、結尾敬語"
        }
        return descriptions

    def validate_category(self, category: str) -> bool:
        """驗證分類是否有效"""
        return category in self.categories
