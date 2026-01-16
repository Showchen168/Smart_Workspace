# 📐 開發規範 Skill

## 【用途】
定義專案的程式碼風格、Git 工作流程和開發標準。

---

## 【程式碼風格】

### Python
```python
# ✅ 好的範例

# 1. 使用有意義的命名
def calculate_total_price(items: list[dict]) -> float:
    """計算商品總價"""
    return sum(item['price'] * item['quantity'] for item in items)

# 2. 使用 Type Hints
def get_user_by_id(user_id: int) -> User | None:
    pass

# 3. 使用 docstring
def process_data(data: dict) -> dict:
    """
    處理輸入資料並返回結果。

    Args:
        data: 包含原始資料的字典

    Returns:
        處理後的資料字典

    Raises:
        ValueError: 當資料格式不正確時
    """
    pass

# 4. 常數使用大寫
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 5. 類別命名使用 PascalCase
class UserService:
    pass
```

### JavaScript/TypeScript
```typescript
// ✅ 好的範例

// 1. 使用 const 和 let
const MAX_ITEMS = 100;
let currentPage = 1;

// 2. 使用箭頭函數
const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

// 3. 使用解構
const { name, email } = user;

// 4. 使用 async/await
const fetchUser = async (id: number): Promise<User> => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
};

// 5. 使用 TypeScript 嚴格類型
interface User {
  id: number;
  name: string;
  email: string;
}
```

---

## 【Git 工作流程】

### 分支命名規範
```
main                    # 主分支，永遠是穩定版本
├── develop             # 開發分支
├── feature/[功能名稱]   # 功能分支
├── bugfix/[問題描述]    # Bug 修復分支
├── hotfix/[緊急修復]    # 緊急修復分支
└── release/[版本號]     # 發布分支
```

### 分支命名範例
```
feature/user-authentication
feature/add-payment-gateway
bugfix/fix-login-error
hotfix/security-patch
release/v1.2.0
```

### Commit 訊息規範
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 類型
| Type | 說明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修復 |
| docs | 文檔更新 |
| style | 格式調整（不影響程式碼邏輯） |
| refactor | 重構（不是新功能或 Bug 修復） |
| perf | 效能優化 |
| test | 測試相關 |
| chore | 維護性工作 |
| ci | CI/CD 相關 |
| build | 建置相關 |

#### Commit 範例
```
feat(auth): 新增 Google OAuth 登入功能

- 實作 Google OAuth 2.0 流程
- 新增登入按鈕到首頁
- 處理 callback 和 token 儲存

Closes #123
```

```
fix(api): 修復使用者查詢 N+1 問題

使用 eager loading 優化查詢效能，
回應時間從 2s 降低到 200ms

Fixes #456
```

---

## 【Pull Request 規範】

### PR 標題格式
```
[TYPE] 簡短描述
```

### PR 模板
```markdown
## 📋 變更說明
[描述這個 PR 做了什麼]

## 🎯 相關 Issue
- Closes #[issue number]

## 📝 變更類型
- [ ] 新功能 (feat)
- [ ] Bug 修復 (fix)
- [ ] 文檔更新 (docs)
- [ ] 重構 (refactor)
- [ ] 效能優化 (perf)
- [ ] 測試 (test)
- [ ] 維護 (chore)

## ✅ 檢查清單
- [ ] 程式碼符合專案風格指南
- [ ] 已新增/更新測試
- [ ] 所有測試通過
- [ ] 已更新相關文檔
- [ ] 已自我 Code Review

## 📸 截圖（如適用）
[UI 變更截圖]

## 🧪 測試方式
[說明如何測試這個變更]

## 💡 備註
[其他需要 Reviewer 注意的事項]
```

---

## 【目錄結構規範】

### Python 專案
```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── services/
│   ├── routes/
│   └── utils/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── fixtures/
├── docs/
├── scripts/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

### Node.js 專案
```
project/
├── src/
│   ├── index.ts
│   ├── config/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── tests/
├── docs/
├── scripts/
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```

---

## 【命名規範總覽】

| 類型 | 規範 | 範例 |
|------|------|------|
| 變數 | camelCase | `userName`, `totalCount` |
| 常數 | UPPER_SNAKE_CASE | `MAX_SIZE`, `API_URL` |
| 函數 | camelCase / snake_case | `getUser`, `get_user` |
| 類別 | PascalCase | `UserService`, `OrderController` |
| 檔案 | kebab-case / snake_case | `user-service.ts`, `user_service.py` |
| 資料庫表 | snake_case | `user_orders`, `product_categories` |
| API 路徑 | kebab-case | `/api/user-orders` |

---

## 【版本號規範】

使用語意化版本 (Semantic Versioning)：
```
MAJOR.MINOR.PATCH

- MAJOR：不相容的 API 變更
- MINOR：向下相容的功能新增
- PATCH：向下相容的 Bug 修復
```

範例：
- `1.0.0` → `1.0.1`：修復 Bug
- `1.0.1` → `1.1.0`：新增功能
- `1.1.0` → `2.0.0`：重大變更
