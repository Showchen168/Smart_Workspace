"""
下載與預覽路由
"""
import os
from flask import Blueprint, jsonify, send_file

from .decorators import require_completed_task

download_bp = Blueprint('download', __name__)


@download_bp.route('/api/download/<task_id>', methods=['GET'])
@require_completed_task
def download_result(task_id: str, task: dict):
    """
    下載結果檔案 API

    Args:
        task_id: 任務 ID

    Returns:
        下載的 Markdown 檔案
    """
    output_file = task.get('output_file')

    if not output_file or not os.path.exists(output_file):
        return jsonify({'error': '找不到輸出檔案'}), 404

    return send_file(
        output_file,
        as_attachment=True,
        download_name='knowledge_base.md',
        mimetype='text/markdown'
    )


@download_bp.route('/api/preview/<task_id>', methods=['GET'])
@require_completed_task
def preview_result(task_id: str, task: dict):
    """
    預覽結果內容 API

    Args:
        task_id: 任務 ID

    Returns:
        content: 預覽內容
        truncated: 是否被截斷
    """
    output_file = task.get('output_file')

    if not output_file or not os.path.exists(output_file):
        return jsonify({'error': '找不到輸出檔案'}), 404

    # 讀取內容（限制預覽大小）
    max_preview_size = 10000
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read(max_preview_size)

    return jsonify({
        'content': content,
        'truncated': len(content) >= max_preview_size
    }), 200
