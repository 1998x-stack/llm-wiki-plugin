# “从 0 到 1 设计 Managed Agents 的系统架构图 + 核心数据表结构 + API 设计草案”。

> Source: 文章解读 Anthropic Agent
> Time: 2026/4/16 14:25:23

## Question

“从 0 到 1 设计 Managed Agents 的系统架构图 + 核心数据表结构 + API 设计草案”。

## Answer

我直接给你一版可落地的系统设计稿，不再停留在概念层。会包含三部分：总体架构图、核心数据模型、API 草案，并且我会把哪些是“对齐 Anthropic 抽象”，哪些是“我建议你自建时补上的部分”分开标出来。


我已经把官方资源模型和工程抽象拼起来了。接下来这版会更偏“设计文档”，你拿去就能当内部 RFC 初稿：上半部分是系统架构图，下半部分是数据表和 API，另外我会标出哪些接口最好从第一天就做成幂等和事件驱动。

Gathering info for architecture and API design


The user is asking for an architecture diagram, core DB schema, and an API design draft. It’s not necessarily a request for an artifact, but I should probably gather info from official docs. I’ll look things up, especially for OpenAI or Anthropic-related aspects. I’ll focus on providing structured, detailed answers.


Browsing official Anthropic docs for architecture and design


Scaling Managed Agents: Decoupling the brain from the hands
Claude Managed Agents 概览 - Claude API Docs


Looking for agent setup and schema details


I might need more documentation, especially on agent setup, environments, vaults, skills, and events. I could search to see if I can find a summary that contains the right info. I also need a precise schema, particularly regarding agent versioning. It's important to get all details right.


Searching documentation for agent setup and environments


Get started with Claude Managed Agents - Claude API Docs


Looking for details on environments, vaults, and skills


I need more info on environments, vaults, and skills. It’s essential to have those details to provide a thorough answer. I’ll look for reliable sources or documentation that cover these topics in depth. Once I gather everything, I’ll make sure to organize it clearly for the user.


Searching for environment, vault, and skill details


隔离库 - 非官方WARFRAME中文维基 | 星际战甲 | 戰甲神兵 ...
Simply Skills - MC百科|最大的Minecraft中文MOD百科
高级作战记录 - PRTS - 玩家共同构筑的明日方舟中文Wiki
火山地牢 - Stardew Valley Wiki


Trying a more direct approach to search


It looks like the search results aren’t ideal, so maybe I’ll try using direct URLs instead. I could search with specific site terms, directing the query to trusted sources for more accurate results. Hopefully, this will get better information quickly without too much extra digging.


Searching Claude API Docs via direct URLs


Claude Managed Agents overview - Claude API Docs
Claude Managed Agents 深度解读：Agent 开发的范式转移来了
Claude Managed Agents：托管式长时智能体的构建与实践 ...
什么是 Claude Managed Agents？企业 IT 团队完整指南 - 七 ...


Using direct URLs for better results


The search results aren't great, so maybe opening official docs directly using guessed URLs will work. I can try searching specifically for environments, vaults, and skills to get more detailed info. I'll use direct URLs to avoid relying on search snippets and ensure I include citations throughout.


Testing direct URLs for official documentation


Cloud environment setup - Claude API Docs


Looking for specific details in vaults, skills, and events


I need to find some specific lines from the vaults, skills, and events sections. It would be great to explore the relevant parts to pull out the key info. I’ll focus on those interesting lines to get a more detailed and precise understanding.


Searching for specific lines from vaults and events


Authenticate with vaults - Claude API Docs


Checking sessions states and agent setup


I probably need to look at specific lines for session states. I could try searching again and check snippets for useful info. It might be enough, or I could open the direct session lines. I’ll also explore the agent setup and any relevant session details that could help clarify things.


Opening agent setup and session lines analysis


Define your agent - Claude API Docs


Exploring sessions, permissions, and tools


I need to focus on opening the relevant lines in sessions, permission policies, and tools to gather the necessary details. I'll check each area for any useful information and make sure I’m getting what I need to proceed with the task correctly. Let’s start digging into these sections.


Opening relevant lines in sessions and permission policies


Start a session - Claude API Docs


Checking session statuses beyond line 225


