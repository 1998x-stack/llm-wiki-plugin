# 交互 Spec 文档规范

用于定义 UI 交互行为，支持：

- AI 根据 spec 生成测试用例
- 浏览器自动化验证（Playwright/Puppeteer）
- 对比实际行为和预期
- 测试/CI 复用

## Spec 格式

使用 YAML 代码块定义，格式如下：

```yaml
feature: 功能名称
description: 功能描述（可选）

# 前置条件
preconditions:
  - auth: logged_in # 登录状态：logged_in | logged_out | any
  - route: /chat/:chatId # 当前路由
  - state: # 应用状态（可选）
      hasApp: true
      hasChat: true

# 测试场景列表
scenarios:
  - name: 场景名称
    description: 场景描述（可选）

    # 执行步骤
    steps:
      - action: click | type | upload | wait | scroll | hover | press
        target: CSS 选择器 | 描述性文本
        value: 输入值（type/upload 时需要）
        options: # 可选参数
          timeout: 5000
          force: true

    # 预期结果
    expect:
      - type: visible | hidden | text | count | url | toast | network
        target: CSS 选择器 | 描述
        value: 预期值
        within: 5000 # 超时时间（毫秒）
```

## Action 类型

| Action     | 描述     | target     | value                   |
| ---------- | -------- | ---------- | ----------------------- |
| `click`    | 点击元素 | CSS 选择器 | -                       |
| `type`     | 输入文本 | CSS 选择器 | 输入内容                |
| `upload`   | 上传文件 | CSS 选择器 | 文件路径或 mock 数据    |
| `wait`     | 等待     | -          | 毫秒数                  |
| `scroll`   | 滚动     | CSS 选择器 | top/bottom/数值         |
| `hover`    | 悬停     | CSS 选择器 | -                       |
| `press`    | 按键     | -          | 键名（Enter/Escape 等） |
| `navigate` | 导航     | -          | URL                     |

## Expect 类型

| Type      | 描述       | target     | value                |
| --------- | ---------- | ---------- | -------------------- |
| `visible` | 元素可见   | CSS 选择器 | -                    |
| `hidden`  | 元素不可见 | CSS 选择器 | -                    |
| `text`    | 文本内容   | CSS 选择器 | 预期文本（支持正则） |
| `count`   | 元素数量   | CSS 选择器 | 数量                 |
| `url`     | 当前 URL   | -          | URL 或正则           |
| `toast`   | Toast 消息 | -          | 消息文本             |
| `network` | 网络请求   | URL 模式   | 状态码/响应          |
| `state`   | 应用状态   | 状态路径   | 预期值               |

---

## 示例：文档上传功能

```yaml
feature: 文档上传
description: 用户可以上传文档到项目

preconditions:
  - auth: logged_in
  - route: /chat/:chatId
  - state:
      hasApp: true

scenarios:
  # 正常上传
  - name: 上传单个文档成功
    steps:
      - action: click
        target: "[data-testid='doc-upload-btn']"
      - action: upload
        target: "input[type='file']"
        value:
          name: "test.md"
          content: "# Test Document"
          size: 1024
    expect:
      - type: toast
        value: "上传成功"
        within: 5000
      - type: visible
        target: "[data-testid='doc-list'] >> text=test.md"

  # 文件过大
  - name: 上传超大文件被拒绝
    steps:
      - action: click
        target: "[data-testid='doc-upload-btn']"
      - action: upload
        target: "input[type='file']"
        value:
          name: "large.pdf"
          size: 20971520 # 20MB
    expect:
      - type: toast
        value: /超过.*限制/
      - type: hidden
        target: "[data-testid='upload-progress']"

  # 多文件上传
  - name: 批量上传多个文档
    steps:
      - action: click
        target: "[data-testid='doc-upload-btn']"
      - action: upload
        target: "input[type='file']"
        value:
          - { name: "doc1.md", size: 1024 }
          - { name: "doc2.txt", size: 2048 }
    expect:
      - type: count
        target: "[data-testid='doc-item']"
        value: 2
```

---

## 示例：消息发送功能

```yaml
feature: 消息发送
description: 用户在聊天窗口发送消息

preconditions:
  - auth: logged_in
  - route: /chat/:chatId
  - state:
      sessionConnected: true

scenarios:
  - name: 发送普通文本消息
    steps:
      - action: type
        target: "[data-testid='chat-input']"
        value: "你好，请帮我创建一个按钮"
      - action: click
        target: "[data-testid='send-btn']"
    expect:
      - type: visible
        target: ".message-user >> text=你好"
      - type: visible
        target: "[data-testid='thinking-indicator']"
        within: 2000
      - type: network
        target: "POST /api/v1/chat/*/message"
        value:
          status: 200

  - name: 发送空消息被阻止
    steps:
      - action: click
        target: "[data-testid='send-btn']"
    expect:
      - type: hidden
        target: "[data-testid='thinking-indicator']"
      - type: text
        target: "[data-testid='send-btn']"
        value: "发送" # 按钮状态未改变

  - name: 超长消息被截断提示
    steps:
      - action: type
        target: "[data-testid='chat-input']"
        value: "{{ repeat('a', 50001) }}" # 超过 MAX_PROMPT_LENGTH
    expect:
      - type: visible
        target: "[data-testid='length-warning']"
      - type: text
        target: "[data-testid='char-count']"
        value: /50001.*50000/
```

---

## AI 使用指南

### 生成测试用例

AI 可以根据 spec 自动生成 Playwright 测试代码：

```typescript
// 由 AI 根据上述 spec 生成
import { test, expect } from "@playwright/test";

test("上传单个文档成功", async ({ page }) => {
  // preconditions
  await page.goto("/chat/test-chat-id");

  // steps
  await page.click('[data-testid="doc-upload-btn"]');
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: "test.md",
    mimeType: "text/markdown",
    buffer: Buffer.from("# Test Document"),
  });

  // expect
  await expect(page.locator(".toast")).toContainText("上传成功", { timeout: 5000 });
  await expect(page.locator('[data-testid="doc-list"]')).toContainText("test.md");
});
```

### 浏览器验证

AI 可以在浏览器中逐条执行 spec 并报告结果：

```
[✓] 上传单个文档成功
    [✓] click: [data-testid='doc-upload-btn']
    [✓] upload: input[type='file'] → test.md
    [✓] expect: toast "上传成功"
    [✓] expect: visible "test.md"

[✗] 上传超大文件被拒绝
    [✓] click: [data-testid='doc-upload-btn']
    [✓] upload: input[type='file'] → large.pdf (20MB)
    [✗] expect: toast /超过.*限制/
        实际: "网络错误"
        预期: 匹配 /超过.*限制/
```

---

## 命名约定

- `data-testid`: 测试专用属性，命名格式 `feature-element`
- 场景名称：动词开头，描述用户行为和结果
- 使用 `>>` 链接嵌套选择器

## 文件组织

```
docs/
├── interaction-spec.md          # 本文档
└── specs/
    ├── document-upload.spec.yaml
    ├── message-send.spec.yaml
    └── publish-flow.spec.yaml
```
