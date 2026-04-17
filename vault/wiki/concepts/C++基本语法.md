---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [cpp, 基本语法, 变量, 控制流, 函数, 数组, C++编程]
aliases: [C++ 语法基础, C++ 入门语法, C++变量与类型]
relates_to: [C++, C++指针与引用, C++面向对象基础, C++ STL vector]
supersedes: null
---
# C++基本语法

## 概述
C++ 入门核心：变量与基本类型、输入输出（cin/cout）、条件判断、循环（for/while）、函数定义与调用、数组操作。

## 关键内容

1. **基本类型**：`int`（整数）、`double`（浮点数）、`char`（单字符）、`bool`（真假）、`string`（字符串，需 `<string>`）。变量声明同时可初始化：`int age = 18;`

2. **输入输出**：`cout << value` 输出，`cin >> var` 输入，两者均位于 `<iostream>` 和 `std` 命名空间。`endl` 输出换行并刷新缓冲区，`'\n'` 只换行（性能更好）。

3. **条件判断**：
   ```cpp
   if (score >= 60) { cout << "及格"; }
   else { cout << "不及格"; }
   ```
   注意 `=`（赋值）和 `==`（比较）的区别。

4. **循环**：
   - `for (int i = 0; i < n; i++)` — 计数循环
   - `while (cond)` — 条件循环
   - 范围 for（C++11）：`for (int x : container)` — 遍历容器

5. **函数**：返回类型 + 函数名 + 参数列表 + 函数体，封装可复用逻辑：
   ```cpp
   int add(int a, int b) { return a + b; }
   ```

6. **数组**：固定长度，下标从 0 开始：`int arr[5] = {10, 20, 30, 40, 50};`

7. **常见坑**：整数除整数结果仍为整数（`5/2 == 2`）；数组越界；语句末尾分号必须有。

## 来源
- [[ChatGPT-C++ 快速入门]] — C++ 快速入门对话整理，涵盖基本语法全貌

## 相关
- C++ — 语言整体概述
- [[C++指针与引用]] — 基本语法之后的进阶类型语义
- [[C++面向对象基础]] — 基础语法向 OOP 的延伸
- [[C++ STL vector]] — 替代原始数组的动态容器
