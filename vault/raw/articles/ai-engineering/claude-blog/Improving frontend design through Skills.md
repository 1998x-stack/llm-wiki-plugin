---
title: "Improving frontend design through Skills"
source: "https://claude.com/blog/improving-frontend-design-through-skills"
author:
published: 2001-11-12
created: 2026-04-16
description: "Best practices for building richer, more customized frontend design with Claude and Skills."
tags:
  - "clippings"
---
You might notice that when you ask an LLM to build a landing page without guidance, it will almost always conform to Inter fonts, purple gradients on white backgrounds, and minimal animations. 你可能会注意到，当你要求大语言模型（LLM）在没有指导的情况下制作一个着陆页时，它几乎总是会采用 Inter 字体、白底紫渐变以及简约的动画效果。

The issue? [Distributional convergence.](https://en.wikipedia.org/wiki/Convergence_of_random_variables) During sampling, models predict tokens based on statistical patterns in training data. Safe design choices–those that work universally and offend no one–dominate web training data. Without direction, Claude samples from this high-probability center.问题何在？ [分布趋同](https://en.wikipedia.org/wiki/Convergence_of_random_variables) 。在采样过程中，模型会根据训练数据中的统计模式来预测标记。那些普适且不引发任何争议的安全设计方案，在网络训练数据中占据主导地位。若无明确指引，Claude 会从这个高概率的中心区域进行采样。

For developers building customer-facing products, this generic aesthetic undermines brand identity and makes AI-generated interfaces immediately recognizable—and dismissible.对于开发面向客户产品的开发者而言，这种通用的美学风格会削弱品牌辨识度，还会让人工智能生成的界面一眼就能被识别出来，进而被用户弃用。

### The steerability challenge 可控性挑战

The good news is that Claude is highly steerable with the right prompting. Tell Claude to "avoid Inter and Roboto" or "use atmospheric backgrounds instead of solid colors," and results improve immediately. This sensitivity to guidance is a feature; it means Claude can adapt to different design contexts, constraints, and aesthetic preferences. 好消息是，只要提示词得当，Claude 的可控性非常强。告诉 Claude“避免使用 Inter 和 Roboto 字体”或“采用大气背景而非纯色背景”，生成的结果会立刻得到改善。这种对指令的敏感度正是它的一大优势；这意味着 Claude 能够适配不同的设计场景、限制条件和审美偏好。

But this creates a practical challenge: the more specialized the task, the more context you need to provide. For frontend design, effective guidance spans typography principles, color theory, animation patterns, and background treatment. You need to specify which defaults to avoid and which alternatives to prefer across multiple dimensions.但这带来了一个实际挑战：任务越专业，需要提供的上下文就越多。对于前端设计而言，有效的指导涵盖排版原则、色彩理论、动效模式以及背景处理。你需要明确在多个维度上应避免哪些默认设置，以及优先选择哪些替代方案。

You could pack all this into a system prompt, but then every request–debugging Python, analyzing data, writing emails–carries frontend design context. The question becomes: how do you provide Claude with domain-specific guidance exactly when needed, without permanent context overhead for unrelated tasks?你可以把所有这些内容都塞进系统提示词里，但这样一来，每一次请求——无论是调试 Python 代码、分析数据、撰写邮件——都会附带前端设计的上下文。问题随之而来：如何在需要的时候，为 Claude 提供特定领域的指导，同时又不会让不相关的任务承担永久的上下文开销？

## Skills: dynamic context loading 技能：动态上下文加载

This is precisely what [Skills](https://www.anthropic.com/news/skills) were designed for: delivering specialized context on demand without permanent overhead. A skill is a document (often markdown) containing instructions, constraints, and domain knowledge, stored in a designated directory that Claude can access through simple file-reading tools. Claude can leverage these skills to dynamically load in information it needs at runtime, progressively enhancing its context instead of loading everything upfront. 这正是技能</b>的设计初衷：按需提供专业上下文，无需长期维护成本。技能是一份文档（通常为 Markdown 格式），包含指令、约束条件和领域知识，存储在指定目录中，Claude 可通过简单的文件读取工具访问该目录。Claude 可利用这些技能在运行时动态加载所需信息，逐步扩充上下文，而非一次性加载所有内容。

When equipped with these skills and the necessary tools to read them, Claude can autonomously identify and load relevant skills based on the task at hand. For instance, when asked to build a landing page or create a React component, Claude can load a frontend design skill and apply its instructions just-in-time. This is the essential mental model: skills are prompts and contextual resources that activate on demand, providing specialized guidance for specific task types without incurring permanent context overhead.掌握这些技能并具备阅读它们的必要工具后，Claude 可根据当前任务自主识别并加载相关技能。例如，当被要求搭建着陆页或创建 React 组件时，Claude 可以加载前端设计技能并即时应用其指令。这是核心的思维模式：技能是按需激活的提示词与上下文资源，能为特定任务类型提供专业指导，同时不会产生持久的上下文开销。

This allows developers to reap the benefits of Claude’s steerability without overloading the context window by stuffing disparate instructions across many tasks into the system prompt. As we’ve [previously explained,](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) too many tokens in the context window can result in degradation of performance, so keeping the contents of the context window lean and focused is extremely important for eliciting the best performance from the model. Skills solve for this by making effective prompts reusable and contextual.这让开发者能够充分利用 Claude 可控性的优势，同时避免因将众多任务中互不相关的指令塞进系统提示词而导致上下文窗口过载。正如我们 [此前所解释的](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) ，上下文窗口中的标记过多会导致性能下降，因此保持上下文窗口内容简洁且聚焦，对于让模型发挥最佳性能至关重要。技能模块通过让高效提示词具备可复用性和上下文关联性，解决了这一问题。

## Prompting for better frontend output优化前端输出的提示词设计

We can unlock significantly better UI generations from Claude, without permanent context overhead, by creating a frontend design skill. The core insight is to think about frontend design the way a frontend engineer would. The more you can map aesthetic improvements to implementable frontend code, the better Claude can execute.通过创建一项前端设计技能，我们可以在不产生永久上下文开销的情况下，让Claude生成效果显著更优的UI。核心思路是以前端工程师的视角看待前端设计。你将视觉美化改进转化为可实现的前端代码的能力越强，Claude的执行效果就越好。

Leveraging this insight, we identified several areas where targeted prompting works well: typography, animations, background effects, and themes. These all translate cleanly to code that Claude can write. Implementing this in your prompts does not require detailed technical instructions, just using targeted language that engages the model to think more critically about these design axes is enough to elicit stronger outputs. This maps closely with the guidance we provided in our [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) blog article, about prompting the model at the right altitude, avoiding the two extremes of low-altitude hardcoded logic like specifying exact hex codes and vague high-altitude guidance that assumes shared context.基于这一洞察，我们确定了几个定向提示词效果显著的领域：排版、动画、背景效果以及主题。这些内容都能清晰转化为 Claude 能够编写的代码。在提示词中实现这一方法，无需详细的技术说明，只需使用定向语言引导模型更审慎地思考这些设计维度，就能生成更优质的输出。这与我们在 [上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 博客文章中提供的指导高度契合——即要在合适的层级上对模型进行提示，避免两个极端：一是低层级的硬编码逻辑，比如指定具体的十六进制颜色代码；二是高层级的模糊指引，这类指引需要模型具备共享上下文认知。

### Typography 字体设计

To see this in action, let's start by viewing typography as one dimension we can influence via prompting. The prompt below specifically steers Claude to use more interesting fonts:要直观地理解这一点，我们先将排版视为一个可以通过提示词来影响的维度。下方的提示词专门引导 Claude 使用更具特色的字体：

```
<use_interesting_fonts>
Typography instantly signals quality. Avoid using boring, generic fonts.

Never use: Inter, Roboto, Open Sans, Lato, default system fonts

Here are some examples of good, impactful choices:
- Code aesthetic: JetBrains Mono, Fira Code, Space Grotesk
- Editorial: Playfair Display, Crimson Pro
- Technical: IBM Plex family, Source Sans 3
- Distinctive: Bricolage Grotesque, Newsreader

Pairing principle: High contrast = interesting. Display + monospace, serif + geometric sans, variable font across weights.

Use extremes: 100/200 weight vs 800/900, not 400 vs 600. Size jumps of 3x+, not 1.5x.

Pick one distinctive font, use it decisively. Load from Google Fonts.
</use_interesting_fonts>
```

**Output generated with base prompt: 基于基础提示词生成的输出：**

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/691366f388193282b0213316_image11.png)

Caption: AI-generated SaaS landing page with generic Inter font, purple gradient, and standard layout. No skills were used. 说明： 由AI生成的SaaS着陆页，采用通用的Inter字体、紫色渐变和标准布局。未使用任何技能。

**Output generated with base prompt and typography section 使用基础提示词和排版部分生成的输出**

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913679c9a202c88b680873b_image13.png)

Caption: AI-generated SaaS landing page with generic Inter font, purple gradient, and standard layout. No skills were used. 说明： 由AI生成的SaaS着陆页，采用通用的Inter字体、紫色渐变和标准布局。未使用任何技能。

Interestingly, the mandate to use more interesting fonts seems to encourage the model to improve other aspects of the design as well. 有趣的是，要求使用更有趣字体的指令似乎也会促使模型改进设计的其他方面。

Typography alone leads to significant improvement, but fonts are just one dimension. What about cohesive aesthetics across the entire interface? 仅靠排版就能带来显著的提升，但字体只是其中一个维度。那整个界面的协调美学又该如何呢？

### Themes 主题

Another dimension we can prompt for is designs inspired by well-known themes and aesthetics. Claude has a rich understanding of popular themes; we can use this to communicate the specific aesthetics we want our frontend to embody. Here’s an example:我们可以要求的另一个维度是受知名主题和美学风格启发的设计。Claude 对热门主题有着深入的理解，我们可以利用这一点来传达希望前端所呈现的特定美学风格。以下是一个示例：

```javascript
<always_use_rpg_theme>
Always design with RPG aesthetic:
- Fantasy-inspired color palettes with rich, dramatic tones
- Ornate borders and decorative frame elements
- Parchment textures, leather-bound styling, and weathered materials
- Epic, adventurous atmosphere with dramatic lighting
- Medieval-inspired serif typography with embellished headers
</always_use_rpg_theme>
```

This produces the following RPG-themed UI:这将生成以下 RPG 风格的用户界面：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913cec4181329835d1da27f_image2.png)

