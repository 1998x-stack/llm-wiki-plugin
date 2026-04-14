---
title: "Lua table 深入解析"
source: "https://chatgpt.com/c/69d65cca-8b88-8323-a242-7c0d5676657e"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
Lua 里的 `table` 是核心数据结构，几乎同时承担了：

所以想“深入”理解 Lua， `table` 基本绕不过去。

---

## 1\. table 本质上是什么

Lua 只有少数几种基本类型， `table` 是其中最强的一种。它本质上是一个 **关联数组** ：

```markdown
t = {}
t["name"] = "Alice"
t[1] = 100
t[true] = "yes"
```

也就是说，key 不一定是字符串，也不一定是整数，几乎任何非 `nil` 值都可以做 key。

但实践里主要有两类用法：

- **数组部分** ：连续正整数 key，通常从 `1` 开始
- **哈希部分** ：字符串或离散 key

例如：

```markdown
local t = {
    "a", "b", "c",   -- 等价于 [1]="a", [2]="b", [3]="c"
    name = "Tom",
    age = 18
}
```

这张表同时有“数组区”和“字典区”。

---

## 2\. 为什么 Lua 的下标从 1 开始

Lua 的惯例是数组从 `1` 开始：

```markdown
local arr = {"x", "y", "z"}
print(arr[1]) -- x
```

不是语法硬性要求，而是语言设计和标准库都围绕这个约定展开。  
你当然可以写：

```markdown
local t = {}
t[0] = "zero"
```

但很多库函数、长度运算、迭代习惯，都是按 1-based 来设计的。  
所以只要你把 table 当数组用，最好老老实实从 1 开始。

---

## 3\. table 是引用类型，不是值类型

这是最容易踩坑的一点。

```markdown
local a = {x = 1}
local b = a
b.x = 2
print(a.x) -- 2
```

`b = a` 不是复制 table 内容，而是让 `b` 和 `a` 指向同一张表。

所以：

- 赋值传递的是 **引用**
- 函数传参传的是 **引用**
- 想复制必须自己写拷贝逻辑

浅拷贝例子：

```markdown
local function shallow_copy(src)
    local dst = {}
    for k, v in pairs(src) do
        dst[k] = v
    end
    return dst
end
```

但这只复制第一层，嵌套 table 还是共享引用。

---

## 4\. table 的 key 规则

合法 key：

- number
- string
- boolean
- table
- function
- userdata
- thread

不合法 key：

- `nil`
- `NaN` （实践上也不能安全当 key）

例如：

```markdown
local t = {}
local k = {}
t[k] = "value"
print(t[k]) -- value
```

注意：table 作为 key，比较的是 **引用身份** ，不是内容相等。

```markdown
local a = {}
local b = {}
local t = {}
t[a] = 1
print(t[b]) -- nil
```

虽然 `a` 和 `b` 都是空表，但它们不是同一个对象。

---

## 5.. 和 \[\] 的区别

这两个经常被混着用，但本质不同。

```markdown
t.name
```

等价于：

```markdown
t["name"]
```

所以点语法只是字符串 key 的语法糖。

但下面这些情况只能用 `[]` ：

```markdown
t["first-name"] = "Tom"
t[key] = 123
t[1] = "a"
```

如果你写：

```markdown
local key = "name"
print(t.key)   -- 取的是 "key" 这个字段
print(t[key])  -- 取的是变量 key 的值对应的字段
```

这是经典坑点。

---

## 6\. table 中的 nil 意味着“删除”

Lua 里 table 不能真正保存 `nil` 值。

```markdown
local t = {a = 1}
t.a = nil
print(t.a) -- nil
```

这不是“值变成 nil”，而是 **这个 key 被删除了** 。

因此你无法区分：

- 这个字段不存在
- 这个字段存在但值是 nil

因为 Lua 里这两件事等价。

如果你需要“空值但字段仍存在”的语义，通常会用特殊哨兵值：

```markdown
local NULL = {}
t.a = NULL
```

---

## 7\. 长度运算符 # 为什么不可靠

`#t` 只对“ **序列** ”有清晰意义。

所谓序列，通常指：

- key 从 `1` 开始
- 连续整数
- 中间没有洞

例如：

```markdown
local t = {"a", "b", "c"}
print(#t) -- 3
```

但如果有空洞：

```markdown
local t = {"a", nil, "c"}
print(#t) -- 未定义边界，不应依赖
```

