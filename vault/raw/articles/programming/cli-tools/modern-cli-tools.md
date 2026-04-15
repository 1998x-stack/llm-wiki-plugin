# 现代 CLI 工具全景指南：AI Agent 推荐配置

> AI Agent（Claude Code / Cursor / Codex CLI）在操作文件系统和代码库时，
> 使用这些现代工具比传统 Unix 工具更快、更精确、更安全。

---

## 🗺 一览表：传统 → 现代

| 传统工具 | 现代替代 | 实现语言 | 核心改进 |
|----------|----------|----------|----------|
| `rm` | `trash` | Go | 移到回收站，防误删 |
| `grep` | `rg` (ripgrep) | Rust | 10-100x 更快，Git 感知 |
| `find` | `fd` | Rust | 更简洁语法，并行搜索 |
| `cat` | `bat` | Rust | 语法高亮，Git diff，分页 |
| `ls` | `eza` | Rust | Git 状态，图标，树视图 |
| `sed` | `sd` | Rust | 正则语法更友好 |
| `du` | `dust` | Rust | 可视化磁盘用量树 |
| `df` | `duf` | Go | 彩色分组磁盘信息 |
| `make` | `just` | Rust | 现代任务运行器 |

**额外必备**：`jq` · `yq` · `fzf` · `glow` · `tldr` · `watchexec` · `difft` · `tokei` · `hyperfine`

---

## 🔍 核心替代工具详解

### 1. `rm` → `trash` 🛡️

**防误删神器**，`rm` 删除无法恢复，`trash` 移到系统回收站。

```bash
# 安装
brew install trash                    # macOS
npm install -g trash-cli              # 跨平台

# 用法
trash file.txt                        # 移到回收站（可恢复）
trash-restore                         # 恢复误删文件
trash-empty                           # 清空回收站
trash-list                            # 查看回收站内容

# 对比
rm -rf ./dist       # ❌ 永久删除，一失手无回头
trash ./dist        # ✅ 安全，可从回收站找回
```

**AI Agent 视角**：Agent 操作文件时配置 `trash` 替代 `rm`，避免误删源码造成不可逆损失。

---

### 2. `grep` → `rg` (ripgrep) 🔍

**速度冠军**，Rust 实现，默认 `.gitignore` 感知，支持 Unicode。

```bash
# 安装
brew install ripgrep
apt install ripgrep

# 基础用法
rg "TODO"                             # 递归搜索当前目录
rg "class.*Model" src/               # 正则搜索
rg -l "import torch"                 # 只列出匹配文件名
rg -n "def train" --type py          # 带行号，限定 Python 文件

# 高级用法
rg "error" -A 3 -B 2                 # 显示上下文（after/before）
rg "TODO|FIXME|HACK" --stats         # 多模式 + 统计
rg "deprecated" -g "!test_*"         # 排除测试文件
rg "config" --json | jq '.'          # JSON 输出管道处理

# 性能对比（大型 monorepo）
# grep -r "error" .  →  需要 45s（包含 node_modules）
# rg "error"         →  需要 0.4s（自动跳过 .gitignore 目录）
```

**速度提升**：真实场景 10-100x，搜索 node_modules 这类大目录时差距尤为显著。

---

### 3. `find` → `fd` 🔎

**更人性化的查找工具**，语法简洁，自动 `.gitignore` 感知，并行执行。

```bash
# 安装
brew install fd
apt install fd-find         # Ubuntu 下二进制名为 fdfind，建议设 alias

# 基础对比
find . -name "*.py" -type f              # 传统
fd -e py                                 # 现代（更简洁）

find . -name "*.ts" -not -path "*/node_modules/*"  # 传统排除
fd -e ts                                 # 自动跳过！

# 实用用法
fd "config"                              # 模糊文件名搜索
fd -e yaml -x cat {}                     # 对每个 yaml 文件执行 cat
fd --changed-within 1d                   # 最近 1 天修改的文件
fd -H "\.env"                            # 包含隐藏文件搜索
fd "" --type d                           # 只列出目录
fd -e py | xargs rg "TODO"              # 组合 ripgrep
```

**AI Agent 视角**：Agent 在 `codebase_search` 操作中用 `fd` 快速定位目标文件，比 `find` 语法错误率更低。

