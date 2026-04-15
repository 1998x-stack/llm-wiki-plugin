---
summary: "Engine version release workflow including semantic versioning rules and release steps"
last_updated: "2026-04-02"
---

# 引擎版本发布指南

## 版本号规则

UrhoX 遵循 [语义化版本控制](https://semver.org/lang/zh-CN/)（Semantic Versioning），版本号格式为 `major.minor.patch`：

| 版本段 | 名称 | 递增时机 | 示例 |
|--------|------|----------|------|
| major | 主版本 | 重大架构变更、不兼容的 API 改动 | 1.x.x → 2.0.0 |
| minor | 次版本 | 新增功能、向后兼容的改进 | 1.2.x → 1.3.0 |
| patch | 修订版本 | Bug 修复、小改进 | 1.2.3 → 1.2.4 |

**稳定分支**：每个 `major.minor` 组合称为一个稳定分支（如 1.2.x），在该分支上持续发布 patch 版本。

## 构建类型

### 开发构建（Development Build）

- **触发方式**：合并 PR 到 main 分支
- **版本号**：最新 tag + 0.0.1（预览下一个 patch 版本）
- **用途**：内部测试、CI 验证
- **特点**：
  - 自动上传到 CDN（更新 `preview.json` 和版本目录）
  - 不更新 `latest.json`
  - 不上传 OSS
  - 不创建 Git Tag
  - 版本目录会被后续构建覆盖

### 正式发布（Release Build）

- **触发方式**：手动触发 `Build and Deploy WASM` workflow
- **版本号**：根据输入计算（见下文）
- **用途**：对外发布
- **特点**：
  - 上传到 CDN（更新 `latest.json` 和版本目录）
  - 可选上传 OSS
  - 创建 Git Tag

## 发布操作

### 手动发布流程

1. 打开 GitHub Actions 页面
2. 选择 `Build and Deploy WASM` workflow
3. 点击 `Run workflow`
4. 填写参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `upload_oss` | 是否上传 WASM 到 OSS | false |
| `version` | 版本号（见下表） | 空 |

### 版本号填写规则

假设当前最新 tag 为 `v1.2.3`：

| 输入 | 结果 | 说明 |
|------|------|------|
| （留空） | 1.2.4 | patch +1，常规发布 |
| `1.3` | 1.3.0 | 新 minor 版本，从 patch 0 开始 |
| `1.3`（已有 v1.3.2） | 1.3.3 | 该 minor 分支的 patch +1 |
| `1.3.5` | 1.3.5 | 精确指定（tag 已存在则失败） |
| `2.0` | 2.0.0 | 新 major 版本 |

### 标记项目标签

经过充分测试的版本可标记为 stable 或其他标签：

1. 运行 `Mark Project Tag` workflow
2. 填写参数：
   - `project_id`: 项目ID（如 `engine`, `engine-res`）
   - `tag`: 标签名（如 `stable`, `beta`, `rc1`）
   - `version`: 源版本号
3. 该版本的 `version.json` 会被复制为 `{tag}.json`
4. 更新到 CDN，供需要该标签版本的环境使用

## 故障处理

### 发布失败

1. 查看 workflow 日志定位问题
2. 修复后重新触发
3. 如版本号已被占用，使用下一个版本号

### 需要回滚

将 stable 指向旧版本：
1. 运行 `Mark Engine Stable`
2. 输入要回滚到的版本号

### 删除错误的 Tag

1. 打开 GitHub 仓库页面
2. 点击 **Releases** → **Tags**
3. 找到要删除的 tag，点击进入
4. 点击右上角 **Delete** 按钮

> CDN 上的文件不会自动删除，会被后续版本覆盖。

### 紧急修复（Hotfix）

**修复 latest 版本：**
1. 修复代码并合并到 main
2. 手动触发发布，版本号留空
3. 系统自动发布 patch +1 版本，更新 `latest.json`
4. 如需上线，运行 `Mark Project Tag` 将新版本标记为 stable

**修复旧版本**（如 latest=1.1.2，需修复 1.0.x）：

方式一：先修 main，再遴选到目标分支
1. 在 main 上修复代码并合并
2. 从目标 tag（如 `v1.0.40`）切出分支 `release-1.0`
3. Cherry-pick 修复 commit 到 `release-1.0`
4. 在 `release-1.0` 分支手动触发发布，版本号填 `1.0`
5. 系统发布 1.0.41，打 tag `v1.0.41`
6. 如有项目标签指向该版本（如 stable.json），运行 `Mark Project Tag` 更新指向

方式二：先修目标分支，再遴选回 main
1. 从目标 tag（如 `v1.0.40`）切出分支 `release-1.0`
2. 在 `release-1.0` 上修复代码
3. 手动触发发布，版本号填 `1.0`
4. 系统发布 1.0.41，打 tag `v1.0.41`
5. Cherry-pick 修复 commit 回 main
6. 如有项目标签指向该版本（如 stable.json），运行 `Mark Project Tag` 更新指向

## CDN 结构

```
base_url/src/
├── engine/
│   ├── preview.json      # 开发构建（push main 更新）
│   ├── latest.json       # 正式发布（手动触发更新）
│   ├── stable.json       # 稳定版本（Mark Project Tag 更新）
│   └── {version}/
│       ├── version.json
│       └── manifest-*.json
└── engine-res/
    └── （同上）
```

## 相关工具

| 工具 | 位置 | 用途 |
|------|------|------|
| version_utils.py | tools/ci/ | 版本号计算 |
| mark_project_tag.py | tools/project-tools/ | 标记项目标签 |

## 参考资料

- [语义化版本控制 2.0.0](https://semver.org/lang/zh-CN/)
- [Godot Release Policy](https://docs.godotengine.org/en/stable/about/release_policy.html)
