---
type: paper
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [密码学, 公钥密码学, 密钥交换, 数字签名, 离散对数, 推荐系统]
aliases: ["New Directions in Cryptography", "New Directions in Cryptography 论文"]
relates_to: 
  - target: "[[Diffie-Hellman 密钥交换协议]]"
    type: extends
  - target: "[[公钥密码学]]"
    type: introduces
  - target: "[[Whitfield Diffie]]"
    type: authored_by
  - target: "[[Martin E. Hellman]]"
    type: authored_by
  - target: "[[离散对数问题]]"
    type: based_on
  - target: "[[RSA算法]]"
    type: inspired
supersedes: null
---

# New Directions in Cryptography

## 概述
这篇1976年由Diffie和Hellman发表的开创性论文，首次提出了公钥密码学的完整概念框架，并给出了人类历史上第一个公钥密钥交换协议（Diffie-Hellman协议），从根本上解决了困扰密码学数千年的密钥分发问题。

## 关键内容

1. **公钥密码学概念框架**：
   论文提出了全新的密码学范式，其中每个用户拥有一个密钥对（公钥和私钥），公钥可公开而私钥需保密。这一框架解决了此前通信双方必须提前共享秘密的传统假设。

2. **Diffie-Hellman密钥交换协议**：
   基于离散对数问题的数学困难性，给出了第一个公钥密钥交换方案。允许两个此前从未接触过的用户通过不安全的公开信道建立共享秘密。

3. **数字签名理论框架**：
   首次提出了公钥数字签名的完整概念模型，定义了签名应满足的认证性、完整性和不可否认性三个核心属性。

4. **计算复杂度基础**：
   将密码学的安全性建立在计算复杂度理论之上，而非算法的保密性，标志着密码学从经验技艺向严格数学科学的转变。

5. **历史意义与影响**：
   论文催生了现代密码学的多个核心分支，为今日的互联网安全、电子商务、数字签名等技术奠定了基础。

## 来源
- [[计算机科学/11-diffie-hellman-new-directions.md]] — 原始分析文档
- [[Whitfield Diffie]] — 作者
- [[Martin E. Hellman]] — 作者

## 相关
- [[Diffie-Hellman 密钥交换协议]] — 基于此论文提出的具体协议
- [[公钥密码学]] — 此论文引入的核心概念
- [[离散对数问题]] — 协议安全性的数学基础
- [[RSA算法]] — 受此论文启发的后续成果
- [[数字签名]] — 此论文定义的重要概念