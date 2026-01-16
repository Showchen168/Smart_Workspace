"""
檔案上傳路由
"""
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from pydantic import ValidationError

from .decorators import require_api_key
from services.validators import UploadRequest

upload_bp = Blueprint('upload', __name__)


def allowed_file(filename: str) -> bool:
    """檢查檔案類型是否允許"""
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'docx', 'pptx'})
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@upload_bp.route('/api/upload', methods=['POST'])
@require_api_key
def upload_file():
    """
    檔案上傳 API

    Headers:
        X-API-Key: Gemini API Key

    Form Data:
        file: 上傳的檔案 (.docx 或 .pptx)
        mode: 處理模式 (new 或 append，預設 append)
        model: AI 模型名稱 (預設 gemini-2.5-flash-lite)

    Returns:
        success: 是否成功
        task_id: 任務 ID
        message: 訊息
    """
    # 檢查是否有檔案
    if 'file' not in request.files:
        return jsonify({'error': '沒有上傳檔案'}), 400

    file = request.files['file']

    if not file.filename:
        return jsonify({'error': '檔案名稱為空'}), 400

    original_filename: str = file.filename

    if not allowed_file(original_filename):
        return jsonify({'error': '不支援的檔案格式，請上傳 .docx 或 .pptx'}), 400

    # 驗證請求參數
    try:
        upload_request = UploadRequest(
            mode=request.form.get('mode', 'append'),
            model=request.form.get('model', 'gemini-2.5-flash-lite')
        )
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    try:
        # 儲存檔案
        filename = secure_filename(original_filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

        # 確保上傳目錄存在
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

        # 建立任務
        task_id = str(uuid.uuid4())
        task_store = current_app.config['TASK_STORE']
        task_store.set(task_id, {
            'task_id': task_id,
            'filename': filename,
            'status': 'queued',
            'message': '任務已加入佇列',
            'created_at': datetime.now().isoformat()
        })

        # 啟動後台處理
        processor = current_app.config['DOCUMENT_PROCESSOR']
        processor.process_async(
            task_id=task_id,
            file_path=file_path,
            filename=filename,
            mode=upload_request.mode,
            api_key=request.api_key,
            model=upload_request.model
        )

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '檔案上傳成功，開始處理'
        }), 200

    except Exception as e:
        return jsonify({'error': f'上傳失敗: {str(e)}'}), 500
