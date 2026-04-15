# UI UX Pro Max 深度解析⑤：99 条 UX 准则 + 25 种图表推荐——工程化的设计知识

> **系列第 5 篇**：`ux-guidelines.csv` 和 `charts.csv` 是 UUPM 中最「工程范儿」的两个模块——它们把软性的设计经验转化成了带优先级标签、可机器检索、可自动验证的结构化规则。

---

## 一、99 条 UX 准则：从「感觉对」到「规则可查」

### 1.1 为什么要把 UX 规则结构化？

经验丰富的设计师看到一个 UI 会「感觉」哪里不对——但这种感觉是隐性知识，AI 没法直接理解。

UUPM 的解决方案是：把这些隐性知识编码成 `ux-guidelines.csv`，每条规则都包含：

```
id              → 规则编号（用于引用）
rule_name       → 规则简称（如 hover-state-required）
category        → 分类（交互/可访问性/性能/布局/...）
priority        → P0/P1/P2（P0 = 必须遵守，P2 = 建议）
description     → 详细描述
anti_pattern    → 对应的错误模式
platform        → 适用平台（web/mobile/all）
stack_notes     → 技术栈相关注记
```

### 1.2 按分类的 99 条规则全景

#### 分类一：交互状态（Interaction States）

这类规则解决「元素在不同状态下应该如何表现」：

```
hover-state-required
  P0 | 所有可点击元素必须有 hover 状态
  正确: background 颜色改变 + 150ms 过渡
  错误: 点击按钮无任何视觉反馈

cursor-pointer-required  
  P0 | 所有可点击元素必须设置 cursor: pointer
  注: a 标签自带，但 div/span 作为按钮使用时常被遗忘

pressed-state-feedback
  P1 | 按钮点击瞬间有压下感（scale 0.97 或色彩加深）
  
disabled-state-clarity
  P0 | 禁用状态必须与激活状态有明显视觉区分
  正确: opacity: 0.5 + cursor: not-allowed
  错误: 仅禁用功能但外观不变

state-consistency
  P1 | 同类元素的 hover/pressed/disabled 必须使用同一套规则
  反模式: 有些按钮 hover 变深，有些变浅
```

#### 分类二：可访问性（Accessibility）

```
contrast-minimum
  P0 | 正常文字对比度 ≥ 4.5:1（WCAG AA）
  工具: https://webaim.org/resources/contrastchecker/

focus-visible-required
  P0 | 所有可聚焦元素必须有可见的 focus 状态
  注: 不能用 outline: none 而不提供替代方案

keyboard-navigation
  P0 | 所有操作必须可以纯键盘完成

prefers-reduced-motion
  P1 | 所有动画必须检测 prefers-reduced-motion 并提供静态替代
  CSS: @media (prefers-reduced-motion: reduce) { ... }

alt-text-required
  P0 | 所有图片必须有描述性 alt 文本
  注: 装饰图片使用 alt=""

aria-labels
  P1 | 图标按钮必须有 aria-label（无文字时）
  错误: <button><svg>...</svg></button>
  正确: <button aria-label="关闭对话框"><svg>...</svg></button>

color-not-sole-indicator
  P0 | 不能仅用颜色传达信息（色盲用户）
  错误: 红色=错误，绿色=正确（仅靠颜色）
  正确: 颜色 + 图标 + 文字标签组合
```

#### 分类三：触控与移动端（Touch & Mobile）

```
touch-target-minimum
  P0 | 触控目标最小 44x44px（iOS HIG / Material 标准）
  注: 视觉大小可以更小，padding 凑足 44px

tap-highlight-control
  P1 | 移动端默认蓝色点击高亮通常需要自定义
  CSS: -webkit-tap-highlight-color: transparent;

swipe-gesture-discoverability
  P1 | 可滑动组件必须有视觉提示（阴影或预览边缘）

safe-area-inset
  P0 | iPhone 刘海/Home Bar 区域需要 safe-area-inset 处理
  CSS: padding-bottom: env(safe-area-inset-bottom);

thumb-zone-optimization
  P2 | 核心操作尽量放在拇指容易触达区域（屏幕底部 1/3）
```

#### 分类四：布局与响应式（Layout & Responsive）

```
responsive-breakpoints
  P0 | 必须测试 375px / 768px / 1024px / 1440px
  注: 375px = iPhone SE，最小测试基准

content-shift-prevention
  P0 | 避免 CLS（Cumulative Layout Shift）
  技术: 图片设置 width/height 属性，骨架屏替代加载

overflow-handling
  P1 | 长文本必须处理截断（text-overflow: ellipsis 或换行）
  常见问题: 动态数据在非预期长度时破坏布局

z-index-management
  P1 | 建立一套 z-index 规范（modal=1000, tooltip=900, ...）
  反模式: z-index: 9999999 的存在
```

#### 分类五：动画与性能（Animation & Performance）

