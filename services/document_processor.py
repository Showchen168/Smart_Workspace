"""
文件處理服務
負責文件解析、AI 分析、知識庫合併
"""
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable

from parsers import WordParser, PPTParser
from analyzer import PhraseExtractor
from knowledge_base import KnowledgeBaseMerger, DifyFormatter
import config

# 全域執行緒池
_executor: ThreadPoolExecutor | None = None


def get_executor(max_workers: int = 4) -> ThreadPoolExecutor:
    """取得或建立執行緒池"""
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=max_workers)
    return _executor


def shutdown_executor(wait: bool = True) -> None:
    """關閉執行緒池"""
    global _executor
    if _executor:
        _executor.shutdown(wait=wait)
        _executor = None


class DocumentProcessor:
    """文件處理器"""

    def __init__(self, task_store, output_folder: str):
        """
        初始化文件處理器

        Args:
            task_store: 任務存儲實例
            output_folder: 輸出資料夾路徑
        """
        self.task_store = task_store
        self.output_folder = output_folder

    def process_async(self, task_id: str, file_path: str, filename: str,
                      mode: str = 'append', api_key: str | None = None,
                      model: str | None = None) -> Future:
        """
        非同步處理文件

        Args:
            task_id: 任務 ID
            file_path: 上傳的文件路徑
            filename: 原始檔名
            mode: new 或 append
            api_key: Gemini API Key
            model: 模型名稱

        Returns:
            Future 物件
        """
        executor = get_executor()
        return executor.submit(
            self._process_document,
            task_id, file_path, filename, mode, api_key, model
        )

    def _process_document(self, task_id: str, file_path: str, filename: str,
                          mode: str = 'append', api_key: str | None = None,
                          model: str | None = None) -> None:
        """
        處理文件的核心邏輯

        Args:
            task_id: 任務 ID
            file_path: 上傳的文件路徑
            filename: 原始檔名
            mode: new 或 append
            api_key: Gemini API Key
            model: 模型名稱
        """
        try:
            # 更新狀態：解析中
            self._update_status(task_id, 'parsing', '正在解析文件...')

            # 步驟 1: 解析文件
            content = self._parse_file(file_path, filename)

            # 更新狀態：分析中
            self._update_status(
                task_id, 'analyzing',
                f'文件解析完成 ({len(content)} 字元)，AI 分析中...'
            )

            # 步驟 2: AI 分析提取
            extractor = PhraseExtractor(api_key=api_key, model=model)
            extracted_content = extractor.extract(content)

            # 更新狀態：合併中
            self._update_status(task_id, 'merging', '正在合併知識庫...')

            # 步驟 3: 處理增量更新
            output_path = os.path.join(self.output_folder, config.OUTPUT_FILENAME)
            merger = KnowledgeBaseMerger(output_path)

            if mode == 'append':
                existing_kb = merger.load_existing()
                if existing_kb:
                    final_content = extractor.merge_with_existing(existing_kb, extracted_content)
                else:
                    final_content = extracted_content
            else:
                final_content = extracted_content

            # 步驟 4: 格式化並儲存
            formatted_content = DifyFormatter.format(final_content)
            merger.save(formatted_content, filename)

            # 更新狀態：完成
            self.task_store.update(task_id, {
                'status': 'completed',
                'message': '處理完成！',
                'output_file': output_path,
                'content_size': len(formatted_content),
                'completed_at': datetime.now().isoformat()
            })

        except Exception as e:
            # 更新狀態：失敗
            self.task_store.update(task_id, {
                'status': 'failed',
                'message': f'錯誤: {str(e)}',
                'error': str(e)
            })

        finally:
            # 清理上傳的檔案
            if os.path.exists(file_path):
                os.remove(file_path)

    def _parse_file(self, file_path: str, filename: str) -> str:
        """解析文件並回傳文字內容"""
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext == '.docx':
            parser = WordParser(file_path)
            parsed = parser.parse()
            return parsed['full_text']
        elif file_ext == '.pptx':
            parser = PPTParser(file_path)
            parsed = parser.parse()
            return parsed['full_text']
        else:
            raise ValueError(f"不支援的檔案格式: {file_ext}")

    def _update_status(self, task_id: str, status: str, message: str) -> None:
        """更新任務狀態"""
        self.task_store.update(task_id, {
            'status': status,
            'message': message
        })
