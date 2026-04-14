# CI/CD 与发布流程

## 文档来源与路径

| 类型 | 路径 |
|------|------|
| GitHub 工作流 | `.github/workflows/` |
| 脚本与自动化 | `.github/scripts/` |
| 发布说明 | `.github/RELEASING.md` |
| Release Please 配置（仓库根） | `release-please-config.json`、`.release-please-manifest.json` |
| PR 模板与标签 | `.github/PULL_REQUEST_TEMPLATE.md`、`pr_labeler.yml`、`pr-labeler.js`、`pr-labeler-config.json` |

---

## 概述

Deep Agents monorepo 使用 **GitHub Actions** 驱动 **持续集成**（按变更路径选择性跑各包）、**行为评估（Evals）**、**Harbor / Terminal Bench 类基准**、**版本与可选依赖一致性检查**，以及基于 **release-please** 的 **CLI 发布流水线**。辅助逻辑集中在 `.github/scripts/`。

---

## 主要工作流（`.github/workflows/`）

### CI（`ci.yml` 及复用子工作流）

- **触发**：`pull_request`、`push` 至 `main`、`merge_group` 等。
- **行为要点**：
  - 通过 **paths filter** 检测 `libs/deepagents`、`libs/cli`、`libs/evals` 及各 `partners`、`repl` 等是否变更，**仅对受影响包跑 lint / 单元测试**；**SDK 变更会连带触发 CLI 测试**。
  - 与 `_lint.yml`、`_test.yml` 等复用工作流配合，完成 **ruff / ty / pytest** 等质量门禁。
- **并发**：同一 workflow + ref 分组，`cancel-in-progress` 取消冗余运行。

### Evals（`evals.yml`）

- **定位**：对 **真实 LLM** 跑 `libs/evals` 下的行为评估（需 `LANGSMITH_*` 及各厂商 API Key 等 secrets）。
- **模型选择**：工作流 `inputs` 提供 **预设集合** 与 **单模型** 规格；预设定义可参考 `libs/evals/MODEL_GROUPS.md`。
- **矩阵来源**：与 `.github/scripts/models.py` 生成的 JSON 矩阵配合（见下文「模型矩阵」）。
- **Eval 并发**：按 **provider 分组的 concurrency**，**同一提供商上的多个 job 串行排队**，**不同提供商并行**，减轻速率限制与配额冲突（详见 `libs/evals/README.md` 中「CI concurrency」）。

### Harbor（`harbor.yml`）

- **定位**：**Terminal Bench** 等基准场景的运行（与 eval 体系共享模型注册脚本思路，环境变量侧使用 `HARBOR_MODELS` 等）。

### Release / release-please（`release.yml`、`release-please.yml`）

- **release-please**：根据 **Conventional Commits** 分析变更，打开/更新 **发布 PR**，合并后触发 **PyPI 发布与 GitHub Release**（细节以 `.github/RELEASING.md` 为准）。

### SDK pin 检查（`check_sdk_pin.yml` 等）

- **目的**：保证 CLI 等对 SDK 的 **版本钉选（pin）** 与仓库策略一致，避免发版时依赖版本漂移。

### 其他质量门禁

- **`check_versions.yml`**：配合 `check_version_equality.py`。
- **`check_extras_sync.yml`**：配合 `check_extras_sync.py`。
- **`check_lockfiles.yml`**：锁文件一致性。
- **`pr_lint.yml`**：PR 标题等符合约定式提交与 scope。
- **`auto-label-by-package.yml`、`pr_labeler.yml`、`pr_labeler_backfill.yml`**：PR 自动打标签；脚本实现见 `.github/scripts/pr-labeler.js` 与 `pr-labeler-config.json`。

---

## `release-please-config.json` 与多包发布

根目录 `release-please-config.json` 声明 **changelog 分段**、**PR 标题模板**、**tag 规则**等。当前仓库中 **`packages` 映射以 `libs/cli`（`deepagents-cli`）为主**：包含 `pyproject.toml` 与 `deepagents_cli/_version.py` 等 **extra-files**，由 release-please 统一改版本号与 `CHANGELOG.md`。

> **说明**：配置结构 **支持扩展多个路径键**（每个 lib 一段）；若未来增加更多 PyPI 包，可在同一文件的 `packages` 下追加条目，并配合 `.release-please-manifest.json` 维护各路径版本。请以仓库内实际 JSON 为准。

---

## 版本一致性：`.github/scripts/check_version_equality.py`

- **作用**：确保 **`pyproject.toml` 中的版本** 与 **`_version.py` 等单一真源** 对 **deepagents**、**cli** 等指定包 **保持一致**，防止发布物与导入版本字符串不一致。

---

## 可选依赖同步：`.github/scripts/check_extras_sync.py`

- **作用**：校验各包 **optional dependency groups / extras** 在 monorepo 内 **声明同步**，避免文档或元数据与可安装 extras 漂移。

---

## 模型矩阵：`.github/scripts/models.py`

- **`Model` 具名元组**：`spec`（如 `anthropic:claude-sonnet-4-6`）+ `groups`（frozenset，标签含 `eval:*`、`harbor:*` 等）。
- **`REGISTRY`**：全量模型清单；预设集合通过 **`_EVAL_PRESETS` / `_HARBOR_PRESETS`**（及文档中的 `EVAL_MODELS`、`HARBOR_MODELS` 环境变量语义）解析为 **并行矩阵 JSON**，供 Actions 使用。
- **调用方式**（脚本注释摘要）：
  - `python .github/scripts/models.py eval` — 读取 `EVAL_MODELS`
  - `python .github/scripts/models.py harbor` — 读取 `HARBOR_MODELS`

---

## Eval CI 并发（再述）

- **同 provider**：共享 concurrency group，**第二个 job 等待第一个**。
- **跨 provider**：可 **并行**，提高吞吐并分散配额风险。

---

## PR 标签与贡献体验

- **`pr-labeler.js` + `pr-labeler-config.json`**：按规则为 PR 自动加标签，便于筛选与发布说明归类。
- **`PULL_REQUEST_TEMPLATE.md`**：引导贡献者填写 **AI 辅助声明**、测试说明等（与 `AGENTS.md` 中 PR 准则呼应）。

---

## 设计取舍

- **变更敏感 CI**：仅测改动相关包，缩短反馈时间；核心 SDK 变更仍拉通 CLI，避免集成断裂。
- **脚本单源化模型列表**：`models.py` 避免在 YAML 中手写冗长矩阵，降低 eval 与 harbor 分叉风险。
- **release-please 与版本脚本双保险**：自动化发版 + CI 版本相等检查，减少人为漏改。

---

## 小结

CI/CD 以 **`.github/workflows/`** 为入口，**脚本层（`check_version_equality.py`、`check_extras_sync.py`、`models.py` 等）** 承担可复用策略；发布以 **release-please** 与 **`.github/RELEASING.md`** 为权威流程说明。
