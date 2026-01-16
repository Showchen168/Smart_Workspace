"""
任務管理路由
"""
from flask import Blueprint, jsonify, current_app

from .decorators import require_task

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/api/status/<task_id>', methods=['GET'])
@require_task
def get_task_status(task_id: str, task: dict):
    """
    查詢任務狀態 API

    Args:
        task_id: 任務 ID

    Returns:
        任務狀態資訊
    """
    return jsonify(task), 200


@tasks_bp.route('/api/tasks', methods=['GET'])
def list_tasks():
    """
    列出所有任務 API

    Returns:
        tasks: 任務列表
    """
    task_store = current_app.config['TASK_STORE']
    all_tasks = task_store.get_all()

    tasks = [
        {
            'task_id': task['task_id'],
            'filename': task['filename'],
            'status': task['status'],
            'created_at': task['created_at']
        }
        for task in all_tasks
    ]

    # 按建立時間排序
    tasks.sort(key=lambda x: x['created_at'], reverse=True)

    return jsonify({'tasks': tasks}), 200
