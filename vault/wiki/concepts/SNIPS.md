---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 因果推断, 去偏, 评估方法]
aliases: [SNIPS, Self-Normalized Inverse Propensity Scoring]
relates_to:
  - {target: 逆倾向评分, type: extends}
  - {target: 倾向性评分, type: uses}
  - {target: 选择偏差, type: compares_to}
supersedes: null
---

# 自归一化逆倾向评分 (SNIPS)

## 概述
SN[[逆倾向评分|IPS]] 是 [[逆倾向评分|IPS]] 的自归一化变体，通过用逆倾向权重总和进行归一化，显著降低估计方差，同时保持最优解不变，是因果推荐中的标准估计器。

## 关键内容

1. **核心公式**：$\hat{R}_{SN[[逆倾向评分|IPS]]}(\hat{Y}) = \frac{\sum_{(u,i): O_{u,i}=1} \frac{\delta(\hat{y}_{u,i}, y_{u,i})}{P_{u,i}}}{\sum_{(u,i): O_{u,i}=1} \frac{1}{P_{u,i}}}$。分母为所有逆倾向权重之和，使归一化后权重总和为 1。

2. **来源**：源自[[因果推断]]文献中的 Hajek 估计器，由 [[Tobias Schnabel]] 等人在 [[Recommendations as Treatments]] 中引入推荐系统领域。

3. **优势**：
   - **显著降低方差**：通过归一化避免极端权重（如 $1/0.001 = 1000$）的影响
   - **牺牲极小偏差**：SN[[逆倾向评分|IPS]] 不再是严格无偏的，但引入的偏差通常可忽略
   - **保持最优解不变**：用于学习时，SN[[逆倾向评分|IPS]] 不改变 a[[ripgrep|rg]]max，最优模型参数不受归一化影响
   - **无需额外调参**：不像倾向性裁剪（propensity clipping）需人工设定截断阈值

4. **与 [[逆倾向评分|IPS]] 的权衡**：[[逆倾向评分|IPS]] 严格无偏但方差高，SN[[逆倾向评分|IPS]] 有微小偏差但方差显著更低。在实际推荐场景中，SN[[逆倾向评分|IPS]] 通常表现更稳定，尤其在各种偏差程度下都维持良好精度。

5. **药物临床类比**：如果某类患者服药概率极低（0.001），一旦观察到这样的患者，其 [[逆倾向评分|IPS]] 权重高达 1000 倍，一个人的数据可能主导整个估计。SN[[逆倾向评分|IPS]] 通过归一化避免"一个极端样本搅动全局"的问题。

## 来源
- [Recommendations as Treatments (Schnabel et al., ICML 2016)](https://arxiv.org/abs/1602.05352)

## 相关
- [[逆倾向评分]] — SNIPS 的基础方法
- [[倾向性评分]] — 权重计算的核心输入
- [[选择偏差]] — SNIPS 旨在校正的问题
