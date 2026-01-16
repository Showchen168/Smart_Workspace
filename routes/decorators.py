"""
路由裝飾器模組
抽取重複的檢查邏輯
"""
from functools import wraps
from flask import jsonify, request, current_app


def require_task(f):
    """
    檢查任務是否存在的裝飾器

    使用方式:
        @bp.route('/api/status/<task_id>')
        @require_task
        def get_status(task_id, task):
            return jsonify(task)
    """
    @wraps(f)
    def decorated(task_id, *args, **kwargs):
        task_store = current_app.config['TASK_STORE']
        task = task_store.get(task_id)

        if not task:
            return jsonify({'error': '找不到該任務'}), 404

        return f(task_id, task, *args, **kwargs)
    return decorated


def require_completed_task(f):
    """
    檢查任務是否存在且已完成的裝飾器

    使用方式:
        @bp.route('/api/download/<task_id>')
        @require_completed_task
        def download(task_id, task):
            return send_file(task['output_file'])
    """
    @wraps(f)
    def decorated(task_id, *args, **kwargs):
        task_store = current_app.config['TASK_STORE']
        task = task_store.get(task_id)

        if not task:
            return jsonify({'error': '找不到該任務'}), 404

        if task['status'] != 'completed':
            return jsonify({'error': '任務尚未完成'}), 400

        return f(task_id, task, *args, **kwargs)
    return decorated


def require_api_key(f):
    """
    檢查 API Key 的裝飾器
    優先從 Header 取得，其次從環境變數

    Header 格式: X-API-Key: your-api-key
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        import os

        # 優先從 Header 取得
        api_key = request.headers.get('X-API-Key')

        # 其次從表單取得（向後相容）
        if not api_key:
            api_key = request.form.get('api_key')

        # 最後從環境變數取得
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            return jsonify({
                'error': '請提供 API Key（透過 X-API-Key Header 或環境變數 GEMINI_API_KEY）'
            }), 401

        # 將 API Key 存入 request context
        request.api_key = api_key
        return f(*args, **kwargs)
    return decorated
