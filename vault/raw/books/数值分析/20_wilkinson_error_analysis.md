# Wilkinson 舍入误差分析：后向误差的哲学革命

## 1. 标题

**Rounding Errors in Algebraic Processes**
（代数过程中的舍入误差）

以及后续更全面的著作：

**The Algebraic Eigenvalue Problem**
（代数特征值问题）

---

## 2. 作者/作者群

**James Hardy Wilkinson**（詹姆斯·哈迪·威尔金森，1919—1986），英国数学家和计算科学先驱，后向误差分析（backward error analysis）的奠基人。

Wilkinson 于 1939 年在剑桥大学三一学院获得数学学位。二战期间，他参与了与弹道计算相关的军事工作。1946 年，他加入英国国家物理实验室（National Physical Laboratory, NPL），在 Alan Turing 的领导下参与了 ACE（Automatic Computing Engine）计算机的开发——这是世界上最早的存储程序计算机之一。Turing 离开 NPL 后，Wilkinson 接替了他的位置，继续推动 ACE 项目。

在 NPL 的工作使 Wilkinson 成为世界上最早大量使用电子计算机进行数值计算的人之一。这种亲身经历让他深刻认识到浮点运算中舍入误差的重要性和微妙性。与许多纯理论家不同，Wilkinson 的误差分析理论植根于大量的实际计算经验。他对舍入误差行为的直觉——哪些算法在实际中可靠，哪些不可靠——来自数以千计的计算实验。

Wilkinson 的贡献获得了广泛认可。1970 年，他获得了 ACM 图灵奖（Turing Award）——计算机科学领域的最高荣誉——以表彰他在"数值分析研究中的贡献，特别是在处理数值线性代数问题中的有效和精确的自动化方面"。此外，他还获得了美国数学学会的 von Neumann 奖和英国皇家学会的会员资格（FRS）。

在 NPL 期间，Wilkinson 与同事们积累了大量数值计算经验。他们发现，某些在理论上完全正确的算法在实际计算中会产生灾难性的结果，而另一些看似没有理论保证的算法却工作得很好。这些观察驱动 Wilkinson 发展了一套全新的误差分析框架——后向误差分析——来解释和预测算法在浮点运算下的行为。

---

## 3. 发表时间

- 1963 年：《Rounding Errors in Algebraic Processes》由 Prentice-Hall 出版（英文版）；同年也有德文译本由 Springer 出版
- 1965 年：《The Algebraic Eigenvalue Problem》由 Oxford University Press（Clarendon Press）出版

---

## 4. 发表载体/文献背景

《Rounding Errors in Algebraic Processes》是一本简洁的专著（约 160 页），由 Prentice-Hall（后来的 Pearson Education）出版。这本书系统地阐述了浮点运算中舍入误差的基本理论，特别是后向误差分析的方法论。它是该主题的第一部系统性著作。

《The Algebraic Eigenvalue Problem》是一部更为全面的巨著（约 660 页），由牛津大学出版社出版。这本书被广泛认为是 20 世纪数值线性代数领域最重要的著作之一——在某种意义上，它定义了这个学科的现代面貌。书中不仅包含了特征值问题的理论和算法，更重要的是，它为每一种算法提供了详尽的舍入误差分析，建立了后向误差分析作为算法评估标准框架的范式。

这两部著作出版的 1960 年代初期，正是计算科学从"早期实验"走向"成熟学科"的关键转折期。IBM System/360 系列（1964 年推出）标志着计算机工业的标准化——浮点运算格式开始统一（虽然完全统一要等到 1985 年的 IEEE 754 标准）。科学计算的规模和复杂性迅速增长，对算法可靠性的要求也越来越高。在这一背景下，Wilkinson 的工作提供了一个系统的理论框架来回答一个根本问题：**我们能在多大程度上信任计算机给出的答案？**

---

## 5. 一句话总结

**计算得到的答案是一个"邻近问题"的精确答案——这就是后向误差分析的核心范式，它将"答案有多错"的问题转化为"我们实际求解了什么问题"。**

---

## 6. 历史背景

舍入误差问题与电子计算同样古老。从最早的计算实验开始，科学家们就注意到数值计算中的结果有时会与理论预期产生巨大的偏差。这些偏差的来源是浮点运算中不可避免的舍入——计算机只能存储有限位数的数字，每一步运算都会产生微小的截断。