I need to take a look at session status lines beyond line 225. There might be more information there that’s useful, so it makes sense to open up additional lines and continue checking the details. Let’s explore further to gather the full picture.


Opening additional session status lines past 225


Start a session - Claude API Docs


Considering design structure and citations


I’m thinking that I may need to include event types, usage, and maybe multi-agent considerations in the design, perhaps as an optional extension. Citation for multi-agent could come from Search4, but I’m not certain about cost/performance or some other details. I might also mention “official objects” like Agent, Environment, Session, and Events. Not sure if the architecture diagram should have a citation — I’ll need to think about those details. Should I offer a system architecture diagram, or convert to RFC?


Organizing design proposal structure


For this proposal, I need to cite any internet-sourced statements directly. I'll keep most design elements as our own proposal, marked with "建议." It's crucial to cite official facts, particularly when aligning with Anthropic. The structure should include sections on design assumptions, an architecture diagram, component explanations, and core DB schema. I might use concise SQL snippets for the tables, ensuring citations are not in the code. I’ll avoid huge tables but aim for clarity.


Thought for 2m 49s

下面给你一版可直接当内部 RFC 初稿的设计稿。我会按三层来写：


系统架构图：从 control plane 到 runtime plane

核心数据表结构：先给 MVP 必选表，再给二期推荐表

API 设计草案：按资源对象和事件流来设计


这版蓝图是 vendor-neutral 的：抽象上对齐 Anthropic 当前公开的 Managed Agents 设计——官方对象是 Agent、Environment、Session、Events，工程上则明确拆成 session、harness、sandbox 三部分；但我会把你自建时应该补的部分一起加上，比如环境版本、审批单、幂等键、artifact 存储和 usage ledger。Claude平台+3Anthropic+3Claude平台+3



1. 先定设计目标


从 0 到 1 设计 Managed Agents，我建议一开始就坚持 6 条原则：


状态不放进程里，放 Session/Event Log 里

Harness 无状态，可随时 crash / reschedule

Sandbox 是执行器，不是 Agent 身份的一部分

Secrets 对模型和生成代码不可达

工具执行与人工审批都走事件流

Agent 与 Environment 都是可复用资源，Session 只是一次运行实例


这些原则并不是空想，而是 Anthropic 当前公开设计的核心：Session 是运行中的 agent 实例并维护历史；事件驱动实际执行；工具审批通过 session.status_idle + user.tool_confirmation 实现；凭证通过 vault 在创建 session 时绑定；环境是可复用模板而 session 拿到的是隔离容器实例。Anthropic+4Claude平台+4Claude平台+4



2. 系统架构图


undefined


这张图里，**Anthropic 已经公开的“硬抽象”**只有 4+3 个：Agent、Environment、Session、Events，以及工程文里的 Session、Harness、Sandbox。其余如 Policy Registry、Artifact Store、Usage Ledger、Approval Service、Scheduler/Recovery，是我建议你自建时补上的“生产级必需件”。Anthropic 官方也已经公开了 permission policies、vaults、skills、event stream 和 custom tools / MCP tools 的区分，所以这套扩展是顺着它的公开接口自然长出来的。Claude平台+7Anthropic+7Claude平台+7



3. 运行时主流程


建议你把整个系统固定成下面这条 canonical flow：


A. 定义资源


先创建：


Agent

Environment

Policy

Vault

Skill bindings


官方语义里，Agent 是可复用、带版本的配置对象，包含 model、system、tools、mcp_servers、skills；Environment 是复用型容器模板；Vault 是按 end-user 绑定的一组 credentials；Skills 是按需加载的领域能力。Claude平台+3Claude平台+3Claude平台+3


B. 启动 Session


Session 只绑定资源，不自动开工；真正工作要靠往 session 发 user events。官方文档明确写了：创建 session 只 provision agent + environment，本身不开始任何任务；任务由事件驱动，会话像一个状态机。Claude平台


C. Harness 被唤醒


Harness Worker 做三件事：


读取 session 当前状态

从 event log 组装 working context

调用模型决定下一步动作


这里最关键的是：Session Log 是 source of truth，Context Window 只是 working set。 这是 Anthropic 工程文最重要的启发。Anthropic


