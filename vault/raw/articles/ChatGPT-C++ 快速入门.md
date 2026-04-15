# C++ 快速入门

**User:**   
**Created:** 4/9/2026 10:25:38  
**Updated:** 4/9/2026 10:27:06  
**Exported:** 4/9/2026 10:28:26  
**Link:** [https://chatgpt.com/c/69d70e1f-1920-839b-9371-7cc5d0beec90](https://chatgpt.com/c/69d70e1f-1920-839b-9371-7cc5d0beec90)  

## Prompt:
2026/4/9 10:25:37

c++ 快速入门

## Response:
2026/4/9 10:25:38

> 已思考若干秒

当然，给你一个 **C++ 快速入门版**，尽量用最少的内容带你上手。

* * *

1\. C++ 是什么
===========

C++ 是一种通用编程语言，常用于：

*   系统开发
*   游戏开发
*   高性能服务
*   算法竞赛
*   嵌入式开发

它的特点是：

*   运行快
*   控制力强
*   既支持面向过程，也支持面向对象

* * *

2\. 第一个 C++ 程序
==============

```
#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```

### 解释

*   `#include <iostream>`：引入输入输出库
*   `using namespace std;`：省得每次都写 `std::`
*   `int main()`：程序入口
*   `cout`：输出
*   `endl`：换行
*   `return 0;`：程序正常结束

* * *

3\. 变量和基本类型
===========

```
#include <iostream>
using namespace std;

int main() {
    int age = 18;
    double height = 175.5;
    char grade = 'A';
    bool isStudent = true;
    string name = "Tom";

    cout << name << endl;
    cout << age << endl;
    return 0;
}
```

常见类型：

*   `int`：整数
*   `double`：小数
*   `char`：单个字符
*   `bool`：真假
*   `string`：字符串

* * *

4\. 输入和输出
=========

```
#include <iostream>
using namespace std;

int main() {
    string name;
    int age;

    cout << "请输入姓名：";
    cin >> name;

    cout << "请输入年龄：";
    cin >> age;

    cout << "你好，" << name << "，你今年 " << age << " 岁。" << endl;
    return 0;
}
```

*   `cin`：输入
*   `cout`：输出

* * *

5\. if 判断
=========

```
#include <iostream>
using namespace std;

int main() {
    int score;
    cin >> score;

    if (score >= 60) {
        cout << "及格" << endl;
    } else {
        cout << "不及格" << endl;
    }

    return 0;
}
```

* * *

6\. 循环
======

for 循环
------

```
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 5; i++) {
        cout << i << endl;
    }
    return 0;
}
```

while 循环
--------

```
#include <iostream>
using namespace std;

int main() {
    int i = 1;
    while (i <= 5) {
        cout << i << endl;
        i++;
    }
    return 0;
}
```

* * *

7\. 函数
======

```
#include <iostream>
using namespace std;

int add(int a, int b) {
    return a + b;
}

int main() {
    cout << add(3, 5) << endl;
    return 0;
}
```

函数作用：把一段逻辑封装起来，方便复用。

* * *

8\. 数组
======

```
#include <iostream>
using namespace std;

int main() {
    int arr[5] = {10, 20, 30, 40, 50};

    for (int i = 0; i < 5; i++) {
        cout << arr[i] << " ";
    }

    return 0;
}
```

* * *

9\. 字符串
=======

```
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "hello";
    cout << s.length() << endl;   // 长度
    cout << s[0] << endl;         // 第一个字符
    return 0;
}
```

* * *

10\. 面向对象最基础
============

```
#include <iostream>
using namespace std;

class Person {
public:
    string name;
    int age;

    void sayHello() {
        cout << "我是 " << name << "，今年 " << age << " 岁。" << endl;
    }
};

int main() {
    Person p;
    p.name = "Alice";
    p.age = 20;
    p.sayHello();

    return 0;
}
```

这里你只要先理解：

*   `class`：类
*   类里可以有 **属性** 和 **函数**
*   用对象来调用

* * *

11\. 指针先知道个概念
=============

```
#include <iostream>
using namespace std;

int main() {
    int a = 10;
    int* p = &a;

    cout << a << endl;   // 10
    cout << &a << endl;  // a 的地址
    cout << p << endl;   // 指针里存的地址
    cout << *p << endl;  // 通过指针取值，结果也是 10

    return 0;
}
```

先记住：

*   `&a`：取地址
*   `int* p`：定义指针
*   `*p`：解引用，拿到地址里的值

* * *

12\. 常用 STL 容器：vector
=====================

`vector` 可以理解成“长度可变的数组”。

```
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums = {1, 2, 3};

    nums.push_back(4);

    for (int x : nums) {
        cout << x << " ";
    }

    return 0;
}
```

常用操作：

*   `push_back()`：尾部加元素
*   `size()`：长度
*   `nums[i]`：访问元素

* * *

13\. C++ 学习顺序建议
===============

推荐按这个顺序学：

1.  基本语法：变量、输入输出、判断、循环
2.  函数
3.  数组 / 字符串
4.  指针和引用
5.  `vector`、`string`、`map`
6.  类和对象
7.  文件读写
8.  模板、STL、智能指针
9.  C++11/14/17 新特性

* * *

14\. 初学者最容易踩的坑
==============

### 分号别漏

```
int a = 10;   // 要有分号
```

### 数组下标从 0 开始

```
int arr[3] = {1, 2, 3};
cout << arr[0];   // 1
```

### `=` 和 `==` 不一样

*   `=` 是赋值
*   `==` 是比较

```
if (a == 10) { ... }
```

### 注意类型

```
int a = 5, b = 2;
cout << a / b << endl;   // 2，不是 2.5
```

因为整数除整数还是整数。

* * *

15\. 一个综合小例子
============

输入两个数，输出较大值和它们的和：

```
#include <iostream>
using namespace std;

int maxNum(int a, int b) {
    if (a > b) return a;
    return b;
}

int main() {
    int x, y;
    cin >> x >> y;

    cout << "较大值: " << maxNum(x, y) << endl;
    cout << "和: " << x + y << endl;

    return 0;
}
```

* * *

16\. 你现在至少该会什么
==============

学完上面，你应该能看懂并写出这种代码：

```
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums;
    for (int i = 1; i <= 5; i++) {
        nums.push_back(i);
    }

    int sum = 0;
    for (int x : nums) {
        sum += x;
    }

    cout << "总和是: " << sum << endl;
    return 0;
}
```

* * *

17\. 一句话记忆
==========

C++ 入门核心就这几块：

**变量 + 条件 + 循环 + 函数 + 容器 + 类**

把这几块打通，后面就能继续深入。

* * *

我还可以继续给你整理一版 **“C++ 1 小时速成路线”**，或者 **“适合零基础的 10 道练习题”**。



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)