在 Wilkinson 之前，处理舍入误差的方法主要有两种：

**前向误差分析（Forward Error Analysis）**。这种传统方法试图直接估计最终答案的误差。具体地，对于一个算法 $f(x)$ 和输入 $x$，前向误差分析试图给出

$$|f(x) - \hat{f}(x)| \leq \text{某个界}$$

其中 $\hat{f}(x)$ 是实际计算得到的结果。这种方法的困难在于：每一步运算的误差都会影响后续步骤，误差的传播和累积非常复杂。对于大型计算（涉及数百万次浮点运算），精确追踪每一个误差的传播几乎是不可能的。

**区间运算（Interval Arithmetic）**。这种方法用区间而非单个数字来表示计算结果，保证真实答案在给定的区间内。虽然这种方法在理论上是严格的，但它倾向于给出过于悲观的误差界——区间会随着计算步骤的增加而迅速膨胀（所谓的"包裹效应"，wrapping effect），最终可能变得毫无实际意义。

**von Neumann 和 Goldstine 的先驱工作**。1947 年，von Neumann 和 Goldstine 发表了一篇关于矩阵求逆的数值稳定性的开创性论文。他们引入了条件数的概念，分析了 Gauss 消元法的舍入误差。然而，他们的分析是前向的（估计最终误差的大小），得到的误差界相当悲观，似乎预示着 Gauss 消元法对于大矩阵是不可靠的。但实际计算表明，带部分主元选取的 Gauss 消元法在实践中工作得非常好——理论与实践之间存在巨大的鸿沟。

**Turing 的贡献**。Alan Turing 在 1948 年发表了一篇关于矩阵计算中舍入误差的论文，引入了"条件数"这一概念的一个早期形式。Turing 的分析也主要是前向的，但他对问题本质的洞察为后来的工作奠定了基础。Wilkinson 在 NPL 与 Turing 的共事经历无疑对他的思想发展产生了重要影响。

Wilkinson 的革命性贡献在于：他提出了一种全新的误差分析范式——后向误差分析——从根本上改变了我们理解和评估数值算法的方式。

---

## 7. 核心问题定义

数值计算中的核心问题可以表述如下：

给定一个数学问题 $P$（例如，求解线性方程组 $Ax = b$），和一个算法 $\mathcal{A}$（例如，带部分主元选取的 Gauss 消元法），在有限精度浮点运算下，算法 $\mathcal{A}$ 实际计算得到的结果 $\hat{x}$ 与真解 $x$ 之间有什么关系？

更具体地：

1. **前向问题**：$\hat{x}$ 与 $x$ 有多近？即 $\|x - \hat{x}\|$ 有多大？
2. **后向问题**：$\hat{x}$ 是否是某个"邻近问题"的精确解？即是否存在 $\Delta A$ 和 $\Delta b$，使得 $(A + \Delta A)\hat{x} = b + \Delta b$？如果是，$\Delta A$ 和 $\Delta b$ 有多小？
3. **条件数问题**：问题 $P$ 本身对输入数据的扰动有多敏感？即即使算法完美（无舍入误差），输入数据中的微小不确定性会导致多大的输出变化？

Wilkinson 的核心洞察是：**问题 2（后向误差）比问题 1（前向误差）更有意义，也更容易分析**。而问题 1 的答案可以通过问题 2 和问题 3 的组合来获得：

$$\text{前向误差} \leq \text{条件数} \times \text{后向误差}$$

这个关系式将算法的质量（后向误差小）和问题的本质难度（条件数大）清晰地分离开来。

---

## 8. 主要结论/方法/定理

**后向误差分析的核心范式**可以表述如下：

> **定义.** 一个算法被称为**后向稳定的**（backward stable），如果对于每个输入 $x$，算法的输出 $\hat{f}(x)$ 是某个扰动输入 $x + \Delta x$ 的精确解，且 $\|\Delta x\| / \|x\| = O(u)$，其中 $u$ 是机器精度（unit roundoff）。

用更直白的话说：**计算得到的答案是一个"邻近问题"的精确答案**。

**Wilkinson 关于 Gauss 消元法的分析**。Wilkinson 对带部分主元选取的 Gauss 消元法给出了以下后向误差分析结果：

设用带部分主元选取的 Gauss 消元法求解线性方程组 $Ax = b$，得到的近似解 $\hat{x}$ 满足

$$(A + \Delta A)\hat{x} = b$$

其中

