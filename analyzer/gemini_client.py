"""
Gemini API 客戶端
"""
import google.generativeai as genai  # type: ignore[import-untyped]
from typing import Optional
import config


class GeminiClient:
    """Gemini API 調用封裝"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model_name = model or config.GEMINI_MODEL

        if not self.api_key:
            raise ValueError("Gemini API Key 未設定，請輸入 API Key")

        genai.configure(api_key=self.api_key)  # type: ignore[attr-defined]
        self.model = genai.GenerativeModel(self.model_name)  # type: ignore[attr-defined]

    def analyze_content(self, content: str, prompt: str) -> str:
        """
        使用 Gemini 分析內容

        Args:
            content: 要分析的文件內容
            prompt: 分析指令

        Returns:
            AI 分析結果
        """
        try:
            full_prompt = f"{prompt}\n\n文件內容：\n{content}"

            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(  # type: ignore[attr-defined]
                    temperature=config.GEMINI_TEMPERATURE,
                    max_output_tokens=config.GEMINI_MAX_TOKENS,
                )
            )

            return response.text

        except Exception as e:
            raise Exception(f"Gemini API 調用失敗: {str(e)}")

    def extract_phrases(self, content: str, categories: list) -> str:
        """
        提煉話術並分類

        Args:
            content: 文件內容
            categories: 分類列表

        Returns:
            結構化的話術字典
        """
        prompt = f"""
你是一位專業的企業文件分析師，擅長識別商業報告中的專業用語、官方話術和行業術語。請仔細分析以下報告文件，提煉出各類話術和術語。

## 任務要求
1. **陸式企業官話**：識別高度概括性但抽象的用詞（如：賦能、抓手、打法、閉環、沉澱）
2. **戰略性詞彙**：宏觀發展方向、架構體系的詞彙（如：頂層設計、生態構建、戰略佈局）
3. **行業術語堆砌**：多個專業術語組合的高端表述（如：全鏈路數位化轉型、端到端解決方案）
4. **政策性語體**：帶有政策導向的用語（如：雙循環、供給側、新質生產力、高質量發展）
5. **話術提煉**：提取有價值的句型、表達方式、慣用語
6. **使用場景**：標註每個話術的適用場景

## 分類類別
{chr(10).join([f'- {cat}' for cat in categories])}

## 輸出格式（使用 Markdown）
請嚴格按照以下格式輸出，每個類別都要包含：

### [類別名稱]

#### 術語/話術 1
**內容**：[具體話術或術語]
**定義/說明**：[簡短解釋，說明這個詞/句的實際意義或為何這樣說]
**使用場景**：[何時使用，如：年度報告、戰略會議、對外宣傳等]
**範例**：[實際應用範例句]

---

## 額外要求
- 重點識別「陸式企業官話」和「戰略性詞彙」這類抽象但常見的表達
- 注意識別政策導向用語和流行商業概念
- 只提取**真正有價值、可複用**的話術，避免無意義的片段
- 每個類別至少提供 3-5 個項目（若文件中有的話）
- 優先提取高頻、專業、具權威感的內容
- 保持繁體中文輸出
"""

        result = self.analyze_content(content, prompt)
        return result

    def compare_and_deduplicate(self, existing_content: str, new_content: str) -> str:
        """
        比對現有知識庫與新內容，進行去重與合併

        Args:
            existing_content: 現有知識庫內容
            new_content: 新提煉的內容

        Returns:
            合併後的內容
        """
        prompt = f"""
你是知識庫管理專家，需要將新內容與現有知識庫進行智能合併。

## 任務
1. 比對「現有知識庫」與「新內容」
2. 識別重複或相似的話術/術語
3. 保留更完整、更準確的版本
4. 補充新的話術，避免重複
5. 維持原有的分類結構

## 去重原則
- 完全相同：保留一個
- 語意相似但表述不同：保留更專業的版本，可在說明中提及變體
- 補充說明：合併到同一項目中
- 全新內容：直接加入對應類別

## 現有知識庫
{existing_content}

## 新內容
{new_content}

## 輸出要求
輸出完整的合併後知識庫，保持 Markdown 格式，結構清晰。
"""

        result = self.analyze_content("", prompt)
        return result
