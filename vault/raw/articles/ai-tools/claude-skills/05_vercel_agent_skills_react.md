# Vercel Agent Skills React 系列深度解析

> **系列**：Claude Code 前端 React 风格 SKILL/Plugin 深度调查  
> **文章编号**：05 / 09  
> **来源仓库**：[github.com/vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)  
> **Stars**：19,487 ⭐ | **License**：MIT  
> **作者**：Vercel Engineering（@shuding 等）  
> **工具支持**：Claude Code, Cursor, OpenCode, Codex, GitHub Copilot 等 18+ 工具  

---

## 一、Vercel Agent Skills 生态概览

Vercel 在 Claude Code Skills 生态中扮演了特殊角色：他们不仅是 Next.js 的创造者，也是 **Agent Skills 规范的早期采用者和主要推动者**。

Vercel 通过三个层面参与 Skills 生态：

1. **vercel-labs/agent-skills**：专注 React/Next.js 性能与架构的官方 Skills
2. **vercel-labs/skills**（`npx skills` 工具）：通用 Skills 安装 CLI 工具，已成为社区标准
3. **vercel-labs/react-best-practices**：70+ 规则的独立规则库，编译为 `AGENTS.md`

本文重点分析前端 React 相关的四个核心 Skills：

| Skill | 核心职责 | Stars 贡献 |
|-------|---------|-----------|
| `react-best-practices` | React/Next.js 70+ 性能优化规则 | 主力 |
| `composition-patterns` | React 组合模式 | 重要 |
| `web-design-guidelines` | Web UI 100+ 设计规范 | 重要 |
| `react-native-skills` | React Native + Expo 移动 UI | 补充 |

---

## 二、安装方式

### 方式一：npx skills（推荐）
```bash
# 安装所有 Vercel skills
npx skills add vercel-labs/agent-skills

# 仅安装特定 skills
npx skills add vercel-labs/agent-skills --skill react-best-practices
npx skills add vercel-labs/agent-skills --skill composition-patterns

# 安装到特定 agent
npx skills add vercel-labs/agent-skills --skill react-best-practices -a claude-code

# CI/CD 无交互安装
npx skills add vercel-labs/agent-skills --skill react-best-practices -g -a claude-code -y
```

### 方式二：Plugin Marketplace
```bash
/plugin marketplace add vercel-labs/agent-skills
/plugin install react-best-practices@vercel-agent-skills
```

### 方式三：skilz（Python 生态）
```bash
pip install skilz
skilz install vercel-labs/agent-skills/vercel-react-best-practices
```

---

## 三、`react-best-practices` Skill 深度解析

### 3.1 规模与结构

这是 Vercel Agent Skills 中**最重量级**的 Skill：

- **规则数量**：70+ 条（持续增长，从早期的 40+ 扩展）
- **来源**：Vercel 工程师 10+ 年生产代码经验
- **编译输出**：所有规则文件编译为单一 `AGENTS.md`（供 AI 查询）
- **原始作者**：@shuding（Next.js 核心维护者）

### 3.2 八大分类与优先级体系

规则按 **CRITICAL → HIGH → MEDIUM → LOW** 四级优先级排列，覆盖八个类别：

---

#### 分类一：Async 模式（CRITICAL 级别）

**规则：`async-parallel` — 并行化独立请求**

```typescript
// ❌ 串行请求（+600ms 延迟）
async function getPageData(userId: string) {
  const user = await getUser(userId)        // 等待
  const posts = await getUserPosts(userId)  // 再等待
  const stats = await getUserStats(userId)  // 再等待
  return { user, posts, stats }
}

// ✅ 并行请求（最慢的那个决定总时间）
async function getPageData(userId: string) {
  const [user, posts, stats] = await Promise.all([
    getUser(userId),
    getUserPosts(userId),
    getUserStats(userId)
  ])
  return { user, posts, stats }
}
```

**规则：`async-cheap-condition-before-await` — 先检查廉价条件**

```typescript
// ❌ 网络请求后再检查 flag（浪费时间）
async function processItem(item: Item) {
  const result = await expensiveAPICall(item)
  if (!isEnabled) return null  // feature flag 检查放在了网络请求后
  return result
}

// ✅ 先检查同步条件
async function processItem(item: Item) {
  if (!isEnabled) return null  // 先检查
  const result = await expensiveAPICall(item)
  return result
}
```