---

### 4. `cat` → `bat` 🦇

**带超能力的 cat**，语法高亮 + Git diff + 自动分页 + 行号。

```bash
# 安装
brew install bat
apt install bat                  # Ubuntu 下二进制为 batcat，设 alias bat='batcat'

# 基础用法
bat file.py                      # 语法高亮 + 行号
bat --paging=never file.py       # 不分页（适合管道）
bat -n file.py                   # 仅显示行号，不高亮
bat --diff file.py               # 显示 Git diff 标注

# 集成用法
rg "error" --json | bat --language json   # 彩色 JSON 输出
git show HEAD:src/main.py | bat -l py     # 查看历史版本带高亮
fd -e py | xargs bat              # 批量高亮显示

# 作为 PAGER 使用
export MANPAGER="sh -c 'col -bx | bat -l man -p'"   # man 带高亮
export BAT_THEME="Monokai Extended"                  # 主题配置
```

---

### 5. `ls` → `eza` 📁

**现代 ls**，exa 的维护分支，Git 感知 + 图标 + 树视图。

```bash
# 安装
brew install eza
cargo install eza

# 常用别名配置
alias ls='eza'
alias ll='eza -la --git --icons'
alias lt='eza --tree --level=2'
alias la='eza -a'

# 基础用法
eza                              # 彩色列表 + 图标
eza -la                          # 长格式，含隐藏文件
eza -la --git                    # + Git 状态标注（N新/M修改/I忽略）
eza --tree                       # 树形视图（替代 tree 命令）
eza --tree --level=3 --git-ignore  # 3层深度，跳过 .gitignore 文件

# 排序 & 过滤
eza -la --sort=modified          # 按修改时间排序
eza -la --sort=size --reverse    # 按大小倒序
eza -la --group-directories-first  # 目录优先

# Git 状态符号含义
# N = 新文件（untracked）
# M = 已修改
# D = 已删除
# A = 已暂存
# I = 被 .gitignore 忽略
```

---

### 6. `sed` → `sd` ✂️

**更友好的流编辑器**，正则语法接近 Python/JS，无需记忆 sed 的奇怪转义。

```bash
# 安装
brew install sd
cargo install sd

# 对比示例
# 替换字符串
sed -i 's/old/new/g' file.txt        # sed（转义噩梦）
sd 'old' 'new' file.txt              # sd（干净直接）

# 多文件替换
sed -i '' 's/foo/bar/g' *.py         # sed macOS 兼容写法
sd 'foo' 'bar' *.py                  # sd（跨平台一致）

# 正则捕获组
echo "2024-01-15" | sed 's/\([0-9]*\)-\([0-9]*\)-\([0-9]*\)/\3\/\2\/\1/'
echo "2024-01-15" | sd '(\d{4})-(\d{2})-(\d{2})' '$3/$2/$1'   # sd 更直观

# 批量重命名（配合 fd）
fd -e py | xargs sd 'from app import' 'from myapp import'
```

---

### 7. `du` → `dust` 💾

**可视化磁盘使用分析**，自动排序，树形展示。

```bash
# 安装
brew install dust
cargo install du-dust

# 用法
dust                             # 当前目录可视化
dust ~/                          # 主目录分析
dust -d 2                        # 深度限制为 2
dust -n 20                       # 显示前 20 个
dust -r                          # 反转（大→小）
dust -X node_modules             # 排除目录

# 对比
du -sh */ | sort -rh | head -20  # 传统（输出难读）
dust -d 1                        # 现代（带进度条和可视化）
```

---

### 8. `df` → `duf` 💿

**彩色分组磁盘信息**，区分设备类型，更易读。

```bash
# 安装
brew install duf
apt install duf

# 用法
duf                              # 全部挂载点分类展示
duf /home /var                   # 指定路径
duf --only local                 # 只显示本地磁盘
duf --json                       # JSON 输出（管道友好）

# 显示分组：
# [local] 本地磁盘
# [network] NFS/SMB 等
# [special] tmpfs/proc 等
```

---

### 9. `make` → `just` 🔨

**现代任务运行器**，不依赖文件更新时间，支持参数，语法简洁。

