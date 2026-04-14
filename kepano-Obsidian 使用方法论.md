# Obsidian 使用方法论

**User:**   
**Created:** 4/12/2026 14:54:06  
**Updated:** 4/14/2026 23:18:13  
**Exported:** 4/14/2026 23:18:53  
**Link:** [https://chatgpt.com/c/69db417a-de5c-8324-ad06-d0f94e77313b](https://chatgpt.com/c/69db417a-de5c-8324-ad06-d0f94e77313b)  

## Prompt:
4/12/2026, 2:54:05 PM

2026-04-12 14:54:05

https://github.com/kepano/kepano-obsidian

obsidian 使用技巧方法论 深度思考分析调研，给出详细易懂解读

## Response:
4/12/2026, 2:54:06 PM

2026-04-12 14:54:06

我先基于你给的仓库和 Obsidian 官方资料做一轮梳理，把「工具技巧」和「方法论」分开讲，再给你一个适合大多数人的实用工作流。

我已经确认这个仓库本质上不是“插件教程”，而是 Steph Ango 的一套个人 vault 模板。接下来我会把它拆成三层：底层理念、仓库结构、落地用法。

> **研究GitHub仓库和Obsidian技巧解析**
>
> [GitHub - kepano/kepano-obsidian: My personal Obsidian vault template. A bottom-up approach to note-taking and organizing things I am interested in. · GitHub](https://github.com/kepano/kepano-obsidian)
>
> **搜索 Steph Ango 和官方 Obsidian 文档**
>
> [How I use Obsidian — Steph Ango](https://stephango.com/vault)
>
> **搜索Obsidian官方文档信息**
>
> [Obsidian Unlimited - Obsidian Help](https://help.obsidian.md/Licenses/Obsidian%2BUnlimited)
>
> **搜索Obsidian帮助文档与功能指南**
>
> [Daily notes - Obsidian Help](https://obsidian.md/help/plugins/daily-notes)
> [每日笔记、日程管理、工作复盘——这是我钻研出的 Obsidian ...](https://sspai.com/post/72385)
> [Obsidian 达人成长之路 #5：使用 Templater 减少重复工作 ...](https://zhuanlan.zhihu.com/p/703459656)
> [obsidian-chinese-help/属性（Properties）.md at master - GitHub](https://github.com/cyddgh/obsidian-chinese-help/blob/master/%E5%B1%9E%E6%80%A7%EF%BC%88Properties%EF%BC%89.md)
> [How to Use Backlinks in Obsidian - Alphr](https://www.alphr.com/obsidian-how-to-use-backlinks/)
>
> **查找相关文章和文档页面**
>
> [How I use Obsidian — Steph Ango](https://stephango.com/vault)
> [Daily notes - Obsidian Help](https://obsidian.md/help/plugins/daily-notes)
>
> **搜索Obsidian的官方功能和插件**
>
> [Obsidian Unlimited - Obsidian Help](https://help.obsidian.md/Licenses/Obsidian%2BUnlimited)
>
> **考虑是否需要进一步搜索**
>
> 搜索结果不理想，可能不需要继续搜索。我可以从文章中提取信息，保持详细但简洁。也许可以更深入地检查仓库结构，看看从第41行开始的内容。
>
> **检查代码库结构及第41行起内容**
>
> [How I use Obsidian — Steph Ango](https://stephango.com/vault)
> [GitHub - kepano/kepano-obsidian: My personal Obsidian vault template. A bottom-up approach to note-taking and organizing things I am interested in. · GitHub](https://github.com/kepano/kepano-obsidian)
>
> 已思考 31s

我认真看了你给的这个仓库和它配套文章，先说结论：

**`kepano/kepano-obsidian` 的价值，不在于“教你怎么把 Obsidian 折腾得很复杂”，而在于它展示了一种很克制、很长期主义的笔记方法。**  
它的核心不是插件，而是三句话：

1.  **文件优先，而不是应用优先**
2.  **少分类，多链接**
3.  **先记录，再让结构慢慢长出来** [Steph Ango+2Steph Ango+2](https://stephango.com/file-over-app)

下面我把它拆开讲，用“理念 → 仓库结构 → 使用技巧 → 适合谁 → 怎么落地”的方式，尽量讲得易懂。

* * *

一、这个仓库到底是什么
-----------

这个 GitHub 仓库并不是一个插件，也不是一套“标准答案”，而是 **Steph Ango 的个人 Obsidian vault 模板**。仓库 README 明确写了：这是他自己的 Obsidian 仓库模板，体现的是一种 **bottom-up approach**，也就是“**自下而上**”的笔记与组织方式；并且他强调这**并不教条**，你应该只拿走适合自己的部分。仓库目录里能看到 `.obsidian`、`Attachments`、`Categories`、`Clippings`、`Daily`、`Notes`、`References`、`Templates` 等文件夹。[GitHub+1](https://github.com/kepano/kepano-obsidian)

这点很重要，因为很多人第一次接触 Obsidian 时会误以为：

*   要先设计一套完整分类体系
*   要先装很多插件
*   要先搭建一套“知识管理系统”

但这套仓库的思想刚好相反：  
**先开始写，结构以后再说。** [Steph Ango](https://stephango.com/vault)

* * *

二、这套方法论最核心的思想
-------------

### 1\. File over app：文件比软件更重要

Steph 强调，vault 本质上只是一个**文件夹**。他认同的是 “file over app” 哲学：  
如果你希望你的数字内容能长期存在，那么它最好是你自己能控制的文件，而且格式要足够通用、容易读取。Markdown 纯文本正符合这个要求。[Steph Ango+1](https://stephango.com/vault)

通俗讲就是：

*   不要把自己的知识完全锁进某个产品的数据库里
*   软件会变，文件更耐久
*   未来你换工具时，Markdown 文件大概率还能继续用

这其实不是 Obsidian 技巧，而是 **知识资产观**。  
真正有价值的不是“你会不会某个插件”，而是“你的笔记能不能十年后还读得懂”。

* * *

### 2\. Bottom-up：不要先搭系统，先留下痕迹

这套方法最有代表性的一句，是它“embraces chaos and laziness to create emergent structure”——  
也就是：**接受一点混乱，接受一点懒惰，让结构自然浮现。** [Steph Ango](https://stephango.com/vault)

什么意思？

很多人做笔记时，最大的阻力不是“不会写”，而是：

*   这条该放哪个文件夹？
*   这个主题属于学习/工作/生活哪类？
*   标签该用 singular 还是 plural？
*   这是不是值得单独建一篇笔记？

这些判断会严重拖慢记录动作。

这套方法认为：  
**记录时不要做太多组织决策。先记下来，之后靠链接、回顾、聚合把结构慢慢长出来。**

这是一种典型的“低摩擦输入，高价值整理”的思路。

* * *

### 3\. 少用文件夹，多用链接与属性

Steph 明确说自己**尽量避免用文件夹组织内容**，因为很多内容会跨多个主题；他也不用嵌套子文件夹，平时导航主要依赖 quick switcher、backlinks、以及笔记里的 internal links。笔记主要通过 `categories` 属性来组织，并借助 Obsidian 的 Bases 按分类查看。[Steph Ango](https://stephango.com/vault)

这背后的思想是：

*   **文件夹是单继承**：一个文件通常只能“放在一个地方”
*   **链接和属性是多维组织**：一条内容可以同时属于多个上下文

举个简单例子：  
一篇《任天堂商业模式》笔记，可能同时属于：

*   游戏行业
*   商业模式
*   日本公司
*   产品策略

如果你靠文件夹，只能硬塞进一个目录；  
如果你靠属性和链接，就可以多维呈现。

这就是为什么 Obsidian 的核心能力不是“目录树”，而是：

*   双链
*   反向链接
*   属性
*   搜索
*   模板

官方文档里，Properties 用于给笔记加结构化信息，支持文本、列表、数字、日期、标签等类型；Backlinks 则专门用来查看哪些笔记链接到了当前笔记。[Obsidian+1](https://obsidian.md/help/properties)

* * *

三、这套仓库结构，分别在解决什么问题
------------------

### 1\. Root 根目录：放“我自己的东西”

Steph 说，他的大多数笔记都在 vault 根目录，而不是某个文件夹里。  
根目录里的内容主要是：

*   journal entries
*   essays
*   evergreen notes
*   其他与自己直接相关的内容 [Steph Ango](https://stephango.com/vault)

也就是：  
**凡是“我写出来的、属于我思考的一部分”的内容，尽量放在主视野里。**

这其实很巧妙。因为它把“我的思考”放在中心，而不是把“分类体系”放在中心。

* * *

### 2\. References：放外部世界对象

他把书、电影、地点、人物、播客这类“外部存在的对象”放进 `References`。并且命名通常直接用标题，比如 `Book title.md`、`Movie title.md`。[Steph Ango](https://stephango.com/vault)

这说明他区分了两类笔记：

*   **我自己的思考**
*   **我在思考的对象**

这个区分特别有用。因为很多人笔记混乱，是把“对象资料”和“自己的观点”写在一起。

更好的方式往往是：

*   `Atomic Habits.md`：书的资料、摘录、评价
*   `习惯设计的行为杠杆.md`：你自己的长期笔记

前者是 reference note，后者是 evergreen note。  
这样更利于长期演化。

* * *

### 3\. Clippings：放别人写的内容

`Clippings` 专门保存别人写的文章、网页摘录。Steph 也提到自己会用 Web Clipper 把网页存进来。[Steph Ango](https://stephango.com/vault)

这个设计非常关键，因为它避免了一个常见问题：

> 把“收藏”误当成“理解”。

你看到一篇好文章，先剪藏进 `Clippings`；  
以后真的消化了，再长成你自己的 note。  
这相当于把“输入仓”和“思考仓”分开。

* * *

### 4\. Daily：不是拿来写长日记，而是时间索引

很有意思的一点：Steph 说 `Daily` 文件夹中的 daily notes **主要用于被其他笔记链接到**，他自己**并不在 daily notes 里写东西**；这些日记文件只是按 `YYYY-MM-DD.md` 命名，作为时间锚点存在。[Steph Ango](https://stephango.com/vault)

这和很多人理解的“日记本”不一样。  
他的 daily note 更像是：

*   一个时间坐标
*   一个聚合入口
*   一个可链接的日期对象

这很高级，因为它把“日期”从普通文本变成了知识网络里的节点。

官方文档也说明 Daily notes 核心插件会基于当天日期创建或打开一篇日记，并支持模板；默认命名就是 `YYYY-MM-DD`。[Obsidian](https://obsidian.md/help/plugins/daily-notes)

* * *

### 5\. Templates：把重复动作压缩掉

官方 Templates 插件支持设置模板目录，用命令插入模板内容，也支持 `{{date}}`、`{{time}}`、`{{title}}` 这类变量。[Obsidian](https://obsidian.md/help/Plugins/Templates)

这和这套仓库的方法论是匹配的：  
**模板不是为了形式感，而是为了减少重复劳动。**

模板最适合：

*   会议纪要
*   阅读笔记
*   书/电影/播客条目
*   周复盘
*   文章卡片

本质上是在问：  
有哪些笔记类型，你每次都在重复同样的骨架？

* * *

四、这套方法里最值得学的 6 个“使用技巧”
----------------------

1\. 先写链接，哪怕目标页面还不存在
-------------------

Steph 说他会大量使用 internal links，而且经常是**未创建的链接**。他认为 unresolved links 很重要，因为它们是未来连接的面包屑。[Steph Ango](https://stephango.com/vault)

这招非常强，原因是：

*   你不用等“想清楚了”再建笔记
*   你可以先把概念挂出去
*   未来再回来补完

例如你写：

`这让我想到 [[产品护城河]] 和 [[游戏内生增长]]。`

哪怕这两篇还没写，也没关系。  
这相当于你在给未来的自己布线。

很多高手用 Obsidian 的本质，不是“存档”，而是“**提前搭关系**”。

* * *

2\. 第一提及时就链接
------------

他提到自己会尽量在某个对象**第一次出现时就加链接**。[Steph Ango](https://stephango.com/vault)

这条看似小，其实很有复利。

因为如果你每次第一次提到一个概念都链接，几年后你的 vault 会自动形成：

*   人物网络
*   作品网络
*   主题网络
*   事件网络

而不是一堆互相孤立的笔记。

* * *

3\. 用属性做“轻数据库”，不要急着上复杂插件
------------------------

官方 Properties 支持文本、列表、数字、日期、标签等；属性名一旦定型，可以在整个 vault 内统一使用。[Obsidian](https://obsidian.md/help/properties)

这意味着你完全可以先用非常轻的结构：

```
---
categories:
  - books
status: unread
rating: 6
author: 某某
date: 2026-04-12
---
```

这已经足够支撑很多查询、筛选和归档需要。  
对多数人来说，先把属性用顺，比一上来研究 Dataview 更重要。

* * *

4\. 用 Backlinks 代替“我该把它放哪”
--------------------------

官方 Backlinks 会显示 linked mentions 和 unlinked mentions，也支持在侧边栏或文档底部查看。[Obsidian](https://obsidian.md/help/plugins/backlinks)

它的真正价值不是“看谁链到了我”，而是：

> 当你不确定一条内容属于哪里时，先随便写；以后通过反链去发现它实际上和哪些主题相连。

这就是从“归档式思维”切到“网络式思维”。

* * *

5\. 做分形回顾：碎片 → 周/月 → 年
----------------------

Steph 说他平时会用 unique note 快速记录单条想法，形成带时间前缀的碎片笔记；然后每几天回顾这些碎片，汇总 salient thoughts；再月度回顾这些回顾，年度再回看月度内容。他把这个叫 **fractal journaling**。[Steph Ango](https://stephango.com/vault)

这是整套方法最有含金量的一部分。

因为知识管理最难的不是“输入”，而是：

*   如何避免碎片淹没自己
*   如何让零散内容长成主题
*   如何让短期记录变成长期洞见

分形回顾解决的正是这个问题：

*   **日级**：捕捉
*   **周级**：筛选
*   **月级**：归纳
*   **年级**：抽象

这比“每天记很多、从不复盘”强太多了。

* * *

6\. 定期 random revisit，随机重访旧笔记
-----------------------------

Steph 每隔几个月会做一次 “random revisit”，用 random note 随机跳转旧笔记，并结合 local graph 查看关联，借此重访旧想法、补全缺失链接、寻找灵感。[Steph Ango](https://stephango.com/vault)

这招特别适合长期使用者，因为大多数笔记系统死掉，不是因为输入不够，而是因为：

*   旧内容再也没被看到
*   旧洞见没有被二次利用
*   笔记库变成“数字坟场”

随机重访本质上是在对抗遗忘和沉没成本。  
它让你的 vault 从“存储系统”变回“思考系统”。

* * *

五、我对这套方法论的深度评价：它强在哪里，弱在哪里
-------------------------

强项 1：极低摩擦，适合长期坚持
----------------

它天然降低了三个阻力：

*   分类阻力
*   命名阻力
*   结构设计阻力

所以特别适合那些：

*   想长期写，但容易被“系统搭建”拖住的人
*   脑子里想法很多，但讨厌管理的人
*   需要快速记工作/阅读/生活碎片的人

* * *

强项 2：结构是“长出来的”，不是“设计出来的”
------------------------

这是最重要的优点。

很多人搭的系统一开始非常漂亮，但一个月后废掉。  
原因不是执行力差，而是系统太依赖前期假设。

Steph 这套方法相反，它假设：

*   你不知道未来会写什么
*   你不知道哪些主题会持续增长
*   你不知道哪些内容日后会变重要

所以先留下链接和片段，再让高频主题自然浮现。  
这更符合真实思考过程。

* * *

强项 3：非常适合“内容型脑力工作”
------------------

比如：

*   写作者
*   研究者
*   产品经理
*   策略岗位
*   创作者
*   阅读量大的人

因为这些工作本来就是：

*   输入大量材料
*   形成自己的理解
*   反复跨主题连接
*   最终产出观点或作品

而这套系统最擅长的，就是“连接”和“复用”。

* * *

弱项 1：对极强流程型任务不一定最优
------------------

如果你的主要需求是：

*   严格项目管理
*   复杂任务流转
*   多人协作数据库
*   高度结构化知识表单

那这套方法未必是最佳。  
因为它偏个人思考系统，不是团队流程系统。

* * *

弱项 2：太自由，容易让初学者“看起来很高级，做起来很散”
-----------------------------

“接受混乱”这件事，本身需要成熟度。  
否则初学者很容易演变成：

*   什么都记
*   但不回顾
*   只会双链
*   没有产出

所以这套方法成立的前提是：  
**你必须建立回顾机制。**

没有回顾，bottom-up 只会变成 bottomless。

* * *

弱项 3：不适合把“收集”误认为“思考”的人
----------------------

如果你只是：

*   网页狂剪藏
*   书摘狂复制
*   标签越打越多
*   真正自己的 note 很少

那这套系统也救不了你。  
因为它的精华从来不是 “clip more”，而是 “connect and revisit”。

* * *

六、给普通用户的易懂版落地方案
---------------

下面我给你一个更适合大多数人的 **简化版**，保留这套思想，但不要求你完全照搬。

### 第一步：只保留 5 类区域

你可以这样开始：

*   `Inbox`：临时输入
*   `Notes`：你自己的思考
*   `References`：书/人/公司/产品/地点等对象
*   `Clippings`：网页/摘录
*   `Templates`：模板

已经够用了。  
不要一开始建 20 个文件夹。

* * *

### 第二步：统一 4 条最小规则

你只要先定下面 4 条就够：

1.  日期全部用 `YYYY-MM-DD`
2.  标签永远用复数或永远用单数，不要混用
3.  第一次提到重要对象时就加 `[[链接]]`
4.  每周至少做一次回顾

这和 Steph 的“consistent style”是一致的：  
风格统一，不是为了美观，是为了减少未来决策成本。[Steph Ango](https://stephango.com/vault)

* * *

### 第三步：先用 3 个模板

建议先做：

**1）会议模板**

```
---
date: {{date}}
categories:
  - meetings
---

# {{title}}

## 背景
## 结论
## 待办
- [ ]
## 相关链接
- [[]]
```

**2）阅读/文章模板**

```
---
date: {{date}}
categories:
  - readings
source:
status:
---

# {{title}}

## 摘要
## 我认同的点
## 我不同意的点
## 可延展的问题
- [[]]
```

**3）周回顾模板**

```
---
date: {{date}}
categories:
  - reviews
---

# Weekly Review

## 本周发生了什么
## 哪些事值得继续
## 哪些问题反复出现
## 下周最重要的三件事
- [ ]
- [ ]
- [ ]
```

官方 Templates 插件本身就支持模板目录和日期变量，不必一开始就上更复杂方案。[Obsidian](https://obsidian.md/help/Plugins/Templates)

* * *

### 第四步：把 Daily Note 当“入口”，不要当负担

Daily notes 最适合做这些：

*   当天临时想法
*   碎片记录
*   会议入口
*   临时 TODO
*   当天看到的关键词链接

官方 Daily notes 插件本来就是为“基于日期打开或创建当天笔记”设计的，并支持模板。[Obsidian](https://obsidian.md/help/plugins/daily-notes)

重点不是把每天写成作文，  
而是让你**永远有一个低门槛落点**。

* * *

### 第五步：每周做一次“碎片升维”

这是整套系统最关键的动作。

每周找 20 分钟，做 3 件事：

1.  看这一周的 Daily / Inbox
2.  把值得留下的内容升级成正式 note
3.  给它们补链接、补属性、补一句自己的判断

你会发现，Obsidian 真正的价值，不在输入那一下，而在“**二次加工**”。

* * *

七、最容易踩的坑
--------

### 坑 1：把 Obsidian 用成收藏夹

看到什么都存，最后什么都不用。

### 坑 2：把 Obsidian 用成玩具

主题、CSS、插件装了一堆，内容没长出来。

### 坑 3：过早追求完美分类

分类系统设计得越精细，越不容易长期执行。

### 坑 4：只有记录，没有回顾

没有回顾，链接网络不会真正形成。

### 坑 5：记了很多“信息”，没记“判断”

真正能积累的是你的看法，不只是资料本身。

* * *

八、我给这套方法的一句话总结
--------------

**这不是一套“整理笔记”的方法，而是一套“降低记录摩擦、放大长期连接、通过回顾让思考结晶”的方法。**

它最值得学的不是界面，不是主题，不是目录结构，而是这几个观念：

*   **知识要保存为你能控制的文件**
*   **结构不必预设，可以生长**
*   **链接比分类更接近真实思考**
*   **回顾比记录更重要**
*   **一致的规则比复杂的规则更有用** [Obsidian+3Steph Ango+3Steph Ango+3](https://stephango.com/vault)

* * *

九、如果你现在就想开始，用这个最小可行方案
---------------------

今天就做这 5 步：

1.  新建一个 vault
2.  开启 `Daily notes`、`Templates`、`Backlinks` 核心插件 [Obsidian+2Obsidian+2](https://obsidian.md/help/plugins/daily-notes)
3.  建 3 个文件夹：`References`、`Clippings`、`Templates`
4.  做一个 daily template 和 weekly review template
5.  从今天开始，遇到任何值得记的东西，直接写进当天笔记，并对关键概念加 `[[链接]]`

执行两周后，你就会开始理解这套仓库真正厉害的地方。

如果你愿意，我下一条可以直接继续给你整理一份：

**「适合中文用户的 Obsidian 最佳实践清单」**，或者  
**「按产品经理 / 研究学习 / 写作输出 三种场景的 Obsidian 工作流模板」**。

---

**Sources:**

- [File over app — Steph Ango](https://stephango.com/file-over-app)
- [GitHub - kepano/kepano-obsidian: My personal Obsidian vault template. A bottom-up approach to note-taking and organizing things I am interested in. · GitHub](https://github.com/kepano/kepano-obsidian)
- [Properties - Obsidian Help](https://obsidian.md/help/properties)

## Prompt:
4/12/2026, 3:20:36 PM

2026-04-12 15:20:36

适合中文用户的 Obsidian 最佳实践清单

## Response:
4/12/2026, 3:20:38 PM

2026-04-12 15:20:37

我会把它整理成一份能直接照着用的中文清单，重点放在中文环境里最常见的问题：命名、链接、标签、模板、检索、输入法兼容和长期维护。

> **浏览官方文档和相关资源**
>
> [属性 - Obsidian 中文帮助](https://obsidian.md/zh/help/properties)
> [File over app - Steph Ango](https://stephango.com/file-over-app)
>
> 已思考 9s

下面这份我按“**适合中文用户**”来写，不追求花哨系统，目标只有两个：

**更容易坚持**，以及 **以后更容易找回、复用、产出**。

我先给结论：

> 对中文用户来说，Obsidian 最重要的不是插件，而是 **命名一致、链接清晰、模板轻量、回顾固定、搜索可用**。  
> 真正常见的问题也不是“不会高级功能”，而是“中文命名混乱、标签失控、记了但找不到、收藏很多却没沉淀”。

* * *

一、先定一个总原则
=========

1\. 把 Obsidian 当“自己的文件库”，不是某个炫酷 App
-----------------------------------

Steph Ango 强调，vault 本质上就是一个文件夹；长期有价值的是你能控制的文件，而不是被某个产品锁住的数据。Obsidian 的优势正是基于本地文件和通用格式。[Steph Ango+1](https://stephango.com/file-over-app?utm_source=chatgpt.com)

对中文用户最实用的理解是：

*   你写的是 **Markdown 文件**
*   文件名、目录、属性、链接，未来都还能迁移
*   所以一开始就要用 **长期可维护** 的方式，而不是为了短期爽感折腾系统

* * *

二、中文用户最推荐的目录结构
==============

不要一开始建很多层目录。  
建议先用这 6 个就够了：

*   `Daily`：日记 / 当天入口
*   `Notes`：自己的正式笔记
*   `References`：书、人、公司、作品、产品、地点
*   `Clippings`：网页摘录 / 微信读书摘录 / 文章收藏
*   `Projects`：项目资料
*   `Templates`：模板

这样做的好处是：

*   中文内容一般主题跨度大，过细分类反而会卡住输入
*   Obsidian 更适合靠 **链接、别名、属性、搜索** 来组织，而不是靠深层文件夹树 [Obsidian+2Obsidian+2](https://obsidian.md/help/properties?utm_source=chatgpt.com)

* * *

三、文件命名：中文用户最容易踩坑的地方
===================

2\. 文件名优先用“自然中文”，别过度技术化
-----------------------

推荐：

*   `产品护城河.md`
*   `米哈游.md`
*   `2026-04-12.md`
*   `任天堂商业模式.md`

不推荐：

*   `PM_Thinking_001.md`
*   `Study-note-2026-v2-final.md`
*   `a1.md`

因为中文用户后期最常用的其实是：

*   快速搜索中文关键词
*   通过 `[[中文链接]]` 直接引用
*   在回顾中靠标题判断内容

标题越自然，越容易复用。

* * *

3\. 日期统一用 `YYYY-MM-DD`
----------------------

Obsidian 的 Daily notes 默认就是按 `YYYY-MM-DD` 新建，当天笔记也支持模板。[Obsidian](https://obsidian.md/help/plugins/daily-notes?utm_source=chatgpt.com)

这在中文环境里尤其重要，因为它同时解决了：

*   排序问题
*   搜索问题
*   跨平台一致性问题

建议统一：

*   日记：`2026-04-12`
*   周回顾：`2026-W15`
*   月回顾：`2026-04`
*   会议：`2026-04-12 项目例会`

* * *

4\. 中英文混排要定规则，不要今天一种明天一种
------------------------

这是中文用户最常见的问题之一。

建议你只选一种：

**方案 A：以中文为主**

*   `OpenAI 产品观察`
*   `Claude 使用体验`
*   `Notion 与 Obsidian`

**方案 B：专有名词保留英文**

*   `OpenAI`
*   `Obsidian`
*   `Prompt Engineering`
*   其余中文表达

核心不是哪种更高级，而是 **一致**。  
Steph 也强调 style 的价值在于把未来无数次小决策一次性压缩掉。[Steph Ango+1](https://stephango.com/file-over-app?utm_source=chatgpt.com)

* * *

四、链接：中文用户应该怎么用双链
================

5\. 重要概念第一次出现就加 `[[链接]]`
------------------------

这是最值得坚持的习惯。

例如：

*   这让我想到 \[\[游戏内生增长\]\]
*   这和 \[\[产品护城河\]\] 很像
*   参考 \[\[任天堂\]\] 的路径

好处是：

*   中文主题之间关系复杂，双链比文件夹更自然
*   你先把“关系”挂出来，未来再慢慢补内容
*   反向链接会逐渐形成你的主题网络 [Steph Ango+1](https://stephango.com/vault?utm_source=chatgpt.com)

* * *

6\. 中文同义词很多，善用 aliases
----------------------

Obsidian 官方支持 `aliases` 默认属性，用来给同一笔记设置不同别名，适合缩写、昵称、不同语言名称。[Obsidian+1](https://obsidian.md/help/properties?utm_source=chatgpt.com)

这对中文用户特别有用，因为中文语境里同一个对象经常有多种叫法：

```
---
aliases:
  - 米哈游
  - miHoYo
  - HoYoverse
---
```

或者：

```
---
aliases:
  - 黄仁勋
  - Jensen Huang
---
```

这样以后你无论写中文还是英文，都更容易连到同一篇笔记。

* * *

7\. 链接优先指向“概念”或“对象”，不是所有句子都加链接
------------------------------

中文写作里很容易过度双链，最后一段话蓝成一片。

更好的做法是只链三类东西：

*   重要对象：人、公司、产品、书、作品
*   核心概念：模型、方法、原则
*   未来会展开的主题

不要把普通叙述词也都链掉。  
链接的目的不是“显得高级”，而是为了 **未来可回访、可重组**。

* * *

五、标签：中文用户别把标签玩坏了
================

8\. 标签只做“少量横切分类”，别拿来代替目录和标题
---------------------------

官方把 `tags` 作为默认属性之一。[Obsidian+1](https://obsidian.md/zh/help/properties?utm_source=chatgpt.com)

但对中文用户来说，最容易出问题的是：

*   `#产品`
*   `#产品思考`
*   `#产品方法`
*   `#产品经理`
*   `#PM`
*   `#pm-thinking`

最后越打越乱。

建议标签只保留 2 到 8 个长期大类，比如：

*   `#工作`
*   `#学习`
*   `#写作`
*   `#项目`
*   `#待读`
*   `#复盘`

更细的分类，不要交给标签，交给：

*   文件名
*   链接
*   属性

* * *

9\. 中文标签要避免近义词泛滥
----------------

例如不要同时出现：

*   `#复盘`
*   `#总结`
*   `#review`

三者最好只保留一个。

规则建议非常简单：

*   中文环境就用中文标签
*   英文软件名、产品名保留英文
*   每季度清一次标签池

* * *

六、属性：中文用户最值得学的“轻数据库”
====================

10\. 用 properties 管“状态”和“类型”，不要一上来搞复杂系统
---------------------------------------

Obsidian Properties 支持文本、列表、数字、日期、复选框、标签等类型；同名属性还能统一类型。模板也可以插入并合并属性。[Obsidian+2Obsidian+2](https://obsidian.md/zh/help/properties?utm_source=chatgpt.com)

对中文用户最实用的，不是做复杂数据库，而是先统一最少的几个字段。

例如文章笔记：

```
---
type: article
status: unread
source: 
date: 2026-04-12
tags:
  - 学习
---
```

书籍笔记：

```
---
type: book
author: 
status: reading
rating: 
tags:
  - 学习
---
```

项目笔记：

```
---
type: project
status: active
owner: 
date: 2026-04-12
---
```

* * *

11\. 属性名一开始就尽量统一
----------------

比如你决定用：

*   `type`
*   `status`
*   `date`
*   `source`
*   `aliases`

那以后尽量一直用这几个。  
不要今天 `category`，明天 `categories`，后天 `type`。

因为 Obsidian 的属性是会跨整个 vault 统一处理的，同名属性会共享类型。[Obsidian+1](https://obsidian.md/zh/help/properties?utm_source=chatgpt.com)

* * *

12\. 中文内容里，属性值可以中文，但属性名建议尽量简短稳定
-------------------------------

推荐：

```
type: meeting
status: active
source: 微信读书
```

而不是：

```
这是一个什么类型的笔记: 会议
当前进行状态: 正在进行
```

原因很简单：  
属性名是系统层面的东西，越稳定越好；  
属性值是内容层面的东西，可以更自然。

* * *

七、模板：中文用户最值得固定的 4 个模板
=====================

13\. 模板只做“重复骨架”，别做复杂仪式感
-----------------------

官方 Templates 支持模板目录和动态变量，比如日期、时间、标题。[Obsidian+1](https://obsidian.md/help/Plugins/Templates?utm_source=chatgpt.com)

最推荐先做这 4 个。

### 日记模板

```
---
date: {{date}}
type: daily
---

# {{date}}

## 今天在做什么
## 临时想法
## 记录
## 待办
- [ ]
```

### 会议模板

```
---
date: {{date}}
type: meeting
status: active
---

# {{title}}

## 背景
## 结论
## 待办
- [ ]
## 相关
- [[]]
```

### 阅读模板

```
---
date: {{date}}
type: reading
status: unread
source:
---

# {{title}}

## 摘要
## 关键观点
## 我的理解
## 可延展主题
- [[]]
```

### 周回顾模板

```
---
date: {{date}}
type: weekly-review
---

# Weekly Review

## 本周发生了什么
## 哪些值得继续
## 哪些需要停止
## 下周最重要的三件事
- [ ]
- [ ]
- [ ]
```

* * *

八、Daily Note：中文用户应该怎么用才不累
=========================

14\. 把 Daily note 当“当天入口”，不要当作文任务
---------------------------------

Obsidian Daily notes 的核心能力就是：按日期打开当天笔记，并能套模板。[Obsidian](https://obsidian.md/help/plugins/daily-notes?utm_source=chatgpt.com)

最适合放进去的是：

*   今天看到的关键词
*   临时想法
*   会议入口
*   零散 TODO
*   当天读到的句子
*   对正式笔记的草稿链接

不要强迫自己天天写完整日记。  
否则 Daily note 很快会变负担。

* * *

15\. 中文用户特别适合“先写当天，再升级正式笔记”
---------------------------

这是很实用的一条：

*   白天所有碎片先进 Daily
*   每周回顾时，再把有价值的内容升级成正式笔记

这样你就不用每次都判断：

*   值不值得单独建一篇？
*   放哪个目录？
*   起什么标题？

先捕捉，再提炼。

* * *

九、搜索与找回：中文环境必须重视
================

16\. 你的系统不是看“记了多少”，而是看“能不能找回来”
------------------------------

中文用户特别依赖搜索，所以你的系统必须服务于搜索。

搜索友好要靠这几件事：

*   标题自然
*   关键词完整
*   同义词用 aliases
*   属性统一
*   重要对象双链

官方也说明属性本身支持搜索语法。[Obsidian+1](https://obsidian.md/zh/help/properties?utm_source=chatgpt.com)

* * *

17\. 一篇笔记里主动写出关键词，不要只写你自己当时懂的简称
-------------------------------

例如你写：

*   不要只写“这次做法像鹅厂那套”
*   更好写成“这次做法很像 \[\[腾讯\]\] 在中台阶段的组织方式”

这样未来你搜：

*   腾讯
*   中台
*   组织方式

都更容易搜到。

这对中文用户非常关键，因为很多中文表达高度语境化，过于省略会导致半年后自己都搜不到。

* * *

十、输入法与中文编辑习惯
============

18\. 中文输入时，链接命名尽量避免只用缩写
-----------------------

例如：

*   `[[AIGC]]` 不如 `[[AIGC 内容生产]]`
*   `[[增长]]` 不如 `[[游戏内生增长]]`

缩写适合做别名，不适合总是做主标题。

* * *

19\. 中英文标点尽量统一
--------------

建议正文随自然输入，  
但以下位置尽量规范：

*   文件名
*   属性名
*   标签
*   日期
*   模板标题

这样后期搜索、替换、迁移都更稳。

* * *

20\. 长中文标题没问题，但要避免太像一句口语
------------------------

例如：

*   `为什么好产品往往不是功能堆出来的`
*   `任天堂为什么能长期维持内容差异化`

这种标题可以。  
但别写成：

*   `关于今天突然想到一个可能跟上次差不多但是也不完全一样的点`

标题要能代表主题，而不是还原当时情绪。

* * *

十一、回顾：这是中文用户最容易忽略、但最该坚持的
========================

21\. 每周至少一次，把碎片变成正式资产
---------------------

这是最重要的一条。

推荐每周做一次 20 到 30 分钟回顾：

*   看这周的 Daily
*   挑出 3 到 10 条值得留下的内容
*   升级成正式笔记
*   补标题、补链接、补属性
*   写一句“我的判断”

这也是 Steph 那套方法真正有效的关键：  
结构不是靠预设长出来，而是靠定期回顾慢慢浮现。[Steph Ango+1](https://stephango.com/vault?utm_source=chatgpt.com)

* * *

22\. 回顾时优先补“判断”，不是补资料
---------------------

很多人回顾时会继续复制内容。  
更好的动作是补一句：

*   我认同什么
*   我不认同什么
*   这和什么有关
*   以后在哪些场景可复用

真正会积累的是你的理解，不只是信息。

* * *

23\. 每隔几个月随机翻旧笔记
----------------

这招很简单但很有用：

*   随机打开几篇旧笔记
*   看有没有可补的链接
*   有没有已过时的判断
*   有没有值得升维成更大主题的内容

旧笔记被重新看见，系统才会活。

* * *

十二、插件建议：适合中文用户的“克制版”
====================

24\. 先只开核心能力，再决定要不要加插件
----------------------

官方核心里就已经有很多够用的能力：

*   Daily notes
*   Templates
*   Backlinks
*   Properties / 属性视图 [Obsidian+3Obsidian+3Obsidian+3](https://obsidian.md/help/plugins/daily-notes?utm_source=chatgpt.com)

对大多数中文用户，前期这几个就够。

不要一上来装十几个插件。  
系统一复杂，反而更不写。

* * *

25\. 插件选择原则：只装能减少重复劳动的
----------------------

装插件前先问一句：

**它是在增加输入摩擦，还是在减少重复劳动？**

值得装的通常是这类：

*   提升捕捉效率
*   优化搜索和回顾
*   减少重复模板操作
*   优化阅读和剪藏

不值得优先折腾的通常是：

*   纯装饰型
*   复杂但你几乎不用的可视化
*   需要长期维护很多字段的系统插件

* * *

十三、最适合中文用户的最小规则集
================

如果你只想记住最精华的，我建议你固定下面这 10 条：

1.  文件名尽量用自然中文
2.  日期统一 `YYYY-MM-DD`
3.  第一次出现的重要概念就加 `[[链接]]`
4.  同义词靠 `aliases`
5.  标签只保留少量横切分类
6.  属性只先统一 `type / status / date / source`
7.  Daily note 只做入口，不做负担
8.  模板只做重复骨架
9.  每周至少一次回顾
10.  回顾时补“判断”和“连接”，不是只补资料

* * *

十四、给中文用户的一句话版本
==============

**Obsidian 最适合中文用户的用法，不是做一个很复杂的知识管理系统，而是做一个“低门槛记录、自然中文命名、双链连接主题、每周固定回顾”的个人思考库。**

你真正要优化的不是“笔记数量”，而是这三件事：

*   以后能不能搜到
*   以后能不能连起来
*   以后能不能拿出来用

如果你愿意，我下一条可以直接继续给你一份：

**「中文用户 Obsidian 模板包设计方案」**  
我会直接给你可复制的目录结构、模板内容、属性字段和命名规范。

---

**Sources:**

- [File over app - Steph Ango](https://stephango.com/file-over-app?utm_source=chatgpt.com)
- [Properties - Obsidian Help](https://obsidian.md/help/properties?utm_source=chatgpt.com)



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)