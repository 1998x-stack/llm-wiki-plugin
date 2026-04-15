# Pi Agent 深度解析（五）：`pi-tui` —— 终端 UI 的差分渲染与无闪烁输出

> **系列导读**：Mario 最初动手写 Pi 的原因之一就是"Claude Code 会闪烁"。`pi-tui` 是 Pi 对终端 UI 工程问题的系统性解答——从渲染模式的选择到 ANSI 输出的同步，每一处都有精确的工程理由。

---

## 一、为什么终端 UI 如此难做好？

所有用过终端 AI 工具的人都经历过：文字闪烁、输出跳动、布局错乱、颜色残留……

根本原因在于**渲染模式的选择**。

### 即时模式（Immediate Mode）—— 大多数终端框架的选择

```
每帧渲染循环：
┌─────────────────────────────┐
│ 1. 清空整个终端屏幕          │
│ 2. 从第一行到最后一行重绘    │
│ 3. 显示结果                 │
└─────────────────────────────┘
```

在低频场景（每秒 1-2 次更新）下完全没问题。

但在 LLM **高速流式输出**场景（每秒 30-60 次更新）下：

```
清空→重绘→清空→重绘→清空→重绘...
   ↑↑↑↑↑↑↑↑↑
   用户肉眼看到的就是「闪烁」
```

这是目前几乎所有终端 AI 工具（Claude Code、Codex、Amp）产生闪烁的根本原因。

---

## 二、pi-tui 的答案：保留模式 + 差分渲染

### 保留模式（Retained Mode）

```
初始化：构建组件树（存储在内存中）

后续每次更新：
┌────────────────────────────────────┐
│ 1. 更新组件树中的相关节点          │
│ 2. 计算新旧组件树的差异（Diff）    │
│ 3. 只向终端输出「变更部分」        │
└────────────────────────────────────┘
```

这类似于前端的 Virtual DOM，但针对终端场景进行了深度优化。

### 差分渲染（Differential Rendering）的工作原理

```
上一帧（已输出到终端）：
行1: "> 帮我写快速排序"
行2: "正在思考..."
行3: ""

新数据到达（LLM 输出了更多文本）：
行1: "> 帮我写快速排序"          ← 未变化，跳过
行2: "好的，我来实现快速排序。"   ← 变化了！
行3: "首先..."                   ← 新增行

差分输出（只向终端发送）：
ESC[2;1H         ← 移动光标到第 2 行第 1 列
ESC[2K           ← 清除当前行
好的，我来实现快速排序。
ESC[3;1H         ← 移动光标到第 3 行
首先...
```

**结果**：即使 LLM 每秒输出 60 次更新，屏幕也**平滑推进**而不是整屏闪烁。

---

## 三、组件树设计

pi-tui 的组件系统与 React 的组件模型相似，但面向终端渲染：

```typescript
// 组件的核心接口
interface TuiComponent {
  // 渲染此组件（返回终端行的数组）
  render(width: number): TerminalLine[];

  // 处理键盘输入
  handleInput?(key: KeyEvent): void;

  // 子组件列表（组件树）
  children?: TuiComponent[];
}
```

### 内置核心组件

```
TuiRoot（根容器）
├── StatusBar（状态栏）
│   ├── ModelName（模型名称）
│   ├── TokenCounter（token 计数）
│   └── [扩展注入的自定义项]
├── ChatView（聊天视图）
│   ├── UserMessage（用户消息）
│   ├── AssistantMessage（助手消息）
│   │   ├── ThinkingBlock（思维链，可折叠）
│   │   ├── TextBlock（Markdown 文本）
│   │   └── ToolCallBlock（工具调用）
│   │       ├── ToolCallHeader（工具名 + 参数）
│   │       ├── ToolProgress（执行进度）
│   │       └── ToolResult（执行结果）
│   └── ...（历史消息）
├── InputEditor（多行输入编辑器）
└── [扩展注入的 Overlay 组件]
```

---

## 四、核心组件详解

### 4.1 流式 Markdown 渲染

这是 pi-tui 技术含量最高的组件之一。LLM 流式输出 Markdown 时，文本是逐字节到达的，但 Markdown 的语义是**基于完整结构**的（比如代码块需要知道完整内容才能做语法高亮）。

pi-tui 的解决方案：**增量 Markdown 解析 + 保守渲染策略**

