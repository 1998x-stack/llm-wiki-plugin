---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 历史
- 计算理论
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
- target: "[[量子密码学]]"
  type: compares_to
  confidence: 0.5
  note: 两者都涉及信任的根本性问题
supersedes: null
---

# Thompson 信任信任论文

## 概述

[[Ken Thompson]] 于1984年发表的《Reflections on Trusting Trust》，展示了如何在编译器中植入自我复制的后门木马，揭示了源[[Code-Review-for-Claude-Code|代码审查]]的根本局限性，开创了[[供应链安全]]研究方向。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Reflections on Trusting Trust |
| **作者** | [[Ken Thompson]] |
| **发表时间** | 1984年8月（1983年[[阿兰·图灵|图灵]]奖演讲） |
| **刊物** | Communications of the ACM, Vol. 27, No. 8, pp. 761-763 |
| **篇幅** | 不到三页 |

### 三段式论证

1. **自复制程序（Quine）**：程序可以输出自身的源代码，揭示自我描述和复制能力
2. **编译器知识编码**：编译器的知识可以存在于二进制文件中，而不存在于源代码中
3. **编译器木马**：将前两个概念结合，在编译器中植入自我复制的后门

### 核心攻击

- 修改编译器，当编译 login 程序时自动插入后门
- 修改编译器，当编译自身时自动复制后门逻辑
- 恢复干净源代码后，木马仍通过编译过程代际传播
- 源[[Code-Review-for-Claude-Code|代码审查]]无法检测到任何异常

### 核心结论

> "You can't trust code that you did not totally create yourself."
> （你无法信任不是你自己完全创建的代码。）

### 历史影响

- 开创了[[供应链安全]]研究方向
- 预见了 SolarWinds 级别的现代供应链攻击
- 推动了[[可重现构建]]运动和多样化双重编译
- 至今仍是安全教育的必读文献

## 来源

- [[raw/books/计算机科学/15-thompson-trusting-trust.md]]

## 相关

- [[Ken Thompson]] — 作者
- [[Dennis Ritchie]] — 同届图灵奖
- [[C 语言]] — 演示工具
- [[UNIX]] — 演示目标
- [[供应链安全]] — 开创的方向
- [[可重现构建]] — 对问题的回应
