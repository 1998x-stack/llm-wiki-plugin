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
- URL
- Uniform Resource Locator
- 统一资源定位符
- URI
relates_to:
- target: "[[万维网]]"
  type: implements
  confidence: 0.99
  note: 万维网的核心组件
- target: "[[Tim Berners-Lee]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[HTTP]]"
  type: related_to
  confidence: 0.9
  note: URL 中常用的协议
- target: "[[分布式系统]]"
  type: implements
  confidence: 0.8
  note: 为分布式资源统一编址
supersedes: null
---

# URL

## 概述

URL（统一资源定位符）是为全球互联网上的每个信息资源赋予唯一地址的系统，由 [[Tim Berners-Lee]] 于1989年发明。

## 关键内容

### 格式

```
http://info.cern.ch/hypertext/WWW/TheProject.html
 |        |              |
协议    服务器地址      文件路径
```

### 意义

- 在 URL 发明之前，互联网上的资源没有统一的"地址格式"
- URL 统一了 FTP、Gopher、超文本等各种资源的标识方式
- 实质上是对互联网信息空间的**统一编址**，意义堪比经纬度坐标

### 设计哲学

- 任何可以通过网络访问的资源都可以用 URL 标识
- 简单、可扩展、不需要中央注册

## 来源

- [[raw/books/计算机科学/17-berners-lee-www.md]]

## 相关

- [[万维网]] — 核心组件
- [[Tim Berners-Lee]] — 发明者
- [[HTTP]] — 常用协议
- [[分布式系统]] — 为分布式资源编址