D. 动作执行


模型输出可能是：


agent.message

agent.tool_use

agent.mcp_tool_use

agent.custom_tool_use

子 agent 调用


官方事件流和权限流已经把其中最关键的阻塞点定义好了：如果某个工具策略是 always_ask，session 会进入 session.status_idle 并等待 user.tool_confirmation；如果是 custom tool，则由你的应用执行并通过 user.custom_tool_result 把结果送回去。Claude平台+2Claude平台+2


E. 回写与恢复


所有动作都回写到 event store；harness 崩了就从 session 恢复；sandbox 崩了就表现成一次 tool failure。Anthropic 工程文明确把这套思路描述为把 pet 变 cattle，让 harness 和 sandbox 都能独立更换。Anthropic



4. 数据模型：先做 8 张 MVP 核心表


如果从 0 到 1，我建议先只做下面 8 张表。这样最小可用，而且足以支撑 versioning、事件流、审批、恢复和审计。


4.1 agents


保存逻辑上的 Agent 身份。


create table agents (
  id                varchar(40) primary key,
  tenant_id         varchar(40) not null,
  name              varchar(255) not null,
  description       text,
  status            varchar(20) not null default 'active', -- active/archived
  current_version   integer not null,
  created_at        timestamptz not null,
  updated_at        timestamptz not null,
  archived_at       timestamptz
);


这样拆的原因是：Anthropic 的 Agent 是可复用、带版本的资源，更新会生成新版本，归档后只读、已有 session 继续跑。Claude平台


4.2 agent_versions


保存每个 Agent 的不可变快照。


create table agent_versions (
  agent_id                varchar(40) not null,
  version                 integer not null,
  model_id                varchar(100) not null,
  model_speed             varchar(20) not null default 'standard',
  system_prompt           text,
  tools_json              jsonb not null default '[]',
  mcp_servers_json        jsonb not null default '[]',
  skills_json             jsonb not null default '[]',
  callable_agents_json    jsonb not null default '[]',
  metadata_json           jsonb not null default '{}',
  created_at              timestamptz not null,
  created_by              varchar(40),
  primary key (agent_id, version)
);


这是最该一开始就做对的表，因为官方 Agent update 语义本身就是 versioned，而且数组字段会整体替换。Claude平台


4.3 environments


保存逻辑上的 Environment 身份。


create table environments (
  id                varchar(40) primary key,
  tenant_id         varchar(40) not null,
  name              varchar(255) not null,
  status            varchar(20) not null default 'active',
  current_revision  integer not null,
  created_at        timestamptz not null,
  updated_at        timestamptz not null,
  archived_at       timestamptz,
  unique (tenant_id, name)
);


这里我故意和 Anthropic 不一样。 Anthropic 官方 Environment 是复用资源，但不版本化，文档还建议如果经常改环境，最好自己记录更新历史；所以自建时最稳妥的做法是自己补一层 revision。Claude平台


4.4 environment_revisions


保存环境的不可变快照。


create table environment_revisions (
  environment_id         varchar(40) not null,
  revision               integer not null,
  runtime_type           varchar(20) not null default 'cloud',
  packages_json          jsonb not null default '{}',
  networking_json        jsonb not null default '{}',
  filesystem_profile     jsonb not null default '{}',
  created_at             timestamptz not null,
  created_by             varchar(40),
  primary key (environment_id, revision)
);


Networking 至少要支持：


unrestricted

limited

allowed_hosts

allow_mcp_servers

allow_package_managers


这与官方 Environment networking 设计一致，而且官方明确建议生产用 limited + 明确 allowlist。Claude平台


4.5 sessions


保存每次运行实例。


create table sessions (
  id                         varchar(40) primary key,
  tenant_id                  varchar(40) not null,
  agent_id                   varchar(40) not null,
  agent_version              integer not null,
  environment_id             varchar(40) not null,
  environment_revision       integer not null,
  title                      varchar(255),
  status                     varchar(20) not null, -- idle/running/rescheduling/terminated/archived
  stop_reason_json           jsonb,
  vault_refs_json            jsonb not null default '[]',
  policy_snapshot_json       jsonb not null default '{}',
  latest_event_seq           bigint not null default 0,
  created_at                 timestamptz not null,
  updated_at                 timestamptz not null,
  archived_at                timestamptz
);


