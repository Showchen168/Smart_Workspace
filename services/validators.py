"""
請求驗證模組
使用 Pydantic 進行輸入驗證
"""
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class UploadRequest(BaseModel):
    """上傳請求驗證"""
    mode: Literal['new', 'append'] = Field(default='append', description='處理模式')
    model: str = Field(default='gemini-2.5-flash-lite', description='AI 模型名稱')

    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        allowed_models = [
            'gemini-2.5-flash-lite',
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
        ]
        if v not in allowed_models:
            raise ValueError(f'不支援的模型: {v}，允許的模型: {allowed_models}')
        return v


class TaskResponse(BaseModel):
    """任務回應格式"""
    task_id: str
    filename: str
    status: str
    message: str
    created_at: str
    completed_at: str | None = None
    output_file: str | None = None
    content_size: int | None = None
    error: str | None = None


class TaskListItem(BaseModel):
    """任務列表項目"""
    task_id: str
    filename: str
    status: str
    created_at: str


class PreviewResponse(BaseModel):
    """預覽回應格式"""
    content: str
    truncated: bool
