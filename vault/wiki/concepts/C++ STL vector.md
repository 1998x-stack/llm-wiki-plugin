---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [cpp, STL, vector, 容器, 动态数组, C++编程]
aliases: [std::vector, C++ vector, vector容器]
relates_to: [C++, C++基本语法, C++面向对象基础]
supersedes: null
---
# C++ STL vector

## 概述
`std::vector` 是 C++ 标准库中最常用的动态数组容器，支持自动扩容、随机访问（O(1)）和尾部高效插入/删除，替代原始固定数组的首选。

## 关键内容

1. **基本用法**：
   ```cpp
   #include <vector>
   vector<int> nums = {1, 2, 3};
   nums.push_back(4);          // 尾部追加
   cout << nums[0];            // 随机访问，O(1)
   cout << nums.size();        // 元素数量
   ```

2. **常用操作**：
   - `push_back(x)` — 尾部追加元素（均摊 O(1)）
   - `pop_back()` — 删除尾部元素
   - `size()` — 元素个数
   - `empty()` — 判断是否为空
   - `clear()` — 清空所有元素
   - `front()` / `back()` — 首/尾元素引用

3. **范围 for 遍历**（C++11）：
   ```cpp
   for (int x : nums) { cout << x << " "; }
   ```

4. **与原始数组对比**：
   - vector：动态大小，自动内存管理，支持拷贝/赋值，有边界检查（`.at(i)`）。
   - 原始数组：固定大小，手动管理，不可直接拷贝。

5. **STL 容器全家桶**（初学路径）：`vector`（动态数组）→ `string`（字符串）→ `map`（键值映射）→ `set`（不重复集合）→ `queue`/`stack`（队列/栈）。

6. **内部机制**：capacity（已分配空间）与 size（实际元素数）分离；扩容时通常翻倍，避免频繁重分配。

## 来源
- [[ChatGPT-C++ 快速入门]] — C++ 快速入门对话，STL vector 基础用法

## 相关
- C++ — 语言整体及标准库体系
- [[C++基本语法]] — 前置语法（数组、循环）
- [[C++面向对象基础]] — 泛型容器与 OOP 结合使用
