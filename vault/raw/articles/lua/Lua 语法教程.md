---
title: "Lua 语法教程"
source: "https://chatgpt.com/c/69d65bb9-90a8-8321-bc95-04e5a304d9b7"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
下面给你一份 **Lua 语法初级教程** ，适合从 0 开始快速入门。

---

## Lua 是什么

Lua 是一种轻量、简单、嵌入式友好的脚本语言，常见于：

Lua 的特点是：

---

## 1\. 第一个 Lua 程序

```markdown
print("Hello, Lua!")
```

`print` 用来输出内容。

---

## 2\. 注释

## 单行注释

```markdown
-- 这是单行注释
print("hi")
```

## 多行注释

```markdown
--[[
这是多行注释
可以写很多行
]]
print("hello")
```

---

## 3\. 变量

Lua 不需要声明类型，直接赋值即可。

```markdown
name = "Tom"
age = 18
isStudent = true
```

也可以一次赋多个值：

```markdown
a, b, c = 1, 2, 3
print(a, b, c)
```

## 局部变量

推荐多用 `local` ，避免污染全局变量。

```markdown
local x = 10
print(x)
```

---

## 4\. 数据类型

Lua 常见数据类型：

示例：

```markdown
local a = nil
local b = true
local c = 3.14
local d = "Lua"
```

查看类型：

```markdown
print(type(a))  -- nil
print(type(c))  -- number
print(type(d))  -- string
```

---

## 5\. 字符串

字符串可以用双引号或单引号。

```markdown
local s1 = "hello"
local s2 = 'world'
```

## 字符串拼接

Lua 用 `..` 拼接字符串：

```markdown
local name = "Lua"
print("Hello, " .. name)
```

## 获取字符串长度

```markdown
local s = "abc"
print(#s)   -- 3
```

---

## 6\. 运算符

## 算术运算

```markdown
print(1 + 2)   -- 3
print(5 - 2)   -- 3
print(3 * 4)   -- 12
print(8 / 2)   -- 4
print(7 % 3)   -- 1
print(2 ^ 3)   -- 8
```

## 比较运算

```markdown
print(3 == 3)  -- true
print(3 ~= 4)  -- true
print(5 > 2)   -- true
print(1 < 2)   -- true
```

## 逻辑运算

```markdown
print(true and false) -- false
print(true or false)  -- true
print(not true)       -- false
```

---

## 7\. 条件语句

## if

```markdown
local age = 18

if age >= 18 then
    print("成年人")
end
```

## if else

```markdown
local score = 60

if score >= 60 then
    print("及格")
else
    print("不及格")
end
```

## if elseif else

```markdown
local score = 85

if score >= 90 then
    print("优秀")
elseif score >= 60 then
    print("及格")
else
    print("不及格")
end
```

---

## 8\. 循环

## while

```markdown
local i = 1

while i <= 5 do
    print(i)
    i = i + 1
end
```

## for 数值循环

```markdown
for i = 1, 5 do
    print(i)
end
```

带步长：

```markdown
for i = 1, 10, 2 do
    print(i)
end
```

## repeat until

这个循环至少执行一次。

```markdown
local i = 1

repeat
    print(i)
    i = i + 1
until i > 5
```

---

## 9\. 函数

## 定义函数

```markdown
function sayHello()
    print("Hello")
end

sayHello()
```

## 带参数

```markdown
function add(a, b)
    return a + b
end

print(add(3, 5))
```

## 多返回值

```markdown
function calc(a, b)
    return a + b, a - b
end

local x, y = calc(8, 3)
print(x, y)
```

---

## 10\. Table（表）

Lua 最重要的数据结构就是 `table` 。

它既可以当：

- 数组
- 字典
- 对象

## 当数组用

```markdown
local arr = {10, 20, 30}
print(arr[1])  -- 10
print(arr[2])  -- 20
```

注意： **Lua 下标默认从 1 开始** 。

## 当字典用

```markdown
local user = {
    name = "Tom",
    age = 18
}

print(user.name)
print(user["age"])
```

## 修改表内容

```markdown
user.age = 20
user.city = "Shanghai"
print(user.age, user.city)
```

---

## 11\. 遍历 table

## 遍历数组

```markdown
local arr = {10, 20, 30}

for i, v in ipairs(arr) do
    print(i, v)
end
```

## 遍历键值对

```markdown
local user = {name = "Tom", age = 18}

for k, v in pairs(user) do
    print(k, v)
end
```

---

## 12\. nil

`nil` 表示“没有值”。

```markdown
local x = nil
print(x)
```

也可以用来删除 table 中的字段：

```markdown
local t = {name = "Tom", age = 18}
t.age = nil
print(t.age)   -- nil
```

---

