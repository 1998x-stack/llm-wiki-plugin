# 06 · 随机森林（Random Forests）
> 《Random Forests》  
> **作者**：Leo Breiman　**期刊**：Machine Learning　**年份**：2001

---

## 一、历史背景

决策树是机器学习中最直觉化的模型——像一棵流程图，每个节点做一次判断，叶节点给出预测。但决策树有一个致命弱点：**极度不稳定（高方差）**。训练数据稍有变化，整棵树的结构就可能面目全非。

贝尔实验室统计学家 Leo Breiman 在研究集成方法多年后，融合两项技术提出了随机森林：

```
随机森林 = Bagging（自举聚合，1996）+ 随机特征子集（新贡献）
```

他的核心洞见：

> **如果一棵树不可靠，就种一片森林——成千上万棵树投票，错误相互抵消。但仅仅 Bagging 还不够，必须进一步降低树间的相关性，才能真正发挥集成优势。**

---

## 二、Bagging：自举聚合

Breiman 于 1996 年提出的 Bagging 是随机森林的基础：

```
训练集 D（N 个样本）

有放回随机抽样，生成 T 个子集：
  D₁ ← 从 D 有放回抽取 N 个样本（约含 63.2% 的唯一样本）
  D₂ ← 同上
  ...
  Dₜ ← 同上

在每个 Dᵢ 上训练一棵完整决策树 hᵢ

集成预测：
  分类：多数投票  ŷ = mode{ h₁(x), h₂(x), ..., hₜ(x) }
  回归：平均值   ŷ = mean{ h₁(x), h₂(x), ..., hₜ(x) }
```

**63.2% 的数学原理**：有放回抽 N 次，某样本不被抽中的概率为 (1-1/N)^N → 1/e ≈ 36.8%，故约 63.2% 被抽中。

---

## 三、随机特征子集：降低树间相关性

单纯 Bagging 的问题：若某特征极强，每棵树都会在根节点选它 → 树高度相关 → 集成收益有限。

随机森林的创新：**每次分裂节点时，只随机选 m 个特征，在这 m 个中找最优分裂点**。

```
全特征数 p（如 p = 100）

每个节点分裂时：
  随机抽 m 个特征     ← 分类任务推荐 m = ⌊√p⌋ ≈ 10
                      ← 回归任务推荐 m = ⌊p/3⌋
  仅在这 m 个特征中寻找最优分裂点

→ 各树差异化更大 → 相关性降低 → 集成效果更好
```

---

## 四、偏差-方差分解视角

```
期望误差 = 偏差² + 方差 + 不可约噪声

单棵完整决策树：
  偏差低（几乎完美拟合训练数据）
  方差高（对训练数据噪声极敏感）

随机森林（T 棵相关系数为 ρ 的树，方差各为 σ²）：
  集成方差 = ρ·σ² + (1-ρ)/T · σ²

  当 T → ∞：方差下限 = ρ·σ²（由树间相关性决定）
  → 随机特征降低 ρ → 集成方差进一步降低
  → 偏差略微升高（限制了每棵树的最优性）
  → 整体误差显著降低
```

---

## 五、袋外误差（Out-of-Bag Error）

Bagging 的神奇副产品：每棵树训练时约 36.8% 的样本未被使用（袋外样本，OOB）。

```
对每个训练样本 xᵢ：
  找到所有"没有用 xᵢ 训练"的决策树（约 T/e 棵）
  用这些树对 xᵢ 预测并投票

OOB 误差 = 所有样本的 OOB 预测误差均值
         ≈ 交叉验证误差（无需额外划分验证集！）
```

---

## 六、特征重要性

随机森林提供了两种量化特征重要性的方法：

**基尼重要性（Mean Decrease Impurity）**：

```
对每个特征 j，累计所有树中以 j 为分裂点时降低的基尼不纯度之和
→ 快速，但对高基数特征有偏
```

**排列重要性（Permutation Importance，更可靠）**：

```
for 每个特征 j：
  1. 计算原始 OOB 误差 E
  2. 随机打乱特征 j 的值（破坏其信息）
  3. 计算打乱后的 OOB 误差 E'
  4. 重要性(j) = E' - E
     （误差增量越大 → 特征越重要）
```

---

## 七、完整代码实现

