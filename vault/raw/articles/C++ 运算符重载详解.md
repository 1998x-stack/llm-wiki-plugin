---
title: "C++ 运算符重载详解"
source: "https://chatgpt.com/c/69d7126c-18dc-8324-8a31-384f4c173be2"
author:
published:
created: 2026-04-09
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
下面把 C++ 里 `operator<<` 和 `operator>>` 的 **自定义重载** 系统讲清楚，重点放在：

1. 它们到底是什么
2. 为什么通常写成 **非成员函数**
3. 标准写法是什么
4. 常见坑有哪些
5. 给出完整可用示例

---

## 一、先理解这两个运算符本质上在做什么

你最常见到的是：

```markdown
std::cout << x;
std::cin >> x;
```

这其实分别等价于：

```markdown
operator<<(std::cout, x);
operator>>(std::cin, x);
```

不过对标准库流来说，实际更多是调用流对象的重载版本。

### 语义上

- `<<` ：通常表示“把对象输出到流”
- `>>` ：通常表示“从流读取对象”

所以给自定义类型重载它们，本质就是让你的类支持：

```markdown
MyType obj;
std::cout << obj;
std::cin >> obj;
```

---

## 二、为什么它们通常写成非成员函数

很多初学者会写成成员函数：

```markdown
class MyType {
public:
    std::ostream& operator<<(std::ostream& os); // 不推荐
};
```

这通常不对，原因很简单：

### 1）左操作数不是你的类对象，而是流对象

表达式：

```markdown
std::cout << obj;
```

左边是 `std::cout` ，类型是 `std::ostream` 。  
如果你把 `operator<<` 写成 `MyType` 的成员函数，那么调用形式会变成：

```markdown
obj.operator<<(std::cout);
```

这和我们想要的语法完全相反。

### 2）所以一般应该写成非成员函数

标准形式：

```markdown
std::ostream& operator<<(std::ostream& os, const MyType& obj);
std::istream& operator>>(std::istream& is, MyType& obj);
```

这样就能支持：

```markdown
std::cout << obj;
std::cin >> obj;
```

---

## 三、标准推荐签名

## 输出运算符 <<

```markdown
std::ostream& operator<<(std::ostream& os, const MyType& obj);
```

### 为什么这么写

- 返回 `std::ostream&` ：为了支持链式调用
	```markdown
	std::cout << a << b << c;
	```
- 第一个参数是 `std::ostream&` ：输出目标流
- 第二个参数是 `const MyType&` ：输出不应该修改对象，且避免拷贝

---

## 输入运算符 >>

```markdown
std::istream& operator>>(std::istream& is, MyType& obj);
```

### 为什么这么写

- 返回 `std::istream&` ：为了支持链式输入
	```markdown
	std::cin >> a >> b;
	```
- 第一个参数是 `std::istream&` ：输入来源流
- 第二个参数是 `MyType&` ：因为读取会修改对象

---

## 四、最完整的基础示例

假设我们有一个 `Person` 类：

```markdown
#include <iostream>
#include <string>

class Person {
private:
    std::string name;
    int age;

public:
    Person() : name(""), age(0) {}
    Person(std::string n, int a) : name(std::move(n)), age(a) {}

    // 声明为友元，便于访问 private 成员
    friend std::ostream& operator<<(std::ostream& os, const Person& p);
    friend std::istream& operator>>(std::istream& is, Person& p);
};

// 输出重载
std::ostream& operator<<(std::ostream& os, const Person& p) {
    os << "Person{name: " << p.name << ", age: " << p.age << "}";
    return os;
}

// 输入重载
std::istream& operator>>(std::istream& is, Person& p) {
    is >> p.name >> p.age;
    return is;
}

int main() {
    Person p;

    std::cout << "请输入 name 和 age: ";
    std::cin >> p;

    std::cout << p << std::endl;
    return 0;
}
```

### 运行示例

输入：

```markdown
Alice 18
```

输出：

```markdown
Person{name: Alice, age: 18}
```

---

## 五、为什么常常要用 friend

因为很多类成员是 `private` ：

```markdown
class Person {
private:
    std::string name;
    int age;
};
```

而 `operator<<` / `operator>>` 如果写成类外非成员函数，默认 **不能直接访问私有成员** 。

所以常见做法是：

```markdown
friend std::ostream& operator<<(std::ostream& os, const Person& p);
friend std::istream& operator>>(std::istream& is, Person& p);
```

---

## 六、不想用 friend 可以吗

可以。你可以提供公共接口：