Session 至少要能记录：


绑定哪个 Agent 版本

绑定哪个 Environment 修订版

当前状态

当前 stop reason

引用了哪些 vault


官方状态机里明确公开了 idle、running、rescheduling、terminated。Claude平台


4.6 session_events


这是全系统最重要的表。


create table session_events (
  session_id             varchar(40) not null,
  seq                    bigint not null,
  event_id               varchar(40) not null,
  direction              varchar(10) not null, -- user/agent/session/span/system
  event_type             varchar(80) not null,
  actor_type             varchar(40) not null, -- user/agent/harness/tool/system
  actor_id               varchar(40),
  payload_json           jsonb not null,
  causal_event_id        varchar(40),
  idempotency_key        varchar(100),
  processed_at           timestamptz,
  created_at             timestamptz not null,
  primary key (session_id, seq),
  unique (event_id)
);
create index idx_session_events_type on session_events(session_id, event_type);
create index idx_session_events_causal on session_events(session_id, causal_event_id);


官方已经把事件模型定义得很清楚：有 user events、agent events、session events、span events，事件名遵循 {domain}.{action}，并且每条事件都有 processed_at。Claude平台


4.7 tool_executions


把工具调用单独拉出来，便于审计、超时、重试和成本分析。


create table tool_executions (
  id                     varchar(40) primary key,
  session_id             varchar(40) not null,
  tool_use_event_id      varchar(40) not null,
  tool_domain            varchar(20) not null, -- agent/mcp/custom/subagent
  tool_name              varchar(100) not null,
  risk_level             varchar(20) not null default 'normal',
  permission_policy      varchar(20), -- always_allow/always_ask/null
  input_json             jsonb not null,
  output_json            jsonb,
  status                 varchar(20) not null, -- pending/running/succeeded/failed/denied
  executor_ref           varchar(100),
  started_at             timestamptz,
  finished_at            timestamptz,
  error_code             varchar(50),
  error_message          text
);


官方区分了：


server-executed tools：agent toolset / MCP toolset

application-executed tools：custom tools


这两类在运行与治理上必须分开建模。Claude平台+1


4.8 approvals


专门记录人工确认。


create table approvals (
  id                     varchar(40) primary key,
  session_id             varchar(40) not null,
  blocking_event_id      varchar(40) not null,
  tool_execution_id      varchar(40),
  status                 varchar(20) not null, -- pending/allowed/denied/expired
  requested_at           timestamptz not null,
  resolved_at            timestamptz,
  resolver_id            varchar(40),
  deny_message           text
);


之所以单独建表，是因为官方的审批流本质上是阻塞事件：先发 agent.tool_use 或 agent.mcp_tool_use，再进入 session.status_idle(stop_reason=requires_action)，然后由 user.tool_confirmation 解锁。Claude平台



5. 二期再补 4 张推荐表


5.1 vaults


create table vaults (
  id                varchar(40) primary key,
  tenant_id         varchar(40) not null,
  display_name      varchar(255) not null,
  metadata_json     jsonb not null default '{}',
  status            varchar(20) not null default 'active',
  created_at        timestamptz not null,
  updated_at        timestamptz not null,
  archived_at       timestamptz
);


5.2 vault_credentials


create table vault_credentials (
  id                    varchar(40) primary key,
  vault_id              varchar(40) not null,
  mcp_server_url        text not null,
  auth_type             varchar(30) not null, -- mcp_oauth/static_bearer
  secret_ref            varchar(100) not null, -- pointer to KMS/HSM/secret manager
  public_metadata_json  jsonb not null default '{}',
  status                varchar(20) not null default 'active',
  expires_at            timestamptz,
  created_at            timestamptz not null,
  updated_at            timestamptz not null,
  archived_at           timestamptz,
  unique (vault_id, mcp_server_url, status)
);


官方 Vault 模型的关键点是：vault 是 per-user credential collection；credential 绑定单个 mcp_server_url；密钥字段 write-only；session 创建时只传 vault_ids。Claude平台+2Claude平台+2


5.3 artifacts