$$\|\Delta A\|_\infty \leq 3n \rho_n u \|A\|_\infty + O(u^2)$$

这里 $n$ 是矩阵的阶数，$u$ 是机器精度，$\rho_n$ 是**增长因子**（growth factor）。

增长因子 $\rho_n$ 定义为消元过程中矩阵元素的最大绝对值与原始矩阵元素最大绝对值的比值。对于带部分主元选取的 Gauss 消元法，理论上 $\rho_n$ 可以达到 $2^{n-1}$（这是 Wilkinson 证明的上界），但在实践中，$\rho_n$ 几乎总是很小——通常不超过 $n^{1/2}$ 到 $n^{2/3}$。

这个结果的深刻之处在于：它解释了为什么带部分主元选取的 Gauss 消元法在实践中如此可靠——虽然理论上的最坏情况界是指数级的，但实际中增长因子几乎总是温和的。

**条件数的角色**。Wilkinson 系统阐述了条件数在误差分析中的核心地位。对于线性方程组 $Ax = b$，矩阵 $A$ 的条件数定义为

$$\kappa(A) = \|A\| \cdot \|A^{-1}\|$$

前向误差界为：

$$\frac{\|x - \hat{x}\|}{\|x\|} \leq \kappa(A) \cdot \frac{\|\Delta A\|}{\|A\|}$$

这清楚地表明：**前向误差 = 条件数 $\times$ 后向误差**。如果问题本身是良态的（$\kappa(A)$ 小），那么后向稳定的算法就能给出准确的答案。如果问题是病态的（$\kappa(A)$ 大），那么即使算法完美，答案也不可能准确——因为问题本身对输入数据太敏感了。

**Wilkinson 多项式**。Wilkinson 构造了一个著名的示例来说明特征值问题的条件敏感性。考虑多项式

$$p(x) = (x-1)(x-2)(x-3)\cdots(x-20)$$

的根（即 $1, 2, 3, \ldots, 20$）。Wilkinson 发现，将 $x^{19}$ 项的系数从 $-210$ 微小地改变为 $-210 + 2^{-23}$（约 $10^{-7}$ 的相对扰动），根就会发生剧变——有些根变成了复数，偏离原始位置达数个单位之远。

这个例子——后来被称为"Wilkinson 多项式"——成为数值分析中最著名的警示故事之一。它生动地说明了：某些看似"简单"的数学问题本身就是病态的，与算法的质量无关。它也说明了为什么通过求解特征多项式的根来计算矩阵特征值是一种糟糕的方法——应该直接使用矩阵算法（如 QR 算法）。

**后向稳定性的哲学意义**。Wilkinson 的后向误差分析代表了一种深刻的哲学转变。传统的前向分析问的是"答案有多错？"（How wrong is the answer?）而后向分析问的是"我们实际求解了什么问题？"（What problem did we actually solve?）

这一转变的深刻之处在于：在实际应用中，输入数据本身通常就有不确定性（来自测量误差、模型简化等）。如果算法的后向误差（即对输入数据的等效扰动）小于输入数据本身的不确定性，那么算法引入的误差就被"淹没"在数据不确定性之中——换句话说，这个算法在实际意义上是完美的。

---

## 9. 核心思想的直觉解释

假设你是一位射箭运动员，目标是射中靶心。

**前向误差分析**就是测量你的箭离靶心有多远。这当然是你最终关心的，但如果你想改善成绩，仅仅知道"箭偏了 3 厘米"并不能告诉你问题出在哪里。

**后向误差分析**则换了一个角度：它问的是"如果箭是完美射出的，那么靶子需要移动多少才能使箭正中靶心？"如果答案是"靶子只需要移动 0.1 毫米"，那么你的射术是非常好的——箭偏离的原因不在于你的技术（算法），而在于靶子的位置不够精确（输入数据的不确定性）。

**条件数**则衡量的是："这个靶子有多难打？"如果是一面大墙（良态问题，条件数小），即使你的射术一般（算法一般），也很容易命中。但如果靶心是一个针尖（病态问题，条件数大），即使是世界冠军（最好的算法）也很难精确命中。

Wilkinson 的核心贡献就是告诉我们：**不要只看箭离靶心多远（前向误差），而要看你的射术有多好（后向误差）以及靶子有多难打（条件数）。这两件事应该分开讨论。**

这个想法简单而深刻：