或者：

```markdown
local t = {}
t[1] = "a"
t[3] = "c"
print(#t) -- 结果不该依赖
```

Lua 对这种“非连续数组”的长度行为不保证一致可预测。  
所以经验法则：

- `#t` 只用于连续数组
- 稀疏数组不要用 `#`
- 字典表不要用 `#`

---

## 8\. pairs 和 ipairs 的区别

## pairs

遍历所有 key-value：

```markdown
for k, v in pairs(t) do
    print(k, v)
end
```

特点：

- 遍历整个 table
- 顺序 **不保证**
- 适合字典表

## ipairs

按 `1,2,3...` 遍历数组部分：

```markdown
for i, v in ipairs(t) do
    print(i, v)
end
```

特点：

- 从 1 开始
- 遇到第一个 `nil` 就停
- 适合连续数组

例子：

```markdown
local t = {10, 20, nil, 40}

for i, v in ipairs(t) do
    print(i, v)
end
-- 只会输出 1 10 / 2 20
```

---

## 9\. next 才是底层遍历原语

`pairs(t)` 本质上依赖 `next` 。

```markdown
local k, v = next(t, nil)   -- 第一个元素
local k2, v2 = next(t, k)   -- 下一个元素
```

手写遍历：

```markdown
local k, v = next(t, nil)
while k do
    print(k, v)
    k, v = next(t, k)
end
```

理解这一点有助于你明白：

- `pairs` 的顺序不稳定
- table 内部有自己的存储布局
- 遍历顺序不是插入顺序

---

## 10\. table 同时有数组区和哈希区

这是 Lua table 很精妙的地方。实现层面上，Lua 通常会把 table 分成：

- **array part**
- **hash part**

例如：

```markdown
local t = {
    [1] = "a",
    [2] = "b",
    [100] = "x",
    name = "Tom"
}
```

这里 `[1]` 、 `[2]` 更可能落在数组区， `[100]` 和 `"name"` 落在哈希区。

这也是为什么：

- Lua 对连续整数索引访问很高效
- 同一个结构能兼顾数组和字典

但你不应该依赖内部布局，只需要知道：

- 连续整数键更适合当数组
- 离散键更适合字典

---

## 11\. 构造器语法细节

Lua table 构造器很灵活：

```markdown
local t = {
    10,            -- [1] = 10
    20,            -- [2] = 20
    x = 1,         -- ["x"] = 1
    ["y"] = 2,
    [3] = 99
}
```

注意：

```markdown
{x = 1}
```

等价于：

```markdown
{["x"] = 1}
```

而：

```markdown
{1, 2, 3}
```

等价于：

```markdown
{[1] = 1, [2] = 2, [3] = 3}
```

---

## 12\. table 当对象用

Lua 没有内建 class，但经常用 table 模拟对象：

```markdown
local person = {
    name = "Tom",
    say = function(self)
        print("Hi, I am " .. self.name)
    end
}

person:say()
```

这里 `:` 很关键。

```markdown
person:say()
```

等价于：

```markdown
person.say(person)
```

所以：

- 定义方法时 `function t:foo(x)` 等价于 `function t.foo(self, x)`
- 调用方法时 `obj:foo(x)` 等价于 `obj.foo(obj, x)`

很多 Lua OOP 风格都建立在这个语法糖上。

---

## 13\. metatable：table 的真正高阶玩法

`table` 强大的地方，不只是存值，而是可以通过 **metatable** 改行为。

例如：

```markdown
local t = {}
setmetatable(t, {
    __index = function(_, key)
        return "missing:" .. key
    end
})

print(t.name) -- missing:name
```

常见元方法：

- `__index` ：访问不存在字段时触发
- `__newindex` ：给不存在字段赋值时触发
- `__tostring`
- `__add` / `__sub` 等运算符重载
- `__len`
- `__call`
- `__eq`, `__lt`, `__le`

## \_\_index 的两种常见写法

### 1）用函数

```markdown
mt.__index = function(tbl, key)
    return ...
end
```

### 2）用另一张表做原型链

```markdown
local proto = {x = 100}
local t = {}
setmetatable(t, {__index = proto})

print(t.x) -- 100
```

这就是 Lua 里最常见的“原型继承”。

---

## 14\. 用 table 实现类

经典写法：

