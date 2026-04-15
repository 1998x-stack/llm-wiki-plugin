**代码领域的 Agentic Search 设计指南**

|  |
| --- |
| **适用场景**：代码仓库探索、Bug 修复、代码生成、重构、跨文件推理 **参考实现**：Claude Code、Cline、Cursor、Relace FAS |

**目录**

1. [为什么代码领域适合 Agentic Search](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#1-%E4%B8%BA%E4%BB%80%E4%B9%88%E4%BB%A3%E7%A0%81%E9%A2%86%E5%9F%9F%E9%80%82%E5%90%88-agentic-search)
2. [核心架构设计](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#2-%E6%A0%B8%E5%BF%83%E6%9E%B6%E6%9E%84%E8%AE%BE%E8%AE%A1)
3. [工具集设计（Tool Set）](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#3-%E5%B7%A5%E5%85%B7%E9%9B%86%E8%AE%BE%E8%AE%A1tool-set)
4. [搜索策略模式](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#4-%E6%90%9C%E7%B4%A2%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8F)
5. [Agent 循环设计](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#5-agent-%E5%BE%AA%E7%8E%AF%E8%AE%BE%E8%AE%A1)
6. [多 Agent 协作架构](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#6-%E5%A4%9A-agent-%E5%8D%8F%E4%BD%9C%E6%9E%B6%E6%9E%84)
7. [性能优化：并行搜索](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#7-%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96%E5%B9%B6%E8%A1%8C%E6%90%9C%E7%B4%A2)
8. [上下文管理策略](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#8-%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86%E7%AD%96%E7%95%A5)
9. [Guardrails 与防止失控](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#9-guardrails-%E4%B8%8E%E9%98%B2%E6%AD%A2%E5%A4%B1%E6%8E%A7)
10. [评估与监控](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#10-%E8%AF%84%E4%BC%B0%E4%B8%8E%E7%9B%91%E6%8E%A7)
11. [实现参考代码](https://claude.ai/chat/5543bc6f-09ef-472a-addd-855c1bb48a6d#11-%E5%AE%9E%E7%8E%B0%E5%8F%82%E8%80%83%E4%BB%A3%E7%A0%81)

1. **为什么代码领域适合 Agentic Search**

**代码的特殊性**

代码不同于普通文档，有以下核心特征：

|  |
| --- |
| Plain Text 代码的本质特征 │ ├─ 结构性强：AST层级、模块边界、调用关系 ├─ 逻辑连接：函数A调用B，B依赖C → 必须跟踪依赖链 ├─ 动态演化：代码每天变化，静态索引快速过期 ├─ 符号导航：import、class.method、变量引用 └─ 上下文敏感：同一函数在不同调用栈中意义不同 |

**RAG 在代码上的核心问题**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**Claude Code 团队的验证**

|  |
| --- |
| Boris Cherny（Claude Code 负责人）："早期版本我们用了 RAG + 本地向量数据库，但很快发现 Agentic Search 通常效果更好——更简单，没有安全、隐私、数据过期和可靠性问题。" |

**核心洞察**：代码搜索的最优解不是"找最相似的片段"，而是"像资深工程师一样探索"——查看目录结构、追踪 import、读整个文件建立心智模型。

2. **核心架构设计**

**整体架构**

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────────────────┐ │ Agentic Search System │ │ │ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │ │ │ 用户任务 │───►│ Task Planner│───►│ Search Agent │ │ │ └─────────────┘ └─────────────┘ └────────┬────────┘ │ │ │ │ │ ┌──────────────────────────────────────┘ │ │ │ │ │ ▼ │ │ ┌───────────────────────────────────────────────────────┐ │ │ │ Tool Dispatcher │ │ │ │ │ │ │ │ [file\_read] [list\_dir] [grep] [git\_log] [lsp\_hover] │ │ │ │ [vector\_search] [symbol\_search] [exec\_code] │ │ │ └───────────────────────────────────────────────────────┘ │ │ │ │ │ ▼ │ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │ │ │ Observation│───►│ Reflection │───►│ Context Merger │ │ │ │ Engine │ │ Engine │ │ │ │ │ └─────────────┘ └─────────────┘ └────────┬────────┘ │ │ │ │ │ ▼ │ │ ┌─────────────┐ │ │ │ Code Answer │ │ │ │ Generator │ │ │ └─────────────┘ │ └─────────────────────────────────────────────────────────────┘ |

**分层设计**

|  |
| --- |
| Plain Text Layer 0: 用户任务层  └─ 自然语言任务输入（"修复这个 bug"/"实现这个功能"）  Layer 1: 规划层（Planning Layer）  └─ 任务分解 → 搜索策略 → 预期终止条件  Layer 2: 执行层（Execution Layer）  ├─ Tool Registry（工具注册中心）  ├─ Parallel Executor（并行执行器）  └─ Result Cache（搜索结果缓存）  Layer 3: 推理层（Reasoning Layer）  ├─ Observation Evaluator（评估当前信息是否足够）  ├─ Gap Identifier（识别信息缺口）  └─ Query Reformulator（重构搜索查询）  Layer 4: 生成层（Generation Layer）  └─ 基于收集的上下文生成最终答案/代码 |

3. **工具集设计（Tool Set）**

**必备工具（核心 3 件套）**

|  |
| --- |
| Python # 工具1：目录列表 @tool def list\_directory(path: str, depth: int = 2) -> str:  """列出目录结构，快速建立仓库心智模型"""  # 输出：文件树结构，过滤 .git / node\_modules  pass  # 工具2：文件读取 @tool def read\_file(path: str, start\_line: int = None, end\_line: int = None) -> str:  """读取文件内容，支持行范围"""  # 支持全文读取 or 指定行范围（避免 token 浪费）  pass  # 工具3：关键词搜索 @tool def grep\_search(pattern: str, path: str = ".", flags: str = "-rn") -> str:  """正则/关键词全仓库搜索"""  # 底层：ripgrep（速度极快）  pass |

**扩展工具（高级能力）**

|  |
| --- |
| Python # 工具4：符号导航（LSP 集成） @tool def find\_symbol(symbol\_name: str, symbol\_type: str = "function") -> list[dict]:  """查找函数/类/变量的定义位置"""  # 输出：[{file, line, column, signature}]  pass  # 工具5：引用查找 @tool def find\_references(symbol\_name: str, file\_path: str) -> list[dict]:  """查找某个符号的所有引用位置"""  pass  # 工具6：Git 历史 @tool def git\_log(path: str = None, n: int = 10) -> str:  """查看提交历史，理解代码演化"""  pass  # 工具7：代码执行 @tool def execute\_code(code: str, language: str = "python") -> dict:  """在沙箱中执行代码，验证假设"""  # 返回：{stdout, stderr, exit\_code}  pass  # 工具8：语义搜索（向量 RAG 作为补充） @tool def semantic\_search(query: str, top\_k: int = 5) -> list[dict]:  """语义相似度搜索，适合概念性查询"""  # 底层：向量数据库  pass  # 工具9：依赖图查询 @tool def get\_dependencies(file\_path: str) -> dict:  """获取文件的导入依赖关系"""  # 输出：{imports: [], imported\_by: []}  pass |

**工具优先级与适用场景**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

4. **搜索策略模式**

**策略1：自顶向下探索（Top-down Exploration）**

适用于：**陌生仓库的初步探索**

|  |
| --- |
| Plain Text Step 1: list\_directory(".") # 建立整体结构认知 Step 2: read\_file("README.md") # 理解项目意图 Step 3: list\_directory("src/", depth=3) # 深入源码目录 Step 4: read\_file("src/main.py") # 读取入口文件 Step 5: grep\_search("class.\*Service") # 找核心业务类 |

**策略2：符号追踪（Symbol Tracing）**

适用于：**追踪函数调用链/依赖关系**

|  |
| --- |
| Plain Text Step 1: grep\_search("def process\_order") # 找函数定义 Step 2: read\_file(found\_path, line±20) # 读实现 Step 3: grep\_search("process\_order") # 找所有调用者 Step 4: find\_references("process\_order", ...) # LSP 精确引用 Step 5: 对每个调用者递归追踪 |

**策略3：错误定位（Error Localization）**

适用于：**Bug 修复**

|  |
| --- |
| Plain Text Step 1: grep\_search("error\_message\_keyword") # 找错误出处 Step 2: read\_file(error\_file, error\_line±30) # 读出错上下文 Step 3: find\_references(failing\_function) # 找调用链 Step 4: git\_log(error\_file) # 看最近改动 Step 5: execute\_code(reproduction\_script) # 复现验证 |

**策略4：概念搜索（Concept Search）**

适用于：**用自然语言描述的概念，不知道具体符号名**

|  |
| --- |
| Plain Text Step 1: semantic\_search("user authentication logic") # 语义搜索 Step 2: grep\_search("auth|login|token") # 关键词扩展 Step 3: list\_directory("src/auth/") # 目录锁定 Step 4: read\_file(candidate\_files) # 深读候选 |

**策略5：影响范围分析（Impact Analysis）**

适用于：**重构前评估改动影响**

|  |
| --- |
| Plain Text Step 1: find\_symbol("TargetClass") Step 2: find\_references("TargetClass", all\_files=True) Step 3: 对每个引用文件执行 read\_file 理解使用方式 Step 4: get\_dependencies 分析完整依赖图 Step 5: 生成影响范围报告 |

5. **Agent 循环设计**

**ReAct 循环（推荐基础模式）**

|  |
| --- |
| Python def agentic\_search\_loop(task: str, tools: list, max\_turns: int = 20):  history = []  context = []    for turn in range(max\_turns):  # Thought: LLM 推理当前需要什么  thought = llm.think(task, history, context)    # 判断是否完成  if thought.is\_complete:  return llm.generate\_answer(task, context)    # Action: 选择并执行工具  tool\_call = thought.next\_action  result = tools[tool\_call.name](\*\*tool\_call.args)    # Observation: 记录结果  history.append({  "thought": thought.reasoning,  "action": tool\_call,  "observation": result  })    # Context Update: 将关键信息加入上下文  if result.is\_relevant:  context.append(result)    # Reflection: 评估信息完整性  if is\_sufficient(context, task):  break    return llm.generate\_answer(task, context) |

**信息充分性评估（Reflection）**

|  |
| --- |
| Python REFLECTION\_PROMPT = """ 当前任务: {task} 已收集的上下文: {context}  评估: 1. 对于完成任务，还缺少什么关键信息？ 2. 目前的信息是否足以生成准确答案？ 3. 如果需要更多信息，下一步应该搜索什么？  输出格式: - is\_sufficient: true/false - missing\_info: [...] - next\_search: {...} """ |

6. **多 Agent 协作架构**

**专职搜索子 Agent 模式（Relace FAS 模式）**

|  |
| --- |
| Plain Text 主 Agent（Orchestrator）  │  ├─► 搜索子 Agent（Search Specialist）  │ │── 专注于 grep / file\_read / list\_dir  │ │── 使用 RL 训练的专用小模型  │ └── 返回：最小相关文件集合  │  ├─► 代码理解子 Agent（Code Analyst）  │ │── 分析调用关系、依赖图  │ └── 返回：结构化代码知识  │  └─► 生成子 Agent（Code Generator）  │── 基于搜索结果生成代码  └── 返回：patch / 完整实现 |

**并行搜索（显著降低延迟）**

|  |
| --- |
| Python # 并行执行多个不相关的搜索 async def parallel\_search(queries: list[SearchQuery]) -> list[Result]:  tasks = [execute\_search(q) for q in queries]  results = await asyncio.gather(\*tasks)  return results  # 示例：同时搜索多个相关文件 queries = [  SearchQuery(tool="grep", args={"pattern": "OrderService"}),  SearchQuery(tool="grep", args={"pattern": "PaymentService"}),  SearchQuery(tool="list\_dir", args={"path": "src/services/"}), ] results = await parallel\_search(queries) |

**Relace 团队数据**：并行工具调用将端到端延迟降低 **4x**（20轮→5轮，10轮→4轮）

7. **性能优化：并行搜索**

**并行机会识别**

|  |
| --- |
| Plain Text 串行（慢）：  grep A → 等待 → read file A → 等待 → grep B → 等待 → read file B  并行（快）：  ┌─ grep A ─────────────┐  ├─ grep B ─────────────┤ → 聚合结果 → read (A+B) 同时  └─ list\_dir src/ ──────┘ |

**任务图（DAG）调度**

|  |
| --- |
| Python # 构建任务依赖图 task\_graph = {  "init": [list\_directory("."), read\_file("README.md")],  "explore": [grep\_search("UserService"), grep\_search("OrderService")], # 并行  "deep\_read": lambda results: [read\_file(f) for f in results], # 依赖 explore  "analyze": synthesize\_context # 依赖 deep\_read } |

**Token 控制策略**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

8. **上下文管理策略**

**上下文窗口分配**

|  |
| --- |
| Plain Text ┌─────────────────────────────────────────────────┐ │ LLM Context Window │ │ │ │ [System Prompt] ~2K tokens │ │ [Task Description] ~1K tokens │ │ [Search History] ~4K tokens （压缩历史） │ │ [Retrieved Code] ~30K tokens （核心内容） │ │ [Current Reasoning] ~5K tokens │ │ [Output Buffer] ~8K tokens │ └─────────────────────────────────────────────────┘ |

**上下文压缩策略**

|  |
| --- |
| Python class ContextManager:  def compress\_history(self, history: list) -> str:  """将搜索历史压缩为摘要，保留关键发现"""  return llm.summarize(  f"将以下搜索过程压缩为要点：\n{history}",  max\_tokens=1000  )    def rank\_context(self, context\_pieces: list, task: str) -> list:  """按相关性排序，优先保留最相关的代码"""  scored = [(piece, relevance\_score(piece, task)) for piece in context\_pieces]  return sorted(scored, key=lambda x: x[1], reverse=True)    def evict\_least\_relevant(self, context: list, budget: int) -> list:  """当超出 token 预算时，淘汰最不相关的上下文"""  ranked = self.rank\_context(context)  return ranked[:budget] |

9. **Guardrails 与防止失控**

**常见失控场景**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**Guardrails 实现**

|  |
| --- |
| Python class AgentGuardrails:  def \_\_init\_\_(self):  self.max\_turns = 20  self.max\_tokens = 100\_000  self.max\_tool\_calls = 50  self.seen\_queries = set()    def check\_duplicate\_query(self, query: str) -> bool:  """防止重复搜索"""  if query in self.seen\_queries:  return False # 阻止重复  self.seen\_queries.add(query)  return True    def check\_depth\_limit(self, current\_depth: int, max\_depth: int = 5) -> bool:  """防止过深追踪"""  return current\_depth <= max\_depth    def check\_relevance(self, result: str, original\_task: str) -> float:  """评估结果与原始任务的相关性"""  return llm.score\_relevance(result, original\_task) |

10. **评估与监控**

**核心评估指标**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**关键评测基准**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

11. **实现参考代码**

**最小可行 Agentic Search 实现**

|  |
| --- |
| Python from langgraph.graph import StateGraph, END from langchain\_core.tools import tool import subprocess  # === 工具定义 === @tool def list\_dir(path: str) -> str:  """列出目录结构"""  result = subprocess.run(  ["find", path, "-maxdepth", "3", "-not", "-path", "\*/.\*"],  capture\_output=True, text=True  )  return result.stdout[:3000] # token 控制  @tool def read\_file(path: str, start\_line: int = 1, end\_line: int = 100) -> str:  """读取文件指定行范围"""  with open(path) as f:  lines = f.readlines()  return "".join(lines[start\_line-1:end\_line])  @tool def grep\_code(pattern: str, path: str = ".") -> str:  """全仓库关键词搜索"""  result = subprocess.run(  ["rg", "--line-number", "--max-count", "20", pattern, path],  capture\_output=True, text=True  )  return result.stdout[:3000]  # === Agent State === class SearchState(TypedDict):  task: str  history: list  context: list  turn: int  done: bool  # === LangGraph 构建 === tools = [list\_dir, read\_file, grep\_code] agent = create\_react\_agent(llm, tools)  workflow = StateGraph(SearchState) workflow.add\_node("search", agent) workflow.add\_node("reflect", reflection\_node) workflow.add\_conditional\_edges(  "reflect",  lambda state: END if state["done"] else "search" ) workflow.set\_entry\_point("search") app = workflow.compile()  # === 执行 === result = app.invoke({  "task": "找到处理用户认证的核心逻辑并解释其工作原理",  "history": [], "context": [], "turn": 0, "done": False }) |

**总结**

**Agentic Search 在代码领域的设计要点**

|  |
| --- |
| Plain Text 核心设计原则 ├─ 1. 工具第一：grep + file\_read + list\_dir 是最小工具集 ├─ 2. 并行执行：无依赖的搜索任务全部并行化 ├─ 3. Token 控制：行范围读取、摘要压缩、优先级淘汰 ├─ 4. 反思机制：每轮评估信息是否充分 ├─ 5. Guardrails：防止循环、深度限制、token 上限 └─ 6. 语义搜索作为补充：不是主力，而是概念搜索的后备 |