**规则：`async-defer-await` — 延迟 await 到真正需要时**

```typescript
// ❌ 立即 await（阻塞后续代码）
const data = await fetchData()
doSomethingUnrelated()
return data

// ✅ 先启动 Promise，后 await
const dataPromise = fetchData()   // 立即启动，不阻塞
doSomethingUnrelated()            // 并发执行
return await dataPromise          // 真正需要时才 await
```

---

#### 分类二：Bundle 优化（CRITICAL 级别）

**规则：动态导入大型组件**

```typescript
// ❌ 同步导入：首屏加载包含完整动画库
import { AnimationPlayer } from './AnimationPlayer'

// ✅ 动态导入：只在需要时加载
const AnimationPlayer = dynamic(() => import('./AnimationPlayer'), {
  loading: () => <Skeleton />,
  ssr: false  // 纯 client-side 组件
})
```

**规则：命名导入优于默认导入（tree-shaking 效果）**

```typescript
// ❌ 引入整个 lodash（70KB）
import _ from 'lodash'
const result = _.debounce(fn, 300)

// ✅ 按需导入
import { debounce } from 'lodash-es'
const result = debounce(fn, 300)
```

**规则：避免模块顶层的副作用**

```typescript
// ❌ 模块加载时立即执行昂贵操作
const config = JSON.parse(fs.readFileSync('./config.json', 'utf8'))

// ✅ 懒加载 + 缓存
let cachedConfig: Config | null = null
function getConfig() {
  if (!cachedConfig) {
    cachedConfig = JSON.parse(fs.readFileSync('./config.json', 'utf8'))
  }
  return cachedConfig
}
```

---

#### 分类三：React Server Components (RSC) 边界（HIGH 级别）

**规则：`minimize-serialization-at-rsc-boundaries` — 最小化 RSC 边界序列化**

```typescript
// ❌ 传递完整用户对象（包含敏感字段）
function ServerPage() {
  const user = await getUser()
  return <ClientComponent user={user} />  // 序列化整个对象
}

// ✅ 只传递 Client 需要的字段
function ServerPage() {
  const user = await getUser()
  const { id, name, avatarUrl } = user  // 最小化数据
  return <ClientComponent userId={id} userName={name} avatarUrl={avatarUrl} />
}
```

RSC 序列化数据会嵌入 HTML 响应和后续 RSC 请求中，直接影响页面大小。

**规则：`parallel-data-fetching-with-composition` — 用组合实现并行数据获取**

```typescript
// ❌ 串行 RSC 树（每个组件等待上一个）
async function BlogPage() {
  const post = await getPost()
  const comments = await getComments(post.id)  // 等 post 完成才开始
  const author = await getAuthor(post.authorId)
}

// ✅ 用组合实现并行
async function BlogPage({ postId }: { postId: string }) {
  const postPromise = getPost(postId)
  const commentsPromise = getComments(postId)  // 同时发起
  
  const post = await postPromise
  
  return (
    <article>
      <PostContent post={post} />
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments commentsPromise={commentsPromise} />
      </Suspense>
      <Suspense fallback={<AuthorSkeleton />}>
        <AuthorCard authorPromise={getAuthor(post.authorId)} />
      </Suspense>
    </article>
  )
}
```

---

#### 分类四：Client 端性能（HIGH 级别）

**规则：稳定化回调引用（避免子组件不必要重渲染）**

```typescript
// ❌ 每次渲染创建新的回调引用
function ParentComponent() {
  const handleClick = (id: string) => {
    doSomething(id)
  }
  return <MemoizedChild onClick={handleClick} />  // 每次 render 都触发重渲染
}

// ✅ useCallback 稳定引用
function ParentComponent() {
  const handleClick = useCallback((id: string) => {
    doSomething(id)
  }, [])  // 空依赖：回调不依赖任何 state
  
  return <MemoizedChild onClick={handleClick} />
}
```

**规则：列表渲染 key 必须稳定且唯一**

```typescript
// ❌ 使用 index 作为 key（重排序时引发 DOM 错误）
{items.map((item, index) => (
  <TodoItem key={index} item={item} />
))}

// ✅ 使用稳定的业务 ID
{items.map((item) => (
  <TodoItem key={item.id} item={item} />
))}
```