Caption: AI-generated SaaS landing page with generic Inter font, purple gradient, and standard layout. No skills were used. 说明： 由AI生成的SaaS着陆页，采用通用的Inter字体、紫色渐变和标准布局。未使用任何技能。

Typography and themes show targeted prompting works. But manually specifying each dimension is tedious. What if we could combine all these improvements into one reusable asset?排版和主题设计表明精准提示法效果显著。但手动指定每个维度的操作十分繁琐。如果我们能将所有这些优化整合为一个可重复使用的资源，会怎么样呢？

### A general-purpose prompt 通用提示词

The same principle extends to other design dimensions: prompting for motion (animations and micro-interactions) adds polish that static designs lack, while guiding the model toward more interesting background choices creates depth and visual interest. This is where a comprehensive skill shines.同样的原则也适用于其他设计维度：要求添加动态效果（动画和微交互）能为静态设计增添其本身不具备的精致感，而引导模型做出更具创意的背景选择则能营造层次感与视觉吸引力。这正是综合设计能力的优势所在。

Bringing this all together, we developed a ~400 token prompt – compact enough to load without bloating context (even when loaded as a skill) – that dramatically improves frontend output across typography, color, motion, and backgrounds:综合所有内容，我们开发了一个约 400 个 token 的提示词——其体积足够紧凑，即便作为技能加载也不会膨胀上下文——该提示词在排版、色彩、动效和背景方面显著优化了前端输出效果。

