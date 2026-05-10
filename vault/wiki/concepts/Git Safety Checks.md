---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [git, security, workflow]
aliases: ["Git Safety Checks", "Git Security Checks", "Safety Checks"]
relates_to: []
supersedes: null
---

# Git Safety Checks

## 概述
Git操作中的安全检查机制，用于防止敏感信息如密钥、证书和大文件被提交到版本控制系统。

## 关键内容

1. ****检测目标**：
   - Secrets文件：.env*, *.key, *.pem, credentials.json, secrets.yaml等
   - API密钥：包含真实值而非占位符的*_API_KEY、*_SECRET、*_TOKEN变量
   - 大文件：>10MB且未使用Git LFS的文件
   - 构建产物：node_modules/, dist/, build/, __pycache__/等

2. ****安全验证流程**：
   - 检查是否存在敏感文件类型
   - 验证API密钥是否仅为占位符
   - 确认.gitignore[[Configuration|配置]]正确
   - 检查是否有合并冲突

3. ****API密钥校验规则**：
   - 检测真实密钥值（如sk-proj-xxxxx, AKIA...等）
   - 接受占位符格式（如your-api-key-here, placeholder, xxx等）

## 来源
- [[Push All Command]] — 

## 相关
- [[Git Push All]] — relates_to
- [[Conventional Commits]] — relates_to