- 如果你的射术好（后向误差小 = 算法后向稳定），但箭偏了很远（前向误差大），那问题在于靶子太小（问题本身病态），不是你的技术问题
- 如果你的射术差（后向误差大 = 算法不稳定），那即使靶子再大也可能射偏，这时候你需要换一种射箭技术（换一种算法）

一个更日常的比喻：假设你用一把普通量尺（精度到毫米）去测量一张桌子的长度。你量得的结果是"1523 毫米"。

- **后向误差**：你的测量结果 1523 mm 是某张桌子的"精确"长度——哪张桌子呢？是一张长度与真实桌子相差不超过 1 mm 的桌子。所以后向误差是约 1 mm。
- **前向误差**：你的测量结果与真实长度的差距。如果桌子的真实长度是 1523.4 mm，前向误差就是 0.4 mm。
- **条件数**：这里条件数约为 1——测量长度是一个良态问题，输入的微小变化只导致输出的微小变化。

现在考虑一个病态问题：测量两根几乎等长的杆子的长度差。如果两根杆子分别是 1523.4 mm 和 1522.6 mm，长度差是 0.8 mm。但你的量尺只精确到 1 mm，所以你可能量得一根是 1523 mm、另一根也是 1523 mm，计算出的差是 0——前向误差 100%！这不是你量尺不好（后向误差仍然只有 1 mm），而是"求差"这个问题本身是病态的（条件数极大）。

---

## 10. 为什么这篇文献重要

Wilkinson 的工作之所以具有划时代的意义，可以从以下几个方面来理解：

**建立了数值算法分析的标准范式**。在 Wilkinson 之前，分析数值算法的质量缺乏统一的标准和方法。Wilkinson 的后向误差分析提供了一个清晰、统一、可操作的框架：一个好的数值算法应该是后向稳定的——它计算的结果是一个邻近问题的精确解。这个标准至今仍是评价数值算法的黄金准则。

**解释了理论与实践之间的鸿沟**。在 Wilkinson 之前，前向误差分析经常给出过于悲观的误差界——按照这些分析，许多常用算法（如 Gauss 消元法）似乎对大矩阵是不可靠的。但实践表明这些算法工作得很好。后向误差分析解释了这一矛盾：虽然前向误差可能大（因为问题本身可能是病态的），但后向误差是小的（因为算法是稳定的）。

**将算法质量与问题难度分离**。这是 Wilkinson 工作中最深刻的洞察之一。通过引入条件数的概念，Wilkinson 清晰地区分了两种不同的"困难"：问题本身对输入数据的敏感性（条件数，这是问题的内在性质，与算法无关），和算法的数值稳定性（后向误差，这是算法的性质）。两者的乘积决定了最终答案的精度。

**指导了数值软件的设计和验证**。后向误差分析成为 LAPACK 等数值软件库的设计哲学和验证标准。LAPACK 中的每个核心例程都附有详细的误差分析，基于后向稳定性来保证结果的可靠性。用户可以通过条件数估计来判断计算结果是否可信。

**图灵奖的认可**。Wilkinson 于 1970 年获得 ACM 图灵奖，这是对他贡献的最高认可。颁奖词特别提到了他在数值分析方面的研究，尤其是在高效精确地处理数值线性代数问题方面的工作。

---

## 11. 它解决了当时什么瓶颈

**瓶颈一：前向误差界的过度悲观**。von Neumann-Goldstine 的前向分析表明，$n$ 阶矩阵的 Gauss 消元法可能产生 $O(4^n)$ 的误差增长——这意味着对于 $n = 100$ 的矩阵，计算结果可能毫无意义。但实际计算表明 Gauss 消元法（带部分主元选取）对大矩阵工作得很好。Wilkinson 的后向分析解释了这一矛盾：增长因子 $\rho_n$ 在实践中远小于理论上界 $2^{n-1}$。

**瓶颈二：缺乏统一的算法评价标准**。不同的研究者使用不同的误差度量和分析方法来评价数值算法，结果之间难以比较。后向稳定性提供了一个统一的、可操作的标准：一个算法要么是后向稳定的（好算法），要么不是（需要改进）。

**瓶颈三：不知道何时可以信任计算结果**。在 Wilkinson 的工作之前，科学家们经常不确定计算机给出的结果是否可信。后向误差分析结合条件数估计提供了一个实用的可靠性判据：如果后向误差小且条件数温和，结果是可信的；如果条件数很大，即使算法完美，结果也可能不准确——但这是问题本身的性质，不是算法的缺陷。