## 13\. 作用域

`local` 变量只在当前作用域有效。

```markdown
local a = 10

do
    local b = 20
    print(a) -- 10
    print(b) -- 20
end

-- print(b) -- 这里会报错，因为 b 不在作用域内
```

---

## 14\. 常用标准函数

## tonumber

把字符串转数字：

```markdown
local s = "123"
local n = tonumber(s)
print(n + 1)   -- 124
```

## tostring

把其他类型转字符串：

```markdown
local n = 100
print("数字是 " .. tostring(n))
```

---

## 15\. 简单综合例子

```markdown
local students = {
    {name = "Alice", score = 90},
    {name = "Bob", score = 75},
    {name = "Cindy", score = 58}
}

for i, student in ipairs(students) do
    if student.score >= 60 then
        print(student.name .. " 及格")
    else
        print(student.name .. " 不及格")
    end
end
```

---

## 16\. 初学者最容易踩的坑

## 1）Lua 数组从 1 开始

```markdown
local arr = {"a", "b", "c"}
print(arr[1]) -- a
```

不是从 0 开始。

## 2）字符串拼接不是 +

错误写法：

```markdown
-- print("hello" + "world")
```

正确写法：

```markdown
print("hello" .. "world")
```

## 3）比较不等于是 ~=

```markdown
print(3 ~= 4)
```

不是 `!=` 。

## 4）尽量使用 local

```markdown
local x = 10
```

这样代码更安全，也更容易维护。

---

## 17\. 学完这一篇后你应该会什么

你现在应该已经知道：

- 怎么定义变量
- 怎么写条件和循环
- 怎么写函数
- 怎么使用 table
- 怎么遍历数据

这些已经足够你开始写简单 Lua 脚本了。

---

## 18\. 下一步建议

建议按这个顺序继续学：

1. table 深入
2. 字符串库
3. 模块与 `require`
4. 面向对象写法
5. 元表（metatable）

---

我也可以继续给你整理一份 **“Lua 语法初级教程 + 练习题版”** ，让你边学边做。

下面给你一份 **Lua 语法初级教程 + 练习题版** 。我会按 **知识点 → 例子 → 练习题** 的方式来讲，适合初学者边学边练。

---

## Lua 语法初级教程 + 练习题版

## 1\. 第一个 Lua 程序

Lua 输出内容用 `print()` 。

```markdown
print("Hello, Lua!")
```

运行后会输出：

```markdown
Hello, Lua!
```

### 练习 1

自己写一段代码，输出：

```markdown
I am learning Lua
```

---

## 2\. 注释

注释是给人看的，程序不会执行。

### 单行注释

```markdown
-- 这是一行注释
print("Lua")
```

### 多行注释

```markdown
--[[
这是多行注释
可以写很多内容
]]
print("Hello")
```

### 练习 2

写一段 Lua 代码，里面同时包含：

- 一行单行注释
- 一段多行注释
- 一个 `print("test")`

---

## 3\. 变量

Lua 是动态类型语言，变量直接赋值即可。

```markdown
name = "Tom"
age = 18
score = 95.5
```

也可以一次赋多个值：

```markdown
a, b, c = 1, 2, 3
print(a, b, c)
```

### 局部变量

推荐使用 `local` ：

```markdown
local name = "Alice"
local age = 20
print(name, age)
```

### 为什么推荐 local

因为不用 `local` 时，变量通常会变成全局变量，不利于维护。

### 练习 3

定义三个变量：

- `name = "Jack"`
- `age = 16`
- `city = "Beijing"`

然后输出这三个变量。

---

## 4\. 数据类型

Lua 常见数据类型有：

- `nil`
- `boolean`
- `number`
- `string`
- `table`
- `function`

示例：

```markdown
local a = nil
local b = true
local c = 123
local d = 3.14
local e = "hello"
```

查看类型可以用 `type()` ：

```markdown
print(type(a))  -- nil
print(type(b))  -- boolean
print(type(c))  -- number
print(type(e))  -- string
```

### 练习 4

定义 4 个变量，分别是：

- 一个数字
- 一个字符串
- 一个布尔值
- 一个空值

然后分别用 `type()` 输出它们的类型。

---

## 5\. 字符串

字符串可以用单引号或双引号。

```markdown
local s1 = "hello"
local s2 = 'world'
```

### 字符串拼接

Lua 用 `..` 拼接字符串：

```markdown
local name = "Lua"
print("Hello, " .. name)
```

### 字符串长度

```markdown
local s = "abcdef"
print(#s)   -- 6
```

### 练习 5

定义变量：

```markdown
local firstName = "Zhang"
local lastName = "San"
```

把它们拼接成：

```markdown
ZhangSan
```

再输出这个字符串的长度。