```bash
# 安装
brew install just
cargo install just

# Justfile 示例（类似 Makefile 但更友好）
```

```makefile
# Justfile
default:
    just --list

# 启动开发环境
dev:
    uv run uvicorn app.main:app --reload

# 运行测试
test *args:
    uv run pytest {{args}} -v

# 代码质量
lint:
    uv run ruff check .
    uv run ruff format --check .

# 构建 Docker
build tag="latest":
    docker build -t myapp:{{tag}} .

# 数据库迁移
migrate:
    uv run alembic upgrade head

# 清理
clean:
    fd -e pyc -x rm {}
    rm -rf .pytest_cache __pycache__
```

```bash
just dev           # 启动开发
just test -k auth  # 运行带参数的测试
just build v1.2.3  # 传参构建
just --list        # 列出所有任务
```

---

## 🛠 额外必备工具

### `jq` — JSON 瑞士军刀

```bash
# 安装
brew install jq

# 用法
curl api.example.com/users | jq '.'                    # 格式化输出
cat data.json | jq '.users[] | select(.age > 30)'      # 过滤
cat data.json | jq '.[] | {name, email}'               # 投影
cat data.json | jq 'map(.price) | add'                 # 聚合计算
rg "error" --json | jq '.data.text'                    # 处理 ripgrep JSON
```

### `yq` — YAML/TOML/XML 处理

```bash
brew install yq

yq '.services.web.image' docker-compose.yaml           # 读取
yq '.version = "2.0"' config.yaml                     # 修改
yq -i '.replicas = 3' deployment.yaml                  # 原地修改
yq eval-all 'select(fileIndex == 0) * fileIndex == 1)' a.yaml b.yaml  # 合并
```

### `fzf` — 交互式模糊搜索

```bash
brew install fzf

# Shell 集成
$(fzf)                          # 模糊选择文件
cd $(fd -t d | fzf)             # 模糊跳转目录
kill -9 $(ps aux | fzf | awk '{print $2}')  # 模糊 kill 进程

# Git 集成
git log --oneline | fzf --preview 'git show {1}'  # 模糊选 commit
git branch | fzf | xargs git checkout              # 模糊切分支

# 历史命令
# Ctrl+R → fzf 增强历史搜索（安装后自动绑定）
```

### `glow` — 终端 Markdown 渲染

```bash
brew install glow

glow README.md                  # 渲染 Markdown
glow -p CLAUDE.md              # 分页渲染
echo "# Hello" | glow -         # 管道输入
glow                            # 交互式浏览当前目录 .md 文件
```

**AI Agent 视角**：查看 SKILL.md、CLAUDE.md 等指令文件时，`glow` 让内容更清晰可读。

### `tldr` — 简洁命令示例

```bash
npm install -g tldr
# 或
brew install tldr

tldr tar                        # 替代 man tar，只看常用示例
tldr git                        # Git 速查
tldr rg                         # ripgrep 速查
tldr --update                   # 更新页面
```

### `watchexec` — 文件变更触发器

```bash
brew install watchexec
cargo install watchexec-cli

watchexec -e py "uv run pytest"              # py 文件变更自动测试
watchexec -e ts,tsx "bun run build"          # TS 变更自动构建
watchexec --restart "uv run python server.py" # 重启进程
watchexec -e md "glow README.md"             # md 变更预览
```

### `difft` (difftastic) — 语义级 diff

```bash
brew install difftastic

# 结构化对比（理解代码语法，而非按行 diff）
difft old.py new.py             # 语义 diff（理解函数/块结构）

# 替换 git diff
git config --global diff.external difft
# 或临时使用
GIT_EXTERNAL_DIFF=difft git diff HEAD~1
```

**对比 `diff`**：传统 diff 按行对比，函数移动会显示大量噪音；difft 理解语法结构，只显示真实改变。

### `tokei` — 代码行数统计

```bash
brew install tokei
cargo install tokei

tokei                           # 当前目录代码统计
tokei src/                      # 指定目录
tokei --exclude "*.json"        # 排除文件类型
tokei --output json             # JSON 输出
tokei -s lines                  # 按行数排序
```

