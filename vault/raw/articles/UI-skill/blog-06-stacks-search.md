# UI UX Pro Max 深度解析⑥：15 个技术栈适配 + BM25 搜索引擎——设计知识的检索架构

> **系列第 6 篇**：UUPM 的底层是一个 Python 实现的混合搜索引擎，本篇深入讲解 `core.py`（BM25 + Regex 混合检索）和 `stacks/` 目录下 15 个技术栈专项指南的设计逻辑。

---

## 一、为什么需要技术栈感知？

「设计」和「实现」并不是两个独立阶段。一个 React + Tailwind 项目和一个 SwiftUI 项目虽然可以实现相同的视觉效果，但实现路径、性能考量、惯用模式完全不同。

举例：

| 设计决策：圆角卡片 hover 效果 |
|------------------------------|
| HTML+Tailwind: `class="hover:shadow-lg transition-shadow duration-200"` |
| React: `useSpring` hook + `to={{ boxShadow: '...' }}` |
| SwiftUI: `.onHover { isHovered in }` + `.animation(.easeInOut)` |
| Flutter: `AnimatedContainer` + `BoxDecoration` |
| Jetpack Compose: `animateFloatAsState` + `Card(elevation)` |

UUPM 的 `stacks/` 目录为每个平台提供这种层面的具体指南。

---

## 二、15 个技术栈的分类与专项知识

### 2.1 Web 前端栈

#### HTML + Tailwind（默认栈）
**stacks/html-tailwind.csv** 包含：

```
主题领域:
  ├── Tailwind 主题变量配置（CSS 自定义属性 + Tailwind config）
  ├── 响应式前缀使用（sm: md: lg: xl: 2xl:）
  ├── 暗黑模式（dark: 前缀 vs class 策略）
  ├── 任意值语法（text-[#1a1a1a]）
  └── 性能优化（PurgeCSS / JIT 模式）

典型规则示例:
  tailwind-color-variables
    对于品牌色，在 tailwind.config.js 中定义主题色
    而非使用任意值 bg-[#4F46E5]
    正确: bg-primary（配置后的语义化颜色）

  dark-mode-class-strategy  
    推荐 class 策略而非 media 策略，便于手动切换
    tailwind.config: { darkMode: 'class' }

  responsive-mobile-first
    Tailwind 是移动优先，基础样式对应最小屏
    sm: 对应 640px+ (非"小屏"，是 640px 以上)
```

#### React 栈
**stacks/react.csv** 的独特知识点：

```
react-component-state-ui
  UI 状态（hover/focus/active）用 CSS 而非 React state
  反模式: const [isHovered, setIsHovered] = useState(false)
  正确:   CSS :hover 伪类 / CSS Module / Tailwind hover:

react-key-prop-lists
  列表渲染必须使用稳定唯一的 key（非 index）
  影响: key 不稳定导致不必要的 DOM 重新挂载，动画失效

framer-motion-layout-id
  共享元素过渡动画使用 layoutId prop
  适合: 卡片展开/收起、列表排序动画

virtualization-large-lists
  > 100 条的列表使用 react-window 或 react-virtual
  影响: 10000 条不虚拟化 = 10000 个 DOM 节点 = 严重卡顿
```

**stacks/react-performance.csv**（独立性能专项）：

```
避免内联对象/函数（重新渲染触发器）:
  反模式: <Component style={{ color: 'red' }} />
  正确:   const style = useMemo(...); <Component style={style} />

懒加载路由和组件:
  const LazyDashboard = lazy(() => import('./Dashboard'))

图片优化:
  使用 loading="lazy" + WebP/AVIF 格式
  优先使用 CSS 背景图而非 <img> 做装饰
```

#### Next.js 栈
**stacks/nextjs.csv** 包含 Next.js 特有的设计实现模式：

```
image-component-priority
  使用 <Image> 而非 <img>，首屏图片加 priority prop
  影响: LCP（最大内容绘制）直接影响 Core Web Vitals

font-optimization-next
  使用 next/font 加载字体（自动内联 CSS，消除字体加载偏移）
  而非直接引用 Google Fonts <link>

app-router-loading-ui
  在 loading.tsx 中提供骨架屏，避免 Suspense 闪白

parallel-routes-modal
  Modal/Drawer 用 Parallel Routes 实现，支持 URL 可分享
```

#### Vue / Nuxt 栈
```
vue-transition-component
  使用 <Transition> 和 <TransitionGroup> 实现进出动画
  name="fade" 对应 .fade-enter-active / .fade-leave-active

nuxtui-component-tokens
  Nuxt UI 使用 app.config.ts 定义 UI 主题 token
  而非直接修改组件 class

scoped-styles-preference
  使用 <style scoped> 防止样式泄漏
  深度选择器: :deep(.child-class)
```

#### Astro 栈（v2.2 新增，53 条专项规则）
```
islands-architecture-hydration
  只对需要交互的组件设置 client:* 指令
  client:load     → 立即加载
  client:idle     → 浏览器空闲时加载
  client:visible  → 进入视口时加载（推荐用于折叠下内容）
  client:media    → 匹配媒体查询时加载

view-transitions-api
  Astro 4+ 内置 View Transitions
  在 <head> 加 <ViewTransitions /> 即可获得页面间平滑过渡

content-collections-seo
  使用 Content Collections 管理博客/文档内容
  提供类型安全 + 自动生成 SEO meta
```

