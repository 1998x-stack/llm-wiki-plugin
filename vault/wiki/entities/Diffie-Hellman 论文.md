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
- New Directions in Cryptography
- Diffie-Hellman 1976 论文
- 公钥密码学论文
relates_to:
- target: "[[Whitfield Diffie]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者
- target: "[[Martin Hellman]]"
  type: caused_by
  confidence: 0.99
  note: 第二作者
- target: "[[公钥密码学]]"
  type: caused
  confidence: 0.99
  note: 首次提出公钥密码学概念
- target: "[[Diffie-Hellman 密钥交换]]"
  type: caused
  confidence: 0.99
  note: 首次提出具体协议
- target: "[[数字签名]]"
  type: caused
  confidence: 0.95
  note: 首次提出数字签名概念框架
- target: "[[单向陷门函数]]"
  type: caused
  confidence: 0.9
  note: 论文中引入的数学基础
- target: "[[后量子密码学]]"
  type: related_to
  confidence: 0.7
  note: 量子计算威胁了论文中的数学假设
- target: "[[信息论]]"
  type: extends
  confidence: 0.7
  note: Shannon 1949年论文是唯一的理论里程碑
- target: "[[计算复杂度理论]]"
  type: depends_on
  confidence: 0.85
  note: 将密码学安全性建立在计算复杂度上
supersedes: null
---

# Diffie-Hellman 论文

## 概述

[[Whitfield Diffie]] 和 [[Martin Hellman]] 于1976年发表的《New Directions in Cryptography》，首次提出了[[公钥密码学]]的完整概念框架和 [[Diffie-Hellman 密钥交换]]协议，开创了现代密码学新纪元。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | New Directions in Cryptography |
| **作者** | [[Whitfield Diffie]], Martin E. Hellman |
| **发表时间** | 1976年11月 |
| **期刊** | IEEE Transactions on [[信息论|Information Theory]], Vol. 22, No. 6, pp. 644-654 |

### 核心贡献

- **[[公钥密码学]]概念**：加密和解密使用不同的、在[[计算]]上不可互推的密钥
- **[[Diffie-Hellman 密钥交换]]协议**：基于[[离散对数问题]]的第一个公钥密钥交换方案
- **[[数字签名]]概念框架**：认证性、完整性、不可否认性
- **[[单向陷门函数]]**：将密码学安全性建立在[[计算复杂度理论]]上

### 历史影响

- 1977年：RSA [[算法]]填补了公钥加密和签名的具体构造
- 1985年：椭圆曲线密码学（ECC）
- 2015年：Diffie 和 Hellman 获得[[阿兰·图灵|图灵]]奖
- 2026年：ECDHE 仍是 TLS 1.3 中唯一支持的密钥交换机制

### 优先权争议

- 英国 GCHQ 的 [[James Ellis]]（1970）、[[Clifford Cocks]]（1973）、[[Malcolm Williamson]]（1974）独立发现了相同概念，但被列为最高机密直到1997年才部分解密

## 来源

- [[raw/books/计算机科学/11-diffie-hellman-new-directions.md]]

## 相关

- [[Whitfield Diffie]] — 第一作者
- [[Martin Hellman]] — 第二作者
- [[公钥密码学]] — 首次提出
- [[Diffie-Hellman 密钥交换]] — 首次提出
- [[数字签名]] — 概念框架
- [[单向陷门函数]] — 数学基础
- [[后量子密码学]] — 量子计算威胁
- [[信息论]] — Shannon 是唯一先驱
- [[计算复杂度理论]] — 安全性基础
