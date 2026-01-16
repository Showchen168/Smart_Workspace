// ==========================================
// 智能工作台 - 主要 JavaScript
// ==========================================

// 全域變數
let currentTaskId = null;
let pollInterval = null;

// LocalStorage Key
const STORAGE_KEY = '_smart_workspace_config';

// ==========================================
// 初始化
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initTabNavigation();
    initSettingsPanel();
    initKnowledgeExtractor();
    initModeSelection();
    loadSavedSettings();
});

// ==========================================
// 分頁導航功能
// ==========================================
function initTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;

            // 移除所有 active 狀態
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // 設定選中的 tab
            btn.classList.add('active');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }

            // 延遲載入 iframe（切換到分頁時才載入）
            loadIframeForTab(targetTab);
        });
    });
}

// 延遲載入 iframe
function loadIframeForTab(tabId) {
    const iframeConfig = {
        'job-management': {
            id: 'jobManagementFrame',
            src: 'https://showchen168.github.io/Job-Management-System/'
        },
        'resignation-system': {
            id: 'resignationSystemFrame',
            src: 'https://showchen168.github.io/resignation-system/#admin-panel'
        },
        'ai-assistant': {
            id: 'aiAssistantFrame',
            src: 'https://udify.app/chat/GoS7U3xM4JmHgGEw'
        }
    };

    const config = iframeConfig[tabId];
    if (config) {
        const iframe = document.getElementById(config.id);
        if (iframe && !iframe.src) {
            iframe.src = config.src;
        }
    }
}

// ==========================================
// 設定面板功能
// ==========================================
function initSettingsPanel() {
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsPanel = document.getElementById('settingsPanel');
    const settingsOverlay = document.getElementById('settingsOverlay');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');

    // 開啟設定面板
    settingsBtn?.addEventListener('click', () => {
        settingsPanel?.classList.add('active');
        settingsOverlay?.classList.add('active');
    });

    // 關閉設定面板
    const closePanel = () => {
        settingsPanel?.classList.remove('active');
        settingsOverlay?.classList.remove('active');
    };

    closeSettingsBtn?.addEventListener('click', closePanel);
    settingsOverlay?.addEventListener('click', closePanel);

    // 儲存設定
    saveSettingsBtn?.addEventListener('click', saveSettings);
}

// 載入已儲存的設定
function loadSavedSettings() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            const config = JSON.parse(atob(saved));
            const modelSelect = document.getElementById('modelSelect');

            if (config.m && modelSelect) {
                modelSelect.value = config.m;
            }
        }
    } catch (e) {
        console.log('無法載入設定');
    }
}

// 儲存設定
function saveSettings() {
    const modelSelect = document.getElementById('modelSelect');
    const model = modelSelect ? modelSelect.value : 'gemini-2.5-flash-lite';

    try {
        const config = { m: model };
        localStorage.setItem(STORAGE_KEY, btoa(JSON.stringify(config)));
        showToast('設定已儲存', 'success');

        // 關閉面板
        document.getElementById('settingsPanel')?.classList.remove('active');
        document.getElementById('settingsOverlay')?.classList.remove('active');
    } catch (e) {
        showToast('儲存失敗', 'error');
    }
}

// ==========================================
// 模式選擇功能
// ==========================================
function initModeSelection() {
    const modeCards = document.querySelectorAll('.mode-card');

    modeCards.forEach(card => {
        card.addEventListener('click', () => {
            // 移除所有 active
            modeCards.forEach(c => c.classList.remove('active'));
            // 設定當前為 active
            card.classList.add('active');
            // 選中 radio
            const radio = card.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
            }
        });
    });
}

// ==========================================
// 知識提取器功能
// ==========================================
function initKnowledgeExtractor() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');

    if (!uploadArea || !fileInput || !uploadBtn) {
        return;
    }

    // 點擊上傳按鈕
    uploadBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // 檔案選擇
    fileInput.addEventListener('change', handleFileSelect);

    // 拖曳上傳
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // 點擊上傳區域
    uploadArea.addEventListener('click', (e) => {
        if (e.target !== uploadBtn && !uploadBtn.contains(e.target)) {
            fileInput.click();
        }
    });

    // 其他按鈕
    document.getElementById('downloadBtn')?.addEventListener('click', downloadResult);
    document.getElementById('previewBtn')?.addEventListener('click', previewResult);
    document.getElementById('closePreviewBtn')?.addEventListener('click', () => {
        document.getElementById('previewSection').style.display = 'none';
    });
    document.getElementById('newTaskBtn')?.addEventListener('click', resetUI);
}

// 處理檔案選擇
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// 處理檔案
function handleFile(file) {
    const allowedExtensions = ['.docx', '.pptx'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        showToast('不支援的檔案格式，請上傳 .docx 或 .pptx', 'error');
        return;
    }

    if (file.size > 50 * 1024 * 1024) {
        showToast('檔案大小超過 50MB 限制', 'error');
        return;
    }

    uploadFile(file);
}

// 上傳檔案
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    // 取得選擇的模式
    const modeInput = document.querySelector('input[name="mode"]:checked');
    const mode = modeInput ? modeInput.value : 'append';
    formData.append('mode', mode);

    // 取得選擇的模型
    const modelSelect = document.getElementById('modelSelect');
    const model = modelSelect ? modelSelect.value : 'gemini-2.5-flash-lite';
    formData.append('model', model);

    try {
        showToast('正在上傳檔案...', 'info');

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showToast('檔案上傳成功，開始處理', 'success');
            currentTaskId = result.task_id;
            showProgressSection(file.name);
            startPolling();
        } else {
            showToast(result.error || '上傳失敗', 'error');
        }
    } catch (error) {
        showToast('網路錯誤: ' + error.message, 'error');
    }
}