### 2.2 移动端栈

#### SwiftUI 栈
```
system-symbols-preferred
  使用 SF Symbols 而非自定义 SVG（系统一致性）
  Image(systemName: "heart.fill")

adaptive-colors-system
  使用系统自适应色（.primary / .secondary / .background）
  而非硬编码 HEX 值，自动支持 Dark Mode

sheet-presentation-detents
  iOS 16+ 使用 .presentationDetents([.medium, .large])
  实现半屏抽屉

safe-area-ignoringEdges
  全屏背景: .ignoresSafeArea()
  但内容区域不能忽略安全区域

navigation-swipe-back
  不要干扰系统侧滑返回手势
  禁止: navigationBarBackButtonHidden(true) 不提供替代
```

#### Flutter 栈
```
material-you-dynamic-colors
  Flutter 3+ 支持 Material You 动态颜色
  colorScheme: ColorScheme.fromSeed(seedColor: brandColor)

sliver-for-scroll
  复杂滚动场景（折叠 AppBar + 列表）使用 Sliver 组件
  而非嵌套 SingleChildScrollView

hero-animation-tag
  共享元素过渡使用 Hero 组件 + 唯一 tag
  在路由跳转时自动触发

responsive-layout-builder
  使用 LayoutBuilder 获取约束，而非 MediaQuery.of(context).size
```

#### React Native 栈
```
platform-specific-styles
  使用 Platform.OS 区分 iOS 和 Android 样式
  Platform.select({ ios: {...}, android: {...} })

safe-area-context
  使用 react-native-safe-area-context
  <SafeAreaView> 而非手动 paddingTop

react-native-reanimated-v3
  复杂动画使用 Reanimated 3（Worklet 线程，60fps）
  简单动画用 Animated（JS 线程，可能掉帧）

accessibility-role
  为自定义组件设置 accessibilityRole
  使屏幕阅读器正确理解组件语义
```

#### Jetpack Compose 栈（v2.1 新增）
```
material3-color-system
  使用 MaterialTheme.colorScheme 而非硬编码颜色
  支持动态颜色（Android 12+）

modifier-order-matters
  Compose Modifier 链式调用顺序影响结果
  .padding(16.dp).background(color) ≠ .background(color).padding(16.dp)

remember-and-state
  状态使用 remember + mutableStateOf
  避免在 @Composable 函数内使用 var（不触发重组）

lazy-column-key
  LazyColumn 中为 item 设置 key { item.id }
  与 React key 同理，稳定的 key 提升动画性能
```

---

## 三、core.py：BM25 + Regex 混合搜索引擎

### 3.1 为什么不直接用向量搜索？

UUPM 选择 BM25 而非向量嵌入，有几个实用原因：

| 维度 | BM25 | 向量搜索 |
|------|------|---------|
| 依赖 | **纯 Python 标准库** | 需要模型（几百 MB）|
| 速度 | 毫秒级 | 取决于模型大小 |
| 可解释性 | 词频匹配，可调试 | 黑盒 |
| 离线支持 | **完全离线** | 通常需要 API |
| 更新维护 | 改 CSV 即可 | 需重新嵌入 |

在 Skill 场景中，「零依赖 + 离线可用 + 结果可解释」比「语义理解精度极高」更重要——大量技术术语（Glassmorphism、BM25、Tailwind）BM25 已经能精确匹配。

### 3.2 BM25 算法原理

BM25（Best Match 25）是 TF-IDF 的改进版，用于评估文档与查询的相关度：

```
BM25(d, q) = Σ IDF(qi) × (TF(qi,d) × (k1+1)) / (TF(qi,d) + k1 × (1-b+b×|d|/avgdl))

参数:
  TF(qi,d)  = 词 qi 在文档 d 中的频率
  IDF(qi)   = log((N - n(qi) + 0.5) / (n(qi) + 0.5))
  |d|        = 文档长度
  avgdl      = 平均文档长度
  k1 = 1.5  (控制词频饱和度)
  b  = 0.75 (控制文档长度归一化)
```

**直觉理解**：
- 一个词在当前文档中出现频率高（TF 高），得分高
- 但如果这个词在所有文档中都很常见（IDF 低），得分降低
- 文档越长，词频贡献会被适度惩罚（避免长文档占优势）

### 3.3 Regex 混合的作用

BM25 负责相关性排序，但有几类查询需要 Regex 精确匹配：

```python
# 示例：用户输入 "#4F46E5" 这种精确色值
# BM25 可能找不到（不是关键词）
# Regex: r'#[0-9A-Fa-f]{6}' 直接命中

# 用户输入 "glassmorphism"（特定术语）
# BM25 + Regex 都能命中，但 Regex 确保精确匹配优先级更高
```

混合策略：
1. 先用 Regex 检测特殊模式（颜色值、版本号、精确术语）
2. 精确匹配结果提升到搜索结果顶部
3. BM25 排序剩余结果

