"""
版本資訊
每次發布新版本時更新此檔案
"""

# 版本號 (遵循 Semantic Versioning)
# MAJOR.MINOR.PATCH
# MAJOR: 重大變更，不向後相容
# MINOR: 新功能，向後相容
# PATCH: Bug 修復，向後相容
VERSION = "1.0.0"

# 版本名稱
VERSION_NAME = "Initial Release"

# 發布日期
RELEASE_DATE = "2026-01-16"

# 變更歷史
CHANGELOG = """
## v1.0.0 (2026-01-16) - Initial Release
- 文件知識提取器：支援 Word/PPT 解析
- Gemini AI 智能分析提取
- Dify 知識庫格式輸出
- Blueprint 模組化架構
- Redis/記憶體雙模式任務存儲
- Rate Limiting 速率限制
- Pydantic 輸入驗證
- 伺服器統一 API Key 管理
"""


def get_version_info() -> dict:
    """取得完整版本資訊"""
    return {
        "version": VERSION,
        "name": VERSION_NAME,
        "release_date": RELEASE_DATE,
    }
