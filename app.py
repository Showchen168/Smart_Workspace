"""
智能工作台 (Smart Workspace)
Flask 後端應用 - 整合多種 AI 工具

重構版本：
- Blueprint 模組化架構
- Redis/記憶體任務存儲
- ThreadPoolExecutor 執行緒管理
- Rate Limiting 速率限制
- Pydantic 輸入驗證
- API Key 安全處理
"""
import os
import sys
import atexit

from flask import Flask, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 添加當前目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from routes import upload_bp, tasks_bp, download_bp
from services import create_task_store, DocumentProcessor, shutdown_executor


def create_app(config_override: dict | None = None) -> Flask:
    """
    應用工廠函數

    Args:
        config_override: 覆蓋預設配置的字典

    Returns:
        Flask 應用實例
    """
    app = Flask(__name__)

    # 基本配置
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OUTPUT_FOLDER'] = 'output'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 上傳限制
    app.config['ALLOWED_EXTENSIONS'] = {'docx', 'pptx'}

    # 覆蓋配置
    if config_override:
        app.config.update(config_override)

    # 初始化 CORS
    CORS(app)

    # 初始化 Rate Limiter
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=os.getenv('REDIS_URL', 'memory://'),
    )

    # 對上傳 API 設定更嚴格的限制
    @limiter.limit("10 per minute")
    def upload_limit():
        pass

    # 初始化任務存儲
    task_store = create_task_store()
    app.config['TASK_STORE'] = task_store

    # 初始化文件處理器
    processor = DocumentProcessor(task_store, app.config['OUTPUT_FOLDER'])
    app.config['DOCUMENT_PROCESSOR'] = processor

    # 註冊 Blueprint
    app.register_blueprint(upload_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(download_bp)

    # 對特定路由套用限制
    limiter.limit("10 per minute")(upload_bp)

    # 首頁路由
    @app.route('/')
    def index():
        """首頁"""
        return render_template('index.html')

    # 健康檢查
    @app.route('/health')
    def health():
        """健康檢查端點"""
        return {'status': 'healthy'}, 200

    # 確保必要目錄存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

    return app


def main():
    """主程式入口"""
    app = create_app()

    # 註冊清理函數
    atexit.register(shutdown_executor)

    print("=" * 60)
    print("  Smart Workspace")
    print("=" * 60)
    print(f"  Server: http://localhost:5000")
    print(f"  Upload: {app.config['UPLOAD_FOLDER']}")
    print(f"  Output: {app.config['OUTPUT_FOLDER']}")
    print("=" * 60)
    print("  Tool 1: Knowledge Extractor")
    print("  Tool 2: AI Assistant (Udify)")
    print("=" * 60)
    print()
    print("  改進項目:")
    print("  ✓ Blueprint 模組化架構")
    print("  ✓ Redis/記憶體任務存儲")
    print("  ✓ ThreadPoolExecutor 執行緒管理")
    print("  ✓ Rate Limiting 速率限制")
    print("  ✓ Pydantic 輸入驗證")
    print("  ✓ API Key 安全處理 (X-API-Key Header)")
    print("=" * 60)
    print()

    # 啟動 Flask 應用
    app.run(debug=True, host='0.0.0.0', port=5000)


# 為 Gunicorn 建立應用實例
app = create_app()

if __name__ == '__main__':
    main()