create table artifacts (
  id                   varchar(40) primary key,
  session_id           varchar(40) not null,
  producing_event_id   varchar(40),
  kind                 varchar(30) not null, -- file/report/diff/image/table/archive
  uri                  text not null,
  mime_type            varchar(100),
  size_bytes           bigint,
  checksum             varchar(128),
  metadata_json        jsonb not null default '{}',
  created_at           timestamptz not null
);


5.4 usage_ledger


create table usage_ledger (
  id                   varchar(40) primary key,
  session_id           varchar(40) not null,
  event_id             varchar(40),
  metric_type          varchar(40) not null, -- input_tokens/output_tokens/cache_read/cache_write/tool_seconds
  amount               numeric(20,4) not null,
  unit                 varchar(20) not null,
  created_at           timestamptz not null
);


Anthropic 官方 overview 里已经明确提到 harness 内置 prompt caching、compaction 等优化；所以你的运行时从第一天就应该有 usage ledger，而不是事后补。Claude平台



6. API 设计草案


我建议 API 只公开三类资源：


控制面资源：Agent / Environment / Policy / Vault

运行面资源：Session / Event / Artifact

治理面资源：Approval / Audit / Usage


而且最外层统一走事件驱动。因为一旦做成长时任务、审批、custom tool、恢复和中断，你最后一定会收敛到 event API。官方 Managed Agents 也是这样设计的。Claude平台+1



6.1 Agent API


创建 Agent


POST /v1/agents
Idempotency-Key: agt-create-001


{
  "name": "Coding Assistant",
  "model": {"id": "claude-sonnet-4-6", "speed": "standard"},
  "system": "You are a helpful coding agent.",
  "tools": [
    {
      "type": "agent_toolset_20260401",
      "default_config": {
        "permission_policy": {"type": "always_allow"}
      },
      "configs": [
        {"name": "bash", "enabled": true}
      ]
    }
  ],
  "mcp_servers": [],
  "skills": [],
  "metadata": {"team": "platform"}
}


更新 Agent


POST /v1/agents/{agent_id}/versions


{
  "base_version": 3,
  "patch": {
    "system": "You are a helpful coding agent. Always write tests."
  }
}


这里我建议不要直接 PATCH /agents/{id}，而是显式生成新版本。因为 Anthropic 官方语义就是 update 生成新 version，而且 session 可以 pin 到具体版本。Claude平台+1



6.2 Environment API


创建 Environment


POST /v1/environments


{
  "name": "python-dev",
  "config": {
    "type": "cloud",
    "packages": {
      "pip": ["pandas==2.2.0", "numpy"],
      "npm": ["express"]
    },
    "networking": {
      "type": "limited",
      "allowed_hosts": ["https://api.example.com"],
      "allow_mcp_servers": true,
      "allow_package_managers": true
    }
  }
}


官方公开了 packages 与 networking 的配置语义，而且建议生产环境使用 limited networking。Claude平台



6.3 Vault API


创建 Vault


POST /v1/vaults


{
  "display_name": "Alice",
  "metadata": {
    "external_user_id": "usr_abc123"
  }
}


添加 Credential


POST /v1/vaults/{vault_id}/credentials


{
  "mcp_server_url": "https://mcp.github.example.com",
  "auth": {
    "type": "static_bearer",
    "token": "SECRET_ONLY_WRITE"
  }
}


这部分最好只返回 public metadata，不回 secret material。官方 vault credential 的 secret fields 明确是 write-only。Claude平台+1



6.4 Session API


创建 Session


POST /v1/sessions
Idempotency-Key: sess-create-001


{
  "agent": {"id": "agent_123", "version": 4},
  "environment": {"id": "env_123", "revision": 7},
  "vault_ids": ["vlt_abc"],
  "title": "Refactor billing service",
  "policy_overrides": {
    "bash": {"permission_policy": {"type": "always_ask"}}
  }
}


官方 API 里 session 至少要绑定 agent + environment，并支持在创建时传 vault_ids。Claude平台


获取 Session


GET /v1/sessions/{session_id}


返回：


{
  "id": "sess_123",
  "status": "idle",
  "latest_event_seq": 42,
  "stop_reason": null
}



6.5 Event API（最关键）


