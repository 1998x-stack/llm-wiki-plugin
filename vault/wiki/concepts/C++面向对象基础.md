---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [cpp, OOP, 类, 对象, 面向对象, C++编程]
aliases: [C++ OOP 基础, C++类与对象, C++ class]
relates_to: [C++, C++基本语法, C++ STL vector]
supersedes: null
---
# C++面向对象基础

## 概述
C++ 用 `class` 定义类，类封装属性（成员变量）和行为（成员函数），通过对象实例化访问；`public`/`private` 控制访问权限。

## 关键内容

1. **类定义结构**：
   ```cpp
   class Person {
   public:
       string name;
       int age;
       void sayHello() {
           cout << "我是 " << name << "，今年 " << age << " 岁。" << endl;
       }
   };
   ```
   `public` 后的成员在类外可直接访问；`private`（默认）则只能在类内访问。

2. **对象实例化**：`Person p;` 创建对象，`p.name = "Alice";` 设置属性，`p.sayHello();` 调用方法。

3. **三大核心概念**：
   - **封装**：属性和方法捆绑在类内，隐藏实现细节。
   - **继承**：子类通过 `: public Base` 继承父类属性和方法，复用代码。
   - **多态**：通过 `virtual` 函数和基类指针/引用实现运行时动态分派。

4. **构造函数**：与类同名、无返回值的特殊函数，在创建对象时自动调用，用于初始化成员；推荐用初始化列表 `Person(string n, int a) : name(n), age(a) {}`。

5. **访问控制关键字**：
   - `public`：任意代码可访问。
   - `private`：仅类内部访问（class 默认）。
   - `protected`：类内部及子类可访问。

## 来源
- [[ChatGPT-C++ 快速入门]] — C++ 快速入门对话，面向对象基础部分

## 相关
- C++ — 语言整体，C++ 支持多范式含 OOP
- [[C++基本语法]] — 前置基础语法知识
- [[C++ STL vector]] — OOP 中常用的标准容器
