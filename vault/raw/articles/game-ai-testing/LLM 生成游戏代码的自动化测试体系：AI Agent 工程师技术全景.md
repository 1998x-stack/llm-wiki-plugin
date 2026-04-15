**LLM 生成游戏代码的自动化测试体系：AI Agent 工程师技术全景**

|  |
| --- |
| **角色**：游戏公司 AI Agent 工程师 **核心命题**：LLM 生成的用户游戏代码（逻辑、角色、系统脚本等）在注入现有生产项目前，如何通过自动化测试体系保障其可靠性？ **参考前沿**：LLMLOOP (ICSME 2025)、SMART (2025)、TITAN (2025)、SWE-Agent、ProxyWar (ICSE 2026)、GameUnitLLM (2024) |

**目录**

1. [为什么游戏代码测试是一个独特难题](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E4%B8%80%E4%B8%BA%E4%BB%80%E4%B9%88%E6%B8%B8%E6%88%8F%E4%BB%A3%E7%A0%81%E6%B5%8B%E8%AF%95%E6%98%AF%E4%B8%80%E4%B8%AA%E7%8B%AC%E7%89%B9%E9%9A%BE%E9%A2%98)
2. [LLM 生成代码的缺陷分类学](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E4%BA%8Cllm-%E7%94%9F%E6%88%90%E4%BB%A3%E7%A0%81%E7%9A%84%E7%BC%BA%E9%99%B7%E5%88%86%E7%B1%BB%E5%AD%A6)
3. [测试体系总体架构](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E4%B8%89%E6%B5%8B%E8%AF%95%E4%BD%93%E7%B3%BB%E6%80%BB%E4%BD%93%E6%9E%B6%E6%9E%84)
4. [第一层：静态分析与合法性验证](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%9B%9B%E7%AC%AC%E4%B8%80%E5%B1%82%E9%9D%99%E6%80%81%E5%88%86%E6%9E%90%E4%B8%8E%E5%90%88%E6%B3%95%E6%80%A7%E9%AA%8C%E8%AF%81)
5. [第二层：编译与构建验证](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E4%BA%94%E7%AC%AC%E4%BA%8C%E5%B1%82%E7%BC%96%E8%AF%91%E4%B8%8E%E6%9E%84%E5%BB%BA%E9%AA%8C%E8%AF%81)
6. [第三层：单元测试与引擎沙箱测试](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%85%AD%E7%AC%AC%E4%B8%89%E5%B1%82%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95%E4%B8%8E%E5%BC%95%E6%93%8E%E6%B2%99%E7%AE%B1%E6%B5%8B%E8%AF%95)
7. [第四层：集成测试与系统行为验证](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E4%B8%83%E7%AC%AC%E5%9B%9B%E5%B1%82%E9%9B%86%E6%88%90%E6%B5%8B%E8%AF%95%E4%B8%8E%E7%B3%BB%E7%BB%9F%E8%A1%8C%E4%B8%BA%E9%AA%8C%E8%AF%81)
8. [第五层：运行时测试与游戏仿真](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%85%AB%E7%AC%AC%E4%BA%94%E5%B1%82%E8%BF%90%E8%A1%8C%E6%97%B6%E6%B5%8B%E8%AF%95%E4%B8%8E%E6%B8%B8%E6%88%8F%E4%BB%BF%E7%9C%9F)
9. [自修复 Agent 循环：LLMLOOP 范式](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E4%B9%9D%E8%87%AA%E4%BF%AE%E5%A4%8D-agent-%E5%BE%AA%E7%8E%AFllmloop-%E8%8C%83%E5%BC%8F)
10. [测试 Agent 的 Agentic 编排架构](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%8D%81%E6%B5%8B%E8%AF%95-agent-%E7%9A%84-agentic-%E7%BC%96%E6%8E%92%E6%9E%B6%E6%9E%84)
11. [CI/CD 管线集成](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%8D%81%E4%B8%80cicd-%E7%AE%A1%E7%BA%BF%E9%9B%86%E6%88%90)
12. [可观测性与诊断报告](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%8D%81%E4%BA%8C%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7%E4%B8%8E%E8%AF%8A%E6%96%AD%E6%8A%A5%E5%91%8A)
13. [关键工程决策与 KPI](https://claude.ai/chat/af4e6f18-548a-4bf3-af67-6acb87bdd24d#%E5%8D%81%E4%B8%89%E5%85%B3%E9%94%AE%E5%B7%A5%E7%A8%8B%E5%86%B3%E7%AD%96%E4%B8%8E-kpi)

**一、为什么游戏代码测试是一个独特难题**

**1.1 游戏代码 vs 普通软件代码的本质差异**

|  |
| --- |
| Plain Text 普通软件测试的假设：  ✓ 纯计算逻辑，确定性输入 → 确定性输出  ✓ 无状态（Stateless）API 可单独测试  ✓ 错误通常是显式异常（Exception）  ✓ 测试环境轻量，可快速 spin up  游戏代码测试面临的额外维度：  ✗ 物理引擎非确定性（浮点精度、帧率波动）  ✗ 状态机极度复杂（玩家状态 × NPC状态 × 关卡状态 的笛卡尔积）  ✗ 错误往往是"软锁"（Soft Lock）：代码运行但游戏不可玩  ✗ 引擎 API 与版本强耦合（UE5.3 与 UE5.4 的 API 可能不兼容）  ✗ 视觉/音效问题无法用断言（Assertion）捕获  ✗ 多人同步逻辑的并发 Bug 难以复现 |

**1.2 用户生产项目注入的特殊挑战**

LLM 生成的代码不是在空白项目中运行，而是**注入**到用户已有的生产项目中：

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**1.3 LLM 代码生成的特有失效模式（2024-2025 实证研究）**

在 ProxyWar 研究中，LLM 在游戏环境中生成代码时，必须处理多样化的对手行为、严格遵守环境接口，并在运行时约束下工作，这使得脆弱的或过度拟合的记忆实现更容易失败。

LLMLOOP 研究表明，迭代反馈循环显著提升了 LLM 生成代码的质量：pass@10 从基线的 76.22% 提升到 90.24%，证明了单轮生成的不可靠性。

**二、LLM 生成代码的缺陷分类学**

在设计测试体系之前，必须系统地理解 LLM 会犯哪些类型的错误。

**2.1 缺陷四象限模型**

|  |
| --- |
| Plain Text  ┌────────────────────────────────────────┐  │ 可检测性（Detection） │  │ 高（静态/编译期） 低（运行期） │  严 ┌─────────────┼────────────────────┬───────────────────┤  重 │ 高严重程度 │ A 象限 │ B 象限 │  程 │ │ • API 不存在 │ • 逻辑语义错误 │  度 │ │ • 类型不匹配 │ • 竞态条件 │  │ │ • 路径幻构 │ • 物理异常行为 │  │ │ → 优先用静态分析 │ → 需运行时测试 │  ├─────────────┼────────────────────┼───────────────────┤  │ 低严重程度 │ C 象限 │ D 象限 │  │ │ • 命名风格违规 │ • 性能轻微退化 │  │ │ • 注释缺失 │ • 边缘帧率抖动 │  │ │ → Lint 处理 │ → 基准测试检测 │  └─────────────┴────────────────────┴───────────────────┘ |

**2.2 游戏领域 LLM 缺陷类型详细分类**

|  |
| --- |
| Plain Text LLM 游戏代码缺陷分类（Game Code Defect Taxonomy） ├── 1. 幻构类（Hallucination Defects） │ ├── 1.1 API 幻构：调用了不存在的引擎方法 │ │ UE: GetCharacterMovementComponent().SetMaxSpeed() // 正确是 MaxWalkSpeed │ ├── 1.2 路径幻构：引用不存在的资产路径 │ │ "/Game/Boss/SK\_DragonBoss" // 实际路径是 "/Game/Characters/Boss/..." │ └── 1.3 参数幻构：错误的函数签名/参数顺序 │ ├── 2. 版本兼容类（Version Compatibility Defects） │ ├── 2.1 引擎 API 废弃：使用了目标引擎版本已废弃的 API │ ├── 2.2 插件依赖缺失：依赖了项目未安装的插件 │ └── 2.3 平台特定 API：PC 专属 API 在移动端编译失败 │ ├── 3. 集成冲突类（Integration Conflict Defects） │ ├── 3.1 命名冲突：与现有代码类名/函数名碰撞 │ ├── 3.2 循环依赖：引入了循环头文件包含 │ └── 3.3 全局状态污染：修改了项目级单例状态 │ ├── 4. 运行时逻辑类（Runtime Logic Defects） │ ├── 4.1 空指针访问：未判空的 Component 访问 │ ├── 4.2 状态机违规：跳过了必要的状态转换检查 │ ├── 4.3 软锁（Soft Lock）：游戏进入无法自行退出的循环状态 │ └── 4.4 语义错误：代码运行但行为与需求完全相反 │ └── 5. 性能类（Performance Defects）  ├── 5.1 Tick 滥用：高代价逻辑放在 per-frame Tick 中  ├── 5.2 GC 压力：频繁创建/销毁对象  └── 5.3 同步 IO：在主线程执行阻塞的文件/网络操作 |

**三、测试体系总体架构**

**3.1 五层测试金字塔（游戏 AI 生成代码专用）**

|  |
| --- |
| Plain Text  ▲  /|\  / | \  / | \  / L5 \ 运行时仿真测试  / 游戏 \ (TITAN/Agent Playtest)  /─────────\  / L4 \ 集成测试  / 系统行为 \ (引擎内 Functional Test)  /───────────────\  / L3 \ 单元 + 引擎沙箱测试  / 逻辑+引擎API测试 \ (UE Spec/Unity UTF)  /─────────────────────\  / L2 \ 编译 + 链接验证  / 增量构建 + 热重载 \ (UnrealBuildTool/MSBuild)  /─────────────────────────────\  / L1 \ 静态分析 + 合法性检查  / AST解析 + API验证 + 资产路径验证 \ (零引擎启动，毫秒级)  /─────────────────────────────────────\   快速（ms） ←────────────────────→ 慢速（min）  低成本 ←────────────────────→ 高成本  高频运行 ←────────────────────→ 低频运行 |

**3.2 整体系统数据流**

|  |
| --- |
| Plain Text 用户自然语言需求  │  ▼ ┌───────────────────┐ │ LLM 代码生成层 │ ← 上游系统（本文档测试体系的输入） │ (Qwen/GPT/Claude) │ └─────────┬─────────┘  │ 生成代码（C++/C#/Lua/GDScript）  ▼ ┌─────────────────────────────────────────────────┐ │ 自动化测试 Agent 系统（本文档核心） │ │ │ │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌────┐│ │ │ L1 │→ │ L2 │→ │ L3 │→ │ L4 │→ │ L5 ││ │ │静态 │ │编译 │ │单元 │ │集成 │ │仿真││ │ │分析 │ │验证 │ │测试 │ │测试 │ │测试││ │ └──────┘ └──────┘ └──────┘ └──────┘ └────┘│ │ ↓ ↓ ↓ ↓ ↓ │ │ ┌────────────────────────────────────────────┐ │ │ │ 自修复 Agent（LLMLOOP 模式） │ │ │ │ 失败 → 诊断 → 修复提示 → 重新生成 → 重测 │ │ │ └────────────────────────────────────────────┘ │ └─────────────────────────────────────────────────┘  │ 通过所有测试层  ▼ ┌───────────────────┐ │ 代码注入用户项目 │ ← 最终产出 │ + 测试报告归档 │ └───────────────────┘ |

**四、第一层：静态分析与合法性验证**

**定位**：零引擎启动，纯文本/AST 分析，毫秒级完成，拦截所有可以在运行前检测到的问题。

**4.1 引擎 API 白名单验证**

LLM 最常见的错误是调用不存在或已废弃的引擎 API。通过构建引擎 API 白名单数据库进行静态验证：

|  |
| --- |
| Python import ast import re from dataclasses import dataclass from typing import Optional  @dataclass class APIValidationResult:  is\_valid: bool  invalid\_calls: list[str]  deprecated\_calls: list[str]  suggestions: dict[str, str] # invalid -> suggested\_replacement  class EngineAPIValidator:  """  引擎 API 白名单验证器  支持 UE5 (C++/Blueprint)、Unity (C#)、Godot (GDScript)  """    def \_\_init\_\_(self, engine: str, version: str):  self.api\_db = self.\_load\_api\_database(engine, version)  self.deprecated\_db = self.\_load\_deprecated\_apis(engine, version)  self.engine = engine    def \_load\_api\_database(self, engine: str, version: str) -> dict:  """  从本地维护的 API 数据库加载（不依赖网络）  数据库来源：引擎头文件解析 + 官方文档爬取  """  # 数据库结构：  # { "UCharacterMovementComponent::MaxWalkSpeed":   # {"type": "property", "return": "float", "since": "4.0", "until": null} }  pass    def validate\_cpp\_code(self, code: str) -> APIValidationResult:  """  对 UE5 C++ 代码进行 API 合法性验证  使用 clang-python 绑定进行真正的 AST 解析  """  import clang.cindex as clang    index = clang.Index.create()  tu = index.parse(  'temp.cpp',   args=['-std=c++17', f'-I/UnrealEngine/{self.version}/Engine/Source/Runtime'],  unsaved\_files=[('temp.cpp', code)]  )    invalid\_calls = []  deprecated\_calls = []    for cursor in tu.cursor.walk\_preorder():  if cursor.kind == clang.CursorKind.CALL\_EXPR:  full\_name = self.\_get\_full\_qualified\_name(cursor)  if full\_name not in self.api\_db:  invalid\_calls.append(full\_name)  # 尝试模糊匹配，给出修复建议  elif self.api\_db[full\_name].get("deprecated"):  deprecated\_calls.append(full\_name)    suggestions = self.\_generate\_suggestions(invalid\_calls)    return APIValidationResult(  is\_valid=len(invalid\_calls) == 0,  invalid\_calls=invalid\_calls,  deprecated\_calls=deprecated\_calls,  suggestions=suggestions  )    def validate\_asset\_paths(self, code: str, project\_asset\_index: dict) -> list[str]:  """  验证代码中所有资产路径的有效性  利用前文资产检索系统的索引数据库  """  # 提取 UE5 资产路径模式  ue5\_path\_pattern = r'TEXT\("(/Game/[^"]+)"\)'  unity\_path\_pattern = r'Resources\.Load[<\w>]\*\("([^"]+)"\)'    paths = re.findall(ue5\_path\_pattern, code)  paths += re.findall(unity\_path\_pattern, code)    invalid\_paths = []  for path in paths:  if path not in project\_asset\_index:  # 尝试模糊匹配，找到最相似的路径  closest = self.\_fuzzy\_match\_path(path, project\_asset\_index)  invalid\_paths.append({  "path": path,  "suggestion": closest,  "confidence": self.\_path\_similarity(path, closest)  })    return invalid\_paths |

**4.2 项目上下文冲突检测**

|  |
| --- |
| Python class ProjectConflictDetector:  """  检测生成代码与用户现有项目的冲突  """    def \_\_init\_\_(self, project\_code\_graph: dict):  """  project\_code\_graph: 由 code\_graph 工具预先构建的项目代码图谱  包含：类名 → 文件路径、函数签名、头文件依赖等  """  self.code\_graph = project\_code\_graph    def detect\_naming\_conflicts(self, generated\_code: str) -> list[dict]:  """检测命名冲突"""  # 提取生成代码中的所有类名/函数名  class\_pattern = r'\bclass\s+(\w+)'  func\_pattern = r'\b(?:void|float|int|bool|FString)\s+(\w+)\s\*\('    generated\_classes = set(re.findall(class\_pattern, generated\_code))  generated\_funcs = set(re.findall(func\_pattern, generated\_code))    conflicts = []  for class\_name in generated\_classes:  if class\_name in self.code\_graph["classes"]:  conflicts.append({  "type": "class\_name\_conflict",  "name": class\_name,  "existing\_file": self.code\_graph["classes"][class\_name]["file"],  "severity": "error"  })    return conflicts    def detect\_circular\_dependencies(self, generated\_includes: list[str]) -> bool:  """检测是否引入循环头文件依赖"""  # 使用 DFS 检测依赖图中的环  existing\_deps = self.code\_graph["include\_graph"]  # ... 图环检测算法    def detect\_global\_state\_mutations(self, generated\_code: str) -> list[dict]:  """检测对全局/单例状态的修改（潜在的副作用）"""  singleton\_patterns = [  r'GEngine\s\*->',  r'GWorld\s\*->',  r'GetGameInstance\(\)\s\*->',  r'UGameplayStatics::',  ]  mutations = []  for pattern in singleton\_patterns:  matches = re.finditer(pattern, generated\_code)  for match in matches:  mutations.append({  "pattern": match.group(),  "line": generated\_code[:match.start()].count('\n') + 1,  "warning": "全局状态访问可能影响整个游戏状态"  })  return mutations |

**4.3 安全性静态扫描**

|  |
| --- |
| Python GAME\_CODE\_SECURITY\_RULES = {  # 防止 LLM 生成危险的文件操作  "dangerous\_io": [  r'std::filesystem::remove',  r'FPlatformFileManager.\*Delete',  r'File\.Delete', # Unity  ],  # 防止网络请求注入  "unexpected\_network": [  r'FHttpModule::Get\(\)',  r'UnityWebRequest',  r'WebClient',  ],  # 防止进程/Shell 调用  "process\_execution": [  r'FPlatformProcess::CreateProc',  r'System\.Diagnostics\.Process',  r'subprocess\.run',  ],  # 防止反射/动态代码执行  "reflection\_abuse": [  r'FindClass\s\*\(',  r'Type\.GetType\s\*\(',  r'Assembly\.Load',  ] } |

**五、第二层：编译与构建验证**

**定位**：引擎实际编译，捕获真正的类型错误和链接问题，分钟级完成。

**5.1 增量编译沙箱策略**

|  |
| --- |
| Python class IncrementalCompileSandbox:  """  核心设计原则：  1. 不污染原始项目：在 Clone 的项目副本中编译  2. 增量构建：只重新编译受影响的模块  3. 并行化：多个测试任务并行编译  """    def \_\_init\_\_(self, project\_path: str, engine\_path: str):  self.project\_path = project\_path  self.engine\_path = engine\_path    def compile\_generated\_code(  self,   generated\_files: list[str],  target\_module: str  ) -> CompileResult:    # 步骤 1：创建项目的轻量副本（使用 hardlink，节省磁盘空间）  sandbox\_path = self.\_create\_sandbox(self.project\_path)    # 步骤 2：将生成的文件注入沙箱  for file in generated\_files:  self.\_inject\_file(sandbox\_path, file)    # 步骤 3：UE5 增量编译  result = self.\_run\_ubt(  sandbox\_path,  target\_module=target\_module,  args=[  "-NoSharedPCH", # 加速首次编译  "-DisableUnity", # 禁用 Unity Build，精确错误定位  "-WarningsAsErrors", # 将警告视为错误（LLM 代码标准要求更严格）  ]  )    # 步骤 4：清理沙箱（保留日志供诊断）  self.\_cleanup\_sandbox(sandbox\_path, keep\_logs=not result.success)    return self.\_parse\_compile\_output(result)    def \_run\_ubt(self, project: str, target\_module: str, args: list) -> subprocess.CompletedProcess:  """调用 UnrealBuildTool"""  cmd = [  f"{self.engine\_path}/Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool",  target\_module,  "Win64", # 或 Linux，用于 CI 服务器  "Development",  f"-Project={project}/Project.uproject",  \*args  ]  return subprocess.run(cmd, capture\_output=True, text=True, timeout=300)    def \_parse\_compile\_output(self, result: subprocess.CompletedProcess) -> CompileResult:  """解析编译输出，结构化错误信息供 LLM 修复"""  errors = []  error\_pattern = r'(.+\.cpp)\((\d+)\): error (\w+): (.+)'    for line in result.stderr.split('\n'):  match = re.match(error\_pattern, line)  if match:  errors.append({  "file": match.group(1),  "line": int(match.group(2)),  "code": match.group(3),  "message": match.group(4),  "context": self.\_get\_code\_context(match.group(1), int(match.group(2)))  })    return CompileResult(  success=result.returncode == 0,  errors=errors,  warnings=self.\_parse\_warnings(result.stderr),  compile\_time=self.\_parse\_time(result.stdout)  ) |

**5.2 热重载测试（Live Coding Validation）**

对于 UE5 项目，还需验证生成代码支持热重载（不影响开发效率）：

|  |
| --- |
| Python def validate\_hot\_reload\_compatibility(code: str) -> HotReloadResult:  """  检查生成代码是否支持 UE5 Live Coding  主要规则：  1. 避免在头文件中定义带有虚函数的全局静态对象  2. UCLASS/USTRUCT 的成员变量顺序不能改变（内存布局破坏性变更）  3. 检测可能导致 Hot Reload 崩溃的模式  """  issues = []    # 规则 1：静态全局 UObject 实例（Hot Reload 后地址失效）  if re.search(r'static\s+U\w+\\*', code):  issues.append(HotReloadIssue(  severity="warning",  message="静态 UObject 指针在热重载后可能悬空",  fix\_suggestion="改用 TWeakObjectPtr 或在构造函数中初始化"  ))    return HotReloadResult(compatible=len(issues) == 0, issues=issues) |

**六、第三层：单元测试与引擎沙箱测试**

**定位**：在引擎沙箱中测试独立的逻辑单元，无需完整游戏世界，秒级到分钟级完成。

**6.1 自动生成单元测试（GameUnitLLM 模式）**

GameUnitLLM 框架通过微调 Code Llama 来自动生成游戏引擎专用的单元测试。该系统首先收集专家编写的已知有效单元测试，在此基础上创建微调版本，然后利用该模型合成数据集，最终生成针对 C++ 和 C# 的专用测试生成模型。

|  |
| --- |
| Python class GameUnitTestGenerator:  """  为 LLM 生成的游戏代码自动生成配套单元测试  参考 GameUnitLLM (2024) 的思路，结合游戏项目上下文  """    UNIT\_TEST\_GENERATION\_PROMPT = """ 你是一个 {engine} 单元测试专家。为以下生成的游戏代码生成完整的单元测试套件。  ## 目标代码 ```cpp {generated\_code} |

**项目测试规范**

* 测试框架：{test\_framework} // UE5: Spec/CQTest, Unity: UTF, Godot: GUT
* 项目命名规范：{naming\_convention}
* 已有测试风格参考：{test\_examples}

**必须覆盖的测试场景（游戏特定）**

1. **正常路径**：标准输入 → 预期输出
2. **边界值**：血量=0, 血量=MAX, 移速=0 等游戏极值
3. **状态机转换**：合法状态转换 + 非法状态转换（应被拒绝）
4. **资产加载**：资产路径有效性（Mock 资产系统）
5. **空指针防护**：Component 未挂载时的防御性处理
6. **帧无关性**：逻辑应在任意 DeltaTime 下行为一致

**输出要求**

* 使用 {test\_framework} 的标准宏/方法
* 每个测试函数独立，不共享状态
* 包含 Mock/Stub 的正确使用
* 附加测试意图注释 """
* def generate\_tests\_for\_ue5(self, generated\_code: str, project\_context: dict) -> str: """为 UE5 C++ 代码生成测试（使用 CQTest 框架）""" prompt = self.UNIT\_TEST\_GENERATION\_PROMPT.format( engine="Unreal Engine 5", generated\_code=generated\_code, test\_framework="CQTest (UE5 推荐框架，来自 Lyra 示例)", naming\_convention=project\_context["naming\_convention"], test\_examples=project\_context["test\_examples"][:3] # 少量 In-Context 示例 )

|  |
| --- |
| Plain Text  test\_code = llm\_client.complete(prompt)  return test\_code |

|  |
| --- |
| Plain Text  ### 6.2 UE5 测试框架深度配置  CQTest 是 UE5 目前推荐的测试库，特别适合编写从单元到功能测试各种范围的游戏测试，但目前参数化测试功能尚待完善，对于资产测试等场景有一定限制。  ```cpp // 为 LLM 生成的角色移动代码生成的 CQTest 测试 // 文件：Tests/LLMGenerated\_PlayerMovement\_Test.cpp  #include "CQTest.h" #include "GameFramework/Character.h" // 导入被测代码（由 LLM 生成） #include "LLMGen\_PlayerMovementComponent.h"  // 测试套件：LLM 生成的玩家移动组件 TEST\_CLASS(LLMGen\_PlayerMovement, "LLMGenerated.Character.Movement") {  // 测试夹具（Fixture）设置  UWorld\* TestWorld;  ACharacter\* TestCharacter;  ULLMGen\_PlayerMovementComponent\* MovComp;    BEFORE\_ALL()  {  TestWorld = UWorld::CreateWorld(EWorldType::Game, false);  TestCharacter = TestWorld->SpawnActor<ACharacter>();  MovComp = NewObject<ULLMGen\_PlayerMovementComponent>(TestCharacter);  TestCharacter->AddInstanceComponent(MovComp);  }    // TC-001：正常速度设置  TEST\_METHOD(SetMaxSpeed\_Normal\_SetsCorrectly)  {  MovComp->SetMaxWalkSpeed(600.f);  TestEqual("MaxWalkSpeed should be 600", MovComp->MaxWalkSpeed, 600.f);  }    // TC-002：边界值 - 负速度应被拒绝  TEST\_METHOD(SetMaxSpeed\_Negative\_ClampsToZero)  {  MovComp->SetMaxWalkSpeed(-100.f);  TestTrue("Negative speed should be clamped", MovComp->MaxWalkSpeed >= 0.f);  }    // TC-003：DeltaTime 无关性 - 位移计算  TEST\_METHOD(Movement\_DeltaTimeIndependent\_ConsistentDisplacement)  {  // 同样的总时间，不同的帧分割，最终位移应该接近一致  FVector pos1 = SimulateMovement(1.0f, 1); // 1帧  FVector pos2 = SimulateMovement(1.0f, 100); // 100帧    TestTrue(  "Frame-independent movement",   FVector::Dist(pos1, pos2) < 1.0f // 误差小于 1cm  );  }    // TC-004：状态机 - 空中不能二次跳跃（如果设计如此）  TEST\_METHOD(Jump\_WhileInAir\_ShouldBeRejected)  {  TestCharacter->Jump(); // 第一次跳跃  TestWorld->Tick(ELevelTick::LEVELTICK\_All, 0.1f); // 模拟0.1秒    bool secondJumpResult = MovComp->CanJump();  TestFalse("Should not be able to double jump", secondJumpResult);  }    AFTER\_ALL()  {  TestWorld->DestroyWorld(false);  } }; |

**6.3 Unity 测试框架配置**

|  |
| --- |
| C# // Unity Test Framework (UTF) - 为 LLM 生成代码自动生成的测试 using NUnit.Framework; using UnityEngine; using UnityEngine.TestTools; using System.Collections;  [TestFixture] [Category("LLMGenerated")] public class LLMGen\_EnemyAI\_Tests {  private GameObject enemyGO;  private LLMGen\_EnemyAIController aiController;    [SetUp]  public void SetUp()  {  // 纯代码创建测试对象，不依赖 Scene  enemyGO = new GameObject("TestEnemy");  aiController = enemyGO.AddComponent<LLMGen\_EnemyAIController>();  }    [Test]  public void DetectPlayer\_WithinRange\_ShouldReturnTrue()  {  // 创建 Mock 玩家  var playerGO = new GameObject("TestPlayer");  playerGO.transform.position = new Vector3(5f, 0f, 0f);    aiController.detectionRange = 10f;  bool detected = aiController.DetectPlayer(playerGO.transform);    Assert.IsTrue(detected, "Enemy should detect player within range");  }    // 边界值测试：恰好在检测边界  [Test]  [TestCase(9.99f, true)] // 刚好在范围内  [TestCase(10.0f, false)] // 恰好在边界（通常为不可检测）  [TestCase(10.01f, false)] // 刚好超出范围  public void DetectPlayer\_BoundaryValues\_ReturnsExpected(float distance, bool expectedDetected)  {  var playerGO = new GameObject("TestPlayer");  playerGO.transform.position = new Vector3(distance, 0f, 0f);  aiController.detectionRange = 10f;    bool result = aiController.DetectPlayer(playerGO.transform);  Assert.AreEqual(expectedDetected, result);  }    // Play Mode 测试：需要引擎运行时的测试  [UnityTest]  public IEnumerator EnemyPatrol\_AfterSpawn\_StartsMoving()  {  aiController.StartPatrol();  yield return new WaitForSeconds(0.5f); // 等待半秒    // 验证敌人已经移动  Assert.AreNotEqual(Vector3.zero, enemyGO.transform.position,  "Enemy should start moving after patrol is initiated");  }    [TearDown]  public void TearDown()  {  Object.DestroyImmediate(enemyGO);  } } |

**七、第四层：集成测试与系统行为验证**

**定位**：在有限的游戏环境中测试多系统交互，10秒~5分钟完成。

**7.1 UE5 功能测试（Functional Test）**

UE5 集成测试通常需要加载更多资产和依赖，大多数游戏逻辑集成测试需要 10-20 秒，这与单元测试仅需约 0.005 秒形成鲜明对比。

|  |
| --- |
| C++ // LLM 生成的 Boss 召唤系统集成测试 // 使用 UE5 Functional Test Actor（可在编辑器 Blueprint 中编写）  UCLASS() class ALLMGen\_BossSummon\_IntegrationTest : public AFunctionalTest {  GENERATED\_BODY()   public:  virtual void StartTest() override  {  // 测试场景：Boss 召唤系统与动画、特效、音效的联动    // Step 1: 验证 Boss Actor 可以正确 Spawn  FActorSpawnParameters SpawnParams;  BossActor = GetWorld()->SpawnActor<ALLMGen\_DragonBoss>(  BossClass,  FVector(0, 0, 100),  FRotator::ZeroRotator,  SpawnParams  );  AssertIsValid(BossActor, TEXT("Boss actor should spawn successfully"));    // Step 2: 触发落地动画序列  BossActor->PlayLandingSequence();    // Step 3: 等待动画完成（异步）  AddTimerToSelf(3.5f); // 动画时长 3.2s + buffer  }    virtual void OnTimerExpired() override  {  // Step 4: 验证动画状态机最终状态  UAnimInstance\* AnimInst = BossActor->GetMesh()->GetAnimInstance();  AssertTrue(  AnimInst->IsAnyMontagePlaying() == false,  TEXT("Landing montage should have completed")  );    // Step 5: 验证特效是否被激活（冲击波）  UNiagaraComponent\* VFX = BossActor->FindComponentByClass<UNiagaraComponent>();  AssertIsValid(VFX, TEXT("Impact VFX component should exist"));  // 注意：VFX 完成后会自动停用，检查已播放次数    // Step 6: 验证音效是否触发（通过 Audio Component 状态）  // 使用 Mock Audio System 记录触发历史  AssertTrue(  MockAudioSystem::GetPlayCount("SFX\_Dragon\_LandImpact\_Heavy") == 1,  TEXT("Landing impact sound should play exactly once")  );    FinishTest(EFunctionalTestResult::Succeeded, TEXT("Boss summon integration test passed"));  }   private:  UPROPERTY()  ALLMGen\_DragonBoss\* BossActor;    UPROPERTY(EditDefaultsOnly)  TSubclassOf<ALLMGen\_DragonBoss> BossClass; }; |

**7.2 跨系统兼容性矩阵测试**

生成代码必须与现有的核心系统（伤害系统、存档系统、UI 系统等）正确交互：

|  |
| --- |
| Python COMPATIBILITY\_TEST\_MATRIX = {  "DamageSystem": [  "generated\_code\_applies\_correct\_damage\_type",  "generated\_code\_respects\_immunity\_flags",  "generated\_code\_triggers\_death\_on\_zero\_health",  ],  "SaveSystem": [  "generated\_code\_state\_is\_serializable",  "generated\_code\_loads\_correctly\_after\_save",  "generated\_code\_handles\_missing\_save\_data\_gracefully",  ],  "UISystem": [  "generated\_code\_sends\_correct\_ui\_events",  "generated\_code\_does\_not\_break\_existing\_hud",  ],  "MultiplayerReplication": [  "generated\_code\_marks\_replicated\_properties",  "generated\_code\_uses\_rpc\_correctly",  "generated\_code\_handles\_network\_latency",  ] }  def run\_compatibility\_matrix(generated\_module: str, project\_systems: list[str]) -> dict:  """运行兼容性矩阵测试"""  results = {}  for system in project\_systems:  if system in COMPATIBILITY\_TEST\_MATRIX:  tests = COMPATIBILITY\_TEST\_MATRIX[system]  results[system] = {  "tests": tests,  "passed": [],  "failed": [],  "skipped": []  }  for test in tests:  result = run\_single\_compat\_test(generated\_module, system, test)  if result.passed:  results[system]["passed"].append(test)  else:  results[system]["failed"].append({  "test": test,  "reason": result.failure\_reason  })  return results |

**八、第五层：运行时测试与游戏仿真**

**定位**：完整游戏运行时，通过 LLM Agent 充当自动玩家进行黑盒测试。

**8.1 TITAN 风格的 Agent Playtest**

TITAN 框架展示了单个 Agent 可以同时处理多个测试目标：通过任务完成检测功能正确性、通过覆盖率引导探索检测彻底性、通过高级 Oracle 检测 Bug。该框架能够发现软锁（Soft Lock）和逻辑错误等人工测试者也常常遗漏的 Bug 类型。

|  |
| --- |
| Python class GamePlaytestAgent:  """  基于 LLM 的自动游戏测试 Agent  扮演"智能玩家"，从功能、覆盖率、Bug 检测三个维度评估 LLM 生成代码  """    def \_\_init\_\_(self, game\_process: GameProcess, llm\_client: LLMClient):  self.game = game\_process  self.llm = llm\_client  self.action\_log = []  self.bug\_log = []  self.state\_coverage = set()    def run\_playtest\_session(  self,   test\_scenario: str,  max\_steps: int = 200,  timeout\_sec: int = 120  ) -> PlaytestReport:  """  运行一次自动游戏测试会话    test\_scenario: 描述要测试的功能，例如  "测试 LLM 生成的 Boss 召唤逻辑：触发召唤 → 验证 Boss 出现 → 攻击 Boss → 验证掉血"  """    initial\_state = self.game.get\_state()    for step in range(max\_steps):  current\_state = self.game.get\_state()    # 状态抽象：将游戏状态转化为 LLM 可理解的文本  state\_summary = self.\_abstract\_game\_state(current\_state)    # 检测异常状态（软锁、崩溃前兆）  anomaly = self.\_detect\_anomaly(current\_state)  if anomaly:  self.bug\_log.append(anomaly)  break    # LLM 决策下一步动作  action = self.llm.decide\_action(  system\_prompt=PLAYTEST\_AGENT\_PROMPT.format(scenario=test\_scenario),  state=state\_summary,  action\_history=self.action\_log[-10:], # 最近10步历史  available\_actions=self.game.get\_available\_actions()  )    # 执行动作  result = self.game.execute\_action(action)  self.action\_log.append({"action": action, "result": result})    # 记录状态覆盖（用于覆盖率计算）  state\_key = self.\_hash\_state(current\_state)  self.state\_coverage.add(state\_key)    # 验证 Oracle：检查生成代码的行为是否符合设计规范  violation = self.\_check\_oracle(current\_state, action, result)  if violation:  self.bug\_log.append(violation)    return PlaytestReport(  scenario=test\_scenario,  steps\_executed=len(self.action\_log),  bugs\_found=self.bug\_log,  state\_coverage\_count=len(self.state\_coverage),  final\_verdict=self.\_compute\_verdict()  )    def \_detect\_anomaly(self, state: GameState) -> Optional[BugReport]:  """检测软锁、无限循环、性能崩溃等异常"""  # 检测 1：FPS 大幅下降（可能是 LLM 代码引入的性能问题）  if state.fps < 20 and state.expected\_fps > 60:  return BugReport(  type="performance\_regression",  description=f"FPS dropped to {state.fps}, expected > 60",  severity="high"  )    # 检测 2：角色进入不可达位置  if state.player\_position.z < -1000: # 掉出地图  return BugReport(  type="geometry\_error",  description="Player fell out of the map",  severity="critical"  )    # 检测 3：同一状态连续重复（软锁检测）  recent\_states = [log["result"] for log in self.action\_log[-10:]]  if len(set(str(s) for s in recent\_states)) == 1:  return BugReport(  type="soft\_lock",  description="Game entered an unrecoverable loop state",  severity="critical"  )    return None  PLAYTEST\_AGENT\_PROMPT = """ 你是一个专业的游戏测试工程师 Agent。你的任务是：  \*\*测试目标\*\*：{scenario}  \*\*测试策略\*\*： 1. 首先执行"快乐路径"（Happy Path）：完成主要功能流程 2. 然后尝试边缘情况：极限值、快速点击、异常顺序操作 3. 最后尝试"破坏性测试"：尝试绕过限制、触发边界条件  \*\*Bug 判断标准\*\*： - 崩溃、异常错误：严重Bug - 游戏进入无法进行的状态：严重Bug - 功能行为与设计规范不符：一般Bug - 视觉显示异常但不影响游戏性：轻微Bug  \*\*输出格式\*\*： 仅输出一个 JSON 对象，包含字段 action（要执行的游戏动作）和 reasoning（简短的推理）。 """ |

**8.2 性能基准测试**

|  |
| --- |
| Python class GamePerformanceBenchmark:  """  验证 LLM 生成代码不会引入性能回归  基线：合并前的项目性能  """    PERFORMANCE\_THRESHOLDS = {  "fps\_regression\_max": 0.05, # FPS 降低不超过 5%  "frame\_time\_spike\_max\_ms": 2.0, # 最大帧时间尖峰增加 < 2ms  "memory\_increase\_max\_mb": 50, # 内存增加不超过 50MB  "draw\_call\_increase\_max\_pct": 0.10, # DrawCall 增加不超过 10%  "tick\_overhead\_max\_us": 100, # 新增 Tick 逻辑开销 < 100μs  }    def benchmark\_generated\_code(  self,   baseline\_metrics: dict,  test\_scenario: str  ) -> BenchmarkResult:  """  在特定场景下对比生成代码前后的性能  使用 UE5 Unreal Insights / Unity Profiler 采集数据  """    # 采集当前（注入生成代码后）的性能数据  with\_generated = self.run\_profiled\_session(test\_scenario, duration=30)    regressions = []  for metric, threshold in self.PERFORMANCE\_THRESHOLDS.items():  baseline\_val = baseline\_metrics[metric]  current\_val = with\_generated[metric]    if metric.endswith("\_pct"):  delta = (current\_val - baseline\_val) / baseline\_val  else:  delta = current\_val - baseline\_val    if delta > threshold:  regressions.append(PerformanceRegression(  metric=metric,  baseline=baseline\_val,  current=current\_val,  delta=delta,  threshold=threshold  ))    return BenchmarkResult(  passed=len(regressions) == 0,  regressions=regressions,  raw\_metrics=with\_generated  ) |

**九、自修复 Agent 循环：LLMLOOP 范式**

**核心设计**：测试失败不是终点，而是触发自修复循环的起点。

**9.1 LLMLOOP 架构实现**

研究表明，迭代反馈循环可以显著提升 LLM 生成代码的质量。编译器反馈涵盖多种粒度：粗粒度反馈提供编译成功与否的二值信息，而细粒度反馈则提供详细的错误原因和位置。

|  |
| --- |
| Python class LLMCodeSelfRepairLoop:  """  基于 LLMLOOP (ICSME 2025) 和 SWE-Agent 的自修复循环    架构：  生成代码 → 测试 → 失败诊断 → 修复提示 → LLM 修复 → 再测试  最多迭代 MAX\_ITERATIONS 次  """    MAX\_ITERATIONS = 5  TEMPERATURE\_SCHEDULE = [0.0, 0.2, 0.5, 0.7, 1.0] # 随迭代增加温度（增加多样性）    def repair\_until\_pass(  self,   original\_code: str,  original\_requirement: str,  test\_results: list[TestResult]  ) -> RepairOutcome:    current\_code = original\_code  repair\_history = []    for iteration in range(self.MAX\_ITERATIONS):  # 收集所有失败的测试信息  failures = [r for r in test\_results if not r.passed]    if not failures:  return RepairOutcome(  success=True,  final\_code=current\_code,  iterations\_taken=iteration,  repair\_history=repair\_history  )    # 构建诊断上下文  diagnosis = self.\_diagnose\_failures(failures, current\_code)    # 生成修复提示（层次化：优先修复最严重的问题）  repair\_prompt = self.\_build\_repair\_prompt(  code=current\_code,  requirement=original\_requirement,  diagnosis=diagnosis,  repair\_history=repair\_history,  iteration=iteration  )    # LLM 修复（温度随迭代增加，引入更多多样性）  temperature = self.TEMPERATURE\_SCHEDULE[min(iteration, len(self.TEMPERATURE\_SCHEDULE)-1)]  repaired\_code = self.llm.complete(  repair\_prompt,  temperature=temperature,  max\_tokens=4096  )    # 记录本次修复  repair\_history.append(RepairAttempt(  iteration=iteration,  failures\_before=failures,  repair\_prompt\_summary=diagnosis["summary"],  repaired\_code=repaired\_code,  temperature=temperature  ))    # 对修复代码重新测试  test\_results = self.test\_runner.run\_all(repaired\_code)  current\_code = repaired\_code    # 超过最大迭代次数，记录为需要人工介入  return RepairOutcome(  success=False,  final\_code=current\_code,  iterations\_taken=self.MAX\_ITERATIONS,  repair\_history=repair\_history,  escalation\_needed=True  )    def \_diagnose\_failures(self, failures: list[TestResult], code: str) -> dict:  """  结构化诊断失败原因，为 LLM 修复提供精确上下文  优先级排序：编译错误 > 资产路径错误 > 运行时崩溃 > 逻辑错误 > 性能问题  """  diagnosis = {  "summary": "",  "root\_cause": None,  "affected\_lines": [],  "fix\_hints": [],  "priority\_order": []  }    # 按严重程度排序  SEVERITY\_ORDER = ["compile\_error", "asset\_not\_found", "crash", "logic\_error", "performance"]    for failure in sorted(failures, key=lambda f: SEVERITY\_ORDER.index(f.error\_type)):  diagnosis["priority\_order"].append(failure.error\_type)    if failure.error\_type == "compile\_error":  # 提取精确的错误位置和上下文代码  diagnosis["affected\_lines"].append({  "line": failure.line\_number,  "error": failure.error\_message,  "context\_code": self.\_get\_code\_context(code, failure.line\_number, radius=5),  "fix\_hint": self.\_lookup\_fix\_hint(failure.error\_code)  })    elif failure.error\_type == "asset\_not\_found":  diagnosis["fix\_hints"].append(  f"资产路径 '{failure.invalid\_path}' 不存在。"  f"最近似的有效路径是：'{failure.suggested\_path}'（相似度 {failure.similarity:.0%}）"  )    diagnosis["summary"] = self.\_generate\_diagnosis\_summary(diagnosis)  return diagnosis    REPAIR\_PROMPT\_TEMPLATE = """ 你是一个 {engine} 代码修复专家。以下代码在测试中失败了，请修复它。  ## 原始需求 {requirement}  ## 当前代码（第 {iteration} 次修复尝试） ```cpp {current\_code} |

**测试失败诊断（按优先级排序）**

{diagnosis}

**历史修复记录（避免重复犯同样的错误）**

{repair\_history}

**修复要求**

1. **只修复上述失败的具体问题**，不要重构无关代码
2. **不要引入新的依赖**或改变函数签名（会破坏其他测试）
3. 如果资产路径错误，使用建议的替代路径
4. 修复后输出**完整的修复后代码**（不是 diff）

**输出格式**

|  |
| --- |
| C++ // [修复说明：在此说明修复了什么] // [修复内容：...] <完整修复后的代码> |

"""

|  |
| --- |
| Plain Text  ### 9.2 多样本并行修复（Pass@K 策略）  对于难以修复的问题，可以并行生成多个修复方案，选择通过测试的版本：  ```python def parallel\_repair\_with\_voting(  code: str,   failures: list[TestResult],  k: int = 5 ) -> str:  """  并行生成 K 个修复方案（不同温度/不同提示），  选择通过测试最多的版本（投票）  """  import asyncio    async def generate\_repair\_candidate(idx: int):  temperature = 0.2 + idx \* 0.2 # 0.2, 0.4, 0.6, 0.8, 1.0  prompt = build\_repair\_prompt(code, failures, variant=idx)  candidate = await llm\_client.async\_complete(prompt, temperature=temperature)  test\_result = await test\_runner.async\_run\_all(candidate)  return candidate, test\_result    # 并行生成 K 个候选  candidates = asyncio.run(  asyncio.gather(\*[generate\_repair\_candidate(i) for i in range(k)])  )    # 选择通过测试最多的候选  best\_candidate = max(candidates, key=lambda x: x[1].pass\_count)  return best\_candidate[0] |

**十、测试 Agent 的 Agentic 编排架构**

**10.1 LangGraph 状态机设计**

|  |
| --- |
| Python from langgraph.graph import StateGraph, END from typing import TypedDict, Annotated import operator  class TestPipelineState(TypedDict):  """测试管线的完整状态"""  generated\_code: str  requirement: str  project\_context: dict    # 各层测试结果  static\_analysis\_result: Optional[dict]  compile\_result: Optional[dict]  unit\_test\_result: Optional[dict]  integration\_test\_result: Optional[dict]  runtime\_test\_result: Optional[dict]    # 修复历史  repair\_history: Annotated[list, operator.add]  current\_iteration: int    # 最终决策  final\_verdict: str # "pass" | "fail" | "escalate"  test\_report: Optional[dict]  def build\_test\_pipeline() -> StateGraph:  """构建测试 Agent 的 LangGraph 状态机"""    graph = StateGraph(TestPipelineState)    # 注册节点  graph.add\_node("static\_analysis", run\_static\_analysis)  graph.add\_node("compile\_test", run\_compile\_test)  graph.add\_node("unit\_test", run\_unit\_tests)  graph.add\_node("integration\_test", run\_integration\_tests)  graph.add\_node("runtime\_test", run\_runtime\_tests)  graph.add\_node("diagnose\_and\_repair", run\_diagnose\_and\_repair)  graph.add\_node("generate\_report", generate\_final\_report)    # 设置入口  graph.set\_entry\_point("static\_analysis")    # 添加条件边（每层测试后的路由决策）  graph.add\_conditional\_edges(  "static\_analysis",  route\_after\_static,  {  "pass": "compile\_test",  "fail\_repairable": "diagnose\_and\_repair",  "fail\_critical": "generate\_report"  }  )    graph.add\_conditional\_edges(  "compile\_test",  route\_after\_compile,  {  "pass": "unit\_test",  "fail\_repairable": "diagnose\_and\_repair",  "fail\_critical": "generate\_report"  }  )    graph.add\_conditional\_edges(  "unit\_test",  route\_after\_unit,  {  "pass": "integration\_test",  "partial\_pass": "integration\_test", # 部分通过也继续（记录问题）  "fail": "diagnose\_and\_repair"  }  )    graph.add\_conditional\_edges(  "integration\_test",  route\_after\_integration,  {  "pass": "runtime\_test",  "fail": "diagnose\_and\_repair"  }  )    graph.add\_conditional\_edges(  "runtime\_test",  route\_after\_runtime,  {  "pass": "generate\_report",  "fail": "diagnose\_and\_repair"  }  )    # 修复后路由：根据迭代次数决定重试哪一层  graph.add\_conditional\_edges(  "diagnose\_and\_repair",  route\_after\_repair,  {  "retry\_static": "static\_analysis",  "retry\_compile": "compile\_test",  "retry\_unit": "unit\_test",  "retry\_integration": "integration\_test",  "max\_iterations\_exceeded": "generate\_report"  }  )    graph.add\_edge("generate\_report", END)    return graph.compile()   def route\_after\_static(state: TestPipelineState) -> str:  """静态分析后的路由决策"""  result = state["static\_analysis\_result"]    if not result["errors"]:  return "pass"    # 判断是否可修复  critical\_errors = [e for e in result["errors"]   if e["type"] in ["hallucinated\_api", "path\_not\_found"]]    if len(critical\_errors) > 10: # 错误太多，人工介入  return "fail\_critical"    if state["current\_iteration"] >= 5: # 修复次数已达上限  return "fail\_critical"    return "fail\_repairable" |

**10.2 测试 Agent 与代码生成 Agent 的协议接口**

|  |
| --- |
| Python @dataclass class TestRequest:  """代码生成 Agent → 测试 Agent 的请求协议"""  request\_id: str  generated\_code: str  original\_requirement: str  target\_engine: str # "unreal5.3" | "unity6" | "godot4"  target\_module: str # 注入的目标模块名  project\_snapshot\_id: str # 项目代码快照 ID  test\_depth: str = "full" # "quick"(L1~L2) | "standard"(L1~L4) | "full"(L1~L5)  auto\_repair: bool = True # 是否启用自修复循环  max\_repair\_iterations: int = 5  @dataclass  class TestResponse:  """测试 Agent → 代码生成 Agent 的响应协议"""  request\_id: str  overall\_verdict: str # "pass" | "conditional\_pass" | "fail" | "escalate"  final\_code: str # 经过修复的最终代码（可能与原始代码不同）    # 各层结果摘要  layer\_results: dict[str, LayerResult]    # 修复历史（用于上游优化 LLM 生成）  repair\_attempts: int  repair\_summary: list[str]    # 注入指导  injection\_instructions: dict # 如何将代码注入项目（文件路径、Build 配置等）  known\_limitations: list[str] # 已知但未解决的限制（需要告知用户）    # 质量指标  test\_coverage\_estimate: float # 估算的代码覆盖率  performance\_delta: Optional[dict] # 性能变化（如果运行了性能测试） |

**十一、CI/CD 管线集成**

**11.1 GitHub Actions / Jenkins 工作流**

|  |
| --- |
| YAML # .github/workflows/llm\_generated\_code\_test.yml name: LLM Generated Code Automated Test Pipeline  on:  workflow\_dispatch:  inputs:  request\_id:  description: 'Test Request ID'  required: true  generated\_code\_artifact:  description: 'Artifact ID containing generated code'  required: true  target\_engine:  description: 'Target Engine (ue53/unity6/godot4)'  required: true  default: 'ue53'  jobs:  # 阶段 1：快速静态分析（无需引擎，2分钟内完成）  static-analysis:  runs-on: ubuntu-latest  outputs:  result: ${{ steps.analyze.outputs.result }}  steps:  - name: Download generated code  uses: actions/download-artifact@v4  with:  name: ${{ inputs.generated\_code\_artifact }}    - name: Run static analysis  id: analyze  run: |  python -m game\_code\_tester.static\_analyze \  --code-dir ./generated \  --engine ${{ inputs.target\_engine }} \  --project-index ${{ secrets.PROJECT\_ASSET\_INDEX\_PATH }} \  --output-format json \  > static\_result.json  echo "result=$(cat static\_result.json | jq -r '.verdict')" >> $GITHUB\_OUTPUT    - name: Upload static analysis report  uses: actions/upload-artifact@v4  with:  name: static-analysis-report  path: static\_result.json   # 阶段 2：编译验证（需要引擎，10-15分钟）  compile-test:  needs: static-analysis  if: needs.static-analysis.outputs.result != 'critical\_fail'  runs-on: [self-hosted, windows, ue5] # 需要带引擎的自托管 Runner  steps:  - name: Restore project from cache  uses: actions/cache@v4  with:  path: D:\GameProject  key: project-snapshot-${{ github.sha }}    - name: Inject generated code into sandbox  run: |  python -m game\_code\_tester.inject\_sandbox \  --project D:\GameProject \  --code-dir ./generated \  --sandbox-dir D:\TestSandbox    - name: Compile with UnrealBuildTool  run: |  D:\UnrealEngine\Engine\Build\BatchFiles\Build.bat `  -Target="GameProjectEditor Win64 Development" `  -Project="D:\TestSandbox\GameProject.uproject" `  -WaitMutex -AllCores 2>&1 | Tee-Object compile\_log.txt    python -m game\_code\_tester.parse\_compile\_log `  --log compile\_log.txt --output compile\_result.json   # 阶段 3：单元测试（引擎启动，5-10分钟）  unit-tests:  needs: compile-test  if: needs.compile-test.outputs.result == 'success'  runs-on: [self-hosted, windows, ue5]  steps:  - name: Run UE5 Automation Tests  run: |  D:\UnrealEngine\Engine\Binaries\Win64\UnrealEditor-Cmd.exe `  D:\TestSandbox\GameProject.uproject `  -ExecCmds="Automation RunTests LLMGenerated; Quit" `  -log=unit\_test.log -unattended -nopause    - name: Parse test results  run: |  python -m game\_code\_tester.parse\_ue5\_test\_log `  --log unit\_test.log --output unit\_test\_result.json   # 阶段 4：集成测试（可选，20-40分钟）  integration-tests:  needs: unit-tests  if: needs.unit-tests.outputs.result == 'pass'  runs-on: [self-hosted, windows, ue5, gpu] # 需要 GPU 渲染  steps:  - name: Run Functional Tests  run: |  # 使用 Gauntlet 框架运行功能测试  python D:\UnrealEngine\Engine\Build\BatchFiles\RunUAT.py `  RunUnreal+RunAutomation `  -project=D:\TestSandbox\GameProject.uproject `  -platform=Win64 `  -configuration=Development `  -test=LLMGenerated.Integration.\*    # 最终：汇总报告  aggregate-report:  needs: [static-analysis, compile-test, unit-tests, integration-tests]  if: always()  runs-on: ubuntu-latest  steps:  - name: Aggregate all test results  run: |  python -m game\_code\_tester.aggregate\_report \  --request-id ${{ inputs.request\_id }} \  --static static\_result.json \  --compile compile\_result.json \  --unit unit\_test\_result.json \  --output final\_report.json    - name: Notify code generation system  run: |  curl -X POST ${{ secrets.CODE\_GEN\_CALLBACK\_URL }} \  -H "Content-Type: application/json" \  -d @final\_report.json |

**11.2 测试优先级与快速失败策略**

|  |
| --- |
| Python # 快速失败决策矩阵 FAST\_FAIL\_RULES = {  "hallucinated\_api\_count > 5": {  "action": "immediate\_fail",  "reason": "LLM 生成了大量不存在的 API，通常意味着根本性的理解错误",  "skip\_layers": ["compile", "unit", "integration", "runtime"]  },  "naming\_conflicts > 0 AND severity == 'error'": {  "action": "immediate\_fail",  "reason": "命名冲突会破坏现有功能，风险过高",  "skip\_layers": ["compile", "unit", "integration", "runtime"]  },  "compile\_errors == 0 AND unit\_pass\_rate < 0.5": {  "action": "repair\_and\_retry",  "reason": "编译通过但单元测试通过率低，逻辑问题",  "repair\_focus": "logic"  },  "all\_tests\_pass AND performance\_regression > 0.1": {  "action": "conditional\_pass",  "reason": "功能正确但有性能问题，需要人工审查",  "notification": "performance\_team"  } } |

**十二、可观测性与诊断报告**

**12.1 结构化测试报告**

|  |
| --- |
| Python @dataclass class FinalTestReport:  """最终交付给用户和上游系统的测试报告"""    # 元信息  request\_id: str  timestamp: str  total\_duration\_sec: float    # 顶层裁决  verdict: str # "PASS" | "CONDITIONAL\_PASS" | "FAIL" | "ESCALATE"  confidence: float # 0.0~1.0，测试覆盖率与置信度    # 各层结果（结构化，LLM 可读）  layers: dict[str, dict]    # 修复历史摘要  total\_repair\_attempts: int  auto\_repaired\_issues: list[str]  remaining\_issues: list[str]    # 用户可读摘要  user\_summary: str # 自然语言摘要    # 开发者技术摘要  developer\_summary: dict    def to\_markdown(self) -> str:  """生成 Markdown 格式的测试报告"""  return f""" # LLM 代码测试报告  \*\*请求 ID\*\*: `{self.request\_id}`  \*\*测试时间\*\*: {self.timestamp}  \*\*总耗时\*\*: {self.total\_duration\_sec:.1f} 秒   ## 总体裁决：{self.\_verdict\_emoji()} {self.verdict}  置信度：{self.confidence:.0%}  ---  ## 各层测试结果  | 测试层 | 状态 | 通过率 | 耗时 | |--------|------|--------|------| {self.\_format\_layer\_table()}  ---  ## 问题摘要  ### 已自动修复的问题（{len(self.auto\_repaired\_issues)} 项） {self.\_format\_repaired\_issues()}  ### 残留问题（{len(self.remaining\_issues)} 项） {self.\_format\_remaining\_issues()}  ---  ## 用户说明 {self.user\_summary}  ---  ## 开发者注意事项 {self.\_format\_dev\_notes()} """ |

**12.2 可观测性指标体系**

|  |
| --- |
| Plain Text Prometheus Metrics（推送至监控系统）：  # 生成代码质量指标 game\_codegen\_static\_pass\_rate # 静态分析通过率 game\_codegen\_compile\_pass\_rate # 编译通过率 game\_codegen\_unit\_test\_pass\_rate # 单元测试通过率 game\_codegen\_defect\_types{type="..."} # 各类型缺陷频率  # 自修复效率指标 game\_codegen\_repair\_iterations\_avg # 平均修复迭代次数 game\_codegen\_auto\_repair\_success\_rate # 自动修复成功率 game\_codegen\_escalation\_rate # 需要人工介入的比例  # 性能指标 game\_codegen\_test\_pipeline\_duration\_p50 # 测试管线 P50 耗时 game\_codegen\_test\_pipeline\_duration\_p99 # 测试管线 P99 耗时 game\_codegen\_compile\_time\_avg # 平均编译时间  # 业务指标 game\_codegen\_user\_acceptance\_rate # 用户接受（不回退）的代码比例 game\_codegen\_post\_merge\_bug\_rate # 合并后生产 Bug 率（长期指标） |

**十三、关键工程决策与 KPI**

**13.1 引擎特定测试框架选型**

![](data:image/png;base64...)

**点击图片可查看完整电子表格**

**13.2 目标 KPI 与度量标准**

|  |
| --- |
| Plain Text 测试质量指标： ───────────────────────────────────────────────────── 指标 目标值 当前基线（参考） ───────────────────────────────────────────────────── 静态分析拦截率 > 90% - （拦截所有可检测的幻构缺陷）  编译通过率（修复后） > 95% -  单元测试通过率（修复后） > 85% -  自动修复成功率 > 70% - （不需要人工介入）  测试误报率（False Positive） < 5% -  测试漏报率（False Negative） < 10% - （通过测试但实际有 Bug）  工程效率指标： ───────────────────────────────────────────────────── 静态分析完成时间 < 30s - 编译+单元测试完成时间 < 15min - 完整测试管线完成时间 < 45min -  业务价值指标： ───────────────────────────────────────────────────── 合并后生产 Bug 率 < 2% 手动开发约 5~8% 程序员代码审查时间节省 > 50% - 用户需求到可用代码时间 < 1小时 手动开发约 2-5天 |

**13.3 落地优先级建议**

|  |
| --- |
| Plain Text Sprint 1（第 1-2 周）：快速价值，低成本  ✅ 实现 L1 静态分析（资产路径验证 + API 白名单）  ✅ 自动生成基础单元测试用例  ✅ 编译沙箱 + 错误解析  预期收益：拦截 60% 的幻构缺陷，无需引擎启动  Sprint 2（第 3-4 周）：核心能力  ✅ LLMLOOP 自修复循环（最多 3 次迭代）  ✅ CI/CD 管线集成（GitHub Actions / Jenkins）  ✅ 结构化测试报告  预期收益：自动修复率 > 60%  Sprint 3（第 5-8 周）：深度测试  ✅ 引擎集成测试（Functional Test）  ✅ 兼容性矩阵测试（与现有系统）  ✅ 性能基准测试  预期收益：覆盖 85%+ 的已知缺陷模式  Sprint 4（第 9-12 周）：运行时仿真（可选）  ✅ Agent 自动游玩测试（Playtest Agent）  ✅ Prometheus 监控仪表板  ✅ 持续优化（基于漏报数据）  预期收益：发现软锁等运行时深层 Bug |

**附录：核心技术参考**

**前沿研究**

* **LLMLOOP** (ICSME 2025) - 迭代反馈循环提升 LLM 生成代码质量
* **SMART** (2025) - LLM + RL + AST Diff 的混合游戏测试框架
* **TITAN** (2025) - MMORPG 场景下的 LLM Agent 游戏测试
* **GameUnitLLM** (Procedia 2024) - Code Llama 微调的游戏单元测试生成
* **ProxyWar** (ICSE 2026) - 游戏竞技场中的 LLM 代码生成动态评估
* **SWE-Agent** (NeurIPS 2024) - ReAct 模式的代码修复 Agent
* **AutoCodeRover** (ISSTA 2024) - 自主程序改进

**工程工具**

* game.ci - Unity 的开源 CI/CD 框架
* AltTester - Unity/Unreal 跨平台自动化测试
* GameDriver - 游戏 QA 自动化平台
* Gauntlet - UE5 多客户端测试编排框架
* CQTest - UE5 新一代测试框架（来自 Lyra 示例）

*文档版本：v1.0 | 2026-03 | 游戏 AI Agent 工程团队*