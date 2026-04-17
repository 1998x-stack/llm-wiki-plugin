---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, Lua编程]
aliases: [Lua栈模型, Lua虚拟栈, Lua C栈, lua_State栈]
relates_to:
  - target: "[[Lua C API 绑定层]]"
    type: implements
    confidence: 0.95
  - target: "[[Lua userdata]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Lua-metatable]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Lua基础语法]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---
# Lua 栈操作模型

## 概述
[[Lua C API 绑定层|Lua C API]] 围绕虚拟栈通信：宿主压入参数，调用函数，读取返回值；所有跨边界数据交换都经由栈完成。

## 关键内容

### 栈索引系统

```
正索引: 1（栈底/最先压入）→ lua_gettop(L)（栈顶/最后压入）
负索引: -1（栈顶）→ -lua_gettop(L)（栈底）
伪索引: LUA_REGISTRYINDEX（注册表，任意位置可访问）
        lua_upvalueindex(n)  （第 n 个 upvalue，1 起始）
```

正负索引等价：`idx > 0` 时从栈底数，`idx < 0` 时从栈顶数（-1 = 栈顶）。伪索引不占栈空间，用于访问特殊表。

### 核心栈管理 API

```c
int  lua_gettop(L)              // 栈上元素数量（= 最大正索引）
void lua_settop(L, int n)       // 设置栈顶：n < 当前 → 弹出；n > 当前 → 补 nil
void lua_pop(L, int n)          // 弹出 n 个（= lua_settop(L, -n-1)）
void lua_remove(L, int idx)     // 移除 idx 处元素，上方元素下移
void lua_insert(L, int idx)     // 将栈顶移入 idx，原 idx 上方元素上移
void lua_replace(L, int idx)    // 栈顶值替换 idx 处，弹出栈顶
void lua_copy(L, int from, int to)  // 复制 from 到 to（Lua 5.2+）
void lua_rotate(L, int idx, int n)  // 旋转 [idx..top] 片段（5.3+）
int  lua_checkstack(L, int n)   // 确保有 n 个额外空间，失败返回 0
```

**重要**：调用 `lua_tostring(L, idx)` 可能修改栈（将数字转为字符串驻留），不要在 key 迭代中对 key 位置调用。

### 压栈 API（Push）

| 函数 | 压入值 |
|------|--------|
| `lua_pushnil(L)` | nil |
| `lua_pushboolean(L, b)` | boolean |
| `lua_pushnumber(L, n)` | number (double) |
| `lua_pushinteger(L, i)` | integer (Lua 5.3+) |
| `lua_pushstring(L, s)` | string（内部复制） |
| `lua_pushlstring(L, s, len)` | 带长度字符串（可含 \0） |
| `lua_pushfstring(L, fmt, ...)` | 格式化字符串 |
| `lua_pushcfunction(L, fn)` | C 函数 |
| `lua_pushcclosure(L, fn, n)` | C 闭包（n 个 upvalue） |
| `lua_pushvalue(L, idx)` | 复制栈上元素 |
| `lua_pushlightuserdata(L, p)` | 轻量 userdata（裸指针） |
| `lua_pushthread(L)` | 当前线程（lua_State*） |

### 读取 API（不弹出）

```c
lua_toboolean(L, idx)           // → int (0/1)
lua_tonumber(L, idx)            // → lua_Number
lua_tonumberx(L, idx, &isnum)  // 带成功标志 (5.3+)
lua_tointeger(L, idx)           // → lua_Integer
lua_tostring(L, idx)            // → const char*（警告：可能修改栈）
lua_tolstring(L, idx, &len)     // → const char* + 长度
lua_touserdata(L, idx)          // → void*
lua_tothread(L, idx)            // → lua_State*
lua_topointer(L, idx)           // → const void*（唯一标识，调试用）
```

### 类型系统

```c
// 类型常量
LUA_TNIL        // 0
LUA_TBOOLEAN    // 1
LUA_TLIGHTUSERDATA // 2
LUA_TNUMBER     // 3
LUA_TSTRING     // 4
LUA_TTABLE      // 5
LUA_TFUNCTION   // 6
LUA_TUSERDATA   // 7
LUA_TTHREAD     // 8
LUA_TNONE       // -1（无效索引）

int  lua_type(L, idx)           // 返回类型常量
const char *lua_typename(L, tp) // 类型名称字符串
lua_isinteger(L, idx)           // 区分整数/浮点 (5.3+)
lua_isnumber(L, idx)            // 包括可转换为数字的字符串！
lua_isstring(L, idx)            // 包括数字（可转换为字符串）
```

**陷阱**：`lua_isnumber` / `lua_isstring` 是宽松检查，会对可互转的类型返回 true，需要严格类型时用 `lua_type()` 比较常量。

### 跨线程移动

```c
void lua_xmove(lua_State *from, lua_State *to, int n);
// 从 from 栈顶移动 n 个元素到 to 栈顶
// 两个 lua_State 必须属于同一 VM（共享主 lua_State）
```

用于协程间传递值，或主线程与协程之间的参数传递。

### 典型栈帧序列

调用 Lua 函数的标准模式：
```c
lua_getglobal(L, "func");    // [func]
lua_pushnumber(L, 1.0);      // [func, 1.0]
lua_pushstring(L, "hello");  // [func, 1.0, "hello"]
int rc = lua_pcall(L, 2, 1, 0);  // 2参数, 1返回值 → [result]
if (rc == LUA_OK) {
    double result = lua_tonumber(L, -1);
    lua_pop(L, 1);           // []
}
```

表迭代标准模式：
```c
lua_pushnil(L);              // 初始 key = nil
while (lua_next(L, tbl_idx) != 0) {
    // 栈: ... | key(-2) | value(-1)
    // 处理 key 和 value
    // 注意：不要对 key 调用 lua_tostring，会破坏 lua_next 状态
    lua_pop(L, 1);           // 弹出 value，保留 key 供下次迭代
}
```

## 来源
- [[lua-c-api]] — Lua C API 完整参考文档，Section 2（栈操作）、Section 3（类型系统）

## 相关
- [[Lua C API 绑定层]] — 栈模型是 C API 绑定的底层机制
- [[Lua userdata]] — 通过栈操作创建和访问的原生对象类型
- [[Lua-metatable]] — 元表操作也经由栈完成
- [[Lua基础语法]] — Lua 语言层（栈对脚本透明）