```
animation-duration
  P1 | 微交互 150-300ms，页面转场 300-500ms
  注: > 500ms 的动画让用户感到「等待」

gpu-accelerated-animation
  P1 | 动画优先使用 transform 和 opacity（GPU 加速）
  反模式: 动画中改变 width/height/top/left（触发重排）

loading-skeleton
  P1 | 加载时使用骨架屏而非空白或 spinner（感知速度更快）

animation-purpose
  P2 | 动画必须服务于功能目的（引导注意、反馈状态）
  反模式: 纯装饰性动画满天飞

font-loading-strategy
  P1 | Google Fonts 使用 display=swap 防止字体加载阻塞
  注: <link href="...&display=swap" rel="stylesheet">
```

#### 分类六：表单与数据输入（Forms & Input）

```
inline-validation
  P1 | 表单验证在 blur 时立即反馈，不等提交
  
error-message-proximity
  P0 | 错误信息必须紧邻对应的输入字段

placeholder-not-label
  P0 | placeholder 不能替代 label（失焦后消失）
  正确: 浮动 label 或 label 在输入框上方

input-type-semantic
  P1 | 使用正确的 input type（tel/email/number/date）
  好处: 移动端自动唤起合适键盘，提升体验

autocomplete-attribute
  P1 | 常见字段设置 autocomplete 属性
  示例: autocomplete="email" / "current-password"
```

#### 分类七：图标使用（Icon Usage）

```
no-emoji-as-icon
  P0 | 禁止用 emoji 替代图标（不同平台渲染差异极大）
  推荐: Heroicons / Lucide / Phosphor（SVG 图标）

icon-style-consistency
  P1 | 全产品使用同一套图标集（相同线条粗细/圆角风格）

icon-size-standard
  P1 | 建立标准尺寸体系（16/20/24/32px）

icon-text-pairing
  P1 | 图标 + 文字组合时，图标用于强化而非替代文字
```

#### 分类八：平台适配（Platform-specific）

```
platform-adaptive
  P1 | 遵守平台惯例（iOS HIG vs Material Design）
  示例: iOS 的 back 手势 vs Android 的系统 back 键

elevation-consistent
  P1 | 卡片/Sheet/Modal 使用一致的阴影层级
  正确: card=2dp, drawer=16dp, modal=24dp

dark-mode-pairing
  P1 | 亮/暗模式必须成对设计，保持品牌一致性

icon-style-platform
  P2 | iOS 偏好轮廓型图标，Android 偏好填充型
```

---

## 二、charts.csv：25 种图表类型推荐系统

### 2.1 图表选择的核心问题

「用什么图表」是数据可视化中最容易出错的决策——柱状图 vs 折线图、饼图 vs 环图、散点图 vs 气泡图，不同的选择传达完全不同的信息。

UUPM 的 `charts.csv` 把图表推荐也结构化了：

```
id, name, category, best_for, data_type,
max_data_points, recommended_library,
anti_patterns, accessibility_notes
```

### 2.2 25 种图表类型的完整分类

#### 类别一：比较类（Comparison）

| 图表 | 最适合 | 数据要求 |
|------|--------|---------|
| Bar Chart（柱状图）| 离散类别比较 | ≤ 12 个类别 |
| Horizontal Bar | 类别名称较长 | ≤ 15 个类别 |
| Grouped Bar | 多系列比较 | ≤ 3 系列, ≤ 8 类别 |
| Radar/Spider | 多维度属性比较 | 4-8 个维度 |

#### 类别二：趋势类（Trend）

| 图表 | 最适合 | 反模式 |
|------|--------|--------|
| Line Chart（折线图）| 时间序列趋势 | 离散数据点 < 5 时（用柱状图）|
| Area Chart（面积图）| 强调总量趋势 | 多系列时（颜色重叠混乱）|
| Sparkline（迷你折线）| 卡片内趋势概览 | 需要精确读值时 |
| Candlestick | 金融 OHLC 数据 | 非金融场景 |

#### 类别三：分布类（Distribution）

| 图表 | 最适合 | 数据要求 |
|------|--------|---------|
| Histogram（直方图）| 数值分布频率 | 连续数据 |
| Box Plot（箱线图）| 数据离散程度 | 需要比较多个组的分布 |
| Scatter Plot | 两变量相关性 | ≥ 50 数据点 |
| Bubble Chart | 三变量关系 | ≤ 30 气泡 |

#### 类别四：构成类（Composition）

| 图表 | 最适合 | 注意事项 |
|------|--------|---------|
| Pie Chart | 部分 vs 整体（< 5 片）| ≥ 6 片时难以分辨 |
| Donut Chart | 同上 + 中间可放 KPI | 同上 |
| Stacked Bar | 多维度构成趋势 | 只有底层基线清晰 |
| Treemap | 层次化构成比例 | 交互式时最有效 |

