---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-17
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags:
- 技术
- 研究
- 历史
- 计算理论
- 计算机安全
- 供应链安全
aliases:
- Reflections on Trusting Trust
- Thompson 1984 论文
- 信任信任论文
relates_to:
- target: "[[Ken Thompson]]"
  type: caused_by
  confidence: 0.99
  note: 作者，1983年图灵奖演讲
- target: "[[Dennis Ritchie]]"
  type: related_to
  confidence: 0.85
  note: 同届图灵奖得主
- target: "[[C 语言]]"
  type: depends_on
  confidence: 0.95
  note: 论文中用 C 编译器演示攻击
- target: "[[UNIX]]"
  type: related_to
  confidence: 0.85
  note: 论文中用 UNIX login 程序演示后门
- target: "[[供应链安全]]"
  type: caused
  confidence: 0.95
  note: 开创了供应链安全研究方向
- target: "[[可重现构建]]"
  type: caused
  confidence: 0.85
  note: 推动了可重现构建运动
- target: "[[SolarWinds 攻击]]"
  type: predicted
  confidence: 0.9
  note: 预见了现代供应链攻击模式
- target: "[[多样化双重编译]]"
  type: caused
  confidence: 0.8
  note: 推动了缓解技术发展
- target: "[[形式化验证]]"
  type: caused
  confidence: 0.75
  note: 推动了形式化验证方法
- target: "[[信任模型]]"
  type: influenced
  confidence: 0.9
  note: 重新定义了信任概念
supersedes: null
---

# Thompson 信任信任论文

## 概述

[[Ken Thompson]] 于1984年发表的《Reflections on Trusting Trust》，展示了如何在编译器中植入自我复制的后门木马，揭示了源[[Code-Review-for-Claude-Code|代码审查]]的根本局限性，开创了[[供应链安全]]研究方向。这篇不到三页的演讲成为了计算机安全领域的经典文献，预见了现代供应链攻击的可能性。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Reflections on Trusting Trust |
| **作者** | [[Ken Thompson]] |
| **发表时间** | 1984年8月（1983年[[阿兰·图灵|图灵]]奖演讲） |
| **刊物** | Communications of the ACM, Vol. 27, No. 8, pp. 761-763 |
| **篇幅** | 不到三页 |
| **领域** | 计算机安全、信任、编译器 |

### 历史背景

1983年，Ken Thompson 与 Dennis Ritchie 因共同创造 UNIX 操作系统而获得 ACM 图灵奖。颁奖典礼上，Thompson 用一篇精妙的演讲向整个计算机科学界投下了一颗深水炸弹。当时正值冷战期间，安全研究尚处萌芽阶段，人们对软件供应链的信任几乎是无条件的。Thompson 以一种近乎轻描淡写的方式，揭示了一个根本性的信任困境。

### 三段式论证

1. **自复制程序（Quine）**：程序可以输出自身的源代码，揭示自我描述和复制能力
   - Quine 程序展示了程序具备"自我描述"和"自我复制"的能力
   - 程序将自身的关键部分编码为数据，然后通过逻辑将这些数据"展开"为完整程序文本

2. **编译器知识编码**：编译器的知识可以存在于二进制文件中，而不存在于源代码中
   - 以 C 语言中 \\n 转义字符为例：编译器"知道"\\n 等于换行符这件事，并不完全记录在源代码中
   - 这个知识的一部分存储在编译器的二进制文件里，是通过自举过程从前一代编译器"继承"而来的

3. **编译器木马**：将前两个概念结合，在编译器中植入自我复制的后门
   - 当编译器检测到正在编译 UNIX 的 `login` 程序时，自动插入后门代码
   - 当编译器检测到正在编译自身时，自动复制全部木马逻辑到新编译器中

### 核心攻击方法

