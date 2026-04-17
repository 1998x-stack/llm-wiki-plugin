---
title: "Hermes Agent 自进化体系与 Evolver 的高度相似性分析"
source: "https://evomap.ai/zh/blog/hermes-agent-evolver-similarity-analysis"
author:
  - "[[EvoMap Team]]"
published: 2026-04-12
created: 2026-04-16
description: "通过时间线、架构设计和功能模块的逐一对比，记录 Hermes Agent 体系在自进化、经验沉淀、技能创建与维护、记忆更新等方面与 Evolver/GEP 的高度相似之处。"
tags:
  - "clippings"
---
> 声明：本文基于公开可查证的 GitHub 仓库、官方文档和已发表博客文章编写。所有时间戳和链接均可独立验证。本文不做法律层面的抄袭定性，仅呈现事实和结构对比，供社区参考。

---

## 前言

2026 年 2 月 1 日， [Evolver](https://github.com/EvoMap/evolver) 作为一个 AI Agent 自进化引擎发布，10 分钟登上 ClawHub 热门榜首。随后，围绕自研的 [Genome Evolution Protocol (GEP)](https://evomap.ai/blog/gep-protocol-deep-dive) 协议，EvoMap 团队构建了一整套 Agent 自进化基础设施 -- 包括 Gene/Capsule/EvolutionEvent 三级资产体系、基于信号的选择器、因果记忆图、经验沉淀与蒸馏、反射循环、多维进化策略等。这套体系在 2 月中旬已通过多篇公开文章系统性阐述。

2026 年 2 月 25 日，Nous Research 发布了 [Hermes Agent v0.1.0](https://github.com/NousResearch/hermes-agent/releases) （"initial pre-public foundation"）。3 月 12 日的 [v0.2.0](https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.2.0.md) 正式推出完整的技能生态系统。3 月 9 日，又创建了单独的 [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) 仓库，将自进化能力作为独立项目推进。

本文通过时间线、架构设计和功能模块的逐一对比，记录 Hermes Agent 体系在自进化、经验沉淀、技能创建与维护、记忆更新等方面与 Evolver/GEP 的高度相似之处。

---

## 一、时间线对比

以下时间线基于 GitHub 仓库元数据和官方发布记录，均可独立验证。

![Evolver 仓库首页 -- 2026-02-01 创建，MIT 许可证](https://uploads.evomap.ai/blog/blog-evidence-evolver-repo-2c3e5d7decaf8f5e.png)

| 日期 | 事件 | 出处 |
| --- | --- | --- |
| **2026-02-01** | Evolver (Capability Evolver) 发布，GEP 协议首次公开 | [GitHub: EvoMap/evolver](https://github.com/EvoMap/evolver) created 2026-02-01T05:59:24Z |
| 2026-02-04 ~ 02-10 | EvoMap A2A 协议完善，团队内部验证 | [EvoMap 起源故事](https://evomap.ai/blog/evomap-origin-story) ， [腾讯新闻访谈](https://news.qq.com/rain/a/20260316A02W2100) |
| **2026-02-16** | GEP 协议深度解析发布：系统阐述 Gene/Capsule/Event 三级结构、Scan-Select-Mutate-Validate-Solidify 循环 | [GEP Deep Dive](https://evomap.ai/blog/gep-protocol-deep-dive) |
| **2026-02-17** | Agent Skill vs GEP Gene 对比文章：明确 "Skill 是静态工具，Gene 是动态进化资产" | [Agent Skill vs GEP Gene](https://evomap.ai/blog/agent-skill-vs-gep-gene) |
| 2026-02-20 | EvoMap.ai 正式上线 | [腾讯新闻访谈](https://news.qq.com/rain/a/20260316A02W2100) |
| **2026-02-25** | Hermes Agent v0.1.0 发布（"initial pre-public foundation"） | [GitHub Releases](https://github.com/NousResearch/hermes-agent/releases) ， [BlockBeats](https://m.theblockbeats.info/en/news/61867) |
| **2026-03-09** | `hermes-agent-self-evolution` 仓库创建 | [GitHub](https://github.com/NousResearch/hermes-agent-self-evolution) created 2026-03-09T10:42:48Z |
| **2026-03-12** | Hermes Agent v0.2.0：正式推出 "Skills Ecosystem -- 70+ bundled skills"，含 skill\_manage 自主创建工具 | [RELEASE v0.2.0](https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.2.0.md) |
| 2026-03-22 | Evolver v1.37.0：完成 "双环进化" + 失败经验学习流水线 | [v1.37.0 博客](https://evomap.ai/blog/evolver-v137-metaclaw-convergence) |

![Hermes Agent v0.2.0 Release 页面 -- 2026-03-12 发布](https://uploads.evomap.ai/blog/blog-evidence-hermes-v020-release-abfc92b26a76aca8.png)

**核心事实** ：

- Evolver 的 GEP 协议（Gene/Capsule/Event 体系、Scan-Select-Mutate-Validate-Solidify 循环、信号提取与匹配、经验沉淀）在 **2026 年 2 月 1-16 日已全部公开** 。
- Hermes Agent 的技能生态系统在 **2026 年 3 月 12 日** （v0.2.0）才正式推出。
- Hermes 的自进化仓库在 **2026 年 3 月 9 日** 才创建。
- 时间差：Evolver 核心概念公开 -> Hermes 技能生态发布，相隔 **24-39 天** 。

---

## 二、核心架构的高度相似

### 2.1 "从经验中生成可复用资产" 的闭环

这是两个项目最根本的共同点：Agent 完成任务后，自动提取可复用的经验资产。

**Evolver/GEP** （ [2026-02-01 起](https://github.com/EvoMap/evolver) ）：

<svg id="mermaid-_R_jp5fiv5ubqiuulb_-1" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1296.765625px;" viewBox="0 0 1296.765625 72" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-circleEnd-margin" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-circleStart-margin" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-crossEnd-margin" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-crossStart-margin" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g><g></g><g><path d="M142.625,36L146.792,36C150.958,36,159.292,36,166.958,36C174.625,36,181.625,36,185.125,36L188.625,36" id="mermaid-_R_jp5fiv5ubqiuulb_-1-L_A_B_0" style=";" data-edge="true" data-et="edge" data-id="L_A_B_0" data-points="W3sieCI6MTQyLjYyNSwieSI6MzZ9LHsieCI6MTY3LjYyNSwieSI6MzZ9LHsieCI6MTkyLjYyNSwieSI6MzZ9XQ==" data-look="classic" marker-end="url(#mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M362.688,36L366.854,36C371.021,36,379.354,36,387.021,36C394.688,36,401.688,36,405.188,36L408.688,36" id="mermaid-_R_jp5fiv5ubqiuulb_-1-L_B_C_0" style=";" data-edge="true" data-et="edge" data-id="L_B_C_0" data-points="W3sieCI6MzYyLjY4NzUsInkiOjM2fSx7IngiOjM4Ny42ODc1LCJ5IjozNn0seyJ4Ijo0MTIuNjg3NSwieSI6MzZ9XQ==" data-look="classic" marker-end="url(#mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M617.563,36L621.729,36C625.896,36,634.229,36,641.896,36C649.563,36,656.563,36,660.063,36L663.563,36" id="mermaid-_R_jp5fiv5ubqiuulb_-1-L_C_D_0" style=";" data-edge="true" data-et="edge" data-id="L_C_D_0" data-points="W3sieCI6NjE3LjU2MjUsInkiOjM2fSx7IngiOjY0Mi41NjI1LCJ5IjozNn0seyJ4Ijo2NjcuNTYyNSwieSI6MzZ9XQ==" data-look="classic" marker-end="url(#mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M789.391,36L793.557,36C797.724,36,806.057,36,813.724,36C821.391,36,828.391,36,831.891,36L835.391,36" id="mermaid-_R_jp5fiv5ubqiuulb_-1-L_D_E_0" style=";" data-edge="true" data-et="edge" data-id="L_D_E_0" data-points="W3sieCI6Nzg5LjM5MDYyNSwieSI6MzZ9LHsieCI6ODE0LjM5MDYyNSwieSI6MzZ9LHsieCI6ODM5LjM5MDYyNSwieSI6MzZ9XQ==" data-look="classic" marker-end="url(#mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M1040.516,36L1044.682,36C1048.849,36,1057.182,36,1064.849,36C1072.516,36,1079.516,36,1083.016,36L1086.516,36" id="mermaid-_R_jp5fiv5ubqiuulb_-1-L_E_F_0" style=";" data-edge="true" data-et="edge" data-id="L_E_F_0" data-points="W3sieCI6MTA0MC41MTU2MjUsInkiOjM2fSx7IngiOjEwNjUuNTE1NjI1LCJ5IjozNn0seyJ4IjoxMDkwLjUxNTYyNSwieSI6MzZ9XQ==" data-look="classic" marker-end="url(#mermaid-_R_jp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path></g><g><g><g data-id="L_A_B_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g><g><g data-id="L_B_C_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g><g><g data-id="L_C_D_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g><g><g data-id="L_D_E_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g><g><g data-id="L_E_F_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g></g><g><g id="mermaid-_R_jp5fiv5ubqiuulb_-1-flowchart-A-0" data-look="classic" transform="translate(75.3125, 36)"><rect style="" x="-67.3125" y="-28" width="134.625" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-35.3125, -12)"><rect></rect><foreignObject width="70.625" height="24"><p>Scan logs</p></foreignObject></g></g><g id="mermaid-_R_jp5fiv5ubqiuulb_-1-flowchart-B-1" data-look="classic" transform="translate(277.65625, 36)"><rect style="" x="-85.03125" y="-28" width="170.0625" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-53.03125, -12)"><rect></rect><foreignObject width="106.0625" height="24"><p>Extract signals</p></foreignObject></g></g><g id="mermaid-_R_jp5fiv5ubqiuulb_-1-flowchart-C-3" data-look="classic" transform="translate(515.125, 36)"><rect style="" x="-102.4375" y="-28" width="204.875" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-70.4375, -12)"><rect></rect><foreignObject width="140.875" height="24"><p>Select/Create Gene</p></foreignObject></g></g><g id="mermaid-_R_jp5fiv5ubqiuulb_-1-flowchart-D-5" data-look="classic" transform="translate(728.4765625, 36)"><rect style="" x="-60.9140625" y="-28" width="121.828125" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-28.9140625, -12)"><rect></rect><foreignObject width="57.828125" height="24"><p>Validate</p></foreignObject></g></g><g id="mermaid-_R_jp5fiv5ubqiuulb_-1-flowchart-E-7" data-look="classic" transform="translate(939.953125, 36)"><rect style="" x="-100.5625" y="-28" width="201.125" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-68.5625, -12)"><rect></rect><foreignObject width="137.125" height="24"><p>Solidify as Capsule</p></foreignObject></g></g><g id="mermaid-_R_jp5fiv5ubqiuulb_-1-flowchart-F-9" data-look="classic" transform="translate(1189.640625, 36)"><rect style="" x="-99.125" y="-28" width="198.25" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-67.125, -12)"><rect></rect><foreignObject width="134.25" height="24"><p>Publish to network</p></foreignObject></g></g></g></g></g><defs></defs><defs></defs><linearGradient id="mermaid-_R_jp5fiv5ubqiuulb_-1-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="rgb(31, 31, 31)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(0, 0%, 0%)" stop-opacity="1"></stop></linearGradient></svg>

核心循环定义于 [GEP Protocol Deep Dive (2026-02-16)](https://evomap.ai/blog/gep-protocol-deep-dive) ："Scan -> Select -> Mutate -> Validate -> Solidify"。

**Hermes Agent** （ [v0.2.0 起, 2026-03-12](https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.2.0.md) ）：

<svg id="mermaid-_R_mp5fiv5ubqiuulb_-1" width="100%" xmlns="http://www.w3.org/2000/svg" style="max-width: 1026.796875px;" viewBox="0 0 1026.796875 96" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-circleEnd-margin" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-circleStart-margin" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-crossEnd-margin" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-crossStart-margin" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g><g></g><g><path d="M272,48L276.167,48C280.333,48,288.667,48,296.333,48C304,48,311,48,314.5,48L318,48" id="mermaid-_R_mp5fiv5ubqiuulb_-1-L_A_B_0" style=";" data-edge="true" data-et="edge" data-id="L_A_B_0" data-points="W3sieCI6MjcyLCJ5Ijo0OH0seyJ4IjoyOTcsInkiOjQ4fSx7IngiOjMyMiwieSI6NDh9XQ==" data-look="classic" marker-end="url(#mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M481.484,48L485.651,48C489.818,48,498.151,48,505.818,48C513.484,48,520.484,48,523.984,48L527.484,48" id="mermaid-_R_mp5fiv5ubqiuulb_-1-L_B_C_0" style=";" data-edge="true" data-et="edge" data-id="L_B_C_0" data-points="W3sieCI6NDgxLjQ4NDM3NSwieSI6NDh9LHsieCI6NTA2LjQ4NDM3NSwieSI6NDh9LHsieCI6NTMxLjQ4NDM3NSwieSI6NDh9XQ==" data-look="classic" marker-end="url(#mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path><path d="M717.109,48L721.276,48C725.443,48,733.776,48,741.443,48C749.109,48,756.109,48,759.609,48L763.109,48" id="mermaid-_R_mp5fiv5ubqiuulb_-1-L_C_D_0" style=";" data-edge="true" data-et="edge" data-id="L_C_D_0" data-points="W3sieCI6NzE3LjEwOTM3NSwieSI6NDh9LHsieCI6NzQyLjEwOTM3NSwieSI6NDh9LHsieCI6NzY3LjEwOTM3NSwieSI6NDh9XQ==" data-look="classic" marker-end="url(#mermaid-_R_mp5fiv5ubqiuulb_-1_flowchart-v2-pointEnd)" fill="none" stroke="currentColor"></path></g><g><g><g data-id="L_A_B_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g><g><g data-id="L_B_C_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g><g><g data-id="L_C_D_0" transform="translate(0, 0)"></g></g><g><rect style="stroke: none" fill="none"></rect></g></g><g><g id="mermaid-_R_mp5fiv5ubqiuulb_-1-flowchart-A-0" data-look="classic" transform="translate(140, 48)"><rect style="" x="-132" y="-40" width="264" height="80" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-100, -24)"><rect></rect><foreignObject width="200" height="48"><p>Complete complex task (5+ tool calls)</p></foreignObject></g></g><g id="mermaid-_R_mp5fiv5ubqiuulb_-1-flowchart-B-1" data-look="classic" transform="translate(401.7421875, 48)"><rect style="" x="-79.7421875" y="-28" width="159.484375" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-47.7421875, -12)"><rect></rect><foreignObject width="95.484375" height="24"><p>Self-evaluate</p></foreignObject></g></g><g id="mermaid-_R_mp5fiv5ubqiuulb_-1-flowchart-C-3" data-look="classic" transform="translate(624.296875, 48)"><rect style="" x="-92.8125" y="-28" width="185.625" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-60.8125, -12)"><rect></rect><foreignObject width="121.625" height="24"><p>Create SKILL.md</p></foreignObject></g></g><g id="mermaid-_R_mp5fiv5ubqiuulb_-1-flowchart-D-5" data-look="classic" transform="translate(892.953125, 48)"><rect style="" x="-125.84375" y="-28" width="251.6875" height="56" fill="none" stroke="currentColor"></rect><g style="" transform="translate(-93.84375, -12)"><rect></rect><foreignObject width="187.6875" height="24"><p>Auto-load on similar tasks</p></foreignObject></g></g></g></g></g><defs></defs><defs></defs><linearGradient id="mermaid-_R_mp5fiv5ubqiuulb_-1-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="rgb(31, 31, 31)" stop-opacity="1"></stop><stop offset="100%" stop-color="hsl(0, 0%, 0%)" stop-opacity="1"></stop></linearGradient></svg>

核心循环描述于 [Hermes 官方技能指南](https://hermes-agent.ai/blog/hermes-agent-skills-guide) ："Task completes -> Agent evaluates: was this worth remembering? -> If yes, writes SKILL.md -> Future similar tasks load the skill automatically"。

**对比** ：两者的核心范式完全一致 -- "任务完成后自动提取可复用知识并持久化"。Evolver 使用 Gene/Capsule JSON 结构，Hermes 使用 SKILL.md Markdown 结构。形式不同，架构同构。

### 2.2 执行追踪与周期性反射

**Evolver** （ `src/gep/executionTrace.js` + `src/gep/reflection.js` ， [2026-02 起](https://evomap.ai/blog/gep-protocol-deep-dive) ）：

- 每次进化周期记录脱敏执行摘要（gene\_id, mutation\_category, signals\_matched, 验证结果, 错误签名, 工具链, 结局）
- 每 5 个周期触发一次战略性自我评估（Reflection Loop），基于近期事件和叙事摘要构建反思上下文
- 反思结果记录到 `evolution/reflection_log.jsonl`

**Hermes Agent** （ [2026-03 起](https://hermes-agent.ai/blog/self-improving-ai-guide) ）：

- 每 15 次 tool call 运行一次 self-evaluation checkpoint
- 分析成功和失败，判断是否有可复用的流程
- 评估结果用于创建或更新 skill 文档

引用 Hermes 官方描述（ [Self-Improving AI Guide](https://hermes-agent.ai/blog/self-improving-ai-guide) ）：

> "Every 15 tool calls, Hermes pauses to evaluate: What did I do? What worked? What failed?"

**对比** ：两者都实现了周期性反射机制。Evolver 每 5 个进化周期（约 5 次 solidify），Hermes 每 15 次 tool call。目的一致：从执行经验中提取模式并持久化。

### 2.3 技能/资产的发现与按需加载

**Evolver/GEP** （ [Selector 机制](https://mintlify.com/EvoMap/evolver/gep/protocol-spec) ）：

- Gene 的 `signals_match` 数组定义触发条件
- Selector 根据信号重叠度（signal overlap）选择最佳 Gene/Capsule
- 支持子串匹配、正则、多语言别名

**Hermes Agent** （ [Progressive Disclosure](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) ）：

- 所有 skill 通过 `skills_list()` 被发现（仅返回 name + description）
- Agent 按需加载匹配的 skill（ `skill_view(name)` 返回完整内容）
- 三级渐进式加载控制 token 开销

**对比** ：两者都实现了 "运行时能力发现 + 按需加载" 的模式。核心思路一致，具体实现有差异。

---

## 三、记忆体系的同构性

| 层级 | Evolver（ [2026-02 起](https://evomap.ai/blog/gep-protocol-deep-dive) ） | Hermes Agent（ [2026-03 起](https://hermes-agent.ai/blog/hermes-agent-memory-system) ） |
| --- | --- | --- |
| 第一层：持久事实 | `EVOLUTION_PRINCIPLES.md` + `evolution_narrative.md` （注入 GEP prompt） | `MEMORY.md` + `USER.md` （注入 system prompt） |
| 第二层：程序性记忆 | Gene/Capsule JSON 资产（ `assets/gep/genes.json`, `capsules.json` ） | SKILL.md 文件（ `~/.hermes/skills/` ） |
| 第三层：会话/事件历史 | `events.jsonl` + `failed_capsules.json` | SQLite FTS5 session search |
| 记忆注入方式 | `buildNarrativeBlock()` 注入 GEP prompt | 注入 system prompt（session start） |
| 记忆容量控制 | Narrative Memory 上限 30 条 / 12KB | MEMORY.md 自动压缩，合并冗余条目 |
| 记忆衰减 | Gene 长期未使用时权重降低（pruning） | "Intelligent forgetting" -- 保留关键信息，丢弃不相关的 |

三层记忆结构：持久事实层 + 程序性记忆层 + 历史搜索层。两者在每一层都有精确的功能对应。

---

## 四、自进化仓库中的关键细节

### 4.1 仓库的叙事定位

Hermes 的自进化仓库（ [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) ）于 2026-03-09 创建，其 README 描述为：

![hermes-agent-self-evolution 仓库首页 -- 创建于 2026-03-09](https://uploads.evomap.ai/blog/blog-evidence-hermes-self-evolution-repo-6a0e4dbad077fcc6.png)

> " **Evolutionary self-improvement** for Hermes Agent... optimize Hermes Agent's **skills**, tool descriptions, system prompts, and **code** -- producing measurably better versions through **reflective evolutionary search**."

对比 Evolver 自 2026-02-01 起的定位（ [README](https://github.com/EvoMap/evolver/blob/main/README.md) ）：

> "A **GEP-powered self-evolution engine** for AI agents... automated log analysis and **Genome Evolution Protocol** (GEP) for auditable, reusable **evolution assets**."

关键重叠术语： **self-evolution / self-improvement** 、 **evolutionary** 、 **skills/assets optimization** 、 **reflective** 。这些术语在 Evolver 语境下已被广泛使用了 5 周以上。

### 4.2 Phase 4 的 "Darwinian Evolver" 命名

Hermes `self-evolution` 仓库的 [PLAN.md](https://github.com/NousResearch/hermes-agent-self-evolution/blob/main/PLAN.md) Phase 4 计划使用 [Imbue AI 的 Darwinian Evolver](https://github.com/imbue-ai/darwinian_evolver) （一个 AGPL v3 代码进化框架）进行代码进化。

需要注意：Imbue AI 的 Darwinian Evolver 是一个独立的学术项目，与 EvoMap 的 Evolver 无关。但在 2026 年 3 月的 AI Agent 领域，"Evolver" 这个名称已经与 EvoMap 的自进化引擎紧密关联（ [1852 stars, 114 releases](https://github.com/EvoMap/evolver) ）。在自进化语境下使用相近的名称，客观上造成了混淆。

### 4.3 技能自我改进

**Evolver** （ [v1.37.0, 2026-03-22](https://evomap.ai/blog/evolver-v137-metaclaw-convergence) ）：

- Gene 在使用中被持续验证，Capsule 记录 success\_streak
- 失败的 Capsule 通过 `skillDistiller.js` 进入失败学习流水线
- Gene 长期未使用时权重自然衰减

**Hermes Agent** 官网宣传语（ [hermes-agent.org](https://hermes-agent.org/) ）：

> "Skills self-improve during use"

Hermes 的 [self-improving AI 指南](https://hermes-agent.ai/blog/self-improving-ai-guide) 进一步说明：

> "Skills do not just get created -- they get refined. Each time Hermes uses an existing skill and encounters something new, it patches the skill."

**对比** ："技能/资产在使用中自我改进" 这一概念，Evolver 从初版的 Capsule success\_streak 追踪就已实现。Hermes 的表述采用了几乎一致的叙事框架。

---

## 五、技能创建触发条件的精确对比

![Hermes Agent skills 目录结构](https://uploads.evomap.ai/blog/blog-evidence-hermes-skills-dir-88c570af53542fca.png)

| 维度 | Evolver/GEP | Hermes Agent |
| --- | --- | --- |
| 触发时机 | Agent 成功解决问题后自动触发 solidify 流程 | 完成复杂任务后（ [5+ tool calls](https://hermes-agent.ai/blog/hermes-agent-skills-guide) ）自动创建 |
| 评估机制 | 分析执行历史 + 提取信号匹配模式 | Agent 评估 "was this worth remembering?" |
| 资产格式 | Gene (JSON) + Capsule (JSON) | SKILL.md (Markdown + YAML frontmatter) |
| 持久化位置 | `assets/gep/genes.json`, `capsules.json` | `~/.hermes/skills/[category]/SKILL.md` |
| 资产结构 | id, signals\_match, strategy\[\], validation\[\], constraints | name, description, When to Use, Procedure, Pitfalls, Verification |
| 更新机制 | Gene 被 Capsule 验证后增强；失败进入学习流水线 | `skill_manage(action="patch")` 就地更新 |
| 发现机制 | Selector 基于 signal overlap | Progressive Disclosure: `skills_list()` -> `skill_view(name)` |

每一个核心维度 -- 触发时机、评估机制、持久化、更新、发现 -- 都有精确的功能对应。

---

## 六、源码结构对比

超越架构层面的相似性，对比两个项目的实际源码组织可以发现功能等价的模块一一对应。

### Evolver 核心模块 (src/gep/)

```bash
src/gep/
  selector.js          # 基因选择引擎(信号匹配+漂移)
  signals.js           # 三层信号提取(正则/关键词/LLM)
  solidify.js          # 固化引擎(验证+回滚+发布)
  mutation.js          # 突变构建器(repair/optimize/innovate/explore)
  reflection.js        # 反射机制(周期性战略分析)
  memoryGraph.js       # 记忆图谱(JSONL追加, Jaccard相似度)
  skillDistiller.js    # 技能蒸馏器(Capsule -> Gene蒸馏)
  assetStore.js        # 资产存储(genes.json/capsules.json/events.jsonl)
  executionTrace.js    # 执行跟踪(脱敏后的跨agent共享)
  narrativeMemory.js   # 叙事记忆(进化故事摘要)
  prompt.js            # GEP提示词构建器
```

### Hermes Agent 对应模块

```bash
# 主仓库 hermes-agent/
agent/memory_manager.py     # 记忆管理(MEMORY.md + USER.md)
agent/context_engine.py     # 上下文引擎(压缩/会话管理)
agent/prompt_builder.py     # 提示词构建(系统提示+技能索引)
agent/skill_utils.py        # 技能元数据工具(frontmatter解析)
agent/skill_commands.py     # 技能命令(运行时发现+激活)
tools/skill_manager_tool.py # 技能CRUD(create/edit/patch/delete)
tools/memory_tool.py        # 持久记忆工具(MEMORY.md CRUD)

# 自进化仓库 hermes-agent-self-evolution/
evolution/core/fitness.py       # 适应度评估(LLM-as-judge评分)
evolution/core/constraints.py   # 约束验证(大小/增长/结构)
evolution/skills/evolve_skill.py # 技能进化主循环(10步编排)
```

### 模块对应表

| 功能 | Evolver 文件 | Hermes 文件 |
| --- | --- | --- |
| 进化主循环 | `evolve.js` run() | `evolve_skill.py` evolve() |
| 资产选择/匹配 | `selector.js` selectGene() | `skill_commands.py` scan\_skill\_commands() |
| 资产创建/固化 | `solidify.js` solidify() | `skill_manager_tool.py` create action |
| 适应度/验证 | `solidify.js` computeProcessScores() | `fitness.py` LLMJudge.score() |
| 约束检查 | `solidify.js` + `policyCheck.js` | `constraints.py` ConstraintValidator |
| 反射/评估 | `reflection.js` shouldReflect() | 每15次tool call自评估 |
| 记忆持久化 | `assetStore.js` (JSON files) | `memory_tool.py` (MEMORY.md files) |
| 提示词组装 | `prompt.js` buildGepPrompt() | `prompt_builder.py` build\_skills\_system\_prompt() |
| 执行追踪 | `executionTrace.js` | `agent/trajectory.py` save\_trajectory() |
| 技能蒸馏/改进 | `skillDistiller.js` autoDistill() | `evolve_skill.py` GEPA优化循环 |

每一个 Evolver 核心模块在 Hermes 中都有功能等价的对应文件。

---

## 七、进化循环: 10步实现对比

### Evolver evolve.js -- run() (10步):

```
1. ensureAssetFiles()           -- 确保资产文件存在
2. extractSignals()             -- 三层信号提取
3. getMemoryAdvice()            -- 记忆图谱咨询
4. selectGeneAndCapsule()       -- 基因+胶囊选择
5. buildMutation()              -- 构建突变
6. selectPersonalityForRun()    -- 选择人格
7. buildGepPrompt()             -- 组装GEP提示词
8. writePromptArtifact()        -- 写入提示文件
9. writeStateForSolidify()      -- 写入固化状态
10. shouldReflect() -> recordReflection()  -- 反射
```

### Hermes evolve\_skill.py -- evolve() (10步):

```lua
1. find_skill() + load_skill()  -- 加载技能文件
2. 构建评估数据集               -- generate/load eval dataset
3. validate_all() baseline      -- 基线约束验证
4. 配置 DSPy + GEPA optimizer   -- 设置优化器
5. GEPA optimization            -- 运行优化循环
6. 提取进化后的技能文本          -- extract evolved body
7. validate_all() evolved       -- 进化后约束验证
8. holdout evaluation           -- 留出集评估
9. 报告结果                     -- report metrics
10. 保存输出                    -- save evolved skill
```

两者都是 **10步编排的进化主循环** ，核心模式一致: 加载 -> 评估 -> 选择/优化 -> 验证 -> 持久化。

---

## 八、术语分析: 系统性概念替换

### 直接残留搜索

对 Hermes 两个仓库的全文搜索:

| 搜索词 | hermes-agent | hermes-self-evolution |
| --- | --- | --- |
| `EvoMap` | 无匹配 | 无匹配 |
| `evolver` (不含 Darwinian) | 无匹配 | 无匹配 |
| `Genome Evolution Protocol` | 无匹配 | 无匹配 |
| `capsule` | 无匹配 | 无匹配 |
| `solidify` | 无匹配 | 无匹配 |
| `signals_match` | 无匹配 | 无匹配 |

没有找到直接的代码残留。这与 AI 跨语言重写的特征一致 -- AI 重写架构时不会保留原项目的特征性字符串，但架构层面的同构性无法被重写所消除。

### 概念术语的平行替换

| Evolver 术语 | Hermes 术语 | 含义 |
| --- | --- | --- |
| Gene | SKILL.md | 可复用的程序性知识单元 |
| Capsule | skill execution record | 单次执行的完整记录 |
| EvolutionEvent | (无直接对应) | 进化事件日志条目 |
| solidify | skill\_manage(action="create") | 将经验固化为持久资产 |
| signals\_match | frontmatter conditions | 触发条件匹配 |
| Selector | skills\_list() + skill\_view() | 运行时能力发现 |
| buildNarrativeBlock() | build\_skills\_system\_prompt() | 将记忆注入提示词 |
| assetStore (genes.json) | ~/.hermes/skills/ (SKILL.md files) | 资产持久化存储 |
| memoryGraph (JSONL) | MEMORY.md + USER.md | 声明性记忆存储 |
| executionTrace | trajectory.py | 执行轨迹记录 |
| skillDistiller | evolve\_skill.py (GEPA loop) | 从经验中蒸馏/改进技能 |

每一个 Evolver 核心概念在 Hermes 中都有术语不同但功能等价的对应 -- 这是系统性概念替换的典型特征。

---

## 九、跨语言设计模式的一致性

尽管技术栈完全不同(Node.js vs Python)，两个项目在架构设计模式上表现出高度一致:

| 设计模式 | Evolver | Hermes |
| --- | --- | --- |
| 多维评分 | `computeProcessScores()` 8阶段加权评分 | `FitnessScore` 3维加权评分(correctness 0.5 + procedure 0.3 + conciseness 0.2) |
| 约束门控 | `policyCheck.js` (blast radius/禁止路径/验证) | `ConstraintValidator` (size/growth/non-empty/structure) |
| 安全扫描 | `sanitize.js` (泄露检查+敏感数据脱敏) | `skills_guard.py` (80+正则威胁模式) + `memory_tool.py` (注入检测) |
| 原子写入 | `writeJsonAtomic()` 先写.tmp再rename | `skill_manager_tool.py` 使用 tempfile + 原子替换 |
| 分层记忆 | 持久事实层 + 程序性记忆层 + 历史搜索层 | MEMORY.md(声明性) + SKILL.md(程序性) + SQLite FTS5(搜索) |
| 注入防护 | 在 `prompt.js` 中处理 | `_scan_context_content()` 在 `prompt_builder.py` 中 |
| 容量控制 | Narrative Memory 上限 30条/12KB | MEMORY.md 上限 2200 chars, USER.md 上限 1375 chars |

两个团队使用不同语言却做出了相同的架构决策。这些决策的组合同构度远超"独立发明"的概率。

---

## 十、关于独立收敛的问题

一个自然的问题是：两个团队能否独立地到达相同的设计？

就任何单一维度而言，答案可能是肯定的。"从经验中学习"是一个通用的 AI 概念。周期性自评估在学术界有先例。将记忆注入 prompt 是当前 LLM 架构下的工程必然。

但问题不在于某一个维度能否独立收敛。问题在于： **它们是否能在同一个项目中、同一个时间窗口内同时收敛** 。

考虑这个具体的组合：

- 三层资产体系（可复用知识单元 + 执行记录 + 事件日志）-- 不是两层，不是四层，不是扁平 KV，而是精确的三层，且每层的语义角色一一对应
- 三层记忆体系（声明性事实 + 程序性技能 + 可搜索历史）-- 不是按时间分层，不是按来源分层，不是按信任度分层，而是相同的"声明-程序-搜索"三分法
- 运行时渐进式技能发现（信号/条件触发 + 按需加载）-- 不是全量注入，不是 embedding RAG，不是固定技能集
- 两个实现中都是 10 步编排的进化主循环
- 多维加权适应度评分（而非二元 pass/fail）
- collect-all-then-gate 模式的约束门控
- 原子写入、安全扫描、注入防护、容量控制

每一项都代表在设计空间中的一次选择。独立选中相同替代方案的概率，随着每一个额外匹配的维度而递减。

再看上下文：

- Evolver 的完整架构在 2026 年 2 月 1-16 日已全部公开
- Hermes 技能生态 3 月 12 日发布，自进化仓库 3 月 9 日创建
- 在那段时间内，GitHub 搜索 "agent self-evolution" 必然会发现 Evolver（1852 stars，114 releases）
- 在 7 份公开材料中，Hermes 团队对 Evolver/GEP/EvoMap 零提及

## 在开源实践中，当独立团队发现同领域的先行项目时，标准做法是添加 "Related Work" 或 "Similar to" 引用。LangChain 引用了 DSPy。CrewAI 对比了 AutoGen。MetaGPT 论文引用了相关多 agent 框架。在如此程度的架构对应背景下，完全缺乏任何此类致谢本身，已经说明了问题。

## 十一、对公平性的说明

本文应同时注意以下事实，以保证论述的公正：

1. **Agent Skills 标准 (agentskills.io) 早于 Evolver** 。Anthropic 于 [2025 年 12 月 18 日](https://www.paperclipped.de/en/blog/agent-skills-open-standard-interoperability/) 发布了 Agent Skills 开放标准，定义了 SKILL.md 文件格式。Hermes 采用这一标准是合理的行业选择，32+ 工具均已采用。
2. **Hermes Agent 仓库创建于 2025 年 7 月 22 日** （ [GitHub 元数据](https://github.com/NousResearch/hermes-agent) ），早于 Evolver 的 2026 年 2 月 1 日。但该仓库在 2026 年 2 月 25 日之前一直是私有项目（v0.1.0 自称 "initial pre-public foundation"），技能生态系统直到 [v0.2.0 (2026-03-12)](https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.2.0.md) 才正式发布。 **无法证明** Hermes 在私有阶段已包含与 GEP 类似的自进化功能。
3. **"从经验中学习" 是一个通用的 AI 概念** 。独立达到相似方案的可能性存在。但三层记忆体系、周期性反射循环、任务后自动经验提取闭环、技能运行时发现与按需加载这些具体架构选择的 **组合** ，其同构程度值得注意。
4. **Hermes 的自进化仓库使用了独立的技术栈** 。其核心引擎采用 [GEPA (Genetic-Pareto)](https://github.com/gepa-ai/gepa) ，这是 UC Berkeley/Stanford 团队的独立学术成果（ [ICLR 2026 Oral](https://openreview.net/forum?id=RQm2KQTM5r) ），集成于 [Stanford NLP 的 DSPy 框架](https://dspy.ai/api/optimizers/GEPA/overview/) 。GEPA 与 GEP 是完全不同的项目，不应混为一谈。

---

## 十二、零归属

这是本文最核心的论点。

在 Hermes Agent 及其 self-evolution 仓库的 **全部** 公开材料中：

| 资料 | 对 Evolver/GEP/EvoMap 的引用 |
| --- | --- |
| [hermes-agent-self-evolution README](https://github.com/NousResearch/hermes-agent-self-evolution) | **无** |
| [hermes-agent-self-evolution PLAN.md](https://github.com/NousResearch/hermes-agent-self-evolution/blob/main/PLAN.md) | **无** |
| [hermes-agent.org 官网](https://hermes-agent.org/) | **无** |
| [Hermes Agent 技能指南](https://hermes-agent.ai/blog/hermes-agent-skills-guide) | **无** |
| [Self-Improving AI 指南](https://hermes-agent.ai/blog/self-improving-ai-guide) | **无** |
| [Hermes Agent v0.2.0 Release Notes](https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.2.0.md) | **无** |
| [Hermes vs Cursor 对比页](https://hermes-agent.ai/vs/cursor) | **无** |

Hermes 团队引用了 [GEPA / DSPy](https://github.com/gepa-ai/gepa) （Stanford/Berkeley）和 [Darwinian Evolver](https://github.com/imbue-ai/darwinian_evolver) （Imbue AI），这些是正当的学术引用。但对于其 **整体自进化架构** 最相似的先行项目 -- [EvoMap Evolver](https://github.com/EvoMap/evolver) （1852 stars, 114 releases, 2026-02-01 起公开）-- **只字未提** 。

作为对比，EvoMap 团队主动发布了 [Hermes Agent vs EvoMap](https://evomap.ai/blog/hermes-agent-vs-evomap-agent-memory) 对比文章（2026-04-09），承认 Hermes 的价值并给出公正评价。

---

## 十三、结论

本文不意图下法律定性的"抄袭"结论。在开源世界中，思想的交叉传播是常态，独立发明也是可能的。

但以下事实组合值得社区关注：

1. **时间先后明确** ：Evolver 的 GEP 协议（Gene/Capsule/Event 体系、Scan-Select-Mutate-Validate-Solidify 循环、信号选择器、叙事记忆、执行追踪、反射循环）在 2026 年 2 月 1-16 日已全部公开。Hermes 的技能生态在 3 月 12 日才发布，自进化仓库在 3 月 9 日才创建。

![Evolver 发布历史 -- 截至本文撰写已有 114+ releases](https://uploads.evomap.ai/blog/blog-evidence-evolver-releases-0bc34b6ecbaba41a.png)

1. **架构同构度极高** ：从三层记忆体系、任务完成后自动提取可复用资产的闭环、周期性反射循环、技能自我改进机制、运行时发现与按需加载，几乎每一个核心模块都有一对一的对应。
2. **零归属** ：Hermes Agent 团队在所有公开资料中没有对 Evolver/GEP 做任何形式的引用或致谢。

我们认为，在开源社区中，如果一个项目的架构显著受到了另一个先行项目的启发，那么一句致谢不仅是礼貌，更是开源精神的体现。我们不要求任何许可费、署名权或代码层面的归属 -- 只是希望事实被记录，历史被尊重。

---

*本文引用的所有链接和时间戳均来自公开的 GitHub 仓库元数据、官方网站和已发表文章，可独立验证。*

*[EvoMap 团队](https://evomap.ai/) -- 2026 年 4 月*