输出示例：
```
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 Python                 42         3821         3012          451          358
 Markdown               15          823          823            0            0
 TOML                    3           87           75           12            0
===============================================================================
```

### `hyperfine` — 命令性能基准测试

```bash
brew install hyperfine
cargo install hyperfine

# 基准测试
hyperfine 'grep -r "TODO" .' 'rg "TODO"'    # 对比 grep vs ripgrep
hyperfine --runs 20 'uv pip install ...'     # 20 次重复取平均
hyperfine --warmup 3 'fd -e py'              # 预热后测试
hyperfine --export-markdown bench.md         # 导出 Markdown 报告

# 输出示例
# Command 'rg "TODO"' ran 47.3x faster than 'grep -r "TODO" .'
```

---

## ⚡ 完整安装脚本

### macOS (Homebrew)

```bash
brew install \
  trash ripgrep fd bat eza sd dust duf just \
  jq yq fzf glow tldr difftastic tokei hyperfine \
  watchexec

npm install -g trash-cli tldr   # 额外 npm 工具

# Shell 配置（~/.zshrc 或 ~/.bashrc）
alias rm='echo "使用 trash 代替 rm！"; trash'
alias grep='rg'
alias find='fd'
alias cat='bat --paging=never'
alias ls='eza'
alias ll='eza -la --git --icons'
alias lt='eza --tree --level=2'
alias du='dust'
alias df='duf'
alias make='just'

# fzf 集成
eval "$(fzf --zsh)"

# zoxide（智能 cd）
brew install zoxide
eval "$(zoxide init zsh)"
alias cd='z'
```

### Ubuntu/Debian

```bash
# apt 可直接安装的
sudo apt install -y ripgrep fd-find bat jq fzf tldr duf

# cargo 安装（需先安装 Rust）
cargo install eza sd dust just watchexec-cli tokei hyperfine difftastic

# 设 Ubuntu 特有 alias
alias bat='batcat'
alias fd='fdfind'

# snap 安装
sudo snap install yq
```

### AI Agent 环境配置（自动化脚本）

```bash
#!/bin/bash
# agent-toolchain-setup.sh — Claude Code Agent 推荐工具链

set -e

echo "🚀 安装 AI Agent 推荐工具链..."

# 核心搜索工具
cargo install ripgrep fd-find

# 文件查看
cargo install bat

# 现代 ls
cargo install eza

# 磁盘分析
cargo install du-dust duf

# 任务运行
cargo install just

# 基准测试
cargo install hyperfine tokei

# 代码 diff
cargo install difftastic

# 监控
cargo install watchexec-cli

echo "✅ 工具链安装完成！"
echo "📝 请将 aliases 添加到你的 shell 配置文件"
```

---

## 🤖 AI Agent 使用场景映射

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 代码库搜索 | `rg` | 自动跳过 `.gitignore`，速度快 |
| 文件定位 | `fd` | 简洁语法，并行，Git 感知 |
| 查看文件内容 | `bat` | 带行号，Agent 引用更精确 |
| 理解目录结构 | `eza --tree` | 清晰层次，一目了然 |
| 删除临时文件 | `trash` | 防止误删关键文件 |
| 批量替换 | `sd` | 正则语法清晰，出错率低 |
| JSON 处理 | `jq` | Pipeline 标配 |
| YAML 配置修改 | `yq` | 原地修改，保留注释 |
| 性能对比验证 | `hyperfine` | 量化优化效果 |
| 代码量估算 | `tokei` | 快速了解项目规模 |
| 任务自动化 | `just` | 统一入口，替代散乱 shell 脚本 |
| 监控文件变化 | `watchexec` | TDD 开发循环必备 |

---

## 📚 参考资源

- [modern-unix 精选列表 (GitHub)](https://github.com/ibraheemdev/modern-unix)
- [Rust 替代 Linux 核心工具 (WebProNews)](https://www.webpronews.com/rust-is-quietly-replacing-the-core-of-linux-and-the-speed-gains-are-real/)
- [CLI++ KDAB 深度指南](https://www.kdab.com/cli-upgrade-your-command-line-with-a-new-generation-of-everyday-tools/)
- [32blog: Modern Rust CLI Tools](https://32blog.com/en/cli/cli-modern-rust-tools)
