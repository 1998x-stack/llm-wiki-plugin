---
type: entity
entity_type: tool
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [C++, 标准库, 输入输出, 流, C++编程]
aliases: [iostream, C++标准IO库]
relates_to: [C++流缓冲区机制, C++运算符重载与流]
supersedes: null
---
# C++ iostream

## 概述

[[C++]] 标准库中用于输入输出的流系统，提供类型安全、可扩展、可格式化的 IO 抽象，核心由流对象、运算符重载和状态格式控制三部分构成。

## 关键内容

1. **四个核心流对象**：`std::cin`（标准输入）、`std::cout`（标准输出）、`std::cerr`（错误输出，无缓冲/及时）、`std::clog`（日志输出，有缓冲）；在 shell 重定向时 `cerr` 仍输出到终端而 `cout` 进文件。

2. **类层次体系**：`ios_base` → `basic_ios<charT>` → `basic_istream` / `basic_ostream` / `basic_iostream`，`istream`/`ostream`/`iostream` 是 `char` 版本别名；`fstream`（文件流）和 `sstream`（字符串流）同属此体系，用法与控制台流一致。

3. **性能调优**：`std::ios::sync_with_stdio(false)` 关闭与 C stdio 的同步；`std::cin.tie(nullptr)` 解除 cin/cout 的自动刷新绑定；关闭后禁止与 `scanf`/`printf` 混用，否则输出顺序异常。

4. **cin 读取规则与陷阱**：`>>` 跳过前导空白并以空白截断，读完整行须用 `getline`；混用时需 `cin.ignore()` 丢弃残留换行；输入失败后流进入 `fail()` 状态，后续读取持续失败，需 `cin.clear()` + `cin.ignore(...)` 恢复。

5. **格式控制（`<iomanip>`）**：`setw`（宽度）、`setfill`（填充字符）、`setprecision`（精度）、`fixed`/`scientific`（浮点格式）、`hex`/`oct`/`dec`（进制）、`boolalpha`（布尔显示）。

## 来源

- [[C++ iostream详解]] — ChatGPT 对话，iostream 系统展开讲解，含缓冲区原理与格式化输出

## 相关

- [[C++流缓冲区机制]] — iostream 的缓冲与刷新原理
- [[C++运算符重载与流]] — `<<` / `>>` 运算符重载实现与链式调用
