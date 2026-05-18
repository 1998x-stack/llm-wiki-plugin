---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [密码学, 安全协议, 网络安全, AI工程]
aliases: ["Transport Layer Security", "SSL/TLS", "HTTPS"]
relates_to: 
  - target: "[[Diffie-Hellman 密钥交换协议]]"
    type: utilizes
  - target: "[[公钥密码学]]"
    type: based_on
  - target: "[[身份认证]]"
    type: provides
  - target: "[[中间人攻击]]"
    type: prevents
supersedes: null
---

# TLS协议

## 概述
传输层安全协议，用于在网络通信中提供端到端的安全保障，包括数据加密、身份认证和完整性验证，是现代[[互联网]]安全的基础协议。

## 关键内容

1. **协议功能**：
   TLS协议为应用层协议（如HTTP、SMTP、POP3等）提供安全通信通道，确保数据在传输过程中的机密性、完整性和身份验证。

2. **握手过程**：
   - 客户端和[[服务]]器协商协议版本和加密套件
   - [[服务]]器发送数字证书进行身份验证
   - 使用如Diffie-Hellman等密钥交换协议建立共享密钥
   - 生成会话密钥用于对称加密

3. **与[[公钥密码学]]的关系**：
   TLS协议大量使用[[公钥密码学]]技术，包括数字证书、公钥加密、[[数字签名]]等，以实现身份认证和密钥交换。

4. **安全机制**：
   - 使用[[公钥密码学]]进行身份验证
   - 使用密钥交换协议建立会话密钥
   - 使用对称加密[[算法]]保护数据传输

5. **演进与标准**：
   TLS是SSL协议的后继者，经历了TLS 1.0、1.1、1.2到最新的TLS 1.3版本，安全性不断提升，握手过程也在不断优化。

## 来源
- [[计算机科学/11-diffie-hellman-new-directions.md]] — 提及其使用DH协议
- [[Diffie-Hellman 密钥交换协议]] — 在TLS中的应用

## 相关
- [[Diffie-Hellman 密钥交换协议]] — TLS握手过程中的密钥交换机制
- [[公钥密码学]] — TLS协议的基础技术
- [[身份认证]] — TLS协议提供的安全服务
- [[数字证书]] — TLS中身份验证的载体
- [[中间人攻击]] — TLS协议防护的攻击类型