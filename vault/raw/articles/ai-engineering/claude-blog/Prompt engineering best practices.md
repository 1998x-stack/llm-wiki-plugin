---
title: "Prompt engineering best practices"
source: "https://claude.com/blog/best-practices-for-prompt-engineering"
author:
published: 2001-11-10
created: 2026-04-16
description: "Master the art of prompt engineering with Claude."
tags:
  - "clippings"
---
[Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) has emerged as an increasingly important part of working with LLMs, with prompt engineering as its essential building block.[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 已成为与大语言模型协作中日益重要的部分，而提示工程是其核心组成部分。

[Prompt engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) is the craft of structuring instructions to get better outputs from AI models. It's how you phrase queries, specify style, provide context, and guide the model's behavior to achieve your goals.[提示工程](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) 是一种通过构建指令来从AI模型中获得更优输出的技巧。它涉及如何表述查询、指定风格、提供上下文以及引导模型的行为，以实现你的目标。

The difference between a vague instruction and a well-crafted prompt can mean the gap between generic outputs and exactly what you need. A poorly structured prompt might require multiple back-and-forth exchanges to clarify intent, while a well-engineered prompt gets you there in one shot.模糊的指令与精心设计的提示词之间的差异，可能会导致输出结果要么千篇一律，要么精准契合你的需求。结构糟糕的提示词可能需要多次来回沟通才能明确意图，而设计精良的提示词则能一步到位达成目标。

To help you get started, we've assembled some of our team's best practices, including practical methods designed to improve your results right away. We'll start with simple habits you can use today, then scale up to advanced methods for complex projects.为了帮助你快速上手，我们整理了团队的一些最佳实践，其中包含旨在立即提升你成果的实用方法。我们将从你如今就能采用的简单习惯开始，再逐步过渡到适用于复杂项目的高级方法。

## How to use prompt engineering 如何使用提示词工程

At its most basic level, prompt engineering is just modifying the query you pass your LLM. Often it's simply adding information to the query before you make your actual request—but knowing *which* information is the *right* information to share is the secret to engineering a great and effective prompt.从最基本的层面来说，提示词工程就是修改你传递给大语言模型（LLM）的查询指令。通常，这只是在提出实际请求之前向查询中添加信息——但要知道 *哪些* 信息是需要分享的 *正确* 信息，才是打造优质高效提示词的关键。

### Core techniques 核心技术

These prompt engineering techniques form the foundation of effective AI interactions. Use them consistently to see immediate improvements in response quality.这些提示工程技术构成了高效人工智能交互的基础。持续运用这些技术，就能立刻看到回复质量的显著提升。

#### Be explicit and clear 清晰明确

Modern AI models respond exceptionally well to clear, explicit instructions. Don't assume the model will infer what you want—state it directly. Use simple language that states exactly what you want without ambiguity.现代人工智能模型对清晰、明确的指令响应效果极佳。不要指望模型能推断出你的意图——直接说明你的需求。使用简洁的语言，准确无误地表达你的想法，避免任何模棱两可。

**The key principle**: Tell the model exactly what you want to see. If you want comprehensive output, ask for it. If you want specific features, list them. Modern models like Claude benefit especially from explicit direction.**核心原则** ：向模型准确说明你希望看到的内容。若想要全面的输出，就明确提出要求；若想要特定的功能，就将其一一列出。像 Claude 这样的现代模型，尤其得益于清晰明确的指令。

**Example: Creating an analytics dashboard 示例：制作分析仪表板**

**Vague**: "Create an analytics dashboard" **模糊** ：“创建一个分析仪表板”

**Explicit**: "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation." **明确要求** ：“创建一个分析仪表板。尽可能包含尽可能多的相关功能和交互。超越基础功能，打造一个功能齐全的实现版本。”

The second version explicitly requests comprehensive features and signals that you want the model to go above and beyond the minimum.第二个版本明确要求全面的功能，并表明你希望模型超越最低要求。

**Best practices**: **最佳实践** ：

- Lead with direct action verbs: "Write," "Analyze," "Generate," "Create" 以直接的动作动词开头：“编写”、“分析”、“生成”、“创建”
- Skip preambles and get straight to the request 跳过开场白，直接提出请求
- State what you want the output to include, not just what to work on 说明你希望输出包含的内容，而不仅仅是说明要处理的对象
- Be specific about quality and depth expectations 明确说明对质量和深度的期望

#### Provide context and motivation 提供背景与动机

Explaining *why* something matters helps AI models better understand your goals and deliver more targeted responses. This is particularly effective with newer models that can reason about your underlying objectives.解释 *为什么* 某件事很重要，有助于人工智能模型更好地理解你的目标，并提供更有针对性的回应。这对于能够推理你潜在目标的新型模型来说效果尤为显著。

**Example: Formatting preferences 示例：格式偏好**

**Less effective**: "NEVER use bullet points" 效果较差</b>：“永远不要使用项目符号”

**More effective**: "I prefer responses in natural paragraph form rather than bullet points because I find flowing prose easier to read and more conversational. Bullet points feel too formal and list-like for my casual learning style." **更高效** ：“我更喜欢自然段落形式的回复，而不是项目符号列表，因为我觉得流畅的散文更容易阅读，也更具对话感。对于我这种随意的学习方式来说，项目符号列表显得过于正式，太像清单了。”

The second version helps the model understand the reasoning behind the rule, which allows it to make better decisions about related formatting choices.第二个版本帮助模型理解规则背后的推理逻辑，这使其能够针对相关的格式选择做出更优的决策。

**When to provide context**: **何时提供上下文** ：

- Explaining the purpose or audience for the output 说明输出的用途或目标受众
- Clarifying why certain constraints exist 说明某些约束存在的原因
- Describing how the output will be used 说明输出的使用方式
- Indicating what problem you're trying to solve 说明你正试图解决的问题

#### Be specific 具体说明

Specificity in prompt engineering means structuring your instructions with explicit guidelines and requirements. The more specific you are about what you want, the better the results.提示工程中的具体性指的是用明确的指导原则和要求来构建你的指令。你对需求描述得越具体，得到的结果就越好。

**Example: Meal planning 示例：膳食规划**

**Vague**: "Create a meal plan for a Mediterranean diet" **模糊** ：“为地中海饮食制定一份膳食计划”

**Specific**: "Design a Mediterranean diet meal plan for pre-diabetic management. 1,800 calories daily, emphasis on low glycemic foods. List breakfast, lunch, dinner, and one snack with complete nutritional breakdowns." **具体要求** ：“为糖尿病前期管理设计一份地中海饮食食谱。每日1800卡路里，重点选择低升糖指数食物。列出早餐、午餐、晚餐以及一份加餐，并附上完整的营养成分分析。”

**What makes a prompt specific enough?是什么让一个提示足够具体？**

Include: 包含：

- Clear constraints (word count, format, timeline) 明确的限制条件（字数、格式、时间线）
- Relevant context (who's the audience, what's the goal) 相关背景信息（目标受众是谁、目标是什么）
- Desired output structure (table, list, paragraph) 期望的输出结构（表格、列表、段落）
- Any requirements or restrictions (dietary needs, budget limits, technical constraints) 任何要求或限制（饮食需求、预算限制、技术限制）

#### Use examples 使用示例

Examples aren't always necessary, but they shine when explaining concepts or demonstrating specific formats. Also known as one-shot or few-shot prompting, examples show rather than tell, clarifying subtle requirements that are difficult to express through description alone.示例并非总是必需，但在解释概念或演示特定格式时能发挥重要作用。这种方法也被称为单样本或少样本提示，通过展示而非讲述的方式，阐明那些仅靠描述难以表达的细微要求。

**Important note for modern models**: Claude 4.x and similar advanced models pay very close attention to details in examples. Ensure your examples align with the behaviors you want to encourage and minimize any patterns you want to avoid.**现代模型的重要提示** ：Claude 4.x 及类似的高级模型会非常关注示例中的细节。请确保你的示例符合你希望鼓励的行为，并尽量减少你希望避免的任何模式。

**Example: Article summarization 示例：文章摘要**

**Without example**: "Summarize this article" **无示例** ：“总结这篇文章”

```
Here's an example of the summary style I want:

Article: [link to article about AI regulation]
Summary: EU passes comprehensive AI Act targeting high-risk systems. Key provisions include transparency requirements and human oversight mandates. Takes effect 2026.

Now summarize this article in the same style: [link to your new article]
```

**When to use examples**: **何时使用示例** ：

- The desired format is easier to show than describe 理想的格式展示起来比描述起来更简单
- You need a specific tone or style 你需要特定的语气或风格
- The task involves subtle patterns or conventions 该任务涉及微妙的模式或惯例
- Simple instructions haven't produced consistent results 简单的指令未能产生一致的结果

**Pro tip**: Start with one example (one-shot). Only add more examples (few-shot) if the output still doesn't match your needs.**专业提示** ：从一个示例开始（单样本提示）。只有当输出仍不符合你的需求时，再添加更多示例（少样本提示）。

#### Give permission to Claude to express uncertainty允许Claude表达不确定性

Give the AI explicit permission to express uncertainty rather than guessing. This reduces hallucinations and increases reliability.明确允许AI表达不确定性而非猜测。这能减少幻觉并提高可靠性。

**Example**: "Analyze this financial data and identify trends. If the data is insufficient to draw conclusions, say so rather than speculating." **示例** ：“分析这份财务数据并找出趋势。如果数据不足以得出结论，请明确说明，而非进行猜测。”

This simple addition makes responses more trustworthy by allowing the model to acknowledge limitations.这个简单的补充让模型能够承认自身的局限性，从而让回复更具可信度。

[**Try**](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) **these in Claude.** [**试试**](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) **这些在 Claude 中。**

## Advanced prompt engineering techniques高级提示词工程技术

These core habits will get you pretty far, but you may still encounter situations that require more sophisticated approaches. Advanced prompt engineering techniques shine when you're building agentic solutions, working with complex data structures, or need to break down multi-stage problems.这些核心习惯能让你取得不小的进展，但你仍可能遇到需要更复杂方法来应对的情况。高级提示工程技巧在你构建智能体解决方案、处理复杂数据结构，或需要拆解多阶段问题时能发挥出最大效果。

### Prefill the AI's response 预设AI的回复

Prefilling lets you start the AI's response for it, guiding format, tone, or structure. This technique is particularly powerful for enforcing output formats or skipping preambles.预填充功能可以为你启动 AI 的响应，引导其格式、语气或结构。这种技巧在强制输出格式或跳过开场白方面尤为有效。

**When to use prefilling**: **何时使用预填充** ：

- You need the AI to output JSON, XML, or other structured formats 你需要让 AI 输出 JSON、XML 或其他结构化格式
- You want to skip conversational preambles and get straight to content 你希望跳过对话式开场白，直接获取内容
- You need to maintain a specific voice or character 你需要保持特定的语气或人设
- You want to control how the AI begins its response 你希望控制AI如何开始其回复

**Example: Enforcing JSON output 示例：强制输出 JSON 格式**

Without prefill, Claude might say: "Here's the JSON you requested: {...}" 没有预填充时，Claude 可能会说：“这是你要求的 JSON 数据：{...}”

With prefill (API usage): 使用预填充（API 用法）：

```python
messages=[
    {"role": "user", "content": "Extract the name and price from this product description into JSON."},
    {"role": "assistant", "content": "{"}
]
```

The AI will continue from the opening brace, outputting only valid JSON.AI 将从左大括号处继续，仅输出合法的 JSON 格式内容。

**Note**: In chat interfaces, you can approximate this by being very explicit: "Output only valid JSON with no preamble. Begin your response with an opening brace." **注意** ：在聊天界面中，你可以通过非常明确的方式来近似实现这一点：“仅输出有效的 JSON，不得有前言。以左大括号开始你的回复。”

### Chain of thought prompting 思维链提示

Chain of thought (CoT) prompting involves requesting step-by-step reasoning before answering. This technique helps with complex analytical tasks that benefit from structured thinking.思维链（CoT）提示指的是在给出答案前要求模型进行逐步推理。该技术适用于那些借助结构化思维能提升表现的复杂分析任务。

**Modern approach**: Claude offers an [extended thinking](https://www.anthropic.com/news/visible-extended-thinking) feature that automates structured reasoning. When available, extended thinking is generally preferable to manual chain of thought prompting. However, understanding manual CoT remains valuable for situations where extended thinking isn't available or when you need transparent reasoning you can review.**现代方法** ：Claude 提供了一项 [扩展思考](https://www.anthropic.com/news/visible-extended-thinking) 功能，可自动化结构化推理。在该功能可用时，它通常优于手动思维链提示。不过，了解手动思维链（CoT）在扩展思考不可用或需要可审查的透明推理的场景下，仍然具有价值。

**When to use chain of thought**: **何时使用思维链** ：

- Extended thinking isn't available (i.e. the free [Claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) plan) 扩展思维功能不可用（即免费的 [Claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) 套餐）
- You need transparent reasoning that you can review 你需要能够查看的透明推理过程
- The task requires multiple analytical steps 该任务需要多个分析步骤
- You want to ensure the AI considers specific factors 你希望确保人工智能考虑特定因素

There are three common implementations of chain of thought:思维链有三种常见实现方式：

**Basic chain of thought 基础思维链**

Simply add "Think step-by-step" to your instructions.只需在你的指令中添加“逐步思考”即可。

```
Draft personalized emails to donors asking for contributions to this year's Care for Kids program.

Program information:
<program>
{{PROGRAM_DETAILS}}
</program>

Donor information:
<donor>
{{DONOR_DETAILS}}
</donor>

Think step-by-step before you write the email.
```

**Guided chain of thought 引导式思维链**

Structure your prompt to provide specific reasoning stages.构建您的提示以提供特定的推理阶段。

```javascript
Think before you write the email. First, think through what messaging might appeal to this donor given their donation history. Then, consider which aspects of the Care for Kids program would resonate with them. Finally, write the personalized donor email using your analysis.
```

**Structured chain of thought 结构化思维链**

Use tags to separate reasoning from the final answer.使用标签将推理过程与最终答案区分开。

```javascript
Think before you write the email in <thinking> tags. First, analyze what messaging would appeal to this donor. Then, identify relevant program aspects. Finally, write the personalized donor email in <email> tags, using your analysis.
```

**Note**: Even when extended thinking is available, explicit CoT prompting can still be beneficial for complex tasks. The two approaches are complementary, not mutually exclusive.**注** ：即便具备扩展思考能力，明确的思维链提示对复杂任务仍有帮助。这两种方法是互补的，而非相互排斥。

### Control the output format 控制输出格式

For modern AI models, there are several effective ways to control response formatting:对于现代人工智能模型，有几种有效的方法可以控制回复格式：

**1\. Tell the AI what TO do instead of what NOT to do 1\. 告诉人工智能该做什么，而不是不该做什么**

Instead of: "Do not use markdown in your response" Try: "Your response should be composed of smoothly flowing prose paragraphs" 不要用“不要在回复中使用 Markdown”，而要用“你的回复应由流畅连贯的散文段落组成”

**2\. Match your prompt style to the desired output 2\. 使你的提示风格与期望输出相匹配**

The formatting style used in your prompt may influence the AI's response style. If you want minimal markdown, reduce markdown in your prompt.你的提示词中使用的格式风格可能会影响 AI 的回复风格。如果你希望使用最少的 Markdown 格式，请减少提示词中的 Markdown 内容。

**3\. Be explicit about formatting preferences 3\. 明确格式偏好**

For detailed control over formatting:要对格式进行详细控制：

```
When writing reports or analyses, write in clear, flowing prose using complete paragraphs. Use standard paragraph breaks for organization. Reserve markdown primarily for inline code, code blocks, and simple headings.

DO NOT use ordered lists or unordered lists unless you're presenting truly discrete items where a list format is the best option, or the user explicitly requests a list.

Instead of listing items with bullets, incorporate them naturally into sentences. Your goal is readable, flowing text that guides the reader naturally through ideas.
```

### Prompt chaining 提示链

Unlike the previous techniques, prompt chaining cannot be implemented in a single prompt. Chaining breaks down complex tasks into smaller sequential steps with separate prompts. Each prompt handles one stage, and the output feeds into the next instruction.与之前的技术不同，提示链无法在单个提示词中实现。链式方法将复杂任务拆解为更小的连续步骤，并为每个步骤配备独立的提示词。每个提示词负责处理一个阶段，其输出会作为下一条指令的输入。

This approach trades latency for higher accuracy by making each individual task easier. Typically this technique would be implemented using workflows or programmatically, but you could manually provide the prompts after receiving responses.这种方法通过简化每个单独的任务，以延迟为代价换取更高的准确率。通常，这种技术会通过工作流或编程方式实现，但你也可以在收到响应后手动提供提示词。

**Example: Research summary 示例：研究摘要**

1. **First prompt**: "Summarize this medical paper covering methodology, findings, and clinical implications." **第一个提示** ：“总结这篇医学论文，涵盖研究方法、研究结果以及临床意义。”
1. **Second prompt**: "Review the summary above for accuracy, clarity, and completeness. Provide graded feedback." **第二个提示** ：“检查上述摘要的准确性、清晰度和完整性。提供分级反馈。”
1. **Third prompt**: "Improve the summary based on this feedback: \[feedback from step 2\]" **第三个提示词** ：“根据以下反馈完善摘要：\[步骤2的反馈\]”

Each stage adds refinement through focused instruction.每个阶段都通过针对性的指导来提升完善度。

**When to use prompt chaining**: **何时使用提示链** ：

- You have a complex request that needs breaking down into steps 你有一个复杂的请求，需要将其拆解为多个步骤
- You need iterative refinement 你需要迭代优化
- You're doing multi-stage analysis 你正在进行多阶段分析
- Intermediate validation adds value 中间验证能提升价值
- A single prompt produces inconsistent results 单个提示词会产生不一致的结果

**Trade-offs**: Chaining increases latency (multiple API calls) but often dramatically improves accuracy and reliability for complex tasks.**权衡** ：链式调用会增加延迟（需进行多次API调用），但通常能显著提升复杂任务的准确性和可靠性。

## Techniques you might have heard about你可能听说过的技巧

Some prompt engineering techniques that were popular with earlier AI models are less necessary with models like Claude. However, you may still encounter them in older documentation or find them useful in specific situations.早期人工智能模型常用的一些提示词工程技巧，在 Claude 等模型中已不再那么必要。不过，你仍可能在旧文档中遇到这些技巧，或在特定场景下发现它们仍有用。

### XML tags for structure 用于构建结构的XML标签

XML tags were once a recommended way to add structure and clarity to prompts, especially when incorporating large amounts of data. While modern models are better at understanding structure without XML tags, they can still be useful in specific situations.XML 标签曾是为提示词添加结构和清晰度的推荐方式，尤其是在整合大量数据时。尽管现代模型在无需 XML 标签的情况下也能更好地理解结构，但它们在特定场景下仍有其价值。

**Example**: **示例** ：

```
<athlete_information>
- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian
</athlete_information>

Generate a meal plan based on the athlete information above.
```

**When XML tags might still be helpful**:**XML 标签何时仍可能有用** ：

- You're working with extremely complex prompts mixing multiple types of content 你正在处理包含多种内容类型的极其复杂的提示词
- You need to be absolutely certain about content boundaries 你需要完全确定内容的边界
- You're working with older model versions 你正在使用旧版本的模型

**Modern alternative**: For most use cases, clear headings, whitespace, and explicit language ("Using the athlete information below...") work just as well with less overhead.**现代替代方案** ：对于大多数使用场景来说，清晰的标题、留白和明确的语言（例如“使用以下运动员信息……”）同样适用，且开销更低。

### Role prompting 角色提示

Role prompting defines expert personas and perspectives in how you phrase your query. While this can be effective, modern models are sophisticated enough that heavy-handed role prompting is often unnecessary.角色提示是在构建查询表述时定义专家角色和视角的方法。尽管这种方法可能有效，但现代模型已经足够成熟，因此通常无需刻意使用复杂的角色提示。

**Example**: "You are a financial advisor. Analyze this investment portfolio..." **示例** ：“你是一名财务顾问。分析这份投资组合……”

**Important caveat**: Don't over-constrain the role. "You are a helpful assistant" is often better than "You are a world-renowned expert who only speaks in technical jargon and never makes mistakes." Overly specific roles can limit the AI's helpfulness.**重要提醒** ：不要过度限定角色。“你是一个乐于助人的助手”通常比“你是一位世界知名的专家，只使用专业术语说话且从不犯错”效果更好。过于具体的角色设定会限制人工智能的实用性。

**When role prompting might help**: **何时角色提示会有帮助** ：

- You need consistent tone across many outputs 你需要在大量输出内容中保持一致的语气
- You're building an application that requires a specific persona 你正在开发一款需要特定人设的应用程序
- You want domain expertise framing for complex topics 你希望为复杂主题获得专业领域视角的解读

**Modern alternative**: Often, being explicit about what perspective you want is more effective: "Analyze this investment portfolio, focusing on risk tolerance and long-term growth potential" rather than assigning a role.**现代替代方案** ：通常，明确说明你想要的视角会更有效：“分析这个投资组合，重点关注风险承受能力和长期增长潜力”，而不是直接分配一个角色。

[Try](https://preview.claude.ai/new) in Claude. 在 Claude 中 [尝试](https://preview.claude.ai/new) 。

## Putting it all together 整合所有技巧

You've now seen individual techniques in isolation, but their real power emerges when you combine them strategically. The art of prompt engineering isn't using every technique available—it's selecting the right combination for your specific need.你现在已经单独了解了各项技巧，但只有当你有策略地将它们组合运用时，它们的真正威力才会显现出来。提示工程的艺术不在于使用所有可用技巧，而在于为你的具体需求选择合适的组合。

**Example combining multiple techniques**:**多种技巧结合示例** ：

```
xtract key financial metrics from this quarterly report and present them in JSON format.

I need this data for automated processing, so it's critical that your response contains ONLY valid JSON with no preamble or explanation.

Use this structure:
{
  "revenue": "value with units",
  "profit_margin": "percentage",
  "growth_rate": "percentage"
}

If any metric is not clearly stated in the report, use null rather than guessing.

Begin your response with an opening brace: {
```

This prompt combines: 此提示词结合了：

- Explicit instructions (exactly what to extract) 明确指令（需提取的具体内容）
- Context (why format matters) 上下文（格式为何重要）
- Example structure (showing the format) 示例结构（展示格式）
- Permission to express uncertainty (use null if unsure) 允许表达不确定性（不确定时使用 null）
- Format control (begin with opening brace) 格式控制（以左大括号开头）

## Choosing the right techniques 选择合适的技术

Not every prompt needs every technique. Here's a decision framework:并非每个提示都需要用到所有技巧。以下是一个决策框架：

**Start here: 从这里开始：**

1. Is your request clear and explicit? If no, work on clarity first 你的请求是否清晰明确？如果不清晰，请先优化清晰度
2. Is the task simple? Use core techniques only (be specific, be clear, provide context) 任务是否简单？仅使用核心技巧（具体说明、清晰表达、提供背景信息）
3. Does the task require specific formatting? Use examples or prefilling 该任务是否需要特定格式？使用示例或预填充内容
4. Is the task complex? Consider breaking it down (chaining) 任务复杂吗？考虑将其拆分（链式处理）
5. Does it need reasoning? Use extended thinking (if available) or chain of thought 是否需要推理？使用扩展思考（如有）或思维链

**Technique selection guide**: **技巧选择指南** ：

| If you need... 如果你需要…… | Use... 使用…… |
| --- | --- |
| Specific output format 特定输出格式 | Examples, prefilling, or explicit format instructions 示例、预填充或显式格式指令 |
| Step-by-step reasoning 分步推理 | Extended thinking (Claude 4.x) or chain of thought 扩展思考（Claude 4.x）或思维链 |
| Complex multi-stage task 复杂的多阶段任务 | Prompt chaining 提示链 |
| Transparent reasoning 透明推理 | Chain of thought with structured output 结构化输出的思维链 |
| To prevent hallucinations 防止幻觉 | Permission to say "I don't know" 允许说“我不知道” |

## Troubleshooting common prompt issues 排查常见提示词问题

Even well-intentioned prompts can produce unexpected results. Here are common issues and how to fix them:即便是初衷良好的提示词也可能产生意想不到的结果。以下是常见问题及解决方法：

- **Problem: Response is too generic** → Solution: Add specificity, examples, or explicit requests for comprehensive output. Ask the AI to "go beyond the basics." **问题：回答过于笼统** →解决方案：增加具体细节、示例，或明确要求输出完整内容。要求人工智能“深入讲解基础内容之外的知识”。
- **Problem: Response is off-topic or misses the point** → Solution: Be more explicit about your actual goal. Provide context about why you're asking.**问题：回答偏离主题或未切中要点** → 解决方案：更明确地说明你的实际目标。提供你提问的背景信息。
- **Problem: Response format is inconsistent** → Solution: Add examples (few-shot) or use prefilling to control the start of the response.**问题：响应格式不一致** → 解决方案：添加示例（少样本）或使用预填充来控制响应的开头。
- **Problem: Task is too complex, results are unreliable** → Solution: Break into multiple prompts (chaining). Each prompt should do one thing well.**问题：任务过于复杂，结果不可靠** →解决方案：拆分为多个提示词（链式提示）。每个提示词只专注做好一件事。
- **Problem: AI includes unnecessary preambles** → Solution: Use prefilling or explicitly request: "Skip the preamble and get straight to the answer." **问题：AI 包含不必要的开场白** → 解决方案：使用预填充或明确要求：“跳过开场白，直接给出答案。”
- **Problem: AI makes up information** → Solution: Explicitly give permission to say "I don't know" when uncertain.**问题：AI 编造信息** → 解决方案：明确允许 AI 在不确定时说“我不知道”。
- **Problem: AI suggests changes when you wanted implementation** → Solution: Be explicit about action: "Change this function" rather than "Can you suggest changes?" **问题：你想要执行操作时，AI 却建议修改方案** → 解决方案：明确说明操作：说“修改这个函数”，而不是“你能给出修改建议吗？”

**Pro tip**: Start simple and add complexity only when needed. Test each addition to see if it actually improves results.**专业提示** ：从简单开始，只在需要时再增加复杂度。对每一项新增内容进行测试，确认其是否真的能提升效果。

## Common mistakes to avoid 需要避免的常见错误

Learn from these common pitfalls to save time and improve your prompts:从这些常见误区中吸取教训，以节省时间并优化你的提示词：

- **Don't over-engineer**: Longer, more complex prompts are NOT always better.**不要过度设计** ：更长、更复杂的提示词并非总是更好。
- **Don't ignore the basics**: Advanced techniques won't help if your core prompt is unclear or vague.**不要忽视基础** ：如果你的核心提示不清晰或模糊，高级技巧也无济于事。
- **Don't assume the AI reads minds**: Be specific about what you want. Leaving things ambiguous gives the AI room to misinterpret.**不要认为人工智能能读懂你的心思** ：要明确说明你的需求。表述模糊会给人工智能留下误解的空间。
- **Don't use every technique at once**: Select techniques that address your specific challenge.**不要同时使用所有技巧** ：选择能解决你特定问题的技巧。
- **Don't forget to iterate**: The first prompt rarely works perfectly. Test and refine.**不要忘记迭代** ：第一个提示词很少能完美生效。要进行测试和优化。
- **Don't rely on outdated techniques**: XML tags and heavy role prompting are less necessary with modern models. Start with explicit, clear instructions.**不要依赖过时的技巧** ：对于现代模型来说，XML 标签和繁琐的角色提示不再是必要的。从明确、清晰的指令开始。

## Prompt engineering considerations 提示工程考量

### Working with long content 处理长内容

One of the challenges of implementing advanced prompt engineering is that it adds context overhead through additional token usage. Examples, multiple prompts, detailed instructions—they all consume tokens, and context management is a skill in its own right.实施高级提示词工程的挑战之一是，它会通过额外的令牌使用增加上下文开销。示例、多个提示词、详细说明——这些都会消耗令牌，而上下文管理本身就是一项技能。

Remember to use prompt engineering techniques when they make sense and justify their usage. For comprehensive guidance on managing context effectively, check out our blog post on [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).记得在合理且能证明其使用必要性时运用提示工程技术。如需获取关于有效管理上下文的全面指导，请查看我们关于 [上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 的博客文章。

**Context awareness improvements**: Modern AI models, including Claude 4.x, have significantly improved context awareness capabilities that help address historical "lost-in-the-middle" issues where models struggled to attend equally to all parts of long contexts.**上下文感知能力提升** ：包括 Claude 4.x 在内的现代人工智能模型，上下文感知能力得到了显著提升，这有助于解决历史上存在的“中间丢失”问题——在该问题中，模型难以同等关注长上下文的各个部分。

**Why task-splitting still helps**: Even with these improvements, breaking large tasks into smaller, discrete chunks remains a valuable technique—not because of context limitations, but because it helps the model focus on doing its best work within a very specific set of requirements and scope. A focused task with clear boundaries consistently produces higher quality results than trying to accomplish multiple objectives in a single prompt.**为何拆分任务仍有帮助** ：即便有这些改进，将大型任务拆分为更小、独立的部分仍是一种有价值的方法——这并非因为上下文存在限制，而是因为它能帮助模型在特定的需求和范围要求下，全力以赴做到最好。一个边界清晰的聚焦型任务，相比在单个提示词中完成多个目标，往往能产出质量更高的结果。

**Strategy**: When working with long contexts, structure your information clearly with the most critical details at the beginning or end. When working with complex tasks, consider whether breaking them into focused subtasks would improve the quality and reliability of each component.**策略** ：处理长上下文时，清晰地组织信息，将最关键的细节放在开头或结尾。处理复杂任务时，可考虑将其拆分为专注的子任务，以提升每个组成部分的质量和可靠性。

### What does a good prompt look like?一个好的提示词是什么样的？

Prompt engineering is a skill, and it's going to take a few tries before you master it. The only way to know if you're doing it right is to test it and see. The first step is to just try it yourself. You'll see right away the differences between queries with and without the prompting techniques we covered here.提示工程是一项技能，要掌握它需要多次尝试。判断自己做得是否正确的唯一方法就是进行测试并观察结果。第一步就是亲自尝试。你会立刻发现，运用我们在这里讲过的提示技巧的查询和未运用的查询之间存在明显差异。

To really hone your prompt engineering skills, you'll need to objectively measure the effectiveness of your prompts. The good news is that is exactly what is covered in our prompt engineering course at [anthropic.skilljar.com](https://anthropic.skilljar.com/claude-with-the-anthropic-api).要真正精进你的提示词工程技能，你需要客观衡量提示词的效果。好消息是，我们在 [anthropic.skilljar.com](https://anthropic.skilljar.com/claude-with-the-anthropic-api) 开设的提示词工程课程中，正好涵盖了这部分内容。

**Quick evaluation tips**: **快速评估技巧** ：

- Does the output match your specific requirements?输出结果是否符合你的具体要求？
- Did you get the result in one attempt or need multiple iterations?你是一次就得到了结果，还是需要多次尝试？
- Is the format consistent across multiple attempts?多次尝试的格式是否一致？
- Are you avoiding the common mistakes listed above?你是否避开了上述列出的常见错误？

## Final words of advice 最后的建议

Prompt engineering is ultimately about communication: speaking the language that helps AI most clearly understand your intent. Start with the core techniques covered early in this guide. Use them consistently until they become second nature. Only layer in advanced techniques when they solve a specific problem.提示词工程归根结底是关于沟通的学问：用能让人工智能最清晰理解你意图的语言来交流。从本指南开头介绍的核心技巧入手，持续运用这些技巧，直到它们成为你的本能。只有在这些技巧能解决具体问题时，再去学习和运用进阶技巧。

Remember: the best prompt isn't the longest or most complex. It's the one that achieves your goals reliably with the minimum necessary structure. As you practice, you'll develop an intuition for which techniques suit which situations.记住：最好的提示词不是最长或最复杂的那一个，而是能以最少的必要结构可靠实现你的目标的那一个。随着练习，你会逐渐掌握哪种技巧适用于哪种场景。

The shift toward context engineering doesn't diminish prompt engineering's importance. In fact, prompt engineering is a fundamental building block within context engineering. Every well-crafted prompt becomes part of the larger context that shapes AI behavior, working alongside conversation history, attached files, and system instructions to create better outcomes.向上下文工程的转变并不会削弱提示工程的重要性。事实上，提示工程是上下文工程中的一个基本构建模块。每一个精心设计的提示都会成为塑造人工智能行为的更大上下文的一部分，与对话历史、附加文件和系统指令协同作用，以产生更优的结果。

[Start prompting](https://preview.claude.ai/new) in Claude today. [现在就在 Claude 中开始编写提示词](https://preview.claude.ai/new) 。

## Additional resources 附加资源

- [Prompt engineering documentation 提示工程文档](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Interactive prompt engineering tutorial 交互式提示工程教程](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [Prompt engineering course 提示工程课程](https://anthropic.skilljar.com/claude-with-the-anthropic-api)
- [Context engineering guide 上下文工程指南](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)