```python
import numpy as np
from typing import List, Optional, Tuple
from collections import Counter


# ── 决策树节点 ─────────────────────────────────────────

class Node:
    """决策树节点"""
    __slots__ = ["feature", "threshold", "left", "right", "value"]

    def __init__(self, feature=None, threshold=None,
                 left=None, right=None, value=None):
        self.feature = feature      # 分裂特征索引
        self.threshold = threshold  # 分裂阈值
        self.left = left            # 左子树
        self.right = right          # 右子树
        self.value = value          # 叶节点预测值（None 表示内部节点）


# ── 单棵决策树 ────────────────────────────────────────

class DecisionTree:
    """CART 分类决策树（基尼不纯度）"""

    def __init__(self, max_depth: int = None,
                 min_samples_split: int = 2,
                 max_features: Optional[int] = None,
                 random_state: Optional[int] = None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.rng = np.random.RandomState(random_state)
        self.root: Optional[Node] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "DecisionTree":
        self.n_features = X.shape[1]
        self.root = self._grow(X, y, depth=0)
        return self

    def _gini(self, y: np.ndarray) -> float:
        """基尼不纯度"""
        n = len(y)
        if n == 0:
            return 0.0
        counts = np.bincount(y)
        probs = counts / n
        return 1.0 - float(np.sum(probs ** 2))

    def _best_split(self, X: np.ndarray, y: np.ndarray
                    ) -> Tuple[Optional[int], Optional[float]]:
        """在随机特征子集中寻找最优分裂点"""
        best_gain, best_feat, best_thr = -1.0, None, None
        gini_parent = self._gini(y)
        n = len(y)

        # 随机选 max_features 个特征
        n_feat = self.max_features or self.n_features
        feat_indices = self.rng.choice(self.n_features, n_feat, replace=False)

        for feat in feat_indices:
            thresholds = np.unique(X[:, feat])
            for thr in thresholds:
                left_mask = X[:, feat] <= thr
                n_l, n_r = left_mask.sum(), (~left_mask).sum()
                if n_l == 0 or n_r == 0:
                    continue
                gain = (gini_parent
                        - (n_l / n) * self._gini(y[left_mask])
                        - (n_r / n) * self._gini(y[~left_mask]))
                if gain > best_gain:
                    best_gain, best_feat, best_thr = gain, feat, thr

        return best_feat, best_thr

    def _grow(self, X: np.ndarray, y: np.ndarray, depth: int) -> Node:
        """递归构建树"""
        # 叶节点条件
        n_classes = len(np.unique(y))
        if (n_classes == 1
                or len(y) < self.min_samples_split
                or (self.max_depth is not None and depth >= self.max_depth)):
            return Node(value=Counter(y).most_common(1)[0][0])

        feat, thr = self._best_split(X, y)
        if feat is None:
            return Node(value=Counter(y).most_common(1)[0][0])

        mask = X[:, feat] <= thr
        return Node(
            feature=feat, threshold=thr,
            left=self._grow(X[mask], y[mask], depth + 1),
            right=self._grow(X[~mask], y[~mask], depth + 1),
        )

    def _traverse(self, x: np.ndarray, node: Node) -> int:
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._traverse(x, node.left)
        return self._traverse(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self._traverse(x, self.root) for x in X])


# ── 随机森林 ──────────────────────────────────────────

class RandomForest:
    """
    随机森林分类器（Breiman, 2001）

    结合 Bagging（有放回抽样）与随机特征子集，
    通过多棵决策树的多数投票进行预测。
    """

    def __init__(self, n_estimators: int = 200,
                 max_features: str = "sqrt",
                 max_depth: Optional[int] = None,
                 min_samples_split: int = 2,
                 oob_score: bool = True,
                 n_jobs: int = 1,
                 random_state: Optional[int] = 42):
        """
        Args:
            n_estimators:      决策树数量（越多越稳定，不会过拟合）
            max_features:      每节点随机特征数 ('sqrt' | 'log2' | int)
            max_depth:         树的最大深度（None=完全生长）
            min_samples_split: 分裂所需最小样本数
            oob_score:         是否计算袋外误差估计
            n_jobs:            并行线程数（此实现为串行）
            random_state:      随机种子
        """
        self.n_estimators = n_estimators
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.oob_score = oob_score
        self.n_jobs = n_jobs
        self.rng = np.random.RandomState(random_state)
        self.trees: List[Tuple[DecisionTree, np.ndarray]] = []  # (树, 使用的样本索引)
        self.oob_score_: Optional[float] = None
        self.feature_importances_: Optional[np.ndarray] = None
        self.n_features_: int = 0
        self.classes_: Optional[np.ndarray] = None

    def _resolve_max_features(self, p: int) -> int:
        if self.max_features == "sqrt":
            return max(1, int(np.sqrt(p)))
        elif self.max_features == "log2":
            return max(1, int(np.log2(p)))
        elif isinstance(self.max_features, int):
            return self.max_features
        return p

    def fit(self, X: np.ndarray, y: np.ndarray) -> "RandomForest":
        n, p = X.shape
        self.n_features_ = p
        self.classes_ = np.unique(y)
        m = self._resolve_max_features(p)

        # OOB 投票矩阵
        oob_votes = np.zeros((n, len(self.classes_)), dtype=int) if self.oob_score else None

        self.trees = []
        for t in range(self.n_estimators):
            # Bagging：有放回抽样
            boot_idx = self.rng.choice(n, n, replace=True)
            X_boot, y_boot = X[boot_idx], y[boot_idx]

            # 构建随机决策树
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=m,
                random_state=self.rng.randint(0, 100000),
            )
            tree.fit(X_boot, y_boot)
            self.trees.append((tree, boot_idx))

            # 累计 OOB 投票
            if oob_votes is not None:
                oob_mask = np.ones(n, dtype=bool)
                oob_mask[np.unique(boot_idx)] = False
                if oob_mask.any():
                    preds = tree.predict(X[oob_mask])
                    for idx, pred in zip(np.where(oob_mask)[0], preds):
                        cls_pos = np.where(self.classes_ == pred)[0]
                        if len(cls_pos):
                            oob_votes[idx, cls_pos[0]] += 1

        # 计算 OOB 误差
        if oob_votes is not None:
            valid = oob_votes.sum(axis=1) > 0
            oob_preds = self.classes_[oob_votes[valid].argmax(axis=1)]
            self.oob_score_ = (oob_preds == y[valid]).mean()
            print(f"  OOB 误差估计：{1 - self.oob_score_:.4f}  "
                  f"（OOB 准确率 {self.oob_score_:.4f}）")

        # 计算特征重要性（基尼）
        self._compute_feature_importances(p)
        return self

    def _compute_feature_importances(self, p: int) -> None:
        importances = np.zeros(p)
        for tree, _ in self.trees:
            self._traverse_importances(tree.root, importances)
        total = importances.sum()
        self.feature_importances_ = importances / total if total > 0 else importances

    def _traverse_importances(self, node: Node, importances: np.ndarray) -> None:
        if node is None or node.value is not None:
            return
        importances[node.feature] += 1.0
        self._traverse_importances(node.left, importances)
        self._traverse_importances(node.right, importances)

    def predict(self, X: np.ndarray) -> np.ndarray:
        # 收集所有树的预测（多数投票）
        all_preds = np.array([tree.predict(X) for tree, _ in self.trees])  # (T, N)
        result = []
        for col in all_preds.T:
            result.append(Counter(col).most_common(1)[0][0])
        return np.array(result)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        return (self.predict(X) == y).mean()


# ── 演示 ──────────────────────────────────────────────
if __name__ == "__main__":
    from sklearn.datasets import load_iris, load_breast_cancer
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    print("=== Iris 数据集 ===")
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForest(n_estimators=100, max_features="sqrt", random_state=42)
    rf.fit(X_train, y_train)
    print(f"  测试准确率：{rf.score(X_test, y_test):.4f}")
    print(f"  特征重要性：{rf.feature_importances_.round(3)}")

    # 与 sklearn 对比
    print("\n=== sklearn 随机森林对比 ===")
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=200, oob_score=True, random_state=42)
    clf.fit(X_train, y_train)
    print(f"  sklearn 测试准确率：{clf.score(X_test, y_test):.4f}")
    print(f"  sklearn OOB 准确率：{clf.oob_score_:.4f}")
```

