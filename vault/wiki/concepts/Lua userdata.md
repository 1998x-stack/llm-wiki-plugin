---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 游戏开发, 编程语言, Lua编程]
aliases: [Lua full userdata, Lua light userdata, Lua原生对象包装]
relates_to:
  - target: "[[Lua C API 绑定层]]"
    type: implements
    confidence: 0.95
  - target: "[[Lua-metatable]]"
    type: uses
    confidence: 0.95
  - target: "[[Lua-table]]"
    type: relates_to
    confidence: 0.6
  - target: "[[Lua脚本宿主模式]]"
    type: depends_on
    confidence: 0.85
supersedes: null
---
# Lua userdata

## 概述
userdata 是 Lua 中唯一由宿主（C API）创建和修改的类型，是游戏引擎将原生对象句柄安全暴露给脚本层的核心机制，可挂 metatable 实现 OOP 风格访问。

## 关键内容

### Full userdata vs Light userdata

| | Full userdata | Light userdata |
|--|--|--|
| 内存 | Lua GC 管理的内存块 | 裸指针/句柄 |
| 类型安全 | 较强（可挂 metatable 和类型标识） | 弱（无类型/所有权信息） |
| 元表 | 支持（可定义 `__gc`、`__index` 等） | 不支持 |
| 典型用途 | 高层对象语义载体 | 注册表 key、内部索引 |
| 风险 | 额外内存与管理成本 | 悬空指针、类型误判、对象已销毁仍被引用 |

工业实践：light userdata 只做内部索引/注册表 key，不做高层对象语义载体。

### Full userdata 包装体常见布局
```
userdata {
  原生对象指针 / 对象ID / handle
  所属 VM / 类型标识
  所有权标志（可选）
  引用计数（可选）
}
```

### 元表驱动 OOP
引擎给每种暴露类型配一个 metatable：
- `__index` → 方法表或属性分发表（实现 `player:SetPosition()`）
- `__newindex` → 写属性处理
- `__gc` → 资源解绑（GC 时回调）
- `__tostring` → 调试输出

脚本看似在"直接操作引擎对象"，实际是在操作元表路由系统。

### 对象唯一包装缓存
同一 C++ 对象应映射到同一 Lua userdata 实例，否则：
- `a ~= b` 但两者指向同一原生对象
- 回调解绑困难
- 生命周期混乱

通常结合注册表（registry）实现缓存。对象不想阻止 GC 时，缓存表配合 **weak table**（弱键/弱值）使用：
- **强引用缓存**：对象不丢，但易泄漏
- **弱引用缓存**：更自然，但需处理对象被回收后的失效路径

### 所有权模型
| 模型 | 说明 | 适用场景 |
|------|------|---------|
| 引擎拥有，Lua 只是引用 | userdata 保存句柄；引擎删对象时标记无效 | 游戏对象（最常见） |
| Lua 拥有包装体 | `__gc` 回收包装资源 | 纯工具资源、独立资源句柄 |
| 共享所有（引用计数） | 智能指针共管 | 小对象，但需注意循环引用 |

**实战建议**：游戏对象尽量用"引擎拥有"模型；短生命周期纯脚本对象或独立资源包装再考虑 Lua 拥有/共享。

## 来源
- [[Lua 游戏引擎连接机制]] — ChatGPT 对话，系统介绍 Lua 与游戏引擎层的对象连接与所有权机制

## 相关
- [[Lua C API 绑定层]] — userdata 是 C API 绑定层的核心对象载体
- [[Lua-metatable]] — 元表赋予 userdata OOP 风格访问能力
- [[Lua脚本宿主模式]] — 对象代理层（第3层）的实现基础