---

## 6\. 算术运算符

Lua 常见算术运算符：

- `+` 加
- `-` 减
- `*` 乘
- `/` 除
- `%` 取余
- `^` 幂

示例：

```markdown
print(1 + 2)   -- 3
print(5 - 3)   -- 2
print(4 * 2)   -- 8
print(8 / 2)   -- 4
print(7 % 3)   -- 1
print(2 ^ 3)   -- 8
```

### 练习 6

已知：

```markdown
local a = 10
local b = 3
```

输出：

- `a + b`
- `a - b`
- `a * b`
- `a / b`
- `a % b`

---

## 7\. 比较运算符和逻辑运算符

### 比较运算符

- `==` 等于
- `~=` 不等于
- `>`
- `<`
- `>=`
- `<=`
```markdown
print(5 == 5)   -- true
print(5 ~= 3)   -- true
print(5 > 3)    -- true
```

### 逻辑运算符

- `and`
- `or`
- `not`
```markdown
print(true and false) -- false
print(true or false)  -- true
print(not true)       -- false
```

### 练习 7

判断下面表达式结果是什么：

```markdown
print(10 > 5 and 3 < 1)
print(10 > 5 or 3 < 1)
print(not (10 > 5))
```

先自己猜，再运行验证。

---

## 8\. if 条件语句

### 基本写法

```markdown
local age = 20

if age >= 18 then
    print("成年人")
end
```

### if else

```markdown
local score = 59

if score >= 60 then
    print("及格")
else
    print("不及格")
end
```

### if elseif else

```markdown
local score = 85

if score >= 90 then
    print("优秀")
elseif score >= 60 then
    print("及格")
else
    print("不及格")
end
```

### 练习 8

写一个程序，定义变量 `score` ，并按下面规则输出：

- 90 分及以上输出 `优秀`
- 60 到 89 输出 `及格`
- 60 以下输出 `不及格`

---

## 9\. while 循环

```markdown
local i = 1

while i <= 5 do
    print(i)
    i = i + 1
end
```

输出 1 到 5。

### 练习 9

用 `while` 循环输出：

```markdown
2
4
6
8
10
```

---

## 10\. for 循环

### 数值 for

```markdown
for i = 1, 5 do
    print(i)
end
```

### 带步长

```markdown
for i = 1, 10, 2 do
    print(i)
end
```

会输出：

```markdown
1
3
5
7
9
```

### 练习 10

用 `for` 循环完成：

1. 输出 1 到 10
2. 输出 10 到 1
3. 输出 5 的乘法表前 10 项，即 `5 10 15 ... 50`

---

## 11\. repeat until

这个循环至少会执行一次。

```markdown
local i = 1

repeat
    print(i)
    i = i + 1
until i > 5
```

### 练习 11

用 `repeat until` 输出 3 到 7。

---

## 12\. 函数

### 定义函数

```markdown
function sayHello()
    print("Hello")
end

sayHello()
```

### 带参数函数

```markdown
function add(a, b)
    return a + b
end

print(add(3, 4))
```

### 多返回值

```markdown
function calc(a, b)
    return a + b, a - b
end

local x, y = calc(8, 2)
print(x, y)
```

### 练习 12

写 3 个函数：

1. `square(x)` 返回平方
2. `max(a, b)` 返回较大的数
3. `hello(name)` 输出 `Hello, xxx`

---

## 13\. table 表

Lua 最核心的数据结构就是 `table` 。

它既可以当数组，也可以当字典。

---

### 13.1 当数组使用

```markdown
local arr = {10, 20, 30}
print(arr[1])  -- 10
print(arr[2])  -- 20
print(arr[3])  -- 30
```

注意： **Lua 下标从 1 开始，不是从 0 开始。**

### 练习 13-1

定义数组：

```markdown
local fruits = {"apple", "banana", "orange"}
```

输出第二个元素。

---

### 13.2 当字典使用

```markdown
local user = {
    name = "Tom",
    age = 18,
    city = "Shanghai"
}

print(user.name)
print(user["age"])
```

### 修改字段

```markdown
user.age = 20
user.job = "student"
print(user.age, user.job)
```

### 练习 13-2

定义一个 `book` 表，包含：

- `title`
- `price`
- `author`

然后输出这三个字段。

---

## 14\. 遍历 table

### 遍历数组：ipairs

```markdown
local arr = {100, 200, 300}

for i, v in ipairs(arr) do
    print(i, v)
end
```

### 遍历键值对：pairs

```markdown
local user = {
    name = "Tom",
    age = 18
}

for k, v in pairs(user) do
    print(k, v)
end
```

### 练习 14