```markdown
local Person = {}
Person.__index = Person

function Person.new(name)
    local self = setmetatable({}, Person)
    self.name = name
    return self
end

function Person:say()
    print("Hi, I am " .. self.name)
end

local p = Person.new("Alice")
p:say()
```

关键点：

```markdown
Person.__index = Person
setmetatable(instance, Person)
```

于是实例查找不到字段时，会去 `Person` 上找。

---

## 15\. table 作为集合 set

Lua 没有内建 set，常用 table 模拟：

```markdown
local set = {}
set["apple"] = true
set["banana"] = true

if set["apple"] then
    print("has apple")
end
```

如果只关心“是否存在”，value 常设成 `true` 。

删除：

```markdown
set["apple"] = nil
```

---

## 16\. table 作为缓存 map

```markdown
local cache = {}

local function fib(n)
    if n <= 2 then return 1 end
    if cache[n] then return cache[n] end
    cache[n] = fib(n-1) + fib(n-2)
    return cache[n]
end
```

这是 Lua 里非常常见的模式。

---

## 17\. table 排序、插入、删除

标准库 `table` 模块常用函数：

## table.insert

```markdown
local t = {"a", "c"}
table.insert(t, 2, "b")
-- {"a", "b", "c"}
```

## table.remove

```markdown
local t = {"a", "b", "c"}
local x = table.remove(t, 2)
-- x = "b", t = {"a", "c"}
```

## table.sort

```markdown
local t = {3, 1, 2}
table.sort(t)
```

自定义比较：

```markdown
table.sort(t, function(a, b)
    return a > b
end)
```

注意：这些函数主要面向 **数组型 table** ，不是通用字典。

---

## 18\. 性能和常见误区

## 误区 1：把 table 当稀疏数组大用特用

```markdown
t[1] = "a"
t[1000000] = "b"
```

这可以用，但通常不适合作“数组”思维。更像 map。

## 误区 2：一边 pairs 遍历一边随意修改结构

这可能导致逻辑混乱，虽然有些改动在实现上能工作，但不推荐依赖。

## 误区 3：用 #t 处理有洞数组

这是最常见 bug 来源之一。

## 误区 4：以为 table 比较按内容来

```markdown
print({} == {}) -- false
```

table 默认比较引用身份。

---

## 19\. 深一点：为什么 table 如此重要

Lua 追求“小而强”，没有塞进大量复杂容器类型。  
于是把能力集中到一个结构上：

- 用整数 key ⇒ 数组
- 用字符串 key ⇒ 对象/记录
- 用布尔/任意 key ⇒ map
- 配 metatable ⇒ 类 / 原型 / 运算符重载
- 嵌套 table ⇒ 树 / 配置 / AST / JSON 风格结构

所以很多别的语言有：

- array
- dict
- object
- set
- class instance

在 Lua 里，往往都落到 `table` 上。

---

## 20\. 一组最值得记住的结论

记这 10 条基本就够硬了：

1. `table` 是关联数组，不只是“数组”
2. 数组惯例从 `1` 开始
3. `table` 是引用类型
4. `t.x` 等价于 `t["x"]`
5. `t[k]` 和 `t.k` 不是一回事
6. `nil` 表示删除字段
7. `#t` 只对连续数组可靠
8. `pairs` 无序， `ipairs` 按 1 开始到首个 nil
9. table 默认比较的是身份，不是内容
10. metatable 才是 table 进阶能力核心

---

## 21\. 一个综合例子

```markdown
local Person = {}
Person.__index = Person

function Person.new(name, age)
    local self = setmetatable({}, Person)
    self.name = name
    self.age = age
    return self
end

function Person:say()
    print(("I am %s, %d years old"):format(self.name, self.age))
end

local p1 = Person.new("Alice", 20)
local p2 = Person.new("Bob", 22)

local people = {p1, p2}

for i, p in ipairs(people) do
    p:say()
end
```

这里 table 同时扮演了：

这就是 Lua 风格。

---

## 22\. 学习顺序建议

如果你想真正吃透 Lua table，建议按这个顺序：

1. 基本增删改查
2. `pairs` / `ipairs`
3. 引用语义
4. `#` 和数组洞
5. `table.insert/remove/sort`
6. `:` 语法糖
7. `setmetatable` / `__index`
8. 用 table 实现对象和类

---

如果你愿意，我下一条可以直接继续讲：

- **Lua table 和 metatable 全面深入**
- **Lua table 常见面试题 / 陷阱题**
- **Lua table 在游戏开发里的典型用法**