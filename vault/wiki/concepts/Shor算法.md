---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [密码学, 量子计算, 安全威胁]
aliases: ["Shor's Algorithm", "秀尔算法"]
relates_to: 
  - target: "[[量子计算]]"
    type: related_to
  - target: "[[离散对数问题]]"
    type: solves
  - target: "[[大整数分解]]"
    type: solves
  - target: "[[公钥密码学]]"
    type: threatens
  - target: "[[后量子密码学]]"
    type: motivates
supersedes: null
---

# Shor算法

## 概述
由Peter Shor在1994年提出的量子算法，能够在多项式时间内解决离散对数问题和大整数分解问题，对基于这些数学难题的公钥密码系统构成根本性威胁。

## 关键内容

1. **算法原理**：
   Shor算法利用量子计算的叠加和纠缠特性，通过量子傅里叶变换来寻找周期函数的周期，从而高效地解决离散对数和大整数分解问题。

2. **解决的问题**：
   - 大整数分解：将合数分解为其质因数
   - 离散对数问题：在给定g、h和g^x≡h (mod p)的情况下求解x

3. **对密码学的影响**：
   一旦大规模量子计算机成为现实，RSA、Diffie-Hellman、椭圆曲线密码学等主流公钥密码系统都将不再安全，因为它们的安全性都依赖于Shor算法能够高效解决的数学问题。

4. **计算复杂度**：
   经典算法对这些问题需要指数时间，而Shor算法只需要O((log N)^3)的量子时间和O(log N)的量子空间，实现了指数级加速。

5. **推动后量子密码学**：
   Shor算法的出现直接推动了后量子密码学（Post-Quantum Cryptography）的发展，研究能够抵抗经典和量子计算机攻击的新型密码系统。

## 来源
- [[计算机科学/11-diffie-hellman-new-directions.md]] — 提及对现代密码学的威胁
- [[量子计算]] — 算法所属的计算模型

## 相关
- [[量子计算]] — Shor算法运行的计算模型
- [[离散对数问题]] — Shor算法能够解决的数学问题
- [[大整数分解]] — Shor算法能够解决的另一数学问题
- [[公钥密码学]] — 受Shor算法威胁的密码学领域
- [[后量子密码学]] — Shor算法推动发展的新领域