**瓶颈四：特征值算法的数值分析**。在 Wilkinson 之前，特征值算法的舍入误差分析几乎是空白。Wilkinson 在《The Algebraic Eigenvalue Problem》中为几乎所有已知的特征值算法（Jacobi 方法、Givens-Householder 化简、QR 算法、反幂迭代等）提供了详尽的后向误差分析，奠定了该领域的理论基础。

---

## 12. 它与前人工作的关系

**von Neumann 和 Goldstine（1947）**。von Neumann 和 Goldstine 在矩阵求逆的误差分析中引入了条件数的概念。他们的前向误差分析虽然过于悲观，但为 Wilkinson 的工作提供了重要的起点和动机。Wilkinson 的后向分析可以看作是对 von Neumann-Goldstine 分析的根本性改进——用更合适的框架重新回答了同一个问题。

**Turing（1948）**。Turing 在他的论文"Rounding-Off Errors in Matrix Processes"中也讨论了矩阵计算中的舍入误差，引入了一种条件数的概念。Wilkinson 在 NPL 与 Turing 的共事经历对他的工作产生了直接影响。可以说，Wilkinson 继承并发展了 Turing 的思想路线。

**Givens（1954）和 Householder（1958）**。Givens 旋转和 Householder 变换的提出部分是出于数值稳定性的考虑——正交变换不放大误差。Wilkinson 的贡献在于将这种直觉上升为严格的理论：他精确地量化了正交变换类算法的后向误差，并与非正交变换类算法（如 Gauss 消元法）进行了系统比较。

**Rutishauser 和 Francis**。LR 算法（Rutishauser, 1958）和 QR 算法（Francis, 1961—1962）的数值稳定性分析是 Wilkinson《The Algebraic Eigenvalue Problem》中的核心内容。Wilkinson 的分析不仅证实了 QR 算法的后向稳定性，还精确地量化了其误差行为。

**浮点运算标准化的需求**。Wilkinson 的工作在浮点运算标准 IEEE 754（1985 年发布）之前完成，当时不同计算机使用不同的浮点格式。Wilkinson 的分析框架足够一般，可以适用于各种浮点系统。反过来，他的工作也为 IEEE 754 标准的制定提供了理论动机——标准化的浮点运算使得误差分析更加可预测和可靠。

---

## 13. 它对后续哪些方向产生了影响

Wilkinson 的后向误差分析框架对数值分析和计算科学产生了全方位的影响。

**LAPACK 和数值软件的设计哲学**。LAPACK（1992 年至今）的设计从根本上遵循 Wilkinson 的后向稳定性原则。每个 LAPACK 例程都以后向稳定性为设计目标，并附有误差界的文档。LAPACK 的用户指南（Anderson et al., 1999）系统地使用后向误差分析来描述每个算法的数值行为。

**条件数估计**。受 Wilkinson 工作的启发，高效的条件数估计方法成为一个重要的研究方向。Cline、Moler、Stewart 和 Wilkinson（1979）以及 Hager（1984）和 Higham（1988）发展了高效的条件数估计算法，这些算法被集成到 LAPACK 中（如 DGECON、DTRCON 等例程），使得用户可以方便地评估计算结果的可靠性。

**Higham 的现代综合**。Nicholas Higham 的著作《Accuracy and Stability of Numerical Algorithms》（第一版 1996 年，第二版 2002 年）是 Wilkinson 工作的现代继承和扩展。Higham 将后向误差分析应用于更广泛的数值算法——包括矩阵函数、结构化矩阵算法、混合精度计算等——并系统化了 Wilkinson 的分析技巧。

**IEEE 754 浮点标准**。虽然 IEEE 754 标准的制定涉及多方面的考虑，但 Wilkinson 的工作为标准中的一些关键设计决策（如正确舍入的要求、渐进下溢等）提供了理论支撑。W. Kahan（IEEE 754 标准的主要设计者之一，1989 年图灵奖获得者）受到了 Wilkinson 工作的深刻影响。

**算法验证和测试**。Wilkinson 的后向误差框架为算法验证提供了客观标准。后向误差的大小可以在计算完成后廉价地估计或精确计算（不需要知道真解），这使得自动化的算法测试成为可能。LAPACK 的测试套件广泛使用后向误差作为通过/失败的判据。

