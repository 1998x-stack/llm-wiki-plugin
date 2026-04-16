# 调查分析 这几年各厂家 LLM API KEY 模型API价格变动背后的关键事件，关键技术，关键产量等等，分析API降价的底层原因，探讨未来API降价的可能方向

> Source: Sonnet vs Opus对比
> Time: 2026/4/16 15:15:00

## Question

调查分析 这几年各厂家 LLM API KEY 模型API价格变动背后的关键事件，关键技术，关键产量等等，分析API降价的底层原因，探讨未来API降价的可能方向和原因

## Answer

我先把这事拆成三层：一层是各家公开价格时间线，一层是背后的事件/技术/产能变化，最后再归纳成为什么会降价、未来还会怎么降。接下来我会优先用官方定价页、官方发布和财报口径来搭框架，再用少量产业链资料补产能与成本逻辑。


已经有一条比较清晰的主线了：价格下行并不只是“算力便宜了”，更像是三股力量叠加——模型架构更省、推理系统更省、竞争更激烈。另外我还发现一个重要反例：像 DeepSeek 这种厂商也出现过促销结束/折扣取消的情况，说明 API 价格不是单边下行，它也受供给紧张和容量管理影响。


我已经把“价格下行”拆出了两种不同机制：
一类是 标签价直接下降，像 OpenAI、Google、Mistral、Qwen、DeepSeek 某些档位的明确降价；另一类是 标签价不动但单位有效智能更便宜，典型是 Anthropic Sonnet 线，价格长期维持在 $3 / $15，但能力持续升级、token 用量下降、缓存/批处理折扣变强。接下来我会把这两类放到同一张逻辑图里，解释为什么它们本质上都是“API 变便宜”。

Investigating LLM API price trends and drivers


The user asks for an analysis of LLM API price changes across major companies like OpenAI, Anthropic, and others. I'll gather historical price data, identify key events and technologies that led to fluctuations, and explore reasons behind price reductions. A detailed, structured comparison with trends and citations should clarify this.


Focusing on major LLM pricing and factors


I’ll focus on major API vendors like OpenAI, Anthropic, Google, and Mistral, and analyze their pricing trends and significant price cuts. Key factors include GPU production capacity, chip shipments, processing power, and associated tech advancements like HBM. I’ll gather data from vendor announcements and reputable sources like Nvidia, TSMC, and SemiAnalysis for a detailed analysis.


Gathering vendor pricing data and key events


I’ll gather official pricing from vendors like OpenAI, Anthropic, and Google, focusing on key LLM changes like GPT-4 and Gemini. I’ll search for historical prices and key announcements, such as launch posts or blog updates, and include relevant supply chain information like Nvidia H100 shipments and TSMC production.


Searching official pricing and vendor announcements


OpenAI API 定价 | OpenAI
Introducing Claude 3.5 Sonnet \ Anthropic
2026年OpenAI API接入完整指南：模型选择+代码示例
OpenAI API Pricing 2026: GPT-4.1 at $2/$8 per M tokens


Refining sources for GPT-4 pricing info


I’ll search for official pages related to the GPT-4 launch to gather precise details about pricing. These will provide the clearest and most authoritative information I need. I'll make sure to rely on official announcements and posts to ensure accuracy for the analysis.


Searching official GPT-4 launch details and pricing


API Pricing - OpenAI
Pricing | OpenAI API


Looking up official GPT-4 versions


I’ll check the official pages for GPT-4, GPT-4o, and GPT-4.1 to gather the most accurate and updated information on these models. These pages should have the precise details I’m looking for, including relevant pricing and launch information, to support the analysis.


Searching for GPT-4 and GPT-4.1 pages


GPT-4 | OpenAI
Introducing Claude 3.5 Sonnet \ Anthropic


Searching for official Anthropic Opus and Haiku pages


I need to check Anthropic’s official pages for both the Opus and Haiku models. These will give me the most precise pricing and details. I'll search for any official announcements or posts that discuss their features, prices, and any updates related to these models.


Searching official Anthropic Opus and Haiku pages


Claude API价格详解：各模型收费标准对比（2026）
Introducing the next generation of Claude - Anthropic
Plans & Pricing | Claude by Anthropic
保姆级教程：Claude Pro/Max 订阅开通与支付指引（含国内 ...
Claude 3.7 Sonnet System Card - assets.anthropic.com
Claude API Pricing 2026: $0.25–$75/M tokens (Haiku, Sonnet, Opus)
Claude Opus 4.6 System Card
Claude API Pricing: Per-Token Costs for Every Model


Searching for official Google Gemini pricing history


I’ll search for the official pages for Google Gemini's pricing history. This should provide me with the most accurate details about the pricing over time. I’ll check for any announcements or updates on their price changes and how they've evolved across different versions.


Searching for official Google Gemini pricing history


Gemini Developer API 价格 | Gemini API | Google AI for ...
Vertex AI 价格 | Google Cloud
Gemini 2.5 Flash-Lite is now stable and generally available


Searching for historical Google Gemini launch pricing


I think I should search specifically for blogs that mention pricing at the time of Google's Gemini launch. The Google developer blog might have these details, so I'll start there. I'll try to find any blog posts or updates that include official launch prices.


Searching for Google Gemini 1.5 pricing blogs


Gemini 1.5 Pro and 1.5 Flash GA, 1.5 Flash tuning support, higher rate ...
Google Gemini updates: Flash 1.5, Gemma 2 and Project Astra


Looking for historical pricing sources


I can check the official pricing page for the current prices, but for historical reduction information, results from the saved search queries should provide enough details. I just need to open and explore those specific results (553019search1 and 3) to find the right information.


Opening historical price reduction search results