```
流式输入（逐字到达）：          渲染结果：

"这是一个"                     这是一个
"这是一个**重要"               这是一个**重要（原始文本，等待闭合）
"这是一个**重要**"             这是一个重要（加粗）
"这是一个**重要**的例子\n```"  这是一个重要的例子（代码块开始）
"typescript\n"                 ┌─────────────────┐
"const x = 1"                  │ const x = 1     │（开始着色）
"const x = 1\n```"             │ const x = 1     │（代码块完整）
                               └─────────────────┘
```

对于未闭合的 Markdown 元素，采用**原始文本显示**策略，完成后再转换为格式化显示。

**支持的 Markdown 元素：**

| 元素 | 终端渲染 |
|------|---------|
| `**bold**` | 粗体（ANSI Bold） |
| `*italic*` | 斜体（ANSI Italic，部分终端支持） |
| `` `code` `` | 等宽字体 + 背景色 |
| `# H1 H2 H3` | 粗体 + 不同颜色 |
| `- 列表项` | 缩进 + `•` 符号 |
| `> 引用` | 竖线 + 灰色文字 |
| 表格 | 对齐的 ASCII 框线 |
| ```` ```lang ``` ```` | 语法高亮 + 带边框代码块 |
| `[链接](url)` | 下划线 + OSC 8 超链接（支持的终端可点击） |

### 4.2 多行编辑器（带智能自动补全）

```
╔══════════════════════════════════════════════════╗
║ > 帮我优化 @src/utils/                            ║
║   ┌────────────────────────────────────────────┐ ║
║   │ ▶ src/utils/sort.ts         (TypeScript)   │ ║
║   │   src/utils/api.ts          (TypeScript)   │ ║
║   │   src/utils/helpers.ts      (TypeScript)   │ ║
║   │   src/utils/__tests__/      (Directory)    │ ║
║   └────────────────────────────────────────────┘ ║
║   Tab 补全 · ↑↓ 选择 · Esc 取消                  ║
╚══════════════════════════════════════════════════╝
```

**编辑器特性：**

- `@` 触发文件路径模糊搜索，遵守 `.gitignore` 规则
- `Tab` 补全路径（类 shell 体验）
- `↑↓` 浏览历史命令（类 shell 体验）
- 多行输入：`Shift+Enter` 换行
- 大段文本粘贴：自动折叠为预览，确认后展开
- 文件拖放：终端支持时直接拖入文件路径

### 4.3 工具执行可视化

```
┌─ 工具调用 ──────────────────────────────────────────┐
│ ⚙ bash                                              │
│ $ npm test -- --coverage src/sort.test.ts           │
│                                                     │
│ ⠹ 执行中...                         [12.3s] [中断]  │
│                                                     │
│ PASS src/sort.test.ts                               │
│ ✓ quickSort sorts empty array (2ms)                 │
│ ✓ quickSort sorts single element (1ms)              │
│ ✓ quickSort sorts numbers ascending (3ms)           │
│                                                     │
│ Coverage: 94.7% statements | 91.2% branches         │
└────────────────────────────────────────────────────-┘
```

bash 命令的**实时输出流**（通过 `onUpdate` 回调）会在工具执行过程中**逐行追加**到这个区域，完成后折叠为摘要。

### 4.4 思维链可视化（Thinking Block）

```
┌─ 思维过程 ─────────────────────────────────── [折叠] ┐
│ 用户想要一个快速排序实现。让我想想最佳的 TypeScript  │
│ 写法...                                              │
│                                                     │
│ 1. 使用泛型 T extends Comparable                    │
│ 2. 原地排序 vs 返回新数组——用户没有指定，我选择...   │
│ ...                                                 │
└─────────────────────────────────────────────────────┘
```

思维链默认**折叠显示**（显示前几行 + "展开" 按钮），避免大量推理内容淹没实际输出。

### 4.5 状态栏（可扩展）

```
┌─────────────────────────────────────────────────────┐
│ claude-sonnet-4-5  │  ↑1.2k ↓487  │  $0.0023  │ ●  │
└─────────────────────────────────────────────────────┘
   ↑模型名称           ↑Token用量    ↑成本估算   ↑状态指示
```

扩展可以向状态栏注入自定义项目（如 git branch、测试覆盖率、API 延迟等）。

---

## 五、同步批量 ANSI 输出——消除另一种闪烁

差分渲染解决了「重绘整屏」导致的闪烁，但还有另一种闪烁来源：**ANSI 控制序列是有状态的**。

