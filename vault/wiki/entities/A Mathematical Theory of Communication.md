---
type: entity
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [信息论, 通信理论, 论文]
aliases: [A Mathematical Theory of Communication, 通信的数学理论]
relates_to:
- target: '[[Claude Shannon]]'
  type: authored_by
  confidence: 0.95
- target: '[[信息论]]'
  type: founded_field
  confidence: 0.95
- target: '[[熵]]'
  type: introduced_concept
  confidence: 0.95
- target: '[[信道容量]]'
  type: established_theorem
  confidence: 0.95
- target: '[[通信理论]]'
  type: transformed_field
  confidence: 0.9
- target: '[[信源编码定理]]'
  type: established_theorem
  confidence: 0.95
- target: '[[有噪信道编码定理]]'
  type: established_theorem
  confidence: 0.95
- target: '[[互信息]]'
  type: introduced_concept
  confidence: 0.9
- target: '[[信息论]]'
  type: originated
  confidence: 0.95
- target: '[[通信系统模型]]'
  type: established_model
  confidence: 0.95
- target: '[[信息熵]]'
  type: defined
  confidence: 0.95
- target: '[[香农]]'
  type: authored_by
  confidence: 0.95
supersedes: null
entity_type: paper
---

# A Mathematical Theory of Communication

## 概述
[[Claude Shannon]]于1948年发表的奠基性论文，标志着[[信息论]]作为一门独立学科的诞生，首次给出了"信息"的精确数学定义。

## 关键内容
1. **创立[[信息论]]**：首次将"信息"定义为[[概率公理体系|概率空间]]中不确定性的度量，以比特为单位，用熵进行量化，彻底改变了人类对通信本质的理解。

2. **[[信息熵]]定义**：提出了[[信息熵]]公式 $H(X) = -\sum_{i=1}^{n} p(x_i) \log_2 p(x_i)$，奠定了整个[[信息论]]大厦的基石。

3. **[[信源编码定理]]**：证明了数据压缩存在理论极限，即熵值，为所有现代数据压缩技术提供了理论根基。

4. **[[信道编码定理]]**：证明了有噪信道存在容量极限，但在该限制内可实现几乎无差错的通信，这是论文中最深刻的结论。

5. **[[通信系统模型]]**：建立了"信源→编码器→信道→解码器→信宿"的经典模型，为所有现代通信系统提供了理论框架。

## 来源
- [[Claude Shannon]] — author
- [[]] — 

## 相关
- [[Claude Shannon]] — authored_by
- [[信息论]] — founded_field
- [[熵]] — introduced_concept
- [[信道容量]] — established_theorem
- [[通信理论]] — transformed_field