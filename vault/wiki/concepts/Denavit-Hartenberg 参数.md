---
type: concept
title: "Denavit-Hartenberg 参数"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [数学，工具，方法论, 机器人学]
aliases: ["DH Parameters", "D-H Convention", "DH 约定"]
relates_to:
  - target: "[[Jacques Denavit]]"
    type: caused
    confidence: 1.0
  - target: "[[Richard S. Hartenberg]]"
    type: caused
    confidence: 1.0
  - target: "[[Robot Manipulators: Mathematics, Programming, and Control]]"
    type: implements
    confidence: 1.0
  - target: "[[齐次变换矩阵]]"
    type: uses
    confidence: 1.0
supersedes: null
---

# Denavit-Hartenberg 参数

## 概述
Denavit-Hartenbe[[ripgrep|rg]]（DH）参数是一种用于描述串联机器人连杆和关节几何关系的标准化方法，由 [[Jacques Denavit]] 和 [[Richard S. Hartenberg]] 于 1955 年提出。该方法通过四个参数（连杆长度 $a$、连杆扭转角 $\alpha$、连杆偏距 $d$ 和关节角 $\theta$）唯一确定相邻两个连杆坐标系之间的相对位姿。虽然最初是为传统机构学设计的，但在 [[Richard P. Paul]] 1981 年的专著中被系统化地应用于机器人建模，从此成为全球工业机器人技术文档和机器人学教育的通用标准，被誉为机器人运动学的“字母表”。

## 关键内容
### 四个核心参数
DH 约定通过在每个连杆上建立局部坐标系，用以下四个参数描述连杆 $i-1$ 到连杆 $i$ 的变换：
1.  **连杆长度 ($a_i$)**：沿 $x_i$ 轴，从 $z_{i-1}$ 到 $z_i$ 的距离。
2.  **连杆扭转角 ($\alpha_i$)**：绕 $x_i$ 轴，从 $z_{i-1}$ 到 $z_i$ 的角度。
3.  **连杆偏距 ($d_i$)**：沿 $z_{i-1}$ 轴，从 $x_{i-1}$ 到 $x_i$ 的距离（对于移动关节，这是变量）。
4.  **关节角 ($\theta_i$)**：绕 $z_{i-1}$ 轴，从 $x_{i-1}$ 到 $x_i$ 的角度（对于旋转关节，这是变量）。

这四个参数可以构造出一个标准的 $4 \times 4$ [[齐次变换矩阵]] $A_i$，该[[矩阵]]包含了旋转和平移信息。

### Paul 的标准化贡献
在 Paul 之前，DH 参数并未在机器人领域得到统一应用，不同的研究者使用不同的符号系统和坐标系定义。Paul 在《[[Robot Manipulators: Mathematics, Programming, and Control|Robot Manipulators]]》中不仅采纳了 DH 方法，还对其进行了严格的标准化定义（通常称为“标准 DH"或"Classic DH"），并展示了如何从物理机器人图纸一步步提取 DH 参数表。他以 [[PUMA 机器人|PUMA 560]] 机器人为例，手把手演示了从参数提取到正向运动学方程生成的全过程。这种“理论 + 实例”的写作方式，使得 DH 参数从一种抽象的机构学描述工具，变成了工程师手中可操作的建模利器。

### 在运动学建模中的核心地位
DH 参数的最大优势在于其通用性和程序化潜力。对于任何串联开链机器人，只要确定了 DH 参数表，其正向运动学方程就可以自动写成一串[[矩阵]]连乘的形式：$T_{0n} = \prod A_i$。这一特性极大地简化了复杂机器人的建模过程，并为后来的计算机辅助设计（CAD）和运动学仿真软件奠定了基础。直到今天，全球所有主流工业机器人制造商（如 ABB, FANUC, KUKA）在其技术手册中仍使用 DH 参数来描述产品的运动学构型。当工程师说“给我这台机器人的 DH 表”时，他们使用的正是 Paul 所标准化的那套方法论。

### 局限性与替代方案
尽管 DH 参数应用广泛，但它也存在一些局限性，例如在处理平行轴相邻连杆时可能出现定义不唯一的情况，且参数物理意义有时不够直观。为此，后来发展出了改进型 DH 参数（Modified DH）以及基于旋量理论（Screw Theory）的积指数公式（PoE）方法。PoE 方法在数学上更加紧凑且避免了某些奇异性，但在工业界的普及程度目前仍不及 DH 参数。尽管如此，DH 参数作为机器人学入门和工业标准的地位依然不可动摇。

## 来源
- [[raw/books/机器人学/05-paul-robot-manipulators-mathematics.md]]

## 相关
- [[Jacques Denavit]]
- [[Richard S. Hartenberg]]
- [[Robot Manipulators: Mathematics, Programming, and Control]]
- [[齐次变换矩阵]]