---

## 八、随机森林的核心优势

| 特性 | 优势说明 |
|------|---------|
| **无需调参即可工作** | 默认参数通常已经很好 |
| **OOB 误差** | 内置验证集，无需交叉验证 |
| **特征重要性** | 可解释性强，支持特征选择 |
| **天然抗过拟合** | 树越多越稳定（不会因树多而过拟合） |
| **并行训练** | 每棵树独立，天然支持多核并行 |
| **处理混合数据** | 数值 + 类别特征均可 |

---

## 九、历史地位

| 维度 | 评价 |
|------|------|
| 理论严格性 | ⭐⭐⭐⭐⭐ 偏差方差分解，收敛证明 |
| 实用性 | ⭐⭐⭐⭐⭐ 至今仍是表格数据的首选 |
| 可解释性 | ⭐⭐⭐⭐ 特征重要性，可视化决策路径 |
| 历史影响 | ⭐⭐⭐⭐⭐ 催生了 XGBoost、LightGBM 等 |

深度学习崛起之前，随机森林是 Kaggle 竞赛的绝对主力；至今在表格数据上仍与 XGBoost 并列最强。

---

## 一句话总结

> 随机森林告诉我们，民主（多数投票）有时比独裁（单一最优模型）更可靠——集体智慧胜过个体天才。

---

*参考：Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32.*