#### 类别五：关系类（Relationship）

| 图表 | 最适合 |
|------|--------|
| Network Graph | 实体关系网络 |
| Sankey Diagram | 流向分析（漏斗/流失）|
| Chord Diagram | 双向关系矩阵 |

#### 类别六：地理类（Geographic）

| 图表 | 最适合 |
|------|--------|
| Choropleth Map | 地区数据分布（颜色深浅）|
| Bubble Map | 地理位置数量对比 |
| Heat Map（地理）| 密度/集中度分布 |

#### 类别七：仪表盘专项

| 图表 | 最适合 |
|------|--------|
| KPI Card | 关键指标数字展示 |
| Gauge/Speedometer | 进度 vs 目标 |
| Progress Ring | 完成度可视化 |

### 2.3 推荐图表库

`charts.csv` 对每种图表都标注了推荐的 JS 库：

| 图表库 | 适合场景 | 特点 |
|--------|---------|------|
| **Recharts** | React 项目，中等复杂度 | 声明式 API，易上手 |
| **Chart.js** | 通用 Web，轻量 | 体积小，文档好 |
| **D3.js** | 高度定制化 | 最灵活但学习成本高 |
| **Echarts** | 大数据量，动态更新 | 百度出品，中文文档好 |
| **Plotly** | 科学数据，交互式探索 | 适合分析师工具 |
| **Nivo** | React，美观开箱即用 | 基于 D3，React 封装好 |

### 2.4 图表 UX 专项规则（来自 ux-guidelines.csv）

```
export-option
  P2 | 数据密集型产品应提供图表数据导出（CSV/PNG）

drill-down-consistency
  P1 | 支持下钻交互的图表必须有清晰的返回路径和层级面包屑

time-scale-clarity
  P1 | 时间序列图表必须清楚标注时间粒度（日/周/月）
  并支持粒度切换

color-meaning-chart
  P1 | 图表中的颜色编码必须有图例，且不能仅依靠颜色区分

zero-baseline-honesty
  P1 | 条形图 Y 轴必须从 0 开始（截断 Y 轴是视觉欺骗）

loading-state-chart
  P1 | 图表加载时显示骨架图而非空白区域
```

---

## 三、UX 准则的优先级系统

UUPM 用 P0/P1/P2 三级优先级给规则分类：

```
P0（必须遵守）：违反会造成严重可用性问题或合规风险
  示例: 对比度 < 4.5:1 / 无 focus 状态 / 点击无反馈

P1（强烈建议）：违反会降低体验质量
  示例: 缺少 hover 过渡 / 表单无内联验证

P2（酌情处理）：上下文依赖，有时可以例外
  示例: 拇指区域优化 / 图表导出功能
```

### 自动 Pre-delivery Check

每次生成代码后，UUPM 对照 P0 规则输出验收清单：

```
PRE-DELIVERY CHECKLIST（P0 必过项）:
  [ ] cursor-pointer-required  — 所有可点击元素有 cursor:pointer
  [ ] contrast-minimum         — 对比度 ≥ 4.5:1
  [ ] hover-state-required     — 所有交互元素有 hover 状态
  [ ] no-emoji-as-icon         — 无 emoji 图标（用 SVG）
  [ ] focus-visible-required   — 焦点状态可见
  [ ] prefers-reduced-motion   — 动画有降级处理
  [ ] responsive-breakpoints   — 测试 375/768/1024/1440px
```

---

## 四、app-interface.csv：应用界面模式库

除了通用 UX 准则，UUPM 还有一个 `app-interface.csv` 专门收录**界面模式**（Interface Patterns）：

- **导航模式**：Tab Bar、Side Drawer、Hamburger、Breadcrumb、Bottom Sheet
- **列表模式**：无限滚动、分页、虚拟列表、下拉刷新
- **表单模式**：步骤导航、即时验证、文件上传、多选
- **内容模式**：卡片网格、Feed 流、Master-Detail、全屏模态
- **数据展示模式**：骨架屏、空状态设计、错误状态设计、加载状态

每种模式都标注了适合的平台（Web / iOS / Android / 通用）和实现复杂度。

---

## 小结

UUPM 的 UX 准则体系有两个关键设计决策：

**决策 1：规则要可机器执行**。每条规则有唯一 ID、优先级标签、具体描述和反模式案例，AI 可以直接用这些规则验证生成的代码，而不只是「知道一些 UX 原则」。

**决策 2：图表选择也要去主观化**。通过 `charts.csv` 把「用什么图表」这个看似主观的决策也结构化了——根据数据类型、数量、展示目的三个维度输出推荐，大幅减少图表选错导致的信息误导。

---

> **下一篇**：⑥ 技术栈适配与 BM25 搜索引擎篇 —— 15 个技术栈为什么需要不同的设计指南，以及 Python 搜索引擎是如何工作的。
