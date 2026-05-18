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
- Diffie-Hellman Key Exchange
- DH 密钥交换
- DHKE
relates_to:
- target: "[[Diffie-Hellman 论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次提出
- target: "[[Whitfield Diffie]]"
  type: caused_by
  confidence: 0.99
  note: 共同发明者
- target: "[[Martin Hellman]]"
  type: caused_by
  confidence: 0.99
  note: 共同发明者
- target: "[[公钥密码学]]"
  type: implements
  confidence: 0.95
  note: 第一个公钥密钥交换方案
- target: "[[离散对数问题]]"
  type: depends_on
  confidence: 0.99
  note: 安全性基于离散对数问题的困难性
- target: "[[中间人攻击]]"
  type: related_to
  confidence: 0.85
  note: DH 协议缺乏身份认证，易受中间人攻击
- target: "[[后量子密码学]]"
  type: related_to
  confidence: 0.8
  note: Shor 算法威胁 DH 协议
- target: "[[TCP-IP]]"
  type: implements
  confidence: 0.85
  note: TLS 使用 ECDHE 进行密钥交换
supersedes: null
---

# Diffie-Hellman 密钥交换

## 概述

Diffie-Hellman 密钥交换是人类历史上第一个公钥密钥交换协议，基于[[离散对数问题]]的数学困难性，使得两个从未谋面的人可以通过公开信道建立共享秘密。

## 关键内容

### 协议过程

1. **公开参数**：双方公开选定大素数 p 和原根 g
2. **各自生成秘密**：Alice 选随机数 a，[[计算]] A = g^a mod p；Bob 选随机数 b，[[计算]] B = g^b mod p
3. **交换公开值**：Alice 发送 A 给 Bob，Bob 发送 B 给 Alice
4. **[[计算]]共享密钥**：Alice [[计算]] K = B^a mod p = g^{ab} mod p；Bob [[计算]] K = A^b mod p = g^{ab} mod p

### 安全性

窃听者能看到 p、g、A、B，但要[[计算]] K = g^{ab} mod p，需要从 A 或 B 中恢复 a 或 b——这正是**[[离散对数问题]]**，目前没有已知的多项式时间经典[[算法]]。

### 弱点

**[[中间人攻击]]**：协议缺乏身份认证，主动攻击者可以分别与双方建立独立的共享密钥，冒充对方进行通信。

### 现代应用

- **ECDHE**（椭圆曲线变体）是 TLS 1.3 中唯一支持的密钥交换机制
- 全球每天数十亿次 [[TLS协议|HTTPS]] 连接依赖此协议
- SSH、IPsec 等安全协议也使用 DH 密钥交换

## 来源

- [[raw/books/计算机科学/11-diffie-hellman-new-directions.md]]

## 相关

- [[Diffie-Hellman 论文]] — 首次提出
- [[Whitfield Diffie]] — 共同发明者
- [[Martin Hellman]] — 共同发明者
- [[公钥密码学]] — 第一个方案
- [[离散对数问题]] — 安全性基础
- [[中间人攻击]] — 缺乏身份认证
- [[后量子密码学]] — Shor 算法威胁
- [[TCP-IP]] — TLS 使用 ECDHE
