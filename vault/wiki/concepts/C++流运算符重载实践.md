---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [C++, 运算符重载, 流, OOP, 最佳实践, C++编程]
aliases: [流运算符实践, operator<<实现, operator>>实现]
relates_to: [C++运算符重载与流, C++流缓冲区机制, C++指针与引用]
supersedes: null
---
# C++流运算符重载实践

## 概述

`operator<<` / `operator>>` 的标准实现模式：非成员函数 + friend 声明；输入重载须先读临时变量再赋值，避免部分更新；模板类需额外模板化友元声明。

## 关键内容

### 1. 标准签名

```cpp
std::ostream& operator<<(std::ostream& os, const MyType& obj);  // 输出：const T&
std::istream& operator>>(std::istream& is, MyType& obj);        // 输入：T&（非 const）
```

- 输出返回 `ostream&`，输入返回 `istream&`，均为链式调用所必须
- 第二参数：输出加 `const`（不修改对象），输入不加 `const`（读入会修改对象）

### 2. friend 声明模式

类成员为私有时，将运算符声明为 friend：

```cpp
class Person {
    std::string name;
    int age;
public:
    friend std::ostream& operator<<(std::ostream& os, const Person& p);
    friend std::istream& operator>>(std::istream& is, Person& p);
};
```

不想用 friend 可暴露 getter/setter，但需要类提供足够的公共接口。

### 3. 输入安全模式：先读临时变量

直接写入对象成员会导致"读坏一半"问题（读取中途失败时对象处于中间状态）：

```cpp
// 不安全
istream& operator>>(istream& is, Person& p) { is >> p.name >> p.age; return is; }

// 安全：先读临时变量，成功后再赋值
istream& operator>>(istream& is, Person& p) {
    std::string name; int age;
    if (is >> name >> age) { p.name = name; p.age = age; }
    return is;
}
```

### 4. 格式校验与 failbit

需要严格输入格式时，校验失败后调用 `is.setstate(std::ios::failbit)` 通知调用者：

```cpp
istream& operator>>(istream& is, Point& p) {
    int x, y; char c1, c2, c3;
    if (is >> c1 >> x >> c2 >> y >> c3) {
        if (c1 == '(' && c2 == ',' && c3 == ')')
            p.x = x, p.y = y;
        else
            is.setstate(std::ios::failbit);
    }
    return is;
}
```

### 5. 含空格字符串：结合 getline

`[[C++运算符重载与流|operator>>]]` 默认按空白分隔，读取含空格的字符串需用 `std::getline`：

```cpp
istream& operator>>(istream& is, Person& p) {
    std::getline(is >> std::ws, p.name);  // 跳过前导空白后读整行
    is >> p.age;
    return is;
}
```

### 6. 模板类重载

模板类需用模板化友元声明（避免只友好特定实例化）：

```cpp
template<typename T>
class Box {
    T value;
public:
    template<typename U>
    friend std::ostream& operator<<(std::ostream& os, const Box<U>& box);
    template<typename U>
    friend std::istream& operator>>(std::istream& is, Box<U>& box);
};
```

### 7. 成员函数版本的适用场景

仅当**左操作数是自己的类对象**时才写成员函数（如自定义 Buffer 类）：

```cpp
class Buffer {
public:
    Buffer& operator<<(int x) { /* write to buffer */ return *this; }
};
```
这与 `std::cout << obj` 场景完全不同。

### 8. 常见错误

| 错误 | 后果 |
|------|------|
| `[[C++运算符重载与流|operator<<]]` 写成成员函数 | `obj.[[C++运算符重载与流|operator<<]](cout)` 语义反转 |
| 返回 void | 无法链式调用 |
| 输出参数不加 const | 无法输出 const 对象或临时对象 |
| 输入参数传值（非引用） | 修改副本，原对象不变 |
| 输入直接写对象成员 | 失败时对象处于中间状态 |

## 来源

- [[C++ 运算符重载详解]] — 完整重载实践指南，含多示例和错误总结

## 相关

- [[C++运算符重载与流]] — 运算符重载机制原理
- [[C++流缓冲区机制]] — 流的底层缓冲实现
- C++ — C++ 语言整体