[

        Updated production-ready Gemini models, reduced 1.5 Pro pricing, increased rate limits, and more

        - Google Developers Blog
        
    ](https://developers.googleblog.com/zh-hans/updated-gemini-models-reduced-15-pro-pricing-increased-rate-limits-and-more/)

Gemini Developer API 价格  |  Gemini API  |  Google AI for Developers


Exploring Gemini 2.5 launch price and historical trends


I can check the current pricing page for the latest Gemini 2.5 launch price, which may give a good view of the trend. But if the user wants historical data, I'll need to look for more vendors and search for official price history from DeepSeek. I should also check for news updates on version changes like V2, V3, and R1.


Searching DeepSeek API pricing and updates


Models & Pricing | DeepSeek API Docs
DeepSeek | 深度求索
DeepSeek API Pricing: deepseek-chat vs deepseek-reasoner (April 2026)
DeepSeek API - 快速集成 DeepSeek R1 和 AI 模型
DeepSeek-V3.2-Exp发布 API成本将降低50%以上_凤凰网
DeepSeek API Guide - DeepSeek AI
“涨价潮”来袭：DeepSeek领涨，国产大模型告别价格战？


Looking up price reductions and change logs from DeepSeek


I should search for official DeepSeek news, specifically related to any price reductions. It’s possible that their documentation includes a change log that could provide helpful information about pricing shifts. Let me look into this to get more details for the user.


Searching for DeepSeek API price reduction news


DeepSeek-V3.1 Release | DeepSeek API Docs


Checking for official DeepSeek pricing details


I think DeepSeek's sources should be sufficient, but it would be helpful to find the official pricing page that includes the most current prices and any caches. I may not need the full pricing history unless I'm specifically making a comparison. I’ll explore the open lines for more details now.


Searching for official pricing and caching solutions


Models & Pricing | DeepSeek API Docs


Considering Mistral's official pricing updates


I’m thinking DeepSeek might be part of the open-source-driven pricing disruption, which leads me to wonder about Mistral’s official pricing. I should look into whether Mistral has made recent pricing changes. Time to search for those updates! I'll see if I can find more specific details.


Searching for Mistral pricing changes and updates


Au Large - Mistral AI
Mistral API Pricing - All Model Costs (2026) | LM Market Cap
Mistral/mistral Large Latest Pricing - mistral | LLM API Costs
Mistral Large API Pricing from $0.25/1M input tokens | Compare 2 ...
Mistral Large 3 - TokenMix
Mistral Large 2 (Nov '24) - Dataconomy
Mistral Mistral Large — Specs, Benchmarks, Pricing & Availability | AI ...


Exploring various LLM pricing changes and vendors


The user asks about LLM API pricing changes, focusing on key events, technologies, and production behind them. To address this, I might leave out some smaller players—since the user is Chinese, I’ll include Qwen and Alibaba as well. Also, I’ll look for DashScope and official Qwen pricing updates.


Searching for LLM API pricing changes and trends


阿里云百炼模型价格-大模型服务平台百炼 (Model Studio ...
模型服务灵积控制台 - aliyun.com
阿里云百炼宣布模型降价_新浪新闻


Considering Chinese cloud providers for pricing changes


The user mentions "各厂家" (all vendors), so I think it’s important to include Chinese cloud providers like Alibaba. I’ll focus on representative vendors like OpenAI, Anthropic, Google, DeepSeek, and Mistral. I also plan to check for Qwen's current pricing and any price cut events.


Searching for Qwen model pricing and Alibaba updates


【大模型服务平台百炼】通义千问3-Max 模型降价通知
千问系列大模型计费调整通知-阿里云帮助中心
通义千问三款主力模型再降价，最高降幅85%-阿里云开发者社区


Including Qwen and reviewing notice lines


千问系列模型降价通知-阿里云帮助中心
〖阿里云〗〖大模型服务产品百炼&灵积〗〖通义千问大模型价格调整通知〗-阿里云官网公告


Searching for GPT-4 API pricing info


I need to find the current pricing for OpenAI’s GPT-4 API. The GPT-4 page doesn’t list pricing, though, so maybe the “general availability” page could have more details, like pricing for 8K context. I’ll give that a search to check.


Searching OpenAI for GPT-4 pricing details


API Pricing - OpenAI
GPT-4 Turbo Model | OpenAI API


Searching for GPT-4 general availability blog


I’m looking for any announcements or blog posts about GPT-4’s general availability. A blog post might have more details on when the API became publicly available or include any pricing updates. Let's search for that and see what turns up.


Searching for GPT-4 general availability blog posts


GPT-4 API general availability and deprecation of older models ... - OpenAI
GPT-4 Model | OpenAI API
GPT-4 API general availability and deprecation of older models in the ...
Retiring GPT-4o and other ChatGPT models - OpenAI Help Center


Looking for GPT-4 Turbo launch details


I think current model pages can help with pricing info for both GPT-4 and GPT-4 Turbo, but launch dates aren’t included. I’ll need to find when GPT-4 Turbo was launched, so I’m thinking it might be best to search for any announcements from Dev Day or similar official sources.


Searching official OpenAI info on GPT-4 Turbo launch


GPT-4 Turbo Model | OpenAI API
API Pricing - OpenAI
2026深度评测：GPT-4与Gemini 1.5 Pro中文能力终极对决 ...
2026年4月AI三巨头全面横评：GPT-5.4、Claude 4.6 ...


Searching for supply chain data and capacity expansion


I need to look into the supply chain details for CoWoS capacity, HBM output, and Nvidia shipments, especially related to inference optimization techniques. I'd focus on authoritative sources like Nvidia's or TSMC's reports to get the most accurate numbers. I can mention capacity expansion broadly if specifics aren’t clear.


Searching for capacity expansion and HBM data


I’ll search for reliable industry reports, such as those from TrendForce, SK hynix, Samsung, and Micron, to get specifics around HBM sales and capacity, particularly whether it’s sold out. I also need to look for official updates on TSMC’s CoWoS capacity expansion to get the most authoritative info.


Searching TSMC CoWoS capacity and expansion details


[News] TSMC’s CoWoS Capacity Doubles for Two Years, Still Insufficient ...
TSMC 2025 Q4 Quarterly Results - Taiwan Semiconductor Manufacturing ...
TSMC (2330.TW/2330 TT) - KGI
TSMC Stock Drops. Why Rising Chip Sales Aren't Boosting Its Shares.
Global semiconductor foundry market hit a record $320 billion in 2025 as TSMC pulled further ahead
TSMC profits jump 54% on back of AI chip boom


Looking up TSMC production details and HBM supply


I could check TSMC’s Q1 2025 official transcript and possibly their annual report for more on their volume production. I also need to search for information about HBM supply to get a clearer picture of the situation. Let’s search for the latest official reports or updates.


Searching for HBM supply and production information


SK hynix Posts Record Annual Financial Results in 2025
the call with me today are Sanjay Mehrotra, our president and CEO, and ...
프레젠테이션 - images.samsung.com
SK海力士发布2024财年及第四季度财务报告
Micron’s 2025 HBM chip supply fully sold out as AI demand surges
HBM | DRAM | 三星半导体官网
Micron says memory shortage will 'persist' beyond 2026
Micron to Dump 'Crucial' Consumer Business. It's All About AI.
SK Hynix and Samsung shares leap after OpenAI deal


Looking up Micron HBM supply details


I should search for Micron's official report or call about HBM being sold out through 2025 and 2026. Getting this information could be enough to better understand the supply situation. Let me look up the latest details from Micron’s official sources to confirm.


Searching for Micron HBM supply updates


Financial results


Looking up Nvidia/TSMC inference performance details


I should search for official information from Nvidia or TSMC about improvements in inference performance, possibly focusing on Blackwell. This could help clarify their latest performance strides. I'll look up any relevant updates or reports from these sources to get the most accurate and up-to-date info.


Searching Nvidia/TSMC official sources on Blackwell inference improvement


NVIDIA Blackwell Platform Arrives to Power a New Era of Computing
Leading Inference Providers Achieve Lowest Token Cost With Open Source ...
NVIDIA Blackwell Platform Arrives to Power a New Era of Computing
NVIDIA Platform Delivers Lowest Token Cost Enabled by Extreme Co-Design
The Engine Behind AI Factories | NVIDIA Blackwell Architecture
NVIDIA Blackwell Architecture Technical Overview


Exploring open-source improvements and mentions from vendors


I need to gather information on open-source serving stack improvements like vLLM, SGLang, and TensorRT-LLM, and also look into prompt caching. I'll check official sources to see if vendors have posted relevant updates. The user wants bottom-line reasons, so I’ll focus on production improvements like distillation, MoE, FP8, and other efficiency factors. I'll search for some specific vendor technical posts too.


Looking for cost reduction info via Anthropic Opus 4.5


I’ll check out the article on Anthropic’s Opus 4.5. It mentions cutting token usage in half, which likely means effective cost reduction rather than just a price cut. I’ll need to look that up for more details to offer the user.


Searching open-source serving stack and vendor insights


Introducing Claude Opus 4.5 \ Anthropic
Google Gemini updates: Flash 1.5, Gemma 2 and Project Astra
Cheaper, Better, Faster, Stronger | Mistral AI


Searching for Mistral pricing details


I need to search for the current prices of Mistral and compare them to the original Mistral Large prices. This will help me gather the relevant data, and I’ll check open sources to find this info. I just have to get that all lined up.


Searching current Mistral and Mistral Large prices


Au Large | Mistral AI


Searching for current Mistral API pricing details


I need to find the current Mistral API pricing, but not just from the pricing page. I should look through the documentation directly to get the most accurate and up-to-date information. I’ll search for the official docs to ensure it's reliable.


Searching Mistral API pricing in official docs


Compare Models | Mistral Docs


Searching for OpenAI/Anthropic/Microsoft capex and cloud capacity


I’m looking for the latest capex and data center capacity information for OpenAI, Anthropic, and Microsoft, as well as cloud spending trends from other companies like Google and Meta. I may also need to check for details about accelerator capacity with TSMC and HBM, focusing on inference specifics.


Searching for AI infrastructure spending and pricing data


GPT-4o Model | OpenAI API


Looking for GPT-4O price drop details


I'm curious about whether GPT-4o's price has dropped. I know the launch price was $5/$15, but now it seems to be listed at $2.5/$10. I'll need to check if the price has changed, and it might be useful to look up the official post confirming any price adjustments.


Searching for official GPT-4o price change details


API Pricing - OpenAI
GPT-4o (Nov '24) - Dataconomy
gpt-4o pricing - OpenAI
Pricing | OpenAI API
GPT-4o Pricing: API Cost, ChatGPT Plus vs Pay-as-You-Go (2025)
OpenAI Price Drop 2025: Full GPT-4o Model Comparison (With Charts)
OpenAI API Pricing (March 2026): GPT-5, GPT-4.1, GPT-4o, o3 Per-Token Costs


Clarifying current GPT-4o pricing and historical context


The GPT-4o price now is $2.5/$10, which is a significant drop from its launch price of around $5/$15. Official statements mention GPT-4o was 50% cheaper than GPT-4 Turbo. It's important to mention this inference, but I should be careful, especially when citing only the current prices. I may look for archived statements for more details.


Outlining GPT and Claude pricing over time


It might be easier to present a timeline showing key pricing steps with official evidence. For OpenAI: GPT-4 was $30/$60 at launch, GPT-4 Turbo was $10/$30, GPT-4o, 50% cheaper than Turbo, was implied at $5/$15, and GPT-4.1 at $2/$8. For Anthropic, Claude 3 Opus started at $15/$75. I need to check the official price history.


Searching historical OpenAI pricing and deductions


Introducing the next generation of Claude \ Anthropic


Searching for historical Google Gemini pricing


I need to find official pricing for Google Gemini, specifically for 1.5 Pro and Flash, both current and historical. I'll focus on any public preview pricing or 2024 price reductions, and check pricing for Gemini 2.5 Flash. The user likely wants a history of price changes, not just the current.


Searching historical and current Gemini 1.5 Pro pricing


Updated production-ready Gemini models, reduced 1.5 Pro pricing ...
Gemini Developer API 价格 | Gemini API | Google AI for ...


Exploring pricing trends across vendors


I could infer initial prices based on reduction percentages, but if current docs don’t list Gemini 1.5 Pro, I may need to look at archived sources. Google’s 2.5 Pro and newer models should help illustrate pricing behavior, and, despite not getting exact numbers, highlighting percentage changes might be sufficient.


Searching DeepSeek pricing and pricing changes


Models & Pricing | DeepSeek API Docs


Searching for historical and current price data


I’ve got the current DeepSeek prices in CNY, but I might not need to convert them since official docs use CNY. I should also look for the exact old and new Google prices—maybe blog posts with percentages could give enough info. For Gemini 1.5 Pro, I’ll check current and archived docs to see if I can infer its reduced price.


Searching current and old Gemini 1.5 Pro prices


Gemini Developer API pricing - Google AI for Developers


Reviewing price reductions and model progression examples


I think it might be enough to look at Google's AI Studio pricing with current models and historical reduction percentages. Using examples like Gemini 1.5: if it had a 78%/71% price cut, I can derive earlier prices from the current ones. We can say something like "roughly from $0.35/$1.05 to $0.075/$0.30" based on this calculation. I should also check for Qwen reductions with official old/new prices.


Searching Google AI Studio and Qwen pricing trends


千问系列模型降价通知-阿里云帮助中心
〖阿里云〗〖大模型服务产品百炼&灵积〗〖通义千问大模型价格调整通知〗-阿里云官网公告


Summarizing key AI price changes and events


I think the May 2024 detail might not be needed if the September 2024 data is sufficient. I found some useful developer community information with a 97% price cut. There are key events shaping AI pricing like GPT-4's 2023 high prices, 2024 multimodal models like GPT-4o and Claude 3, and 2025 model efficiency changes.


Summarizing AI price reductions and DeepSeek service changes


In 2024, Qwen saw up to 85% reductions for Turbo inputs and similar cuts for Plus and Max. DeepSeek's pricing history is more complex, with initial promotional cuts and fluctuating costs. V3.2 has seen considerable decreases in service costs, although performance varies based on promotional or off-peak discounts. The introduction of V3.1 led to canceled discounts but expanded capacity.


Checking supply chain and GPU growth


I might use lines from the official DeepSeek V3 page to support the findings. Regarding GPU supply, TSMC forecasts growth with over 17 million 12” wafers by 2025, and they’re doubling CoWoS to meet rising demand. However, bottlenecks remain despite supply expansion. I'll mention these trends with proper citation.


Searching GPU supply, AI chip bottlenecks, and more


Q1 2025 Taiwan Semiconductor Manufacturing Co Ltd Earnings Call on April 17, 2025 / 6:00AM
PowerPoint Presentation
NVIDIA Corporation - NVIDIA Blackwell Platform Arrives to Power a New Era of Computing
NVIDIA Enters Production With Dynamo, the Broadly Adopted Inference Operating System for AI Factories | NVIDIA Newsroom


Discussing potential future pricing and model trends


I could mention future directions like more model tiers (e.g., large, mini, nano), improved caching solutions, and batch pricing strategies. Techniques like distillation, MoE, and speculative decoding will likely shape efficiency, while competition from open-source models could keep prices in check. I'll consider mentioning some of these key trends.


Discussing pricing trends for models


The major trend here is price cuts over time, like the drop from GPT-4's $30/$60 to GPT-4o's $2.5/$10, and even lower for GPT-4.1. It's worth mentioning the overall price reduction, even if we can't pinpoint exact launch prices. I'll show a comparison from GPT-4, GPT-4 Turbo, to current GPT-4o and GPT-4.1.


Considering pricing strategies


Many vendors reduce prices by launching cheaper successors rather than directly cutting prices of older models. That’s an important point for analysis. I might need to check the exact current price for GPT-4 from the model page, but an open search result might be sufficient to confirm.


Searching for current OpenAI GPT-4 pricing details


GPT-4 Model | OpenAI API


Finding current pricing details


It could be helpful to check the official OpenAI API pricing page to confirm the current rates for batch and other services. For Anthropic’s Opus 4.6, it seems the price didn’t change. I might explore the OpenAI page or the Opus 4.5/4.6 pages for specific price details.


Searching official OpenAI and Anthropic pricing pages


Claude Opus 4.6 \ Anthropic


Looking into Anthropic's deprecation rationale


It might be helpful to search for the official reasoning behind the deprecation of older models by Anthropic. Understanding their rationale for ending support or phased-out models could offer valuable insights into their strategy and product lifecycle.


Searching for Anthropic deprecation rationale and policies


Commitments on model deprecation and preservation \ Anthropic
Model Card and Evaluations for Claude Models - Anthropic
Claude Mythos Preview \ red.anthropic.com


Finalizing prices and citations


I need to craft a precise response in Chinese with credible references. It might be useful to gather a few more targeted sources, especially from OpenAI's official blogs or pricing pages. I already have enough data, but some additional details, like the exact pricing for GPT-4.1 and GPT-4o, could help. I'll check the relevant lines available in the search results.


Browsing for OpenAI pricing pages and sources


GPT-4o Model | OpenAI API
Introducing GPT-4.1 in the API | OpenAI
[

        Updated production-ready Gemini models, reduced 1.5 Pro pricing, increased rate limits, and more

        - Google Developers Blog
        
    ](https://developers.googleblog.com/zh-hans/updated-gemini-models-reduced-15-pro-pricing-increased-rate-limits-and-more/)

千问系列模型降价通知-阿里云帮助中心
AI in abundance | Mistral AI
Mistral Medium 3 - Mistral AI | Mistral Docs


Searching for open questions about pricing


千问系列模型降价通知-阿里云帮助中心


Finalizing production analysis and citations


I need to ensure I gather relevant citations from the web for the final answer and clarify that the sources are representative, not exhaustive. Since the user wants a multi-year analysis (2023-2026), it’s important to address silicon capacity/output, mentioning TSMC, Micron, and Nvidia. I’ll interpret "产量" as production capacity and avoid ambiguous claims. I'll also look for specific data on chip, packaging, HBM, and server capacity. Let's inspect the available sources.


Investigating chip production capacity for TSMC, Micron, Nvidia


Q1 2025 Taiwan Semiconductor Manufacturing Co Ltd Earnings Call on April 17, 2025 / 6:00AM
PowerPoint Presentation
NVIDIA Corporation - NVIDIA Blackwell Platform Arrives to Power a New Era of Computing
NVIDIA Enters Production With Dynamo, the Broadly Adopted Inference Operating System for AI Factories | NVIDIA Newsroom
DeepSeek-V3.2-Exp 发布，训练推理提效，API 同步降价 | DeepSeek API Docs


Clarifying TSMC demand and CoWoS details


I think I should find exact information about TSMC's mentions of demand and CoWoS doubling. It might be easier if I search again to get specific snippets from the search results. I'll focus on getting the most relevant, up-to-date information to support this.


Searching for TSMC Q1 2025 transcript details


Q1 2025 Taiwan Semiconductor Manufacturing Co Ltd Earnings Call on ...
Financial results - investors.micron.com
NVIDIA Blackwell Platform Arrives to Power a New Era of Computing


Finding exact pricing for GPT-4


I need to find the exact line for the current price of OpenAI's GPT-4. I’ll open more relevant lines of results to gather the most accurate and up-to-date pricing info. This way, I can provide the user with a clear and trustworthy answer.


Searching current OpenAI GPT-4 pricing details


GPT-4 Model | OpenAI API
Introducing GPT-4.1 in the API | OpenAI
Introducing the next generation of Claude \ Anthropic
model_pricing_july2023_V2


Searching for Claude and Opus 4.6 pricing details


Claude Sonnet 4.6 \ Anthropic
Cheaper, Better, Faster, Stronger | Mistral AI
[

        Updated production-ready Gemini models, reduced 1.5 Pro pricing, increased rate limits, and more

        - Google Developers Blog
        
    ](https://developers.googleblog.com/zh-hans/updated-gemini-models-reduced-15-pro-pricing-increased-rate-limits-and-more/)

Google Gemini updates: Flash 1.5, Gemma 2 and Project Astra


Inspecting GPT-4 Turbo pricing from DevDay


I could refer to the OpenAI DevDay search results to highlight the GPT-4 Turbo design as a cheaper and potentially better version. The current page mentions it being up to 3 times cheaper than GPT-4. I'll check the search results to confirm and gather more details.


Inspecting OpenAI DevDay results for GPT-4 Turbo


New models and developer products announced at DevDay | OpenAI


Considering major LLM pricing for historical context


The user wants pricing behind historical events, so we can highlight major vendors like OpenAI, Anthropic, Google, Mistral, DeepSeek, and Qwen/Alibaba, but avoid exhaustive lists. I'll mention vendors using "各厂家" to cover various providers. Meta may be less relevant, and xAI’s history would be brief, so I might skip that.


Handling PDF analysis with screenshots


The system requires using screenshots when analyzing PDFs, even though we've previously opened them for text. We have PDFs from TSMC, Micron, etc., and need to comply with the rules. I think we’ll opt for screenshots of pages with relevant content, like TSMC’s page 3, or cite search results instead of opening the document.


Choosing between PDF screenshots and search snippets


To be safe, I think I'll use screenshots of relevant TSMC, Micron, and Anthropic pages—just in case we decide to cite them. However, search result snippets might already provide enough detail, especially for older pricing. So, I might prefer citing search snippets for those, which don’t require screenshots.


Analyzing pricing data from major LLM API vendors


Q1 2025 Taiwan Semiconductor Manufacturing Co Ltd Earnings Call on April 17, 2025 / 6:00AM
PowerPoint Presentation
model_pricing_july2023_V2


Deciding which pages to screenshot for compliance


I think for compliance, it’s best to screenshot specific pages. For TSMC, I’ll use page 3 (which may correspond to page 4 due to cover pages) and for Micron, pages 7 and 8. For Anthropic, I'll start with page 0. These satisfy the instruction, even though they might not be needed for citations.


Generating PDF screenshots for specified pages


Considering final screenshot and citation strategy


I don't think another screenshot for Micron page 8 is absolutely necessary. We already have a screenshot for page 7, and the relevant information is on pages 8-9, but I can just rely on the text I already have. For citation, I can use the lines I’ve opened from the PDF text.


As for the Gemini 1.5 Flash pricing, I’ll make sure to use the exact numbers, like $0.075/$0.3, which are most likely found in the search results.  I'll double-check the search results for confirmation!


Analyzing screenshots and PDF lines for product details


[

        Gemini 1.5 Flash price drop with tuning rollout complete, and more

        - Google Developers Blog
        
    ](https://developers.googleblog.com/en/gemini-15-flash-updates-google-ai-studio-gemini-api/)

Looking into Qwen May 2024 pricing


I might need to rely on search snippets for the May 2024 pricing for Qwen, especially if the document isn't clear or up-to-date. Let me check official sources or help notices for May to ensure the information is accurate and current. I’ll aim to get that confirmed!


Searching official Aliyun help for May 2024 updates


千问系列模型降价通知-阿里云帮助中心


Searching for official Alibaba May doc


I think we've gathered enough for now, but just to be thorough, I may want to search for an official May document from Alibaba. I’ll focus on finding something related to model billing notices or similar details to get the most accurate and up-to-date information. Let’s give it a try!


Searching for Alibaba May official model billing docs


千问系列大模型计费调整通知-阿里云帮助中心


Searching for official Qwen May 97% data


I need to search for official details about Qwen's potential 97% cut in May. It might be a bit trickier to find, but I’ll look into any official sources that could confirm that figure or provide more context. Let’s see what we can find!


Searching web for Qwen API price reduction details


Clarifying pricing change timeline and DeepSeek details


I can mention the March and September price changes, focusing on the aggressive Chinese market price war in 2024 and significant cuts in September, along with March's billing restructuring. For DeepSeek, I’ll look for the official current pricing and include relevant details, especially from the English page. This should work!


Summarizing price changes and trends for DeepSeek


pricing-details-usd | DeepSeek API Docs


Checking current Mistral pricing


I have a good set of information so far!


Now, I might check for the latest pricing on Mistral Large 2.1 and Medium 3. I think I’ll look for an official source and check for any recent updates on their page. Let me see if the search results can point to the exact details.


Searching for Mistral Large 2.1 and Medium 3


Compare Models | Mistral Docs


Structuring the response on API pricing


I think I have enough information now. The user mentioned “API model API prices,” which likely refers to API pricing in general. I could touch on concepts like prompt caching, quality-adjusted pricing, and cover the underlying reasons/issues and future directions. I’ll produce a well-organized essay with four sections and citations at the end of each paragraph.


Structuring the essay and quantifying pricing changes


I’ll structure the essay around key events, pricing changes, and future trends. It’ll include examples like OpenAI’s GPT pricing evolution—e.g., GPT-4 at $30/$60, GPT-4 Turbo at $10/$30, and GPT-4o at $2.5/$10. Also, Anthropic’s Claude pricing changes, showing quality improvements while maintaining stable pricing, suggesting effective price cuts.


Summarizing pricing and updates for DeepSeek


For Flash-8B, output is 5-20% shorter to reduce the cost, with Oct 2024 price at $0.0375/$0.15. DeepSeek's Dec 2024 V3 launch offers substantial improvements, with promo pricing. Current official prices from the English page: deepseek-chat $0.07/$0.27/$1.10 and reasoner $0.14/$0.55/$2.19.


Understanding Mistral pricing and efficiency


Looking at Mistral, the pricing isn't a simple, steady decline but instead includes promotions and cuts driven by tech upgrades. In April 2024, Mixtral 8x22B used 39B active, showing cost efficiency. In May 2025, the Medium 3 model offers frontier-like performance at 8x lower cost than other models. Let’s confirm pricing details with official sources.


Analyzing GPT pricing changes, token efficiency, and cuts


Medium is the new large. | Mistral AI


Considering GPT-4.5 deprecation evidence


I think it might be helpful to find additional official evidence for why OpenAI may be deprecating the GPT-4.5 preview, especially since GPT-4.1 seems to offer similar, if not better, performance with lower cost and latency. Let’s take a closer look at lines 47-63 to investigate further.


Inspecting code lines around 47 for updates


Introducing GPT-4.1 in the API | OpenAI


Searching for current OpenAI GPT-4.1 pricing


I think I should search for the official current pricing for GPT-4.1 to get the exact details. I'll also check lines beyond 156 for additional relevant information. This could help clarify the proper cost structure and give me a more solid grounding for further analysis.


Searching current OpenAI pricing and plans


Introducing GPT-4.1 in the API | OpenAI


Confirming Sonnet 4.6 and checking Opus pricing


It looks like the pricing for Sonnet 4.6 is the same as 4.5, which is good to note. I can use Anthropic Sonnet models like 3.5 and 4.6 as benchmarks to show the price has stayed stable. Now, I need to find the exact Opus 4.6 pricing, so I'll check more lines for that.


Clarifying Sonnet and Opus pricing details


Claude Opus 4.6 \ Anthropic


Citing efficiency improvements and vendor claims


I might need citations for the 2023 Anthropic pricing, either from a PDF or a screenshot. Also, I could use the Google claim about models reducing output length by 5-20% for token efficiency. I'll also try to cite Micron’s slide and Nvidia's advances in reducing inference costs and improving performance. I'll focus more on search results and avoid over-relying on vendor claims.


Discussing key semiconductor capacity and risks


I might mention TSMC's logic capacity surpassing 17 million wafers in 2025, using a source for confirmation. Also, TSMC's CoWoS capacity doubling and Micron’s HBM being sold out in 2025 could be crucial points. However, I should be careful with citations since they can be seen as self-serving. I'll include an analysis of how these factors impact supply chain efficiency amidst tight memory bottlenecks.


Structuring a detailed analysis with citations in Chinese


I’ll craft the final response to be detailed but manageable, aiming for around 1200-2500 characters. The introduction will summarize key price drops across providers — including OpenAI, Anthropic, Google, and others — with citations. The first section will cover major price shifts, and the second will highlight pivotal events/technologies such as GPT-4 Turbo and Gemini 1.5.


Considering key technology advancements


I’m thinking about integrating key technologies like distillation, MoE, and sparse attention. For instance, Gemini 1.5 Flash was trained on 1.5 Pro, and DeepSeek’s mixtral model uses MoE with active units. I need to further check FP8 details for DeepSeek V3 to make sure everything aligns.


Analyzing Key AI Pricing and Tech Developments


DeepSeek-V3 正式发布 | DeepSeek API Docs


Discussing pricing trends and output-token pricing


I’m considering pointing out stable mid-tier prices, like for DeepSeek, to show more predictability. Mentioning OpenAI’s batch API discount and Qwen batch pricing will highlight pricing innovation. Also, output-token prices likely won’t drop as quickly as input prices due to the nature of reasoning models’ token generation.


Discussing token reductions and pricing influences


I’m focusing on how providers aim to reduce output token count, with examples like DeepSeek and Google adopting strategies for token compression and cutting context. I’ll mention model retirements too, since complexity grows linearly. Also, I’ll highlight that inference efficiency and prompt caching discounts have helped cut prices.


Discussing cloud deployment and price trends


I’ll point out that Mistral Medium 3 is deployable on any cloud with at least four GPUs, potentially lowering total cost of ownership and increasing pressure on API prices. I'll also mention that not all prices are dropping—DeepSeek V3 had a promo, but V3.1 canceled off-peak discounts due to expanded service.


Discussing Pricing Trends and Model Cost Factors


DeepSeek-V3.1 发布 | DeepSeek API Docs


Discussing future trends and market segmentation


DeepSeek can cancel discounts due to capacity. I’ll also mention that Qwen's batch price is half of real-time prices. Future trends may include smaller distilled models, more MoE/sparse attention, and output-token suppression. I should discuss serving optimization, packaging expansions, and market segmentation. Premium frontier prices may not fall quickly, given reasoning token consumption and enterprise features, but trends like OpenAI 4.1 mini/nano discounts and DeepSeek's nighttime discount cancellation can support this. A concise table might help.


Thought for 21m 5s

先给结论：过去这几年真正持续下降的，不只是“每百万 token 的标价”，而是“单位有效智能的价格”。OpenAI 的高智能通用模型，能从 GPT-4 的 $30 / $60，一路看到 GPT-4 Turbo 的 $10 / $30，再到 GPT-4o 的 $2.5 / $10，以及 GPT-4.1 的 $2 / $8；OpenAI 还明确把这一轮降价归因于 推理系统效率提升。Anthropic 则更多表现为“价格基本不变，但能力持续上升”：Sonnet 线从 3.5 到 4.6 长期维持 $3 / $15，但性能不断增强；Google、Mistral、Qwen、DeepSeek 则在 2024–2025 明显把市场价格带继续往下压。Anthropic+7OpenAI开发者+7OpenAI开发者+7


这里我用的是代表性厂商，不是穷举所有供应商；但这几家已经足够说明主线：降价是模型架构、推理系统、供应链、以及竞争格局共同作用的结果，而不是单一“算力便宜了”。Micron Technology+3OpenAI+3Google Developers Blog+3


1）这几年价格变化背后的关键事件


OpenAI 的关键拐点有三个。第一是 2023 DevDay：OpenAI 发布 GPT-4 Turbo，明确说输入价格比 GPT-4 便宜 3 倍、输出便宜 2 倍。第二是 2024 年 5 月 GPT-4o：OpenAI 说它在英语文本和代码上可媲美 GPT-4 Turbo，但 API 快很多且便宜 50%。第三是 2025 年 4 月 GPT-4.1：OpenAI 直接写明，GPT-4.1 系列更便宜是因为 inference systems 的效率改进，并因此开始弃用更贵、更重的 GPT-4.5 Preview。这个序列说明，OpenAI 的降价不是“原模型硬砍价”，而是用更高效的新模型替换旧模型。OpenAI+4OpenAI+4OpenAI+4


Anthropic 的关键事件不是“频繁降价”，而是 定价分层 + 同价升级。2023 年的 Claude 2 官方公开价还是 $11.02 / $32.68；到 2024 年 Claude 3 家族，Anthropic 把产品分成 Opus、Sonnet、Haiku 三档，其中 Sonnet 定在 $3 / $15。随后 Claude 3.5 Sonnet、3.7 Sonnet、4.5、4.6 基本都维持这个价位，同时官方反复强调“same price, better performance”；到 Opus 4.6，Anthropic 也没有把价格抬回 Claude 3 Opus 那种 $15 / $75 的高位，而是定在 $5 / $25，再叠加 prompt caching 最高 90% 和 batch 50% 折扣。对客户来说，这种路径本质上也是“变便宜”。Anthropic+6www-cdn.anthropic.com+6Anthropic+6


Google 的关键事件集中在 2024 年 Gemini 1.5 系列。Google 明确说 Gemini 1.5 Flash 是由 1.5 Pro 蒸馏得到的高效模型；8 月把 1.5 Flash 的输入/输出价格分别下调 78% / 71% 到 $0.075 / $0.3；10 月又把 1.5 Pro 在 <128K prompt 档位下调 64% / 52%，连 cached tokens 也一起降 64%。同一时期，Flash-8B 进一步压到 $0.0375 / $0.15。更关键的是，Google 公开写了另一件很少有人注意的事：新版模型默认输出更简洁，长度缩短约 5%–20%，目的就是减少开发者成本。这意味着 Google 不只是降单价，也在降每次请求的输出 token 数。Google Developers Blog+3blog.google+3Google Developers Blog+3


DeepSeek 的关键事件最能说明“价格既受技术影响，也受容量管理影响”。V3 发布时，官方写明它是 MoE 架构，671B 总参数、37B 激活参数，在 14.8T token 上预训练；并且通过算法和工程创新把生成速度从 20 TPS 提到 60 TPS。价格上，V3 上线时官方价改成 0.5 / 2 / 8 元，但又给了 45 天促销价 0.1 / 1 / 2 元。之后 V3.1 通过 CoT 压缩，在输出 token 减少 20%–50% 的同时保持接近原来的表现；但 9 月又取消夜间优惠，同时说明已经进一步扩容 API 资源。到 V3.2-Exp，DeepSeek 直接把降价原因写成了 DSA 稀疏注意力让服务成本显著下降，于是 API 成本再降 50% 以上。这说明 API 价格不是线性下滑，它会同时被技术进步和供给紧张程度拉扯。DeepSeek API 文档+3DeepSeek API 文档+3DeepSeek API 文档+3


Mistral 与 Qwen 的作用更像“把市场锚点往下拖”。Mistral 在 Mixtral 8x22B 上强调 SMoE 架构只激活 39B/141B 参数，先把“高能力不一定高算力”做实；到 2024 年 9 月又对 Nemo、Small、Codestral、Large 分别降价 50%、80%、80%、33%。2025 年的 Mistral Medium 3 继续把价格压到 $0.4 / $2，并宣称很多专业任务接近 Sonnet 3.7、但成本低 8 倍。阿里云这边，2024 年 3 月先调整 Qwen 计费结构，9 月又对 qwen-max、qwen-plus、qwen-turbo 大幅降价；例如 qwen-plus 实时输入从 0.004 元/千 token 降到 0.0008 元/千 token，qwen-turbo 从 0.002 降到 0.0003，而 Batch 价格继续比实时调用更低。这类动作的意义不只是“自己便宜了”，而是把全行业的心理价位一起拉低。阿里云帮助中心+4mistral.ai+4mistral.ai+4


2）API 降价背后的关键技术


最核心的技术方向之一是 “少算很多，但效果别掉太多”。Google 明说 1.5 Flash 是从 1.5 Pro 蒸馏出来的；DeepSeek-V3 和 Mixtral 8x22B 都使用 MoE/SMoE，也就是总参数很大，但每次推理只激活其中一部分；DeepSeek-V3 还用了 FP8 训练与推理支持，V3.2-Exp 再往前一步，用 稀疏注意力 DSA 直接降低长文本服务成本。换句话说，降价不是把同样的计算卖便宜了，而是每个 token 背后的真实计算量被做薄了。DeepSeek API 文档+3blog.google+3DeepSeek API 文档+3


第二个方向是 “让模型少吐字，但别少能力”。Google 公开说更新版 Gemini 默认输出更短、平均缩短 5%–20%；DeepSeek-V3.1 说其 CoT 压缩后，输出 token 减少 20%–50% 而性能基本持平；Anthropic 客户案例里也出现了 up to 65% fewer tokens 的表述。对 API 成本来说，这件事极关键，因为很多模型的输出 token 比输入 token 贵得多，而 reasoning/agent 模型又天然容易“想太多、说太多”。所以未来一段时间，API 变便宜很大概率不是先砍“每百万 token”的牌价，而是先砍“完成同一任务所需的总 token 数”。NVIDIA 投资者网站+3Google Developers Blog+3DeepSeek API 文档+3


第三个方向是 推理系统和服务软件。OpenAI 对 GPT-4.1 的官方说法非常直白：低价来自 inference systems 的效率提升；Anthropic 在 Sonnet 4.6 和 Opus 4.6 上都把 prompt caching 和 batch processing 当成主要省钱手段；NVIDIA 则公开宣称，Blackwell 对 LLM inference 的性能可比同量 H100 提升 30 倍，成本和能耗最高可降 25 倍，而 Dynamo 1.0 还能把 Blackwell 推理性能再拉高到 7 倍。这些说法当然有厂商口径成分，但方向非常一致：模型架构、缓存、批处理、路由、KV/上下文管理、分离式 serving，已经和模型本身一样重要。NVIDIA 投资者网站+5OpenAI+5Anthropic+5


3）“关键产能”到底怎么影响 API 价格


如果把“产量”翻成 LLM 行业真正 relevant 的概念，它更接近 先进制程晶圆、先进封装 CoWoS、HBM、以及整机/机柜的有效供给。TSMC 在 2025Q1 电话会上说，AI 相关需求在 2025 年仍然强劲，AI accelerator 收入预计 翻倍，并计划把 CoWoS 产能在 2025 年翻倍；TSMC 官网还写了其 2025 年逻辑产能超过 1700 万片 12 吋当量晶圆。这说明底层供给确实在扩，但仍是在高速追赶需求。台积电+1


内存和封装的约束也没消失。Micron 在 2025 年材料里说，HBM 的 2025 年 TAM 已上调到 350 亿美元以上，其 2025 年 HBM 产出已售罄，2026 年需求仍然很强；同时 HBM3E 12H 已开始量产，HBM4 将在 2026 年进入量产爬坡。也就是说，供给改善是真的，但高端供给依然紧张也是真的。这正是为什么你会同时看到“低端/中端 API 快速降价”和“最强旗舰不一定跟着同速下降”。Micron Technology


4）API 降价的底层原因，归根到底是什么


我会把底层原因压成五条。


第一，竞争把“能力溢价”打散了。当 GPT-4 时代稀缺性最强时，价格可以明显更高；但一旦 GPT-4 Turbo、GPT-4o、Claude Sonnet、Gemini Flash/Pro、Mistral Medium、DeepSeek-V3 这些模型把“够用甚至很好用”的能力铺到更低价位，厂商就只能靠更高效的下一代模型，而不是靠旧模型高价硬撑。OpenAI 甚至明确因为 GPT-4.1 在很多关键能力上更强或相近、但成本和时延更低，所以开始退 GPT-4.5 Preview。OpenAI+2mistral.ai+2


第二，推理成本的下降越来越来自“系统工程”而不是单一硬件迭代。OpenAI 把 GPT-4.1 降价归因于 inference systems；Google 把蒸馏、tuning、context caching 和更短输出一起用上；Anthropic、Qwen、DeepSeek 都在把 cache、batch、off-peak、compaction 之类手段做成价格体系的一部分。这说明 API 价格越来越像云服务价格：算法效率 + 集群利用率 + 调度策略共同决定毛利空间。DeepSeek API 文档+6OpenAI+6Google Developers Blog+6


第三，供给虽紧，但“单位 token 成本”仍在下降。Micron 甚至在自己的材料里直接说，硬件的显著改进已经降低了生成式 AI 的 per-token cost，而更高效的算法和软件进一步拉低了 inference cost。TSMC、Micron、NVIDIA 这些底层环节给出的信号是一致的：更强芯片 + 更好封装 + 更高带宽 + 更好推理软件，正在不断压低 token 成本，但不会均匀压到所有层级。NVIDIA Newsroom+3Micron Technology+3台积电+3


第四，厂商更愿意降“可计费形态”，而不是一直降 headline list price。OpenAI 把 prompt cache 折扣从 50% 提到 75%，Batch 再打 5 折；Anthropic 的 Sonnet 4.6 / Opus 4.6 也分别给出 90% cache 节省 和 50% batch 节省；Qwen 的 Batch 也明显低于实时调用；DeepSeek 则做过促销价和夜间优惠。对厂商来说，这种做法更好，因为它能把高利用率客户和低利用率客户分层定价，而不是一刀切伤害整体收入。DeepSeek API 文档+4OpenAI+4Anthropic+4


第五，模型越多，维护成本越高，所以“新模型替旧模型”会多于“无限保留旧模型并不断降价”。Anthropic 已经公开写明：把很多模型长期公开提供推理服务，其成本和复杂度会随着服务模型数量大致线性上升，所以退役旧模型是必要的。这解释了为什么很多 API 厂商最终会选择“推出更便宜更强的新 SKU”，而不是长期养着一大堆老 SKU 慢慢打折。Anthropic


5）未来 API 继续降价，更可能往哪些方向走


我认为最可能继续下探的是中低端与高频调用层，不是最强旗舰层。原因是 OpenAI 已经在 GPT-4.1 mini/nano 上展示出非常激进的价格梯度，Google 有 Flash-8B，Mistral 有 Medium 3，DeepSeek 也在 chat / reasoner 双线运营。也就是说，未来更常见的不是“旗舰腰斩”，而是更小、更快、更便宜的分流模型继续出现，再通过 router 把大多数请求导到便宜模型。DeepSeek API 文档+3OpenAI+3Google Developers Blog+3


第二个方向是输出 token 继续被压缩。因为 reasoning 模型会在一次请求里生成成千上万甚至上万 token 来“思考”，所以未来厂商会更重视“思考更短、输出更短、同样正确”。Google 的更短回答、DeepSeek 的 CoT 压缩、Anthropic 客户案例里的 token efficiency，都在朝这个方向走。对企业买方来说，真正该盯的是任务完成成本，而不是名义每百万 token 价格。Anthropic+3NVIDIA 投资者网站+3Google Developers Blog+3


第三个方向是价格体系本身继续金融化/云化：更多 cache、batch、flex、off-peak、region-specific、compliance-specific 定价会出现。Anthropic 已经有 US-only inference 1.1x，OpenAI 和 Anthropic 都在强化 cache 与 batch，DeepSeek 有过时段优惠，Qwen 也把 Batch 单独列价。这类价格机制的目标不是单纯便宜，而是让厂商把集群利用率做满。阿里云帮助中心+4Anthropic+4OpenAI+4


第四个方向是硬件和封装成熟后，低端价格会继续掉，但高端前沿模型未必同步掉。TSMC 在扩 CoWoS，Micron 在推 HBM4，NVIDIA 在推 Blackwell 和 Dynamo，这些都会继续压低单位 token 成本；但同时 HBM 仍紧、推理需求仍爆发、agent/reasoning 任务又更吃算力，所以最强模型的价格下降速度大概率会慢于中小模型。换句话说，未来更便宜是大概率，但“最强模型也按同样速度降价”不是大概率。这是我基于当前供应链和厂商产品策略做出的判断。Anthropic+4台积电+4Micron Technology+4


最后压成一句话：API 降价的底层，不是“模型突然慈善了”，而是“单位有效智能的供给曲线在右移”。推动它右移的，是架构效率、输出压缩、serving 软件、芯片/封装扩产，以及更激烈的市场竞争；而阻止它无限快下移的，是 HBM/封装等高端供给仍紧、reasoning 带来的 token 膨胀、以及企业级 SLA/合规成本。Anthropic+5DeepSeek API 文档+5DeepSeek API 文档+5


下一步最适合把这份分析压成一页汇报版：时间线、关键事件、技术驱动、供应约束、未来判断。



Sources:


https://developers.openai.com/api/docs/models/gpt-4

https://openai.com/index/gpt-4-1/

https://www-cdn.anthropic.com/90df03aed08b794ab03c5a7bf28b2ad9cf26cf3c/model_pricing_july2023.pdf

https://blog.google/innovation-and-ai/products/google-gemini-update-flash-ai-assistant-io-2024/

https://api-docs.deepseek.com/zh-cn/news/news1226

https://mistral.ai/news/mixtral-8x22b

https://developers.googleblog.com/zh-hans/updated-gemini-models-reduced-15-pro-pricing-increased-rate-limits-and-more/

https://investor.tsmc.com/chinese/encrypt/files/encrypt_file/reports/2025-04/7630274eecc1197a4e3ea6a415f44a47204fe10a/TSMC%201Q25%20Transcript.pdf

https://investors.micron.com/static-files/df96216e-3e07-4b97-a4ef-df0a5fa684d6

https://www.anthropic.com/research/deprecation-commitments

https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Dynamo-Open-Source-Library-Accelerates-and-Scales-AI-Reasoning-Models/default.aspx
