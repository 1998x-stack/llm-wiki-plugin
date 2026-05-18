---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [密码学, 公钥密码学, 密钥交换, LLM能力]
aliases: ["Diffie-Hellman Key Exchange Protocol", "DH协议"]
relates_to: 
  - target: "[[New Directions in Cryptography]]"
    type: described_in
  - target: "[[Whitfield Diffie]]"
    type: invented_by
  - target: "[[Martin E. Hellman]]"
    type: invented_by
  - target: "[[离散对数问题]]"
    type: based_on
  - target: "[[公钥密码学]]"
    type: implements
  - target: "[[TLS协议]]"
    type: used_in
supersedes: null
---

# Diffie-Hellman 密钥交换协议

## 概述
人类历史上第一个公钥密钥交换协议，允许两个此前从未接触过的用户通过不安全的公开信道建立共享秘密，基于[[离散对数问题]]的数学困难性实现安全性。

## 关键内容

1. **协议流程**：
   - 双方公开选定大素数p和模p的原根g
   - 各自生成随机秘密整数，[[计算]]公开值并交换
   - 基于收到的公开值和自己的秘密，[[计算]]出相同的共享密钥

2. **数学基础**：
   协议的安全性依赖于[[离散对数问题]]的[[计算]]困难性——给定g、p和g^a mod p，[[计算]]a在[[计算]]上是不可行的。目前最优的经典[[算法]]（数域筛法）具有亚指数级复杂度。

3. **具体实现**：
   Alice选择秘密a，[[计算]]A=g^a mod p发送给Bob；Bob选择秘密b，[[计算]]B=g^b mod p发送给Alice；双方分别[[计算]]K=B^a mod p=A^b mod p=g^(ab) mod p获得共享密钥。

4. **实际应用**：
   现代TLS 1.3协议中仍采用其椭圆曲线变体ECDHE作为唯一的密钥交换机制，广泛应用于[[TLS协议|HTTPS]]、SSH等安全协议中。

5. **局限性**：
   协议本身缺乏身份认证功能，易受[[中间人攻击]]，需配合数字证书等机制使用。

## 来源
- [[计算机科学/11-diffie-hellman-new-directions.md]] — 协议的原始描述和分析
- [[New Directions in Cryptography]] — 首次提出的论文

## 相关
- [[New Directions in Cryptography]] — 首次描述该协议的论文
- [[公钥密码学]] — 协议所属的密码学范式
- [[离散对数问题]] — 协议安全性的数学基础
- [[TLS协议]] — 现代应用中的重要协议
- [[椭圆曲线密码学]] — 协议的优化变体基础