**迭代精化（Iterative Refinement）**。Wilkinson 分析了迭代精化技术——使用高精度的残差计算来逐步改进近似解的精度。这一技术后来被推广为混合精度计算（mixed precision computing）的基础，在 GPU 计算时代获得了新生（Langou et al., 2006; Higham et al., 2019）。

**数值分析的教育**。Wilkinson 的后向误差分析范式成为数值分析课程的核心内容。几乎所有数值分析教科书都以后向误差分析为框架来讨论算法的稳定性，这极大地提高了数值分析教育的系统性和深度。

**对机器学习的潜在影响**。在当今的深度学习时代，低精度浮点运算（如 float16、bfloat16、甚至 int8）被广泛使用以加速训练和推理。Wilkinson 的误差分析框架为理解低精度计算的可靠性提供了理论工具。虽然深度学习中的误差分析远比线性代数复杂，但后向误差分析的哲学——"我们实际在优化什么？"——对于理解低精度训练的行为具有启发意义。

---

## 14. 今天回看它的价值

在 Wilkinson 的著作出版 60 余年后的今天，他的工作的价值不仅没有减弱，反而在新的技术背景下获得了新的意义。

**在混合精度计算中的复兴**。现代 GPU（如 NVIDIA 的 Tensor Cores）支持多种精度的浮点运算——float64、float32、float16、bfloat16。利用低精度计算加速求解、然后通过迭代精化在高精度中改进结果——这正是 Wilkinson 分析的迭代精化技术在现代硬件上的应用。Higham 和 Mary（2019）等人的最新工作将 Wilkinson 的理论推广到多精度环境中。

**在可重现计算中的意义**。计算可重现性（reproducibility）是当今科学计算面临的重要挑战。由于浮点运算的非结合性，同一个程序在不同硬件或不同并行配置下可能给出不同的结果。Wilkinson 的后向误差分析框架提供了一个理论基础来理解和量化这些差异。

**在数据科学中的应用**。当代数据科学中广泛使用的矩阵分解——SVD、QR 分解、特征值分解、Cholesky 分解——的数值稳定性分析都建立在 Wilkinson 的后向误差框架之上。数据科学家可能不需要了解误差分析的细节，但他们使用的每一个矩阵计算工具的可靠性都由 Wilkinson 的理论来保证。

**作为思维范式的持久影响**。后向误差分析所体现的思维方式——将"答案有多错"的问题转化为"我们实际求解了什么问题"——已经超越了数值线性代数的具体领域，成为一种普遍的科学思维方式。在任何涉及近似计算的领域——从统计推断到优化算法，从信号处理到控制理论——这种思维方式都具有启发意义。

**"Wilkinson 多项式"的经久魅力**。Wilkinson 多项式作为一个教学工具，至今仍然出现在几乎所有数值分析课程中。它简洁地展示了一个深刻的道理：数值不稳定性不仅可能来自算法，更可能来自问题本身。这个例子的持久魅力在于它的简单性和说服力——它只需要 20 个整数的乘积就能展示出令人震惊的数值敏感性。

---

## 15. 面向普通读者的通俗解释

想象你是一位翻译官，需要把一段英文翻译成中文。原文是一位外国领导人的讲话，可能在传达过程中已经经过了多次转述（输入数据本身就有不确定性）。

**前向误差分析**就像有人拿着你的中文翻译和原始英文进行逐字比对，指出你翻错了几个词。这虽然有用，但你可能会辩解说："原文本身就有多种理解方式。"

**后向误差分析**则更加公允：它问的是，"如果你的翻译是完美翻译的话，那么你翻译的原文是什么？"如果这个"隐含的原文"与实际原文只有微小差异（几个标点或措辞的不同），那么你的翻译水平是很高的——即使最终中文表达与某些人的期望有所不同。

**条件数**则衡量的是"这段话有多难翻"。有些话——如技术性很强的法律条款——是"病态"的，任何微小的理解偏差都可能导致完全不同的翻译。而有些话——如日常寒暄——是"良态"的，即使理解有小偏差，翻译结果也差不多。

Wilkinson 告诉我们：**评价一位翻译（算法）的水平，不应该只看最终翻译与原意的差距（前向误差），而应该看翻译官的"等效理解误差"有多小（后向误差）。如果等效理解误差很小，但翻译结果仍然偏差较大，那是因为原文本身太微妙了（条件数太大），不是翻译官的错。**

