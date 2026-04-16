---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [C++, 运算符重载, 流, OOP, C++编程]
aliases: [流插入运算符, 流提取运算符, operator<<, operator>>]
relates_to: [C++ iostream, C++流运算符重载实践]
supersedes: null
---
# C++运算符重载与流

## 概述

[[C++ iostream]] 的 `<<`（流插入）和 `>>`（流提取）本质是运算符重载，返回流引用以支持链式调用；自定义类型通过重载这两个运算符即可无缝融入流系统。

## 关键内容

1. **运算符本质**：`std::cout << 123` 等价于 `operator<<(std::cout, 123)`；`std::cin >> x` 等价于 `operator>>(std::cin, x)`。它们不是专用语法，是普通函数调用。

2. **链式调用原理**：每次 `<<`/`>>` 操作均返回流对象自身引用（`ostream&` / `istream&`），因此 `cout << a << b << c` 等价于 `((cout << a) << b) << c`，依次展开。

3. **自定义 `operator<<`**：
   ```cpp
   ostream& operator<<(ostream& os, const Point& p) {
       os << "(" << p.x << ", " << p.y << ")";
       return os;  // 必须返回 os 以支持链式调用
   }
   ```
   函数接收 `ostream&` 而非具体类型，使其同时兼容文件流、字符串流、控制台流。

4. **自定义 `operator>>`**：
   ```cpp
   istream& operator>>(istream& is, Point& p) {
       is >> p.x >> p.y;
       return is;
   }
   ```
   同理返回 `istream&`，支持 `cin >> a >> b` 的链式读取。

5. **流状态位**：`good()`/`eof()`/`fail()`/`bad()` 四种状态；`fail()` 后流停止响应，需 `clear()` + `ignore(...)` 恢复，是健壮输入校验的基础。

6. **必须写成非成员函数**：`<<` 左操作数是 `std::ostream`，若写为成员函数则调用形式变为 `obj.operator<<(cout)`，与 `cout << obj` 语义相反。正确签名：`std::ostream& operator<<(std::ostream&, const T&)`；`std::istream& operator>>(std::istream&, T&)`（输入参数不加 const）。

## 来源

- [[C++ iostream详解]] — 运算符重载原理、自定义类型 IO 重载示例
- [[C++ 运算符重载详解]] — 非成员函数原因、friend 模式、错误处理、模板类重载

## 相关

- [[C++ iostream]] — 运算符重载所属的流系统整体
- [[C++流缓冲区机制]] — 流操作的底层缓冲机制
- [[C++流运算符重载实践]] — 实现模式：friend、封装、错误处理、格式校验