1. 用 `ipairs` 遍历数组 `{5, 10, 15, 20}`
2. 用 `pairs` 遍历表 `{name="Lucy", age=22, city="Shenzhen"}`

---

## 15\. nil

`nil` 表示空值。

```markdown
local x = nil
print(x)
```

也可以删除表中的字段：

```markdown
local t = {name = "Tom", age = 18}
t.age = nil
print(t.age)   -- nil
```

### 练习 15

定义：

```markdown
local user = {name="Mike", age=20}
```

然后把 `age` 删除，再输出 `user.age` 。

---

## 16\. 作用域

`local` 定义的变量只在当前作用域有效。

```markdown
local a = 10

do
    local b = 20
    print(a)
    print(b)
end
```

出了 `do ... end` 后， `b` 就不能用了。

### 练习 16

自己写一个 `do ... end` 代码块，里面定义一个局部变量 `x = 100` ，在块内输出它。

---

## 17\. 常用类型转换

### tonumber()

把字符串转数字：

```markdown
local s = "123"
local n = tonumber(s)
print(n + 1)
```

### tostring()

把数字转字符串：

```markdown
local n = 456
print("数字是：" .. tostring(n))
```

### 练习 17

1. 把 `"88"` 转成数字后加 12
2. 把数字 `999` 转成字符串并拼接到 `"结果是："` 后面

---

## 18\. 综合小案例

### 案例：判断学生成绩

```markdown
local students = {
    {name = "Alice", score = 90},
    {name = "Bob", score = 75},
    {name = "Cindy", score = 58}
}

for i, student in ipairs(students) do
    if student.score >= 60 then
        print(student.name .. " 及格")
    else
        print(student.name .. " 不及格")
    end
end
```

### 练习 18

仿照上面的例子，自己定义 3 个学生的数据，并输出每个人是“及格”还是“不及格”。

---

## 初学者常见错误

## 1\. 数组下标写成 0

错误：

```markdown
local arr = {"a", "b", "c"}
print(arr[0])
```

Lua 通常从 1 开始。

正确：

```markdown
print(arr[1])
```

---

## 2\. 用 + 拼接字符串

错误：

```markdown
-- print("hello" + "world")
```

正确：

```markdown
print("hello" .. "world")
```

---

## 3\. 不等于写成!=

错误：

```markdown
-- print(3 != 4)
```

正确：

```markdown
print(3 ~= 4)
```

---

## 4\. 忘记 then 或 do

例如：

```markdown
if age >= 18 then
    print("成年人")
end
```
```markdown
for i = 1, 5 do
    print(i)
end
```

---

## 自测小作业

你可以尝试独立完成下面 5 题。

## 作业 1

定义两个变量 `a = 15` 、 `b = 4` ，输出它们的和、差、积、商、余数。

## 作业 2

定义一个变量 `age` ，判断是否成年。

## 作业 3

用 `for` 循环输出 1 到 100 中所有偶数。

## 作业 4

定义一个函数 `isEven(n)` ，如果是偶数返回 `true` ，否则返回 `false` 。

## 作业 5

定义一个数组 `{3, 6, 9, 12}` ，遍历并输出每个元素。

---

## 练习题参考答案

## 练习 1 参考答案

```markdown
print("I am learning Lua")
```

## 练习 3 参考答案

```markdown
local name = "Jack"
local age = 16
local city = "Beijing"

print(name, age, city)
```

## 练习 5 参考答案

```markdown
local firstName = "Zhang"
local lastName = "San"
local fullName = firstName .. lastName

print(fullName)
print(#fullName)
```

## 练习 8 参考答案

```markdown
local score = 85

if score >= 90 then
    print("优秀")
elseif score >= 60 then
    print("及格")
else
    print("不及格")
end
```

## 练习 9 参考答案

```markdown
local i = 2

while i <= 10 do
    print(i)
    i = i + 2
end
```

## 练习 10 参考答案

```markdown
for i = 1, 10 do
    print(i)
end

for i = 10, 1, -1 do
    print(i)
end

for i = 1, 10 do
    print(5 * i)
end
```

## 练习 12 参考答案

```markdown
function square(x)
    return x * x
end

function max(a, b)
    if a > b then
        return a
    else
        return b
    end
end

function hello(name)
    print("Hello, " .. name)
end
```

## 练习 14 参考答案

```markdown
local arr = {5, 10, 15, 20}
for i, v in ipairs(arr) do
    print(i, v)
end

local user = {name="Lucy", age=22, city="Shenzhen"}
for k, v in pairs(user) do
    print(k, v)
end
```

---

## 学完这份后，下一步建议学什么

建议继续按这个顺序学：

---

我还可以继续帮你整理一份 **“Lua 初级 20 道练习题 + 详细答案”** 。

Is this conversation helpful so far?