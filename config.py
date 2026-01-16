"""
配置檔案
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API 設定
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# 輸出設定
OUTPUT_DIR = 'output'
OUTPUT_FILENAME = 'knowledge_base.md'

# 分類設定
CATEGORIES = [
    # 企業官話類
    "陸式企業官話",           # 中國大型企業/網路公司常見的高度概括性抽象用詞
    "戰略性詞彙",             # 宏觀發展方向、架構或體系的詞彙
    "行業術語堆砌",           # 多個專業術語組合，形成高端權威感的表述
    "政策性語體",             # 帶有強烈政策導向的用語（如：雙循環、供給側）

    # 表達技巧類
    "開場話術",               # 報告/簡報開頭引言
    "數據陳述話術",           # 數據報告、業績分析的表達方式
    "分析論證話術",           # 邏輯推理、分析論證的句型
    "轉折與強調",             # 轉折語、強調句型
    "風險與挑戰",             # 描述風險、挑戰的話術
    "建議與結論",             # 總結、建議的表達方式

    # 專業術語類
    "專業術語庫",             # 行業專有名詞與定義
    "縮寫與簡稱",             # 常見縮寫（KPI、OKR、ROI 等）
    "流行商業概念",           # 當紅商業概念（元宇宙、AI、數位轉型等）

    # 場景應用類
    "會議簡報用語",           # 會議主持、簡報常用語
    "郵件與文件慣用語",       # 正式書信、公文慣用語
    "圖表說明話術",           # 圖表、數據視覺化說明
    "案例引用話術",           # 引用案例、best practice 的說法
    "問答對應",               # Q&A 常見問答模式
]

# Gemini 參數
GEMINI_MODEL = 'gemini-2.5-flash-lite'
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 8000