### 3.4 搜索接口设计

```python
# search.py CLI 接口
python3 search.py "<query>" [--domain <domain>] [-n <max_results>] [--stack <stack>]

# 域名自动检测
# 当未指定 --domain 时，core.py 根据 query 内容猜测最合适的域：
def auto_detect_domain(query: str) -> str:
    if any(kw in query.lower() for kw in ['glassmorphism', 'brutalism', 'style']):
        return 'style'
    if any(kw in query.lower() for kw in ['font', 'typography', 'serif']):
        return 'typography'  
    if any(kw in query.lower() for kw in ['color', 'palette', '#']):
        return 'color'
    if any(kw in query.lower() for kw in ['chart', 'graph', 'dashboard data']):
        return 'chart'
    ...
    return 'product'  # 默认域
```

### 3.5 可搜索的 8 个域

| 域 | CSV 来源 | 典型查询 |
|----|---------|---------|
| `product` | products.csv | "SaaS startup" / "healthcare app" |
| `style` | styles.csv | "glassmorphism dark" / "minimal enterprise" |
| `color` | colors.csv | "banking trustworthy" / "warm food" |
| `typography` | typography.csv | "elegant serif luxury" / "modern sans" |
| `landing` | landing.csv | "lead generation conversion" |
| `chart` | charts.csv | "time series trend" / "comparison bar" |
| `ux` | ux-guidelines.csv | "accessibility contrast" / "mobile touch" |
| `google-fonts` | google-fonts.csv | "variable font RTL arabic" |

---

## 四、search.py CLI 完整功能参考

```bash
# 基础查询
python3 search.py "query"                          # 自动检测域
python3 search.py "query" --domain style           # 指定域
python3 search.py "query" -n 5                     # 限制结果数

# 技术栈查询
python3 search.py "form validation" --stack react
python3 search.py "responsive layout" --stack html-tailwind
python3 search.py "animation" --stack swiftui

# 设计系统生成
python3 search.py "beauty spa wellness" --design-system
python3 search.py "fintech" --design-system -p "MyFinApp"  # 项目名
python3 search.py "saas" --design-system -f markdown       # Markdown 输出

# 持久化
python3 search.py "saas dashboard" --design-system --persist -p "AppName"
python3 search.py "saas dashboard" --design-system --persist -p "AppName" --page "checkout"
```

---

## 五、templates/ 目录：平台适配的生成系统

UUPM 支持 18 个 AI 助手平台，但只有一份源代码（`src/ui-ux-pro-max/`）。`templates/` 目录是实现「一套内容，多平台输出」的关键：

```
templates/
├── base/
│   ├── skill-content.md     # 通用 SKILL 内容（技能描述、激活条件）
│   └── quick-reference.md   # Claude Code 专属快速参考
└── platforms/
    ├── claude.json          # Claude Code: .claude/skills/ 路径
    ├── cursor.json          # Cursor: .cursorrules 配置
    ├── windsurf.json        # Windsurf: .windsurfrules
    ├── copilot.json         # GitHub Copilot: .github/copilot-instructions.md
    ├── kiro.json            # Kiro: /ui-ux-pro-max slash command
    ├── roocode.json         # Roo Code: .roocode/
    └── ...（15个平台）
```

### CLI 模板渲染引擎（template.ts）

当你运行 `uipro init --ai claude` 时，CLI 做了什么：

```typescript
// 伪代码：template.ts
function renderPlatformFiles(platform: string, targetDir: string) {
  const config = loadPlatformConfig(platform);  // 读取 claude.json
  const skillContent = renderTemplate(          // 渲染内容模板
    'base/skill-content.md', 
    config.variables
  );
  
  // 生成平台特定文件结构
  for (const [targetPath, content] of config.files) {
    writeFile(path.join(targetDir, targetPath), content);
  }
  
  // 复制数据文件和脚本
  copyDir('assets/data/', path.join(targetDir, config.dataPath));
  copyDir('assets/scripts/', path.join(targetDir, config.scriptsPath));
}
```

这个设计将 CLI 体积从 ~34MB 压缩到 **~564KB**（v2.1 优化），因为不再存储 18 份平台文件副本，而是运行时生成。

---

## 小结：UUPM 的工程架构亮点

1. **零依赖原则**：纯 Python 标准库实现搜索引擎（只需 Python 3.x），用户无需安装额外包。

2. **CSV 作为知识库**：相比 SQLite/JSON，CSV 更易于人工编辑、版本控制 diff 清晰、Git PR review 友好。

3. **BM25 vs 向量搜索的务实选择**：在 Skill 场景下，BM25 的可解释性和零依赖比向量搜索的语义精度更有价值。

4. **模板生成 vs 多份副本**：通过 template.ts 运行时生成平台文件，维护成本从 O(n) 降到 O(1)（n=平台数量）。

5. **CSV 单一数据源**：`src/ui-ux-pro-max/data/` 是唯一事实来源，CLI assets 和所有平台文件通过同步/生成得到。

---

> **下一篇**：⑦ 设计系统持久化篇 —— Master + Overrides 模式如何解决 AI 跨会话设计一致性问题。