#### 攻击实施步骤
1. 修改 C 编译器源代码，添加第一个木马：当编译 UNIX 的 `login` 程序时，自动在二进制文件中插入后门代码
2. 修改 C 编译器源代码，添加第二个木马：当编译自身时，自动复制全部木马逻辑
3. 用干净的编译器编译被修改的源代码，产生第一个被感染的编译器
4. 删除所有修改，将源代码恢复为干净版本
5. 用被感染的编译器编译干净的源代码，新编译器仍包含木马（自复制机制）
6. 用被感染的编译器编译 `login` 程序，自动插入后门
7. 审查所有源代码均显示干净，但后门依然存在

#### 攻击特点
- 木马仅存在于编译器的二进制文件中，不存在于任何源代码中
- 通过编译器自举过程实现代际传播
- 源代码审查、代码差异比较、版本控制都无法检测到此木马

### 深层影响

#### 信任链断裂
传统安全思维的信任链：
> "我审查了源代码 -> 源代码没有问题 -> 所以编译出的程序没有问题。"

Thompson 揭示的实际信任链断裂：
> "我审查了源代码 -> 源代码没有问题 -> 但编译器可能会添加源代码中不存在的东西 -> 所以编译出的程序可能有问题。"

信任链追溯问题：
> 编译器 N 由编译器 N-1 编译，编译器 N-1 由编译器 N-2 编译……在链条的某个起点，必须存在一个"无条件被信任"的二进制文件。

#### 哲学启示
Thompson 将安全问题从技术层面提升到了认识论层面，质疑了"你怎么知道你知道的东西是正确的？"和"你怎么知道你使用的工具是诚实的？"等哲学问题。

### 创新点

1. **揭示源代码审查的根本局限性**：源代码审查只能保证源代码本身没有问题，但无法保证从源代码到可执行程序的转换过程是忠实的
2. **发现编译器作为攻击向量的可能性**：开创了通过攻击开发工具来间接攻击所有由该工具生产的软件的全新攻击思路
3. **将信任从技术问题提升为哲学问题**：使"信任"从简单的二元概念（可信/不可信）演变为分层的、有条件的、可传递的复杂概念
4. **自复制木马的概念**：恶意代码可在二进制层面实现自我复制和跨代传播，而不需要在任何源代码文件中留下痕迹
5. **写作典范**：三段式层层递进的叙事结构，从编程技巧到编译器观察，最终到达安全结论

### 后续影响与缓解方案

#### 历史意义
- 开创了供应链安全研究方向
- 成为安全教科书的必讲内容
- 影响了可信计算技术发展
- 推动了可重现构建运动
- 预见了现代供应链攻击（如 SolarWinds 事件）

#### 现代回应
- **多样化双重编译（Diverse Double-Compiling, DDC）**：用两个独立开发的编译器分别编译同一份源代码，比较生成的二进制文件
- **可重现构建（Reproducible Builds）**：给定相同源代码和构建环境，任何人都应得到逐位相同的二进制文件
- **形式化验证**：如 CompCert 编译器，通过数学证明保证编译器的正确性

### 核心结论

"You can't trust code that you did not totally create yourself."（你无法信任不是你自己完全创建的代码。）

但在现代软件工程中，"完全自己创建"是不可能的。每一个程序员都站在无数前人的工作之上，使用着自己没有完全理解、更不可能完全验证的工具。信任是不可避免的，而信任就意味着风险。

## 来源

- [[raw/books/计算机科学/15-thompson-trusting-trust.md]]
- Thompson, K. (1984). Reflections on Trusting Trust. Communications of the ACM, 27(8), 761--763.
- Wheeler, D. A. (2005). Countering Trusting Trust through Diverse Double-Compiling. PhD dissertation, George Mason University.

## 相关

- [[Ken Thompson]] — 作者
- [[Dennis Ritchie]] — 同届图灵奖
- [[C 语言]] — 演示工具
- [[UNIX]] — 演示目标
- [[供应链安全]] — 开创的方向
- [[可重现构建]] — 对问题的回应
- [[SolarWinds 攻击]] — 现代实例
- [[多样化双重编译]] — 缓解方案
- [[形式化验证]] — 缓解方案
- [[编译器]] — 攻击载体
- [[信任模型]] — 核心概念
