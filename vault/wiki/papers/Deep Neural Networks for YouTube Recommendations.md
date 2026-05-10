---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [recommendation-systems, deep-learning, youtube]
aliases: [Deep Neural Networks for YouTube Recommendations, YouTube DNN Paper]
relates_to:
  - {target: "[[YouTube]]", type: part_of}
  - {target: "[[候选生成]]", type: extends}
  - {target: "[[双塔模型]]", type: implements}
  - {target: "[[Example Age]]", type: introduces}
  - {target: "[[期望观看时长]]", type: introduces}
  - {target: "[[采样 Softmax]]", type: uses}
  - {target: "[[近似最近邻检索]]", type: uses}
  - {target: "[[Paul Covington]]", type: authored_by}
  - {target: "[[Jay Adams]]", type: authored_by}
  - {target: "[[Emre Sargin]]", type: authored_by}
  - {target: "[[RecSys 2016]]", type: published_at}
supersedes: null
entity_type: paper
---

# Deep Neural Networks for YouTube Recommendations

## 概述
YouTube推荐系统经典论文，提出了"候选生成+排序"的两阶段架构，奠定了工业推荐系统十年的架构范式。

## 关键内容

1. **核心贡献**：
   - 首次在工业级推荐系统中成功应用深度神经网络
   - 提出"候选生成+排序"两阶段架构，解决数十亿规模推荐问题
   - 将推荐问题建模为超大规模多分类问题

2. **两阶段架构**：
   - 候选生成：从数十亿视频中筛选数百个候选，使用深度神经网络+采样softmax
   - 排序：对候选进行精细化排序，优化期望观看时长而非点击率

3. **关键技术创新**：
   - Example Age特征：解决新鲜度偏差问题，让模型倾向推荐新内容
   - 加权逻辑回归：用点击率优化观看时长，避免"标题党"效应
   - 训练-服务不对称设计：训练用softmax，服务用近似最近邻检索

## 来源
- [[07-youtube-dnn]] — 深度解读文档
- [[]] —

## 相关
- [[YouTube]] — part_of
- [[候选生成]] — extends
- [[双塔模型]] — implements
- [[Example Age]] — introduces
- [[期望观看时长]] — introduces
- [[采样 Softmax]] — uses
- [[近似最近邻检索]] — uses
- [[Paul Covington]] — authors
- [[Jay Adams]] — authors
- [[Emre Sargin]] — authors
- [[RecSys 2016]] — published_at