// 顯示進度區域
function showProgressSection(filename) {
    const uploadSection = document.querySelector('.upload-section');
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');
    const previewSection = document.getElementById('previewSection');

    if (uploadSection) uploadSection.style.display = 'none';
    if (resultSection) resultSection.style.display = 'none';
    if (previewSection) previewSection.style.display = 'none';

    if (progressSection) {
        progressSection.style.display = 'block';

        const filenameEl = document.getElementById('progressFilename');
        const statusEl = document.getElementById('progressStatus');
        const messageEl = document.getElementById('progressMessage');
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');

        if (filenameEl) filenameEl.textContent = filename;
        if (statusEl) {
            statusEl.textContent = '排隊中';
            statusEl.className = 'status-badge status-queued';
        }
        if (messageEl) messageEl.textContent = '等待處理...';
        if (progressBar) progressBar.style.width = '5%';
        if (progressPercent) progressPercent.textContent = '5%';

        // 重置步驟狀態
        document.querySelectorAll('.progress-steps .step').forEach(step => {
            step.classList.remove('active', 'completed');
        });
    }
}

// 開始輪詢狀態
function startPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
    }
    pollInterval = setInterval(checkTaskStatus, 2000);
}

// 檢查任務狀態
async function checkTaskStatus() {
    if (!currentTaskId) return;

    try {
        const response = await fetch(`/api/status/${currentTaskId}`);
        const task = await response.json();

        if (response.ok) {
            updateProgress(task);

            if (task.status === 'completed' || task.status === 'failed') {
                clearInterval(pollInterval);

                if (task.status === 'completed') {
                    showResult(task);
                } else {
                    showToast('處理失敗: ' + task.message, 'error');
                }
            }
        }
    } catch (error) {
        console.error('狀態查詢錯誤:', error);
    }
}

// 更新進度顯示
function updateProgress(task) {
    const statusElement = document.getElementById('progressStatus');
    const messageElement = document.getElementById('progressMessage');
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');

    const statusMap = {
        'queued': { text: '排隊中', progress: 5 },
        'parsing': { text: '解析中', progress: 25 },
        'analyzing': { text: 'AI 分析中', progress: 55 },
        'merging': { text: '合併中', progress: 85 },
        'completed': { text: '完成', progress: 100 },
        'failed': { text: '失敗', progress: 0 }
    };

    const statusInfo = statusMap[task.status] || { text: task.status, progress: 0 };

    if (statusElement) {
        statusElement.textContent = statusInfo.text;
        statusElement.className = 'status-badge status-' + task.status;
    }

    if (messageElement) {
        messageElement.textContent = task.message;
    }

    if (progressBar) {
        progressBar.style.width = statusInfo.progress + '%';
    }

    if (progressPercent) {
        progressPercent.textContent = statusInfo.progress + '%';
    }

    // 更新步驟狀態
    updateStepStatus(task.status);
}

// 更新步驟狀態
function updateStepStatus(currentStatus) {
    const steps = ['parsing', 'analyzing', 'merging', 'completed'];
    const currentIndex = steps.indexOf(currentStatus);

    steps.forEach((step, index) => {
        const stepEl = document.querySelector(`.step[data-step="${step}"]`);
        if (!stepEl) return;

        stepEl.classList.remove('active', 'completed');

        if (index < currentIndex) {
            stepEl.classList.add('completed');
        } else if (index === currentIndex) {
            stepEl.classList.add('active');
        }
    });
}

// 顯示結果
function showResult(task) {
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');

    if (progressSection) progressSection.style.display = 'none';

    if (resultSection) {
        resultSection.style.display = 'block';

        const resultSize = document.getElementById('resultSize');
        const resultTime = document.getElementById('resultTime');

        if (resultSize) {
            resultSize.textContent = task.content_size ? task.content_size.toLocaleString() : '-';
        }

        if (resultTime && task.completed_at) {
            const date = new Date(task.completed_at);
            resultTime.textContent = date.toLocaleString('zh-TW');
        }
    }

    showToast('知識庫生成完成', 'success');
}

// 下載結果
async function downloadResult() {
    if (!currentTaskId) return;

    try {
        window.location.href = `/api/download/${currentTaskId}`;
        showToast('開始下載...', 'success');
    } catch (error) {
        showToast('下載失敗: ' + error.message, 'error');
    }
}

// 預覽結果
async function previewResult() {
    if (!currentTaskId) return;

    try {
        const response = await fetch(`/api/preview/${currentTaskId}`);
        const result = await response.json();

        if (response.ok) {
            const previewSection = document.getElementById('previewSection');
            const previewContent = document.getElementById('previewContent');

            if (previewSection && previewContent) {
                previewSection.style.display = 'block';
                previewContent.textContent = result.content;

                if (result.truncated) {
                    showToast('內容過長，僅顯示前 10000 字元', 'info');
                }

                previewSection.scrollIntoView({ behavior: 'smooth' });
            }
        } else {
            showToast(result.error || '預覽失敗', 'error');
        }
    } catch (error) {
        showToast('預覽失敗: ' + error.message, 'error');
    }
}

// 重置 UI
function resetUI() {
    const fileInput = document.getElementById('fileInput');
    const uploadSection = document.querySelector('.upload-section');
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');
    const previewSection = document.getElementById('previewSection');

    if (fileInput) fileInput.value = '';
    if (uploadSection) uploadSection.style.display = 'block';
    if (progressSection) progressSection.style.display = 'none';
    if (resultSection) resultSection.style.display = 'none';
    if (previewSection) previewSection.style.display = 'none';

    currentTaskId = null;

    if (pollInterval) {
        clearInterval(pollInterval);
    }
}

// ==========================================
// Toast 提示系統
// ==========================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas ${icons[type] || icons.info}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    // 自動移除
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}
