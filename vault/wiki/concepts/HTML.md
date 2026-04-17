---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 计算理论
aliases:
- HTML
- HyperText Markup Language
- 超文本标记语言
relates_to:
- target: "[[万维网]]"
  type: implements
  confidence: 0.99
  note: 万维网的核心组件
- target: "[[Tim Berners-Lee]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[URL]]"
  type: depends_on
  confidence: 0.9
  note: HTML 中的超链接使用 URL
- target: "[[HTTP]]"
  type: depends_on
  confidence: 0.9
  note: HTML 文档通过 HTTP 传输
supersedes: null
---

# HTML

## 概述

HTML（超文本标记语言）定义了 Web 文档的结构和链接方式，脱胎于 SGML 但做了大幅简化，使得没有编程经验的人也能写出网页。

## 关键内容

### 基本结构

```html
<html>
<head><title>我的页面</title></head>
<body>
<h1>欢迎</h1>
<p>这是一个 <a href="http://info.cern.ch">链接</a>。</p>
</body>
</html>
```

### 设计哲学

- 脱胎于 SGML，但大幅简化
- 只保留最基本的文档结构元素
- 去掉了 SGML 中复杂的模式定义和验证机制

### 后续发展

- **1996年**：CSS 发布，Web 具备视觉设计能力
- **1997年**：HTML 4.0 发布
- **2014年**：HTML5 成为 W3C 推荐标准

## 来源

- [[raw/books/计算机科学/17-berners-lee-www.md]]

## 相关

- [[万维网]] — 核心组件
- [[Tim Berners-Lee]] — 发明者
- [[URL]] — 超链接使用
- [[HTTP]] — 传输协议