---

#### 分类五：数据获取缓存（HIGH 级别）

**规则：`cross-request-lru-caching` — 跨请求 LRU 缓存**

Vercel Fluid Compute 的多个并发请求共享同一函数实例，因此模块级缓存特别有效：

```typescript
import { LRUCache } from 'lru-cache'

// 模块级缓存（跨请求共享）
const userCache = new LRUCache<string, User>({
  max: 500,
  ttl: 1000 * 60 * 5  // 5 分钟 TTL
})

async function getUser(id: string): Promise<User> {
  const cached = userCache.get(id)
  if (cached) return cached
  
  const user = await db.users.findById(id)
  userCache.set(id, user)
  return user
}
```

---

#### 分类六～八（其余类别）

| 类别 | 代表规则 | 优先级 |
|------|---------|--------|
| **Security** | Server Actions 鉴权要像 API Routes 一样严格 | HIGH |
| **State** | 避免 useEffect 驱动的状态同步（改用 useSyncExternalStore） | MEDIUM |
| **Advanced** | useEffectEvent 稳定回调（React 19+） | LOW |

---

## 四、`composition-patterns` Skill 深度解析

### 4.1 定位：根治 Boolean Props 地狱

> If you have ever inherited a React component with 15 boolean props (isCompact, showHeader, isRounded, hasBorder, isHighlighted...), you understand the problem this skill solves.

**Boolean Props 地狱的典型症状**：
```tsx
// ❌ 这是组件设计腐败的标志
<Card 
  isCompact={true}
  showHeader={false}
  isRounded={true}
  hasBorder={false}
  isHighlighted={true}
  hasFooter={false}
  isPrimary={false}
  isSecondary={true}
/>
```

### 4.2 Compound Components 模式

```tsx
// ✅ Compound Components：自描述、可组合
<Card>
  <Card.Body compact>
    <Card.Content>{children}</Card.Content>
  </Card.Body>
  <Card.Footer>
    <Button variant="secondary">Action</Button>
  </Card.Footer>
</Card>

// 实现方式
const Card = ({ children }: { children: React.ReactNode }) => (
  <div className="bg-card rounded-lg border border-border">{children}</div>
)

Card.Body = function CardBody({ 
  children, 
  compact = false 
}: { children: React.ReactNode; compact?: boolean }) {
  return (
    <div className={cn("p-6", compact && "p-3")}>{children}</div>
  )
}

Card.Content = function CardContent({ children }: { children: React.ReactNode }) {
  return <div className="text-card-foreground">{children}</div>
}

Card.Footer = function CardFooter({ children }: { children: React.ReactNode }) {
  return (
    <div className="border-t border-border px-6 py-4 flex gap-2">{children}</div>
  )
}
```

### 4.3 Context Providers 替代 Props Drilling

```tsx
// 表单组件的 Context 模式
const FormContext = createContext<FormContextType | null>(null)

function Form({ children, onSubmit }: FormProps) {
  const [errors, setErrors] = useState<Record<string, string>>({})
  
  return (
    <FormContext.Provider value={{ errors, setErrors }}>
      <form onSubmit={onSubmit}>{children}</form>
    </FormContext.Provider>
  )
}

// 深层子组件直接消费 context，无需层层传递
function FieldError({ name }: { name: string }) {
  const { errors } = useContext(FormContext)!
  return errors[name] ? <span className="text-destructive">{errors[name]}</span> : null
}
```

### 4.4 显式 Variants 替代 Boolean 开关

```tsx
// ✅ 用 variant 替代多个 boolean
type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'destructive'
type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps {
  variant?: ButtonVariant
  size?: ButtonSize
  children: React.ReactNode
  onClick?: () => void
}

// 配合 cva (class-variance-authority)
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium",
  {
    variants: {
      variant: {
        primary: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  }
)
```

---

## 五、`web-design-guidelines` Skill

**来源**：`vercel-labs/web-interface-guidelines`（持续更新的独立仓库）

**核心特点**：Skill 在执行时会**动态 fetch 最新规范内容**，确保始终使用最新版本：

```markdown
# SKILL.md 伪代码
Fetch the latest guidelines from: 
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/guidelines.md
Then review the current code against those guidelines.
```