```
# 错误的做法：逐字节发送 ANSI 序列
write(ESC)          ← 终端处于"等待序列"状态
write([)            ← 终端处于"等待序列"状态
write(3)            ← 终端处于"等待序列"状态
write(1)            ← 终端处于"等待序列"状态
write(m)            ← 终端完成解析：开启粗体

# 如果在 write([) 和 write(m) 之间有别的内容...
# 终端会把中间的字符误认为是 ANSI 参数，产生混乱
```

pi-tui 的解决方案：**一帧所有的 ANSI 序列先积累在缓冲区，最后一次性 flush**：

```typescript
class TuiRenderer {
  private buffer: string[] = [];

  // 所有渲染操作写入缓冲区
  moveCursor(row: number, col: number) {
    this.buffer.push(`\x1B[${row};${col}H`);
  }

  clearLine() {
    this.buffer.push('\x1B[2K');
  }

  write(text: string) {
    this.buffer.push(text);
  }

  // 帧结束时一次性输出
  flush() {
    process.stdout.write(this.buffer.join(''));
    this.buffer = [];
  }
}
```

**结果**：从终端操作系统的角度看，每一帧的所有更新是**原子的**——要么全部到达，要么全部没到达，不会出现中间状态。

---

## 六、中断恢复：Ctrl+C 后的状态清理

```typescript
process.on('SIGINT', () => {
  // 1. 中止 LLM 请求（通过 AbortController）
  controller.abort();

  // 2. 等待工具执行完成（或强制终止）
  await session.interrupt();

  // 3. 重置终端状态
  renderer.resetTerminal();
  // ESC[0m  ← 重置所有文字属性（颜色、粗体等）
  // ESC[?25h ← 显示光标（防止光标被隐藏后卡死）
  // ESC[?1049l ← 退出备用屏幕（如果使用了）
  // \n ← 确保提示符从新行开始

  process.exit(0);
});
```

---

## 七、主题系统

pi-tui 支持完整的主题定制：

```typescript
// 内置主题
const themes = {
  default: { primary: '#7c6af7', accent: '#4CAF50', ... },
  dracula: { primary: '#bd93f9', accent: '#50fa7b', ... },
  nord:    { primary: '#88c0d0', accent: '#a3be8c', ... },
  tokyo:   { primary: '#7aa2f7', accent: '#9ece6a', ... },
};

// 自定义主题（通过扩展）
const myTheme: Theme = {
  name: 'my-theme',
  colors: {
    primary:    '#ff6b6b',
    secondary:  '#4ecdc4',
    accent:     '#45b7d1',
    background: 'transparent',
    text:       '#ffffff',
    dimText:    '#888888',
    success:    '#51cf66',
    warning:    '#fcc419',
    error:      '#ff6b6b',
    toolName:   '#74c0fc',
    userMsg:    '#b2f2bb',
    assistMsg:  '#d0ebff',
  },
  symbols: {
    spinner: ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'],
    success: '✓',
    error:   '✗',
    tool:    '⚙',
    user:    '>',
    assist:  '◆',
    think:   '💭',
  }
};
```

---

## 八、与其他 TUI 框架对比

| 特性 | Ink（React for CLI） | Blessed | Textual（Python） | pi-tui |
|------|--------------------|---------|--------------------|--------|
| 渲染模式 | 即时模式 | 即时模式 | 保留模式 | **保留模式** |
| 差分渲染 | 有，但基于全树 | 部分 | 有 | **行级精确差分** |
| LLM 流式优化 | 否 | 否 | 否 | **原生集成** |
| TypeScript 原生 | 是 | 否 | 否 | **是** |
| Agent 事件集成 | 否 | 否 | 否 | **原生集成** |
| 批量 ANSI 输出 | 否 | 否 | 是 | **是** |
| 可作为 SDK 使用 | 是 | 是 | 否 | **是** |

---

## 九、pi-tui 是可选的

这一点值得单独强调：**pi-tui 不是 pi-agent-core 的依赖**。

```
pi-agent-core 发出事件
    │
    ├── 如果你用 pi-tui：       事件 → TUI 渲染
    ├── 如果你用 pi-web-ui：    事件 → React 组件更新
    ├── 如果你用 OpenClaw：     事件 → IM 平台消息
    └── 如果你自己实现：        事件 → 任何你想要的输出
```

pi-tui 只是 Pi 提供的**参考终端 UI 实现**。整个框架的事件驱动设计确保了 UI 层可以被任意替换。

---

*下一篇（终章）：扩展系统 —— 用 TypeScript 把 Pi 变成你想要的任何东西*
