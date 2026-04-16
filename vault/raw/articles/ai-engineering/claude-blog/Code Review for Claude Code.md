---
title: "Code Review for Claude Code"
source: "https://claude.com/blog/code-review"
author:
published: 2001-03-09
created: 2026-04-16
description: "Claude Code now dispatches a team of agents on every PR to catch bugs that skims miss. Available in research preview for Team and Enterprise."
tags:
  - "clippings"
---
Today we're introducing Code Review, which dispatches a team of agents on every PR to catch the bugs that skims miss, built for depth, not speed. It's the system we run on nearly every PR at Anthropic. Now in research preview for Team and Enterprise.今天我们推出了代码审查（Code Review）功能，该功能会为每个拉取请求（PR）派遣一组智能体，以找出常规快速扫描会遗漏的漏洞，它追求深度而非速度。这是我们在 Anthropic 几乎每个拉取请求上都采用的系统，目前面向团队版和企业版推出研究预览版。

![](https://www.youtube.com/watch?v=RKsADl0ZC3Y)

## Managing the review bottleneck 解决代码评审瓶颈

Code output per Anthropic engineer has grown 200% in the last year. Code review has become a bottleneck, and we hear the same from customers every week. They tell us developers are stretched thin, and many PRs get skims rather than deep reads.Anthropic 工程师的代码输出量在过去一年增长了200%。代码审核已成为一个瓶颈，我们每周都会从客户那里听到同样的反馈。他们表示开发人员人手紧张，许多代码合并请求（PR）都只是被快速浏览，而非深入审阅。

We needed a reviewer we could trust on every PR. Code Review is the result: deep, multi-agent reviews that catch bugs human reviewers often miss themselves. It's a more thorough (and more expensive) option than our existing [Claude Code GitHub Action](https://code.claude.com/docs/en/github-actions), which remains open source and available.我们需要一位在每个拉取请求（PR）上都值得信赖的审核者。代码审核（Code Review）由此诞生：它能进行深度的多智能体审核，捕捉人类审核者自身常常忽略的漏洞。这是比我们现有的 [Claude Code GitHub 操作](https://code.claude.com/docs/en/github-actions) 更全面（但成本也更高）的选择，而该操作仍保持开源且可正常使用。

We run Code Review on nearly every PR at Anthropic. Before, 16% of PRs got substantive review comments. Now 54% do. It won't approve PRs — that's still a human call — but it closes the gap so reviewers can actually cover what's shipping.在 Anthropic，我们几乎会对每一个拉取请求（PR）进行代码审查。此前，只有16%的拉取请求会收到实质性的审查意见，而现在这一比例达到了54%。我们不会直接批准拉取请求——这仍然需要人工判断——但这一改进缩小了审查范围，让审核人员能够真正覆盖即将上线的代码内容。

## How it works 它的工作原理

When a PR is opened, Code Review dispatches a team of agents. The agents look for bugs in parallel, verify bugs to filter out false positives, and rank bugs by severity. The result lands on the PR as a single high-signal overview comment, plus in-line comments for specific bugs.当拉取请求（PR）被创建时，代码审查系统会派遣一组智能体。这些智能体并行查找漏洞，验证漏洞以过滤误报，并按严重程度对漏洞进行排序。最终结果会以一条高价值的总览评论以及针对特定漏洞的行内评论的形式，呈现在拉取请求（PR）上。

Reviews scale with the PR. Large or complex changes get more agents and a deeper read; trivial ones get a lightweight pass. Based on our testing, the average review takes around 20 minutes.评审工作量与拉取请求（PR）的规模挂钩。大型或复杂的变更会安排更多评审人员并进行深入审核；琐碎的变更则只需快速通过。根据我们的测试，平均评审耗时约20分钟。

## Code Review in action 代码审核实战

We've been running Code Review internally for months: on large PRs (over 1,000 lines changed), 84% get findings, averaging 7.5 issues. On small PRs under 50 lines, that drops to 31%, averaging 0.5 issues. Engineers largely agree with what it surfaces: less than 1% of findings are marked incorrect.我们已经在内部运行代码审查数月了：对于大型拉取请求（更改超过1000行），84%会发现问题，平均有7.5个问题。而对于50行以下的小型拉取请求，这一比例降至31%，平均只有0.5个问题。工程师们对其发现的问题基本认可：只有不到1%的发现结果被标记为错误。

In one case, a one-line change to a production service looked routine and was the kind of diff that normally gets a quick approval. But Code Review flagged it as critical. The change would have broken authentication for the service, a failure mode that’s easy to read past in the diff but obvious once pointed out. It was fixed before merge, and the engineer shared afterwards that they wouldn't have caught it on their own.有一次，对生产服务的一行代码修改看似常规，也是那种通常能快速获得批准的代码差异。但代码审查将其标记为关键问题。这次修改本会导致该服务的身份验证功能失效，这种故障模式在代码差异中很容易被忽略，但一旦被指出就显而易见。该问题在合并前得到了修复，工程师事后表示，他们自己根本无法发现这个问题。

Early access customers have seen similar patterns. On a [ZFS encryption refactor in TrueNAS's open-source middleware](https://github.com/truenas/middleware/pull/18291), Code Review surfaced a pre-existing bug in adjacent code: a type mismatch that was silently wiping the encryption key cache on every sync. It was a latent issue in code the PR happened to touch, the kind of thing a human reviewer scanning the changeset wouldn't immediately go looking for.早期访问的客户也观察到了类似的情况。在TrueNAS开源中间件的 [ZFS加密重构](https://github.com/truenas/middleware/pull/18291) 工作中，代码审查发现了相邻代码中一个早已存在的漏洞：一种类型不匹配问题，该问题会在每次同步时静默清除加密密钥缓存。这是此次代码变更所涉及的代码中存在的潜在问题，也是人工审查者在浏览代码变更时不会立即去查找的那类问题。

## Cost and control 成本与管控

Code Review optimizes for depth and is more expensive than lighter-weight solutions like the [Claude Code GitHub Action](https://code.claude.com/docs/en/github-actions). Reviews are billed on token usage and generally average $15–25, scaling with PR size and complexity. 代码审查更注重深度，且比 [Claude Code GitHub 操作](https://code.claude.com/docs/en/github-actions) 这类轻量级解决方案的成本更高。审查费用按令牌使用量计费，通常平均费用在 15 至 25 美元之间，具体会根据拉取请求（PR）的规模和复杂程度浮动。

Admins have many ways to control spend and usage:管理员有多种方式控制支出和使用情况：

- **Monthly organization caps**: Define total monthly spend across all reviews **每月组织上限** ：定义所有审核的总月度支出
- **Repository-level control**: Enable reviews only on the repositories you choose **仓库级控制** ：仅在你选择的仓库上启用审核
- **Analytics dashboard**: Track PRs reviewed, acceptance rate, and total review costs **分析仪表板** ：跟踪已审核的拉取请求、接受率以及审核总成本

## Getting started 快速入门

Code Review is available now as a research preview in beta for Team and Enterprise plans. 代码审查目前作为研究预览版，已面向团队版和企业版开放测试。

- **For admins**: Enable Code Review in your [Claude Code settings](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2/admin-settings/claude-code), install the GitHub App, and select repositories you’d like to run reviews on.**管理员操作指南** ：在 [Claude Code 设置](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2/admin-settings/claude-code) 中启用代码审查，安装 GitHub 应用，并选择你希望运行审查的代码仓库。
- **For developers**: Once enabled, reviews run automatically on new PRs. No configuration needed.**面向开发者** ：启用后，新的拉取请求（PR）将自动运行审核。无需任何配置。

[Explore the docs](http://code.claude.com/docs/en/code-review) for more information.[查看文档](http://code.claude.com/docs/en/code-review) 以获取更多信息。