发送用户消息


POST /v1/sessions/{session_id}/events
Idempotency-Key: evt-001


{
  "events": [
    {
      "type": "user.message",
      "content": [
        {"type": "text", "text": "List the files in the working directory."}
      ]
    }
  ]
}


发送 custom tool 结果


{
  "events": [
    {
      "type": "user.custom_tool_result",
      "custom_tool_use_id": "evt_tool_001",
      "content": [
        {"type": "text", "text": "{\"ok\": true, \"rows\": 128}"}
      ]
    }
  ]
}


发送工具确认


{
  "events": [
    {
      "type": "user.tool_confirmation",
      "tool_use_id": "evt_tool_002",
      "result": "allow"
    }
  ]
}


Anthropic 官方事件流已经把这三个交互模式定义出来了：普通 user event、custom tool result、tool confirmation。Claude平台+1


流式消费事件


GET /v1/sessions/{session_id}/events/stream
Accept: text/event-stream


返回 SSE：


event: agent.message
data: {...}

event: agent.tool_use
data: {...}

event: session.status_idle
data: {...}


官方就是通过 SSE 持续把 agent / session / span 事件流回来。Claude平台+1



6.6 Approval API


虽然也可以全走 event API，但内部系统最好再加一层审批资源，便于后台管理。


查询待审批项


GET /v1/approvals?status=pending&session_id=sess_123


批准


POST /v1/approvals/{approval_id}/allow


拒绝


POST /v1/approvals/{approval_id}/deny


然后系统内部自动翻译成 user.tool_confirmation 事件。这样前台不需要直接拼 event payload，但底层仍保持事件一致性。



7. 事件命名规范


我建议直接采用和官方一致的 {domain}.{action} 约定，再扩展你自己的系统域。官方文档已经公开这种命名习惯。Claude平台


推荐保留这些事件：


用户侧


user.message

user.tool_confirmation

user.custom_tool_result

user.interrupt


Agent 侧


agent.message

agent.tool_use

agent.mcp_tool_use

agent.custom_tool_use


Session 侧


session.status_running

session.status_idle

session.status_rescheduling

session.status_terminated


Span 侧


span.started

span.completed

span.failed


系统侧（你自建补充）


system.artifact_created

system.usage_recorded

system.approval_requested

system.approval_resolved



8. 从第一天就必须做的 5 个工程约束


1. 每个 POST 都支持 Idempotency-Key


否则重试会制造重复 session、重复 event、重复工具执行。
这是我自己的建议，但和 event-sourced runtime 高度一致。


2. session_events 必须 append-only


不要更新旧事件，只追加补偿事件。
因为恢复、审计、回放都依赖不可变历史。Anthropic 的 session 定义本质上就是 append-only log。Anthropic


3. 工具执行要单独表


别把所有 tool result 都塞在 event payload 里。
否则后面做审批、SLA、失败分析会非常痛苦。


4. Environment 自己做 revision


因为官方 Environment 不版本化，但生产系统一定需要“本次 session 究竟跑在哪个环境快照上”这个问题的答案。Claude平台


5. Secrets 只存引用，不存明文


数据库里只保留 secret_ref，真正 secret 放 KMS / HSM / secret manager。
这与官方 vault 的 write-only secret 设计方向一致。Claude平台



9. 一句话收束


如果你问“从 0 到 1”最小应该做成什么样，我的答案是：


做成一个事件驱动的 Agent Runtime，而不是一段 while loop。


最小闭环就是：


Agent / AgentVersion

Environment / EnvironmentRevision

Session

SessionEvent

ToolExecution

Approval

Vault / VaultCredential

Artifact / UsageLedger


只要这 8+4 个对象立住，后面无论你接 Anthropic、OpenAI、内部模型，还是以后做 multi-agent、memory、eval、workflow DSL，架构都不会散。这个判断与 Anthropic 公开出来的资源模型和工程分层是同方向的：稳定接口层比当前一代 harness 更重要。Anthropic+2Claude平台+2


下一条我可以直接继续给你一版 “Postgres DDL + OpenAPI YAML + 事件流时序图”。



Sources:


Scaling Managed Agents: Decoupling the brain from the hands

Start a session - Claude API Docs