```markdown
class Person {
private:
    std::string name;
    int age;

public:
    const std::string& getName() const { return name; }
    int getAge() const { return age; }

    void setName(const std::string& n) { name = n; }
    void setAge(int a) { age = a; }
};

std::ostream& operator<<(std::ostream& os, const Person& p) {
    os << "Person{name: " << p.getName() << ", age: " << p.getAge() << "}";
    return os;
}

std::istream& operator>>(std::istream& is, Person& p) {
    std::string name;
    int age;
    is >> name >> age;
    if (is) {
        p.setName(name);
        p.setAge(age);
    }
    return is;
}
```

### 这种方式的优点

- 降低 `friend` 使用
- 更符合封装思想

### 缺点

- 如果类没有合适的 getter/setter，写起来更麻烦

---

## 七、链式调用为什么一定要返回流引用

比如：

```markdown
std::cout << a << b;
```

它实际等价于：

```markdown
(operator<<(std::cout, a)) << b;
```

所以第一次 `operator<<` 的返回值必须还是一个 `std::ostream&` ，这样才能继续接 `<< b` 。

输入同理：

```markdown
std::cin >> a >> b;
```

如果不返回引用，链式操作就断了。

---

## 八、operator>> 的一个关键点：失败状态处理

输入重载不能只顾着读，还要考虑 **输入失败** 。

例如：

```markdown
std::istream& operator>>(std::istream& is, Person& p) {
    is >> p.name >> p.age;
    return is;
}
```

如果用户输入：

```markdown
Alice abc
```

那么 `age` 读取会失败，流会进入失败状态。

更稳妥的写法是 **先读到临时变量，成功后再赋值** ：

```markdown
std::istream& operator>>(std::istream& is, Person& p) {
    std::string name;
    int age;

    if (is >> name >> age) {
        p.name = name;
        p.age = age;
    }

    return is;
}
```

这样可以避免对象被“读坏一半”。

---

## 九、处理带空格字符串时，>> 往往不够用

`operator>>` 默认按空白分隔。  
比如输入：

```markdown
Tom Hanks 60
```

如果你想把 `Tom Hanks` 当成一个完整名字，直接：

```markdown
is >> p.name >> p.age;
```

会失败，因为 `p.name` 只会读到 `Tom` 。

这时可以结合 `std::getline` ：

```markdown
std::istream& operator>>(std::istream& is, Person& p) {
    std::getline(is >> std::ws, p.name); // 跳过前导空白再读整行
    is >> p.age;
    return is;
}
```

或者约定更清晰的输入格式，比如：

```markdown
Tom_Hanks 60
```

---

## 十、一个更工程化的示例：带格式校验

比如 `Point` 类，输入格式要求是：

```markdown
(3,4)
```

### 实现

```markdown
#include <iostream>

class Point {
private:
    int x, y;

public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    friend std::ostream& operator<<(std::ostream& os, const Point& p);
    friend std::istream& operator>>(std::istream& is, Point& p);
};

std::ostream& operator<<(std::ostream& os, const Point& p) {
    os << '(' << p.x << ',' << p.y << ')';
    return os;
}

std::istream& operator>>(std::istream& is, Point& p) {
    int x, y;
    char ch1, ch2, ch3;

    if (is >> ch1 >> x >> ch2 >> y >> ch3) {
        if (ch1 == '(' && ch2 == ',' && ch3 == ')') {
            p.x = x;
            p.y = y;
        } else {
            is.setstate(std::ios::failbit);
        }
    }

    return is;
}

int main() {
    Point pt;
    std::cin >> pt;

    if (std::cin) {
        std::cout << "读取成功: " << pt << '\n';
    } else {
        std::cout << "输入格式错误\n";
    }
}
```

### 说明

这里最重要的是：

```markdown
is.setstate(std::ios::failbit);
```

它会把流标记为失败，让调用者知道输入不合法。

---

## 十一、模板类怎么重载 << / >>

如果是模板类，例如：

```markdown
template<typename T>
class Box {
private:
    T value;
public:
    Box(T v) : value(v) {}
};
```

可以这样写：

```markdown
#include <iostream>

template<typename T>
class Box {
private:
    T value;

public:
    Box(T v = T{}) : value(v) {}

    template<typename U>
    friend std::ostream& operator<<(std::ostream& os, const Box<U>& box);

    template<typename U>
    friend std::istream& operator>>(std::istream& is, Box<U>& box);
};

template<typename U>
std::ostream& operator<<(std::ostream& os, const Box<U>& box) {
    os << "Box(" << box.value << ")";
    return os;
}

template<typename U>
std::istream& operator>>(std::istream& is, Box<U>& box) {
    is >> box.value;
    return is;
}
```

