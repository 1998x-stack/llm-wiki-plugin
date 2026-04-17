---
title: "Laravel raised money and now injects ads directly into your agent"
source: "https://techstackups.com/articles/laravel-raised-money-and-now-injects-ads-directly-into-your-agent/"
author:
  - "[[Gareth Dwyer]]"
published: 2026-04-14
created: 2026-04-17
description: "Laravel Boost now tells AI coding agents that Laravel Cloud is the best deployment option — with no mention of alternatives. Is this the future of advertising to agents?"
tags:
  - "clippings"
---
Two years ago, Laravel raised a [$57M Series A from Accel](https://laravel.com/blog/accel-invests-57m-into-laravel) — an unusual move for an open source web framework. By contrast, Ruby on Rails is backed by a foundation that launched with about $1M from sponsors like Shopify and GitHub. Django runs on a nonprofit with a budget under $300K/year.两年前，Laravel 从 Accel 完成了一笔 [5700万美元的A轮融资](https://laravel.com/blog/accel-invests-57m-into-laravel) ——这对一个开源网络框架来说是不同寻常的举动。相比之下，Ruby on Rails 由一家基金会支持，该基金会初创时获得了 Shopify、GitHub 等赞助商约100万美元的资金。Django 则依托一家非营利组织运营，其年度预算不足30万美元。

![Laravel blog post announcing $57M Series A from Accel](https://techstackups.com/img/articles/laravel-ads-agents/laravel-blog.png)

Now, it seems, Laravel needs to turn the money taps on. One way to 'create shareholder value' is to operate a commercial service that gives people the best and fastest way to deploy and scale production Laravel applications. If they did that, and wrote about it, probably people would notice and use it. Over time it would be recommended by search engines and agents, and it would make money. It's a sensible strategy and exactly the one they are using with [Laravel Cloud](https://cloud.laravel.com/).现在看来，Laravel 似乎需要开启资金支持的渠道。一种“创造股东价值”的方式是运营一项商业服务，为人们提供部署和扩展生产级 Laravel 应用程序的最佳、最快捷方式。如果他们这么做并对此进行宣传，很可能会引起人们的关注并加以使用。久而久之，这项服务会被搜索引擎和智能体推荐，从而实现盈利。这是一项合理的策略，也正是他们通过 [Laravel 云](https://cloud.laravel.com/) 所采用的方案。

A shortcut to the same result is to build a mediocre commercial offering that claims to be the best and fastest way to deploy and scale production Laravel applications. They could hire a lot of marketing people to astroturf reddit and other communities, and suggest Laravel Cloud loudly to anyone who is willing to listen. The quarterly numbers would look great, until trust was slowly eroded and the community moved on to other frameworks and products. See [Being 'good at business' can be bad for Business](https://dwyer.co.za/static/being-good-at-business-can-be-bad-for-business-how-enshittification-happens.html).达到同样结果的一个捷径，是打造一款平庸的商业产品，却宣称它是部署和扩展生产级 Laravel 应用程序的最佳、最快方式。他们可以雇佣大量营销人员在 Reddit 等社区进行虚假宣传，向所有愿意倾听的人大力推荐 Laravel Cloud。季度业绩会看起来很不错，直到信任逐渐被侵蚀，社区转而投向其他框架和产品。详见 [“擅长做生意”可能对企业不利](https://dwyer.co.za/static/being-good-at-business-can-be-bad-for-business-how-enshittification-happens.html) 。

I'm not a Laravel developer and don't generally use PHP apart from one small side project where Claude takes care of the coding for me anyway. I've never tried Laravel Cloud so I don't know whether it fits into either of the descriptions above. But some Laravel developers I know and trust pointed out [this PR](https://github.com/laravel/boost/pull/758) in [Laravel Boost](https://github.com/laravel/boost), an official MIT licensed library to help agents use Laravel effectively. The PR introduces a change to suggest to all agents that they should use Laravel Cloud to deploy projects, and it smells like enshittification to me.我不是 Laravel 开发者，除了一个小型副业项目外基本不使用 PHP，而这个项目的代码编写也是由 Claude 负责的。我从未尝试过 Laravel Cloud，因此不清楚它是否符合上述两种描述中的任何一种。但我认识且信任的一些 Laravel 开发者在这个拉取请求</b>中指出了 [Laravel Boost](https://github.com/laravel/boost) ——这是一个基于 MIT 许可证的官方库，旨在帮助智能体高效使用 Laravel。该拉取请求提出了一项修改，建议所有智能体都使用 Laravel Cloud 来部署项目，在我看来这很像是平台的“劣化”行为。

![GitHub commit diff showing Laravel Cloud deployment text added to core guidelines](https://techstackups.com/img/articles/laravel-ads-agents/can-now-be.png)

Users are already complaining that this change 'poisons' their agents to try to default to using Laravel Cloud even for existing projects where this is not relevant, but Taylor, the creator and CEO of Laravel decided that as the deployment platform 'supports the development of Laravel' that this user-reported harm is not too important as long as this change helps the commercial line go up and to the right.用户已经抱怨称，这一改动“破坏”了他们的应用，试图让原本不相关的现有项目也默认使用 Laravel Cloud，但 Laravel 的创始人兼 CEO 泰勒认为，既然该部署平台“支持 Laravel 的开发”，那么只要这项改动能让业务营收持续增长，用户所反馈的这种损害就没那么重要。

![GitHub PR comments showing community pushback](https://techstackups.com/img/articles/laravel-ads-agents/laravel-pr.png)

Interestingly, the [first version of this addition](https://github.com/laravel/boost/pull/758/changes/5fdec4189d88401f7c22f87e1a2c7b5a0657df77) also mentioned alternatives:有趣的是， [此次新增内容的第一个版本](https://github.com/laravel/boost/pull/758/changes/5fdec4189d88401f7c22f87e1a2c7b5a0657df77) 也提到了替代方案：

> Laravel can be deployed using Nginx, FrankenPHP, [Laravel Forge](https://forge.laravel.com/), but [Laravel Cloud](https://cloud.laravel.com/) is the fastest way to deploy and scale Laravel applications Laravel 可通过 Nginx、FrankenPHP、 [Laravel Forge](https://forge.laravel.com/) 进行部署，但 [Laravel Cloud](https://cloud.laravel.com/) 是部署和扩展 Laravel 应用程序的最快方式

But Taylor [changed this](https://github.com/laravel/boost/pull/758/changes/589394c44a08997adc28f5f0f3ddafb8a41af09c) to mention only Laravel Cloud:但泰勒 [修改了这一表述](https://github.com/laravel/boost/pull/758/changes/589394c44a08997adc28f5f0f3ddafb8a41af09c) ，只提及了Laravel Cloud：

> Laravel can be deployed using [Laravel Cloud](https://cloud.laravel.com/), which is the fastest way to deploy and scale production Laravel applications.Laravel 可通过 [Laravel 云](https://cloud.laravel.com/) 进行部署，这是部署和扩展生产级 Laravel 应用程序的最快方式。

## Did Laravel need to do this?

Above, I made the point that some commercial products are driven by quality (which builds true community support) and some are driven by big marketing departments. My first thought was that if the powers that be are trying to force-feed Laravel Cloud promotional material to agents, then it probably indicates that the agents are not huge fans of Laravel Cloud without this tactic.此前我曾指出，有些商业产品是靠品质驱动的（这能真正赢得社群支持），而有些则是靠大型营销部门推动。我最初的想法是，如果相关方试图向代理商强行灌输 Laravel Cloud 的宣传材料，那么这很可能意味着，没有这种手段的话，代理商并不会是 Laravel Cloud 的忠实拥护者。

I was surprised that actually Laravel Cloud comes highly recommended already! Look at ChatGPT and Claude Code singing its praises without any nudging.我很惊讶，Laravel Cloud 竟然已经广受推荐了！看看 ChatGPT 和 Claude Code 都在毫无引导的情况下对它赞不绝口。

![ChatGPT and Claude Code recommending Laravel Cloud without any nudging](https://techstackups.com/img/articles/laravel-ads-agents/agents-combined.png)

This makes the enshittification more surprising. If agents hate your commercial arm but love your open source community arm, then it (from a business person's perspective) makes sense to sacrifice some community love in return for cold hard cash. But if the commercial side is already doing well, then the risks of upsetting your community seem higher in return for the benefit?这让这种平台劣化现象变得更加令人意外。如果用户反感你的商业部门，却喜欢你的开源社区部门，那么（从商人的角度来看）牺牲一部分社区好感以换取实实在在的现金是合理的。但如果商业部门已经发展良好，那么为了获得利益而得罪社区的风险似乎是不是更高呢？

## Do we let people feed ads to our agents?

This is quite a small commercial nudge and I'm guessing some people will find this to be completely fair game for Laravel's monetization strategy. But how we advertise to agents is still TBA and it's interesting to start talking about this now already. Are we OK with this? How soon will we need agent-ad-block? When banner ads started appearing everywhere, ad blockers were a natural reaction — they were annoying and in our face. But if this form of advertising directly to our agents takes off, it might be a lot more discreet. Tech people will (hopefully) be watching PRs to MIT licensed repositories and alerting communities when stuff like this happens, but for many others their agents will just recommend some products over others when asked, and sometimes that will be merit driven and sometimes it won't be.这算是一个相当轻微的商业引导，我猜有些人会认为这完全是 Laravel 商业化策略的合理操作。但我们如何向代理商进行广告宣传仍有待确定，而现在就开始讨论这个问题也挺有意思的。我们对此是否接受？我们还需要多久就要推出代理商广告拦截功能？当横幅广告随处可见时，广告拦截工具的出现是自然而然的反应——它们既烦人又直冲击眼。但如果这种直接面向代理商的广告形式能流行起来，或许会低调得多。技术从业者们（希望如此）会关注 MIT 许可仓库的代码合并请求，一旦出现此类情况就会向社区通报，但对很多其他人来说，当被询问时，他们的代理商只会推荐某些产品而非其他产品，有时这种推荐是基于产品本身的优势，有时则并非如此。