回到计算机的世界：当你的计算机求解一个含有 1000 个未知数的方程组，每一步计算都会有微小的舍入误差。Wilkinson 的理论告诉我们，如果使用好的算法（如带部分主元选取的 Gauss 消元法），那么计算结果虽然不是原始方程的精确解，但它是一个与原始方程极其接近的方程的精确解。如果这个"极其接近"的程度小于输入数据本身的测量误差，那么计算结果在实际意义上是完美的。

---

## 16. 阅读原文建议

**《Rounding Errors in Algebraic Processes》（1963）**：
- 这是一本相对简短（约 160 页）的著作，可以作为入门读物
- 它系统地介绍了浮点运算的基本性质、前向和后向误差分析方法
- 推荐按顺序阅读，特别注意第一部分（浮点运算基础）和第三部分（线性代数中的误差分析）
- 预备知识：线性代数基础、浮点运算的基本概念

**《The Algebraic Eigenvalue Problem》（1965）**：
- 这是一部巨著（约 660 页），内容极为丰富
- 可以作为参考书使用，不需要从头到尾阅读
- 重点章节：第一章（矩阵理论基础）、第二章（扰动理论）、第三章（误差分析）
- 每个特征值算法的讨论都包含详尽的误差分析，可以根据兴趣选择性阅读
- 预备知识：矩阵分析、特征值理论、浮点运算

**更现代的替代材料**：
- Higham, N. J. *Accuracy and Stability of Numerical Algorithms*. 2nd ed. SIAM, 2002. 这是 Wilkinson 工作的现代继承者，覆盖范围更广，写作风格更现代。强烈推荐作为学习后向误差分析的首选教科书。
- Trefethen, L. N. and Bau, D. *Numerical Linear Algebra*. SIAM, 1997. 以讲座风格呈现后向误差分析的核心思想，第 12—18 讲特别相关。
- Golub, G. H. and Van Loan, C. F. *Matrix Computations*. 4th ed. Johns Hopkins University Press, 2013. 第 2 章系统讨论了浮点运算和误差分析。

---

## 17. 局限性/历史局限

**主要针对线性代数问题**。Wilkinson 的两部著作主要关注线性方程组和特征值问题。虽然后向误差分析的哲学可以推广到更广泛的数值计算领域（如非线性方程、微分方程、优化等），但具体的推广需要额外的技术工作。

**最坏情况分析与平均情况的差距**。Wilkinson 的分析（如 Gauss 消元法的增长因子界 $2^{n-1}$）给出的是最坏情况下的界。在实践中，实际增长因子远小于这个理论上界。这种最坏情况与平均情况之间的差距——即为什么 Gauss 消元法在实践中比理论预测更好——直到几十年后才通过 Spielman 和 Teng 的"光滑分析"（smoothed analysis, 2004）和 Sankar、Spielman 和 Teng 的增长因子分析等工作得到部分解释。

**对非正规矩阵的处理**。Wilkinson 的条件数理论主要基于范数扰动分析。对于非正规矩阵（non-normal matrices），特征值对扰动的敏感性更为微妙，需要使用伪谱（pseudospectra）等更精细的工具来刻画。Trefethen 和 Embree 的《Spectra and Pseudospectra》（2005）将这方面的分析推向了更深入的层次。

**浮点标准的局限**。Wilkinson 的工作在 IEEE 754 浮点标准（1985）之前完成。虽然他的分析框架足够一般，但某些细节（如非正规数、渐进下溢、特殊值 NaN 和 Inf 的处理）在现代浮点标准下需要更新和补充。

**对并行计算的考虑不足**。Wilkinson 的分析假设计算是顺序的。在并行计算中，浮点运算的非结合性意味着不同的并行调度可能产生不同的结果。虽然后向误差分析的基本框架仍然适用，但并行化带来的额外复杂性需要专门处理。

**遗留的开放问题**。Gauss 消元法增长因子的确切行为至今仍然是数值分析中最大的未解之谜之一。Wilkinson 猜测增长因子对于带部分主元选取的 Gauss 消元法最多为 $n^{1/2}$（对于随机矩阵），但严格的证明仍然缺失（虽然已有许多部分结果）。

---

## 18. 延伸阅读建议

**Wilkinson 的著作**：
- Wilkinson, J. H. *Rounding Errors in Algebraic Processes*. Prentice-Hall, 1963. (Also published in German by Springer.) 后向误差分析的奠基之作。
- Wilkinson, J. H. *The Algebraic Eigenvalue Problem*. Clarendon Press, Oxford, 1965. 特征值问题的权威参考。

