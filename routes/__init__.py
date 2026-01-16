"""
路由模組
"""
from .upload import upload_bp
from .tasks import tasks_bp
from .download import download_bp

__all__ = ['upload_bp', 'tasks_bp', 'download_bp']