```
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design,this creates what users call the "AI slop" aesthetic. Avoid this: make creative,distinctive frontends that surprise and delight. 

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

In the example above, we start by giving Claude general context on the problem and what we're trying to solve for. We've found that giving the model this type of high-level context is a helpful prompting tactic to calibrate outputs. We then identify the vectors of improved design we discussed before and give targeted advice to encourage the model to think more creatively across all of these dimensions.在上面的示例中，我们首先向 Claude 提供了关于该问题以及我们试图解决的问题的整体背景。我们发现，为模型提供这种高层次的背景信息是一种有效的提示策略，可用于校准输出结果。随后，我们明确了之前讨论过的优化设计的关键方向，并给出针对性建议，以鼓励模型在所有这些维度上进行更具创造性的思考。

We also include additional guidance at the end to prevent Claude from converging to a different local maximum. Even with explicit instructions to avoid certain patterns, the model can default to other common choices (like Space Grotesk for typography). The final reminder to "think outside the box" reinforces creative variation.我们还在末尾加入了额外的指导，以防止 Claude 收敛到不同的局部最优值。即便有明确指令要求避免某些样式，该模型仍可能默认选择其他常见样式（比如排版字体选用 Space Grotesk）。最后那句“跳出思维定式”的提醒，能强化创意层面的多样性。

### Impact on frontend design 对前端设计的影响

With this skill active, Claude's output improves across several types of frontend designs, including: 激活此技能后，Claude 在多种前端设计类型上的表现都会得到提升，包括：

**Example 1: SaaS landing page 示例1：SaaS 着陆页**

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f77b_6d547f28.png)

Caption: AI-generated SaaS landing page with generic Inter font, purple gradient, and standard layout. No skills were used. 说明： 由AI生成的SaaS着陆页，采用通用的Inter字体、紫色渐变和标准布局。未使用任何技能。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f790_c47f37ab.png)

Caption: AI-generated frontend generated using the same prompt as the rendering above in addition to the frontend skill, now with distinctive typography, cohesive color scheme, and layered backgrounds. 说明： AI生成的前端界面，除了使用与上述渲染相同的提示词外，还结合了前端设计技巧，如今已具备独特的排版、统一的配色方案和分层的背景。

**Example 2: Blog layout 示例2：博客布局**

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f78d_f7040147.png)

AI-generated blog layout with default system fonts and flat white background. No skills were used. AI生成的博客布局，采用默认系统字体和纯白背景。未使用任何技能。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f77e_0ce357ff.png)

AI-generated blog layout using the same prompt as well as the frontend skill, featuring editorial typeface with atmospheric depth and refined spacing. 使用相同提示词及前端技术生成的AI博客布局，采用具有氛围感层次与精致间距的编辑字体。

**Example 3: Admin dashboard 示例3：管理后台**

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f784_7beb17d0.png)

AI-generated admin dashboard with standard UI components with minimal visual hierarchy. No skills were used. AI生成的管理仪表板，采用标准UI组件，视觉层级极简。未使用任何技能。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f781_3705adad.png)

AI-generated admin dashboard with bold typography, cohesive dark theme, and purposeful motion, using the same prompt in addition to the frontend skill. 基于相同提示词结合前端技能，生成采用粗体排版、统一深色主题且带有有意义动效的AI生成式管理后台。

## Improving artifact quality in claude.ai with Skills通过技能提升claude.ai上的工件质量

Design taste isn't the only limitation. Claude also faces architectural constraints when building artifacts.[Artifacts](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them) are interactive, editable content (like code or documents) that Claude creates and displays alongside your chat.设计风格并非唯一的限制。Claude 在构建人工制品时还面临架构限制。 [人工制品](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them) 是指 Claude 创建并与你的聊天内容一同展示的交互式、可编辑内容（如代码或文档）。

In addition to the issue with design taste explored above, Claude has another default behavior that limits its ability to generate fantastic frontend artifacts in [claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2). Currently, when asked to create a frontend, Claude just builds a single HTML file with CSS and JS. This is because Claude understands that frontends must be single HTML files to be properly rendered as artifacts.除了上文探讨的设计审美问题外，Claude 还有另一种默认行为，这限制了它在 [claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) 中生成出色前端作品的能力。目前，当被要求创建前端时，Claude 只会构建一个包含 CSS 和 JS 的单一 HTML 文件。这是因为 Claude 明白，前端要作为可正常渲染的作品呈现，必须是单一的 HTML 文件。

In the same way you’d expect a human developer to only be able to create very basic frontends if they could only write HTML/CSS/JS in a single file, we hypothesized that Claude would be able to generate more impressive frontend artifacts if we gave it instructions to use richer tooling.就像你会认为如果一名人类开发者只能在单个文件里编写HTML/CSS/JS，那他只能做出非常基础的前端界面一样，我们做出了一个假设：如果让Claude使用更丰富的工具来进行开发，它就能生成更出色的前端成果。

This led us to create a [web-artifacts-builder skill](https://github.com/anthropics/skills/blob/main/web-artifacts-builder/SKILL.md) which leverages Claude’s ability to [use a computer](https://www.claude.com/blog/create-files) and guides Claude to build artifacts using multiple files and modern web technologies like [React](https://react.dev/), [Tailwind CSS](https://tailwindcss.com/) and [shadcn/ui](https://ui.shadcn.com/). Under the hood, the skill exposes scripts that (1) help Claude efficiently set up a basic React repo and (2) bundle everything into a single file using [Parcel](https://parceljs.org/) to meet the single-HTML-file requirement after it is done editing. This is one of the core benefits of skills - by giving Claude access to scripts to execute boilerplate actions, Claude is able to minimize token usage while increasing reliability and performance.这促使我们开发了一个 [网页构件构建技能](https://github.com/anthropics/skills/blob/main/web-artifacts-builder/SKILL.md) ，该技能利用 Claude 的 [使用计算机](https://www.claude.com/blog/create-files) 能力，并引导 Claude 借助多个文件以及 [React](https://react.dev/) 、 [Tailwind CSS](https://tailwindcss.com/) 和 [shadcn/ui](https://ui.shadcn.com/) 等现代网页技术来构建构件。在底层，该技能提供了以下脚本：(1) 帮助 Claude 高效搭建基础的 React 代码仓库，(2) 在 Claude 完成编辑后，使用 [Parcel](https://parceljs.org/) 将所有内容打包成单个文件，以满足单 HTML 文件的要求。这正是技能的核心优势之一——通过让 Claude 能够调用脚本执行标准化操作，Claude 得以最大限度减少令牌使用量，同时提升可靠性和性能。

With the web-artifacts-builder skill, Claude could leverage shadcn/ui's form components and Tailwind's responsive grid system to create a more comprehensive artifact.借助 web-artifacts-builder 技能，Claude 可以利用 shadcn/ui 的表单组件和 Tailwind 的响应式网格系统来创建更全面的工件。

**Example 1: Whiteboard app 示例1：白板应用**

For example, when prompted to create a whiteboard app without the web-artifacts-builder skill, Claude outputted a very basic interface:例如，当被要求创建一个白板应用程序但不具备 web-artifacts-builder 技能时，Claude 输出了一个非常基础的界面：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f787_b07e5190.png)

On the other hand, when using the new web-artifacts-builder skill, Claude generated a much cleaner and more featureful application out-of-the-box that included drawing different shapes and text:另一方面，在使用新的 web-artifacts-builder 技能时，Claude 直接生成了一个简洁且功能更丰富的应用程序，其中包含绘制不同形状和文本的功能：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f78a_57c49993.png)

**Example 2: Task Manager App 示例2：任务管理器应用**

Similarly, when asked to create a task management app, without the skill, Claude generated a functional but very minimal application:同样地，当被要求创建一个任务管理应用时，在不具备该技能的情况下，Claude 生成了一个具备基本功能但非常简陋的应用程序：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f793_875d1eef.png)

With the skill, Claude generated an app that was more featureful out of the box. For example, Claude included a “Create New Task” form component that allows users to set an associated Category and Due Date on tasks:凭借这项技能，Claude 直接生成了一个功能更丰富的应用。例如，Claude 内置了一个“新建任务”表单组件，用户可通过该组件为任务设置关联的类别和截止日期：

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f7c9_7ae52606.png)

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6913d5b728dcecc13bc1f7a1_4c4951af.png)

To try out this new skill in [Claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2), simply enable the skill and then ask Claude to “use the web-artifacts-builder skill” when building artifacts.要在 [Claude.ai](http://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) 中试用这项新技能，只需启用该技能，然后在构建工件时让 Claude “使用 web-artifacts-builder 技能”即可。

## Optimizing Claude’s frontend design capabilities with Skills借助技能优化Claude的前端设计能力

This frontend design skill demonstrates a broader principle about language model capabilities: models often have the ability to do more than they express by default. Claude has strong design understanding, but distributional convergence obscures it without guidance. While you could add these instructions to your system prompt, this entails that every request carries frontend design context, even when this knowledge isn’t relevant to the task at hand. Instead, using Skills transforms Claude from a tool that needs constant guidance into one that brings domain expertise to every task. 这种前端设计技能体现了关于语言模型能力的一个更广泛原则：模型通常具备超出其默认表达范围的能力。Claude 具备扎实的设计理解力，但在缺乏引导的情况下，分布收敛会掩盖这一能力。你固然可以将这些指令添加到系统提示词中，但这意味着每一次请求都要附带前端设计相关的上下文，即便该知识与当前任务无关。而借助技能，Claude 从一个需要持续引导的工具，转变为能为每项任务带来领域专业知识的工具。

Skills are also highly customizable – you can create your own tailored to your specific needs. This allows you to define the exact primitives you want to bake into the skill, whether that's your company's design system, specific component patterns, or industry-specific UI conventions. By encoding these decisions into a Skill, you transform component parts of an agent’s thinking into a reusable asset that your entire development team can leverage. The skill becomes organizational knowledge that persists and scales, ensuring consistent quality across projects.技能也具备高度的可定制性——你可以根据自身特定需求创建专属技能。这使你能够定义想要融入技能的精准原语，无论是公司的设计系统、特定的组件模式，还是行业专属的用户界面规范。通过将这些设计决策编码到技能中，你将智能体思维的组件部分转化为可复用资源，供整个开发团队使用。该技能会成为留存并可扩展的组织知识，确保各项目的质量保持一致。

This pattern extends beyond frontend work. Any domain where Claude produces generic outputs despite having more expansive understanding is a candidate for Skill development. The method is consistent: identify convergent defaults, provide concrete alternatives, structure guidance at the right altitude, and make it reusable through Skills.这种模式不仅适用于前端开发工作。在任何领域，只要 Claude 尽管具备更广泛的认知却仍输出通用化内容，都可以通过开发技能来优化。方法始终一致：确定通用的默认设定，提供具体的替代方案，以合适的层级构建指导内容，并通过技能使其具备可复用性。

For frontend development, this means Claude can generate distinctive interfaces without per-request prompt engineering. To get started, explore our [frontend design cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb) or try out our [new frontend design plugin in Claude Code](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design).对于前端开发而言，这意味着 Claude 无需针对每个请求进行提示工程就能生成独具特色的界面。要开始使用，你可以查看我们的 [前端设计食谱](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb) ，或试用我们在 [Claude Code 中的新前端设计插件](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) 。

**Feeling inspired? To create your own frontend skills, check out our** [**skill-creator**](https://github.com/anthropics/skills/tree/main/skill-creator)**.****灵感满满？要创建自己的前端技能，请查看我们的** [**技能创建工具**](https://github.com/anthropics/skills/tree/main/skill-creator) **。**

**Acknowledgements 致谢**  
Written by Anthropic's Applied AI team: Prithvi Rajasekaran, Justin Wei, and Alexander Bricken, alongside our marketing partners Molly Vorwerck and Ryan Whitehead.由 Anthropic 应用人工智能团队的普里特维·拉贾塞卡兰、贾斯汀·魏和亚历山大·布里肯，以及我们的营销合作伙伴莫莉·沃沃克和瑞安·怀特黑德共同撰写。

eBook 电子书

## Agent Skills 智能体技能

Start using Skills with Claude to build more powerful applications today.现在就开始结合 Claude 使用技能，打造更强大的应用程序。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6915038fea2f5466c171c21f_Hand-NodeWeb.svg) ![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/691503928e574d7dc8407b4a_Hand-NodeWeb-1.svg)