**现代后向误差分析**：
- Higham, N. J. *Accuracy and Stability of Numerical Algorithms*. 2nd ed. SIAM, 2002. Wilkinson 工作的现代继承者和扩展，覆盖范围更广，是学习后向误差分析的最佳教科书。

**教科书中的后向误差分析**：
- Trefethen, L. N. and Bau, D. *Numerical Linear Algebra*. SIAM, 1997. 第 12—18 讲以极其清晰的方式讲解后向误差分析和稳定性。
- Golub, G. H. and Van Loan, C. F. *Matrix Computations*. 4th ed. Johns Hopkins University Press, 2013. 第 2 章。

**条件数和扰动理论**：
- Stewart, G. W. and Sun, J. *Matrix Perturbation Theory*. Academic Press, 1990. 矩阵扰动理论的全面参考。
- Trefethen, L. N. and Embree, M. *Spectra and Pseudospectra: The Behavior of Nonnormal Matrices and Operators*. Princeton University Press, 2005. 将扰动分析推向更深入的层次。

**IEEE 754 浮点标准**：
- Overton, M. L. *Numerical Computing with IEEE Floating Point Arithmetic*. SIAM, 2001. 清晰地介绍了 IEEE 754 标准及其对数值计算的影响。

**光滑分析**：
- Spielman, D. A. and Teng, S.-H. "Smoothed analysis of algorithms: Why the simplex algorithm usually takes polynomial time." *Journal of the ACM*, 51(3):385--463, 2004. 光滑分析理论可以部分解释 Wilkinson 分析中最坏情况与实际情况的差距。

**混合精度计算**：
- Higham, N. J. and Mary, T. "Mixed precision algorithms in numerical linear algebra." *Acta Numerica*, 31:347--414, 2022. Wilkinson 误差分析在现代混合精度计算中的应用。

**传记和历史**：
- Fox, L. "Obituary: James Hardy Wilkinson, 1919--1986." *Bulletin of the London Mathematical Society*, 19(5):477--495, 1987.
- Moler, C. B. "Reminiscences about Wilkinson." *SIAM News*, 1987. Cleve Moler（MATLAB 的创始人）对 Wilkinson 的回忆。

---

## 19. 参考资料/实际引用文档

1. Wilkinson, J. H. *Rounding Errors in Algebraic Processes*. Prentice-Hall, 1963.

2. Wilkinson, J. H. *The Algebraic Eigenvalue Problem*. Clarendon Press, Oxford, 1965.

3. von Neumann, J. and Goldstine, H. H. "Numerical inverting of matrices of high order." *Bulletin of the American Mathematical Society*, 53(11):1021--1099, 1947.

4. Turing, A. M. "Rounding-off errors in matrix processes." *Quarterly Journal of Mechanics and Applied Mathematics*, 1(1):287--308, 1948.

5. Higham, N. J. *Accuracy and Stability of Numerical Algorithms*. 2nd ed. SIAM, 2002.

6. Trefethen, L. N. and Bau, D. *Numerical Linear Algebra*. SIAM, 1997.

7. Golub, G. H. and Van Loan, C. F. *Matrix Computations*. 4th ed. Johns Hopkins University Press, 2013.

8. Anderson, E. et al. *LAPACK Users' Guide*. 3rd ed. SIAM, 1999.

9. Stewart, G. W. and Sun, J. *Matrix Perturbation Theory*. Academic Press, 1990.

10. Trefethen, L. N. and Embree, M. *Spectra and Pseudospectra: The Behavior of Nonnormal Matrices and Operators*. Princeton University Press, 2005.

11. Higham, N. J. and Mary, T. "Mixed precision algorithms in numerical linear algebra." *Acta Numerica*, 31:347--414, 2022.

12. Spielman, D. A. and Teng, S.-H. "Smoothed analysis of algorithms: Why the simplex algorithm usually takes polynomial time." *Journal of the ACM*, 51(3):385--463, 2004.

13. Fox, L. "Obituary: James Hardy Wilkinson, 1919--1986." *Bulletin of the London Mathematical Society*, 19(5):477--495, 1987.

14. Overton, M. L. *Numerical Computing with IEEE Floating Point Arithmetic*. SIAM, 2001.