**100+ 规则覆盖的领域**：

| 领域 | 典型规则 |
|------|---------|
| 无障碍 | 所有图片必须有 alt；表单字段必须有关联 label；ARIA 属性使用正确 |
| 焦点管理 | 可见的 focus ring；合理的 tab 顺序；模态框打开时焦点捕获 |
| 触摸目标 | 按钮最小 44×44px（iOS HIG 标准） |
| 减弱动效 | 所有动画 respect `prefers-reduced-motion` |
| 语义 HTML | 正确使用 `<nav>`, `<main>`, `<article>`, `<aside>` |
| 键盘导航 | 所有功能可用键盘完成 |
| 颜色对比 | WCAG AA：正常文字 ≥ 4.5:1，大文字 ≥ 3:1 |

---

## 六、`react-native-skills` Skill

**定位**：React Native + Expo 移动端 UI 性能与规范

**最重要的规则：FlashList 替代 FlatList（CRITICAL 级别）**

```tsx
// ❌ FlatList：内存占用大，长列表必 jank
import { FlatList } from 'react-native'
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}
/>

// ✅ FlashList：Shopify 开源，大幅优化内存和帧率
import { FlashList } from '@shopify/flash-list'
<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={80}           // 必须提供，用于虚拟化计算
  keyExtractor={(item) => item.id}
/>
```

**列表性能 8 条规则**（CRITICAL 分类）：

1. FlashList 替代 FlatList
2. 列表 item 组件用 `React.memo` 包裹
3. 稳定化回调引用（`useCallback`）
4. 避免 inline style object（每次 render 创建新对象）
5. 将函数提取到组件外部
6. 优化列表中的图片（使用 `expo-image` 替代 `<Image>`）
7. 将昂贵计算移到组件外部
8. 使用 `itemType` 处理异构列表

---

## 七、Skills 在 Vercel 内部的工程实践

Vercel 博客公开了几个真实的生产优化案例，这些案例直接影响了 react-best-practices 规则的形成：

**案例一：Chat 应用消息扫描优化**
> A chat page was scanning the same list of messages **eight separate times**. We combined it into a single pass, which adds up when you have thousands of messages.

→ 对应规则：合并重复 map/filter 操作

**案例二：API 并行化**
> An API was waiting for one database call to finish before starting the next, even though they didn't depend on each other. Running them at the same time cut the **total wait in half**.

→ 对应规则：`async-parallel`

**案例三：JSON 解析缓存**
> A component was parsing a JSON config from localStorage on **every render**, even though it only needed it once for state initialization.

→ 对应规则：懒加载初始化器 `useState(() => JSON.parse(...))`

---

## 八、与 Anthropic frontend-design Skill 的互补关系

> The most effective approach is to combine skills from multiple categories. They **do not conflict**. They complement each other, each adding a different layer of quality.

```
Anthropic frontend-design          ← 美学层：设计方向、字体、色彩、动效
        +
Vercel web-design-guidelines       ← 规范层：无障碍、语义 HTML、触摸目标
        +
Vercel react-best-practices        ← 性能层：请求并行化、Bundle 优化、缓存
        +
Vercel composition-patterns        ← 架构层：组件设计、可扩展性
        =
四层质量防护的 React 界面
```

---

## 九、小结

Vercel Agent Skills 是**工业级 React 工程知识的 AI 可读化**：

| Skill | 核心价值 |
|-------|---------|
| `react-best-practices` | 10+ 年 Vercel 生产经验 → 70+ 可执行规则 |
| `composition-patterns` | 告别 Boolean Props 地狱，建立可扩展组件架构 |
| `web-design-guidelines` | 100+ UI 规范的自动化审查，包含无障碍 |
| `react-native-skills` | 移动端 60fps 的关键路径优化 |

这四个 Skills 与 Anthropic `frontend-design` 形成完美互补：后者负责"看起来好"，前者确保"运行好"。

---

**下一篇** → `06_bencium_ux_designer_skill.md`  
bencium/bencium-claude-code-design-skill 深度解析：28,000+ 字的 UX 设计圣经，controlled 与 innovative 双模式设计师

---

*调查时间：2025年4月 | 数据来源：github.com/vercel-labs/agent-skills, vercel.com/blog, infoq.com, snyk.io*
