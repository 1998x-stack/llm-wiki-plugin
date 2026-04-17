---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 判别模型, 分类]
aliases: [DLLM4Rec, Discriminative LLM for Recommendation]
relates_to:
  - {target: 生成式推荐 (LLM), type: compares_to}
  - {target: 生成式 LLM 推荐, type: compares_to}
  - {target: CTR 预估, type: extends}
  - {target: Pointwise 学习, type: uses}
supersedes: null
---

# 判别式 LLM 推荐

## 概述
使用 LLM 进行判别式推荐（分类/排序）的范式，将推荐建模为预测用户对物品偏好的判别任务而非生成任务。

## 关键内容

1. **范式定义**：判别式 LLM 推荐（DLLM4Rec）将推荐建模为判别任务——给定用户和物品，预测用户是否喜欢该物品（二分类）或预测评分（回归），而非生成式地产生推荐结果。

2. **与[[生成式推荐 (LLM)]]的对比**：
   - 生成式：输入 Prompt，输出物品 ID 或推荐文本（如 P5 的 "item_92"）
   - 判别式：输入用户-物品对，输出偏好分数或分类标签（如 "Yes/No" 或评分）

3. **与[[生成式 LLM 推荐]]的关系**：Wu 等人的综述将 LLM 推荐方法分为判别式（DLLM4Rec）和生成式（[[生成式 LLM 推荐|GLLM4Rec]]）两大范式。判别式侧重预测准确性，生成式侧重灵活性和可解释性。

4. **技术特点**：
   - 通常使用 LLM 的[[嵌入表示]]能力编码用户和物品特征
   - 在 LLM 之上添加分类头或回归头
   - 训练目标多为[[二元交叉熵]]或RMSE
   - 推理效率通常优于生成式方案

5. **与[[CTR 预估]]的关系**：判别式 LLM 推荐可视为传统[[CTR 预估]]的 LLM 化升级，用 LLM 的语义理解能力增强特征表示。

6. **与[[Pointwise 学习]]的关系**：判别式 LLM 推荐通常采用 pointwise 学习目标，逐个预测用户-物品对的偏好。

## 来源
- Wu et al. — A Survey on Large Language Models for Recommendation, ACM TOIS 2024

## 相关
- [[生成式推荐 (LLM)]] — 对立范式
- [[生成式 LLM 推荐]] — 同属 LLM 推荐的另一分支
- [[CTR 预估]] — 判别式推荐的传统形式
- [[Pointwise 学习]] — 判别式 LLM 推荐的学习方式
- [[二元交叉熵]] — 判别式 LLM 推荐的损失函数
- RMSE — 判别式 LLM 推荐的回归指标
- [[嵌入表示]] — 判别式 LLM 推荐的特征编码方式
