---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [Lua, 编程语言, 数据结构, Lua编程]
aliases: [Lua关联数组, Lua哈希表]
relates_to: [Lua-metatable, Lua-OOP, lua-language-server]
supersedes: null
---
# Lua table

## 概述
Lua 唯一的复合数据结构，本质是关联数组，同时充当数组、字典、对象、集合等多种角色。

## 关键内容
1. **双区存储**：实现层将连续正整数键放入 array part，其余键放入 hash part。连续整数索引访问性能最优，惯例下标从 1 开始。
2. **引用语义**：赋值与传参传递的是引用，不会复制内容。浅拷贝需手动 `for k,v in pairs(src) do dst[k]=v end`；深拷贝需递归处理。
3. **nil 即删除**：给字段赋 `nil` 等同于删除该键，无法区分"字段不存在"与"值为 nil"。需要空值语义时使用哨兵对象 `local NULL = {}`。
4. **# 运算符限制**：`#t` 仅对无洞连续整数序列有确定结果。稀疏数组或有洞数组不可依赖 `#`。
5. **遍历**：`pairs` 遍历全部键值，顺序不保证；`ipairs` 从 1 开始按整数顺序遍历，遇首个 nil 停止。`next(t, key)` 是底层原语，`pairs` 依赖它实现。
6. **点语法糖**：`t.name` 等价于 `t["name"]`，但 `t.key` 与 `t[key]` 语义不同——前者取字面字段 "key"，后者取变量 key 的值对应的字段。
7. **标准库操作**：`table.insert(t, pos, v)` / `table.remove(t, pos)` / `table.sort(t, cmp)` 均面向数组型 table，不适用于字典表。
8. **key 规则**：除 `nil` 与 `NaN` 外均可做 key；table 作为 key 时按引用身份比较，内容相同的不同 table 是不同的 key。

## 来源
- [[Lua table 深入解析]] — ChatGPT 对话，Lua table 全面解析，涵盖内部结构、常见陷阱与使用模式

## 相关
- [[Lua-metatable]] — metatable 是 table 的进阶能力核心，通过元方法改变 table 行为
- [[Lua-OOP]] — 用 table + metatable 实现面向对象编程
- [[lua-language-server]] — Lua 语言服务器，提供 table 类型检查支持
