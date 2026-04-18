---
type: entity
entity_type: tool
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: '2026-04-18'
source_count: 1
tags: ["技术", "AI", "推理引擎", "工具与框架"]
aliases:
  - ONNX Runtime
  - ONNXRuntime
  - ort
relates_to:
  - target: '[[DocLayout-YOLO]]'
    type: uses
    confidence: 0.85
  - target: '[[MinerU]]'
    type: uses
    confidence: 0.8
supersedes: null
---

# ONNX Runtime

## 概述

ONNX Runtime 是微软开源的跨平台机器学习推理加速器，支持 ONNX 格式模型的 GPU/CPU 自动选择执行，是 [[MinerU]] 中 [[DocLayout-YOLO]] 等模型的推理引擎。

## 关键内容

### 核心特性

- **跨平台**：支持 Windows、Linux、macOS
- **多硬件后端**：自动选择 CUDAExecutionProvider（GPU）或 CPUExecutionProvider
- **ONNX 格式**：接受标准化的模型交换格式，解耦训练框架与推理环境

### 在 MinerU 中的使用

```python
import onnxruntime as ort

session = ort.InferenceSession(
    "doclayout_yolo.onnx",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)

input_tensor = img_normalized[np.newaxis, :]  # 添加 batch 维度
outputs = session.run(None, {"images": input_tensor})
```

通过 providers 列表指定优先级，优先使用 GPU 加速，不可用时自动降级到 CPU。

### 推理流程

1. 加载 .onnx 模型文件创建 InferenceSession
2. 预处理输入（归一化、添加 batch 维度）
3. 调用 session.run() 执行推理
4. 解析原始输出（[1, num_predictions, 4+num_classes] 格式）
5. 后处理（坐标还原、NMS、类别映射）

## 来源

- [[raw/assets/MinerU/minerU_03_layout.md]] — MinerU 深度解析系列 · 第三篇：布局检测系统

## 相关

- [[DocLayout-YOLO]] — 使用 ONNX Runtime 进行推理
- [[MinerU]] — 整体项目使用 ONNX Runtime 作为推理引擎
