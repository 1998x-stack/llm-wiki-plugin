---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [统计学, 模型选择, 信息论, 概率论]
aliases: ["Bayesian Information Criterion", "BIC", "贝叶斯信息准则", "施瓦茨准则"]
relates_to:
  - target: "[[模型选择]]"
    type: part_of
    confidence: 0.95
  - target: "[[AIC（赤池信息准则）]]"
    type: compares_to
    confidence: 0.95
  - target: "[[吉迪恩·施瓦茨]]"
    type: created_by
    confidence: 0.95
  - target: "[[贝叶斯统计]]"
    type: part_of
    confidence: 0.9
  - target: "[[信息论]]"
    type: foundation_for
    confidence: 0.85
supersedes: null
---

# BIC准则

## 概述
[[托马斯·贝叶斯|贝叶斯]]信息准则（Bayesian Information Criterion, BIC），又称施瓦茨准则，由[[吉迪恩·施瓦茨]]于1978年提出，公式为BIC = -2ln(L) + kln(n)，是一种基于[[托马斯·贝叶斯|贝叶斯]]理论的[[模型选择]]准则。

## 关键内容

1. **公式定义**：BIC = -2ln(L) + kln(n)，其中L是模型的最大似然值，k是模型的自由参数个数，n是样本量。与AIC类似，BIC值越小模型越好。

2. **与AIC的比较**：AIC惩罚项为2k（固定），BIC惩罚项为kln(n)（随样本量增大）。当样本量n≥8时，ln(n)>2，BIC的惩罚比AIC更重，倾向于选择更简洁的模型。

3. **理论目标**：AIC目标是最小化预测误差（信息损失），而BIC目标是找到"真实模型"（后验概率最大）。AIC假设真实模型可能不在候选集中，BIC假设真实模型就在候选集中。

4. **应用场景**：BIC更适合解释性分析和确认性分析，当研究者关心识别真正的数据生成机制时使用。在预测准确性更重要的场合，AIC通常更合适。

5. **实用建议**：许多学者会同时报告AIC和BIC的结果，以便全面评估模型。当两个准则给出一致结果时，结论更加可靠。

## 来源
- [[07-akaike-1974-aic]] — 用一把"奥卡姆剃刀"丈量统计模型
- [[Schwarz, G. (1978). Estimating the Dimension of a Model]]

## 相关
- [[模型选择]] — part_of
- [[AIC（赤池信息准则）]] — compares_to
- [[吉迪恩·施瓦茨]] — created_by
- [[贝叶斯统计]] — part_of
- [[信息论]] — foundation_for
- [[赤池弘次]] — compares_to