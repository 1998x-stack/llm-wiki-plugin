---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", "工具与框架", 时间序列]
aliases: ["Facebook Prophet", "Prophet 预测模型", "可加时间序列模型"]
relates_to:
  - target: "[[ARIMA 模型]]"
    type: compares_to
    confidence: 0.8
  - target: "[[指数平滑]]"
    type: compares_to
    confidence: 0.75
  - target: "[[AIC（赤池信息准则）]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# Prophet

## 概述
Prophet 是 [[Meta|Facebook]]（Meta）于 2017 年开源的时间序列预测工具，由 Sean Taylor 和 Benjamin Letham 开发，旨在让非统计学专家也能对业务时间序列进行高质量预测，解决了大规模预测场景下的人机协作难题。

## 关键内容

1. **历史背景**：[[Meta|Facebook]] 需要对数千条业务时间序列（日活、广告收入、服务器负载等）做预测，但传统方法（[[ARIMA 模型|ARIMA]]、[[指数平滑]]）对使用者专业要求极高，无法扩展到业务分析师和产品经理。

2. **设计哲学**：与其追求全自动化，不如让人机协作变得更容易。Prophet 提供直观的参数接口（如节假日、突变点），让领域专家注入业务知识，而非统计学知识。

3. **模型结构**：基于可加模型——趋势分量（分段线性或逻辑增长）+ 季节分量（傅里叶级数）+ 节假日分量。对缺失数据、趋势变化、异常值具有鲁棒性。

4. **三重规模化**：序列数量规模化（数千条不同特征序列）、预测者规模化（非统计专家可用）、问题多样性规模化（周期/突变/节假日等复杂场景）。

## 来源
- [[13-prophet-2017-forecasting-at-scale]] — Prophet：Facebook 如何让"预测未来"变成人人可用的工具

## 相关
- [[ARIMA 模型]] — compares_to
- [[指数平滑]] — compares_to
- [[AIC（赤池信息准则）]] — relates_to
