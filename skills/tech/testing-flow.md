# 🧪 測試流程 Skill

## 【用途】
定義測試策略、撰寫測試案例和 QA 檢查清單。

---

## 【測試金字塔】

```
        /\
       /  \      E2E Tests (10%)
      /----\     端對端測試
     /      \
    /--------\   Integration Tests (20%)
   /          \  整合測試
  /------------\
 /              \ Unit Tests (70%)
/----------------\ 單元測試
```

---

## 【單元測試規範】

### 命名規範
```
test_[功能]_[情境]_[預期結果]
```

### Python 範例 (pytest)
```python
import pytest
from services.user_service import UserService

class TestUserService:
    """使用者服務測試"""

    def setup_method(self):
        """每個測試前的設定"""
        self.service = UserService()

    # ✅ 正常情境
    def test_create_user_with_valid_data_returns_user(self):
        """測試：使用有效資料建立使用者，應返回使用者物件"""
        # Arrange
        user_data = {"name": "John", "email": "john@example.com"}

        # Act
        result = self.service.create_user(user_data)

        # Assert
        assert result.name == "John"
        assert result.email == "john@example.com"

    # ❌ 錯誤情境
    def test_create_user_with_invalid_email_raises_error(self):
        """測試：使用無效 email 建立使用者，應拋出 ValueError"""
        # Arrange
        user_data = {"name": "John", "email": "invalid-email"}

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.service.create_user(user_data)

        assert "Invalid email" in str(exc_info.value)

    # 🔄 邊界情境
    def test_create_user_with_empty_name_raises_error(self):
        """測試：使用空名稱建立使用者，應拋出 ValueError"""
        user_data = {"name": "", "email": "john@example.com"}

        with pytest.raises(ValueError):
            self.service.create_user(user_data)

    # 🔧 使用 fixture
    @pytest.fixture
    def sample_user(self):
        return {"name": "Test User", "email": "test@example.com"}

    def test_get_user_by_id_returns_correct_user(self, sample_user):
        """測試：根據 ID 取得使用者"""
        created = self.service.create_user(sample_user)
        result = self.service.get_user_by_id(created.id)

        assert result.id == created.id
```

### JavaScript 範例 (Jest)
```javascript
import { UserService } from './user-service';

describe('UserService', () => {
  let service;

  beforeEach(() => {
    service = new UserService();
  });

  describe('createUser', () => {
    // ✅ 正常情境
    it('should create user with valid data', async () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };

      // Act
      const result = await service.createUser(userData);

      // Assert
      expect(result.name).toBe('John');
      expect(result.email).toBe('john@example.com');
    });

    // ❌ 錯誤情境
    it('should throw error with invalid email', async () => {
      const userData = { name: 'John', email: 'invalid-email' };

      await expect(service.createUser(userData))
        .rejects
        .toThrow('Invalid email');
    });
  });
});
```

---

## 【整合測試規範】

### API 測試範例 (Python)
```python
import pytest
from fastapi.testclient import TestClient
from main import app

class TestUserAPI:
    """使用者 API 整合測試"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_create_user_endpoint(self, client):
        """POST /api/users - 建立使用者"""
        response = client.post(
            "/api/users",
            json={"name": "John", "email": "john@example.com"}
        )

        assert response.status_code == 201
        assert response.json()["name"] == "John"

    def test_get_user_endpoint(self, client):
        """GET /api/users/{id} - 取得使用者"""
        # 先建立
        create_response = client.post(
            "/api/users",
            json={"name": "John", "email": "john@example.com"}
        )
        user_id = create_response.json()["id"]

        # 再查詢
        response = client.get(f"/api/users/{user_id}")

        assert response.status_code == 200
        assert response.json()["id"] == user_id

    def test_get_nonexistent_user_returns_404(self, client):
        """GET /api/users/{id} - 查詢不存在的使用者應返回 404"""
        response = client.get("/api/users/99999")

        assert response.status_code == 404
```

---

## 【QA 檢查清單】

### 功能測試
- [ ] 所有使用者故事的功能都已實作
- [ ] 正常流程可以正確執行
- [ ] 錯誤訊息清楚且有幫助
- [ ] 表單驗證正確運作
- [ ] 按鈕和連結都能正常點擊

### 邊界測試
- [ ] 空值輸入的處理
- [ ] 最大/最小值的處理
- [ ] 特殊字元的處理
- [ ] 超長文字的處理
- [ ] 並發請求的處理

### 效能測試
- [ ] 頁面載入時間 < 3 秒
- [ ] API 回應時間 < 500ms
- [ ] 大量資料的處理效能
- [ ] 記憶體使用合理

### 安全測試
- [ ] 輸入驗證（防止 SQL Injection）
- [ ] XSS 防護
- [ ] CSRF 防護
- [ ] 權限控制正確
- [ ] 敏感資料加密

### 相容性測試
- [ ] Chrome 最新版
- [ ] Firefox 最新版
- [ ] Safari 最新版
- [ ] Edge 最新版
- [ ] 行動裝置（iOS/Android）

### 無障礙測試
- [ ] 鍵盤可操作
- [ ] 螢幕閱讀器相容
- [ ] 顏色對比度足夠
- [ ] 圖片有 alt 文字

---

## 【測試報告格式】

```markdown
# 🧪 測試報告

## 📊 測試摘要
| 項目 | 數量 |
|------|------|
| 總測試數 | XX |
| 通過 | XX |
| 失敗 | XX |
| 跳過 | XX |
| 覆蓋率 | XX% |

## ✅ 通過的測試
[列出通過的測試]

## ❌ 失敗的測試

### 測試名稱：[名稱]
**檔案**：`tests/test_xxx.py`
**錯誤訊息**：
```
[錯誤訊息]
```
**預期**：[預期結果]
**實際**：[實際結果]
**分析**：[失敗原因分析]

## 📈 覆蓋率報告
| 模組 | 覆蓋率 |
|------|--------|
| services/ | XX% |
| models/ | XX% |
| routes/ | XX% |

## 💡 建議
[改進建議]
```

---

## 【測試執行指令】

### Python (pytest)
```bash
# 執行所有測試
pytest

# 執行特定檔案
pytest tests/test_user.py

# 顯示詳細輸出
pytest -v

# 顯示覆蓋率
pytest --cov=src

# 生成 HTML 覆蓋率報告
pytest --cov=src --cov-report=html
```

### JavaScript (Jest)
```bash
# 執行所有測試
npm test

# 監視模式
npm test -- --watch

# 顯示覆蓋率
npm test -- --coverage

# 執行特定檔案
npm test -- user.test.js
```
