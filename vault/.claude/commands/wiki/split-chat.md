# wiki:split-chat

将 ChatGPT 导出的 JSON 文件拆分为每轮问答一个 markdown 文件。

## 输入

$ARGUMENTS — JSON 文件路径（相对于 raw/ChatGPT-Chat/），或 "all" 处理该目录下所有 .json 文件。

## 流程

1. **定位文件**
   - 如果 $ARGUMENTS 是 "all"，扫描 `raw/ChatGPT-Chat/*.json`
   - 否则，读取 `raw/ChatGPT-Chat/$ARGUMENTS`
   - 如果文件不存在 → 报告错误并停止

2. **执行拆分**
   - 对每个 JSON 文件运行：
     ```
     Bash: bash scripts/wiki.sh split_chat_json <json_file_path>
     ```
   - 脚本会在 JSON 文件同级目录下创建同名文件夹（去掉 .json），将每轮问答写入单独的 markdown 文件
   - 每个 markdown 包含：标题、来源、时间、Question 和 Answer 两个部分
   - 拆分成功后自动删除源 JSON 文件

3. **报告结果**
   - 列出处理了哪些 JSON 文件
   - 每个文件生成了多少个 markdown
   - 输出目录路径

## 输出格式

每个生成的 markdown 文件结构：

```markdown
# <问题标题>

> Source: <对话标题>
> Time: <时间戳>

## Question

<问题内容>

## Answer

<回答内容>
```

## 示例

```
/wiki:split-chat ChatGPT-Self-Attention机制解析.json
/wiki:split-chat all
```