---

## 十二、成员函数版本什么时候会出现

虽然 **流输入输出重载** 一般是非成员函数，但成员函数版本不是完全不存在。

比如你自己的类，如果你希望支持：

```markdown
obj << something;
obj >> something;
```

那当然可以定义为成员函数：

```markdown
class Buffer {
public:
    Buffer& operator<<(int x) {
        // 写入 buffer
        return *this;
    }
};
```

但这和 `std::cout << obj` 是两回事。

### 记忆方法

- **左边是流对象** ：通常写非成员
- **左边是你自己的对象** ：可以写成员

---

## 十三、常见错误总结

## 错误 1：把 operator<< 写成成员函数去支持 cout << obj

```markdown
class A {
public:
    std::ostream& operator<<(std::ostream& os); // 错
};
```

这不能自然支持：

```markdown
std::cout << obj;
```

---

## 错误 2：返回 void

```markdown
void operator<<(std::ostream& os, const A& a); // 不推荐
```

这样不能链式调用。

---

## 错误 3：输出运算符第二参数不加 const

```markdown
std::ostream& operator<<(std::ostream& os, A& a); // 不好
```

输出通常不修改对象，应写成：

```markdown
std::ostream& operator<<(std::ostream& os, const A& a);
```

否则无法输出 `const` 对象或临时对象。

---

## 错误 4：输入运算符参数传值

```markdown
std::istream& operator>>(std::istream& is, A a); // 错
```

这样修改的是副本，读完原对象没变。

必须传引用：

```markdown
std::istream& operator>>(std::istream& is, A& a);
```

---

## 错误 5：在 operator>> 中直接写入对象，导致部分更新

不安全写法：

```markdown
is >> obj.name >> obj.age;
```

更安全：

```markdown
std::string name;
int age;
if (is >> name >> age) {
    obj.name = name;
    obj.age = age;
}
```

---

## 十四、推荐模板

## 最常用输出模板

```markdown
friend std::ostream& operator<<(std::ostream& os, const MyType& obj) {
    os << obj.some_member;
    return os;
}
```

## 最常用输入模板

```markdown
friend std::istream& operator>>(std::istream& is, MyType& obj) {
    // 可先读入临时变量
    if (is) {
        // 更新 obj
    }
    return is;
}
```

---

## 十五、实际开发建议

### 输出 <<

建议做到：

- 输出格式清晰
- 尽量和调试/日志需求一致
- 不修改对象
- 返回流引用

### 输入 >>

建议做到：

- 格式约定明确
- 尽量有失败检测
- 失败时设置 `failbit`
- 优先“全部读成功后再更新对象”

---

## 十六、一份非常标准的最终写法

```markdown
#include <iostream>
#include <string>

class Person {
private:
    std::string name;
    int age;

public:
    Person(std::string n = "", int a = 0) : name(std::move(n)), age(a) {}

    friend std::ostream& operator<<(std::ostream& os, const Person& p) {
        os << "Person{name=\"" << p.name << "\", age=" << p.age << "}";
        return os;
    }

    friend std::istream& operator>>(std::istream& is, Person& p) {
        std::string name;
        int age;

        if (is >> name >> age) {
            p.name = name;
            p.age = age;
        }

        return is;
    }
};

int main() {
    Person p;

    std::cout << "Input name age: ";
    if (std::cin >> p) {
        std::cout << p << '\n';
    } else {
        std::cerr << "Invalid input\n";
    }
}
```

---

## 十七、一句话记忆

可以直接记这两句：

```markdown
std::ostream& operator<<(std::ostream& os, const T& obj);
std::istream& operator>>(std::istream& is, T& obj);
```

然后记住原因：

- `<<` 输出，不改对象，所以 `const T&`
- `>>` 输入，要改对象，所以 `T&`
- 返回流引用，支持链式调用
- 一般写成非成员，常配合 `friend`

---

## 十八、你可以把它理解成一个固定套路

只要你想让类支持：

```markdown
std::cout << obj;
std::cin >> obj;
```

就优先想到这套：

```markdown
class T {
    friend std::ostream& operator<<(std::ostream& os, const T& obj);
    friend std::istream& operator>>(std::istream& is, T& obj);
};
```

---

如果你愿意，我下一条可以继续给你讲：

**“operator<< / >> 和友元、封装、模板、继承、多态之间的关系”** ，或者直接给你一套 **面试高频问法总结** 。