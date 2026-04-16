---
title: "What is Model Context Protocol? Connect AI to your world"
source: "https://claude.com/blog/what-is-model-context-protocol"
author:
published: 2001-10-31
created: 2026-04-16
description: "Connect AI assistants to your tools without custom integrations using Model Context Protocol. AI models are only as good as the context provided to them. AI assistants like Claude can answer questions and perform an impressive range of tasks, but if they can't access the data or tools they need,..."
tags:
  - "clippings"
---
AI models are only as good as the context provided to them. AI assistants like [Claude](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) can answer questions and perform an impressive range of tasks, but if they can't access the data or tools they need, they're limited in what they can do for you. You typically solve this by copying and pasting context from one tab to another, whether it's editing a document in Google Drive, replying to a thread in Slack, or updating code in an IDE. This process is slow, manual, and risks leaving out important context.AI 模型的能力取决于提供给它们的上下文。像 [Claude](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) 这样的 AI 助手能够回答问题并完成各类出色的任务，但如果它们无法获取所需的数据或工具，能为你提供的帮助就会受到限制。通常情况下，无论是在 Google 云端硬盘中编辑文档、在 Slack 里回复话题线程，还是在集成开发环境中更新代码，你都需要通过在不同标签页之间复制粘贴上下文来解决这个问题。这个过程既缓慢又繁琐，还存在遗漏重要上下文的风险。

The **Model Context Protocol (MCP)** offers a solution that is open and widely available across all AI apps and assistants. In this article, you'll learn what MCP is, how it works and why it matters, and who it's for. You'll see examples of MCP in action and understand how you can start using or building with MCP today.**模型上下文协议（MCP）** 提供了一种开放且可在所有人工智能应用和助手之间广泛使用的解决方案。在本文中，你将了解什么是MCP、它的工作原理、重要性以及适用人群。你会看到MCP的实际应用案例，并了解如今如何开始使用或基于MCP进行开发。

## What is the Model Context Protocol (MCP)?什么是模型上下文协议（MCP）？

The **Model Context Protocol** is an open standard that defines how LLMs communicate with external systems.**模型上下文协议** 是一种定义大语言模型如何与外部系统通信的开放标准。

Think of MCP as **USB-C for LLMs**. Just as USB-C provides a universal connector for your phone, laptop, and other devices, MCP provides a universal format for LLMs to connect with external systems. Before USB-C, every electronic gadget had its own cable: Lightning for iPhone, micro-USB for Android, proprietary connectors for cameras. As more devices adopted USB-C, connectivity became seamless across the ecosystem.可以将 MCP 视为 **大语言模型的 USB-C** 。正如 USB-C 为你的手机、笔记本电脑和其他设备提供了通用接口一样，MCP 为大语言模型与外部系统的连接提供了通用格式。在 USB-C 普及之前，每一个电子设备都有专属线缆：iPhone 用 Lightning 接口，安卓设备用 micro-USB 接口，相机则使用专用连接器。随着越来越多的设备采用 USB-C，整个生态系统的连接变得无缝衔接。

MCP brings this same simplicity to AI integrations. Before MCP, every application and database required custom code to connect with LLMs. Google Drive needed its own integration, Slack needed another, Figma yet another. Now, MCP provides a single, standardized format for connecting these tools to Claude and other AI applications.MCP 将这种简洁性同样带到了 AI 集成领域。在 MCP 出现之前，每个应用程序和数据库都需要编写自定义代码才能与大语言模型（LLMs）连接。Google Drive 需要专属的集成方案，Slack 需要另一种，Figma 又需要不同的。而现在，MCP 提供了一种统一的标准化格式，用于将这些工具连接到 Claude 及其他人工智能应用程序。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/68f64b7d51a1d57549b3ad8e_What%20is%20MCP_%20Final%402x.png)

## Where did MCP come from? MCP 源自何处？

MCP was created at Anthropic by David Sorria Para and Justin Spahr-Summers. The idea originated from David's frustration with constantly copying code between Claude Desktop and his Integrated Development Environment (IDE). Recognizing this as a classic M×N problem where multiple applications need multiple integrations, David pitched building a protocol to solve this to Justin. They designed MCP based on the popular Language Server Protocol and open-sourced it in November 2024 with Anthropic's support to ensure the entire AI ecosystem could benefit.MCP 由大卫·索里亚·帕拉（David Sorria Para）和贾斯汀·斯帕尔-萨默斯（Justin Spahr-Summers）在 Anthropic 公司研发。这一创意源于大卫在 Claude Desktop 与集成开发环境（IDE）之间频繁复制代码的困扰。他意识到这是一个典型的多对多问题，即多个应用程序需要多种集成方式，于是向贾斯汀提出了开发一套协议来解决该问题的想法。二人基于广受欢迎的语言服务器协议（Language Server Protocol）设计了 MCP，并在 Anthropic 的支持下于 2024 年 11 月将其开源，以确保整个人工智能生态系统都能从中受益。

## How does MCP work? MCP是如何运作的？

MCP works through a two-sided approach. AI agents and chatbots like Claude create **MCP Clients**, so they can connect to applications like Notion, Canva, or Figma, who make their tools and data available through **MCP Servers**.MCP 通过双向方式运作。Claude 等人工智能智能体和聊天机器人会创建 **MCP 客户端** ，这样它们就能连接到 Notion、Canva 或 Figma 等应用程序，这些应用程序会通过 **MCP 服务器** 开放自身的工具和数据。

By building an **MCP Client**, AI agents and chatbots can access thousands of MCP Servers built by the community, giving them a straightforward path to extend their capabilities. By building an **MCP Server**, companies and developers can make their products readily available to AI, creating a new avenue to provide value.通过构建一个 **MCP 客户端** ，智能体和聊天机器人可以访问社区开发的数千个 MCP 服务器，为它们拓展能力提供了一条简便的途径。通过构建一个 **MCP 服务器** ，企业和开发者能够让其产品便捷地为人工智能所用，开辟出创造价值的新途径。

As MCP is open-source, anyone can build an MCP Server or Client.由于 MCP 是开源项目，任何人都可以开发 MCP 服务器或客户端。

## Why is MCP important? 为什么 MCP 如此重要？

MCP allows LLMs to go beyond chat and perform real-world tasks: reading an email thread and sending a reply, accessing a codebase and deploying an update, or reviewing a design brief and generating a first draft. The protocol creates a foundation for LLMs to connect with external systems, tools, and applications to access data and take actions. This provides:MCP 让大语言模型（LLMs）不再局限于聊天，而是能完成现实世界的任务：阅读邮件线程并发送回复、访问代码库并部署更新、或是审阅设计概要并生成初稿。该协议为大语言模型搭建了与外部系统、工具和应用对接的基础，使其能够获取数据并执行操作。这带来了以下优势：

### Universal compatibility for AI 人工智能通用兼容性

**AI assistants gain access to thousands of tools** — Once an AI assistant implements MCP (via an MCP client), it can instantly connect to thousands of MCP-compatible applications, from specialized coding tools to enterprise workflow platforms, without building custom integrations for each one.**AI 助手可接入数千种工具** ——一旦 AI 助手通过 MCP 客户端实现了模型上下文协议（MCP），就能立即连接数千种兼容 MCP 的应用，从专业编码工具到企业工作流平台，无需为每一种应用都开发自定义集成。

**Tools and applications connect to every AI assistant at once** — Companies like Notion, Figma, or Asana build a single MCP server that works with any AI assistant that’s compatible (i.e. has implemented an MCP client). Developers only need to build one integration for all AI connections.**工具和应用可同时连接所有AI助手** ——Notion、Figma 或 Asana 等公司可搭建一个通用 MCP 服务器，适配所有兼容的AI助手（即已实现MCP客户端的助手）。开发者仅需构建一次集成，即可实现与所有AI助手的连接。

### An Open, AI-native ecosystem 一个开放的、原生AI生态系统

**Anyone can build and share** — As an open standard, MCP servers published by developers or companies are compatible with any MCP client. This openness has created a thriving ecosystem of thousands of community-built servers, accelerating the availability of tools and applications for AI assistants..**人人皆可构建与分享** ——作为一种开放标准，开发者或企业发布的MCP服务器可与任意MCP客户端兼容。这种开放性打造出了一个繁荣的生态系统，拥有数千个社区构建的服务器，加速了AI助手所需工具和应用的落地应用。

**Makes software AI-accessible by design** — Traditional software is built for humans using web interfaces. MCP provides a parallel interface designed for AI interaction, allowing applications to become truly AI-native. This means better, more reliable integrations between AI models and the tools people already use.**从设计上实现软件的AI可访问性** ——传统软件是为人类通过网页界面构建的。MCP提供了一个专为AI交互设计的并行接口，让应用能够真正成为AI原生。这意味着AI模型与人们日常使用的工具之间能实现更优质、更可靠的集成。

### A foundational protocol for agents 面向智能体的基础协议

MCP creates the infrastructure for AI agents to access any number of services and tools, creating true end-to-end task automation. As more applications adopt the protocol, the vision of AI agents that can independently handle complex, multi-step workflows becomes increasingly practical.MCP 为 AI 智能体访问任意数量的服务和工具搭建了基础设施，实现了真正的端到端任务自动化。随着越来越多的应用采用该协议，AI 智能体能够独立处理复杂的多步骤工作流程的愿景变得愈发可行。

## Who is MCP for? MCP 面向哪些人群？

Developers get a standardized way to build integrations once and have them work with any compatible AI. Enterprises gain secure, IT-controlled AI connectivity that scales across their organization. Consumers can connect their favorite tools to AI instantly, with no technical knowledge required.开发者获得了一种标准化的集成构建方式，只需构建一次，就能与任何兼容的人工智能协同工作。企业获得了由信息技术部门管控的安全人工智能连接方案，可在整个组织范围内扩展使用。消费者无需任何技术知识，就能立即将自己常用的工具与人工智能连接起来。

### For developers: one standard for connecting AI to applications面向开发者：连接人工智能与应用的统一标准

Developers can follow a single standard to connect external products to your AI applications and agents. This simplifies the process of building integrations, grows the number of available products to connect to, and improves the overall quality and security of connectivity in the ecosystem.开发者可遵循单一标准将外部产品接入你的人工智能应用与智能体。这简化了集成搭建流程，扩充了可接入的产品数量，同时提升了生态系统中连接的整体质量与安全性。

Building an agent that will connect to many applications? Building an application that will connect to many agents? MCP provides you with access to an ecosystem of compatible tools with streamlined integration.想要构建一个能连接众多应用程序的智能体？还是想开发一个能连接多个智能体的应用程序？MCP 为你提供了一个兼容工具的生态系统，让集成过程更加高效便捷。

### For enterprises: secure, scalable AI connectivity across your organization面向企业：全组织范围内安全、可扩展的人工智能连接

Enterprises can drive internal adoption of AI tools and applications more effectively, as MCP simplifies the process of connecting your systems to AI. This helps make AI more connected within your organization, expanding its capabilities and usefulness for your staff.企业能更有效地推动内部对AI工具和应用的采纳，因为MCP简化了将企业系统与AI相连接的流程。这有助于让AI在企业内部实现更深度的互联互通，从而拓展其功能，并提升其对员工的实用价值。

### For consumers: instant access to your favorite tools面向消费者：即时使用你最爱的工具

MCP provides end-users with seamless connectivity between their favorite AI assistants and work tools. It makes it easier to automate tasks and avoid copying and pasting across tabs. In short, MCP gives AI greater access and connectivity to your world.MCP 为终端用户提供其常用人工智能助手与办公工具之间的无缝连接。它能简化任务自动化流程，避免在不同标签页间复制粘贴。简而言之，MCP 让人工智能能更广泛地接入你的各类应用并实现互联互通。

In [Claude](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2), you can instantly connect to MCP Servers, known as [**Connectors**](https://claude.com/partners/mcp). This provides you with a straightforward way to connect Claude to your favorite work apps.在 [Claude](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2) 中，你可以即时连接到被称为 [**连接器**](https://claude.com/partners/mcp) 的MCP服务器。这为你提供了一种简单直接的方式，将Claude与你常用的工作应用程序连接起来。

## Connectors (MCP) in action 连接器（MCP）实际应用

The real value of MCP becomes clear when you see it in action with the tools you already use. Here are some examples of MCP being used to power integrations in Claude, known as **Connectors**:当你在日常使用的工具中实际体验 MCP 时，它的真正价值便会显现出来。以下是一些 MCP 在 Claude 中驱动集成的示例，这些集成被称为 **连接器** ：

### Canva in Claude Claude 中的 Canva

The Canva Connector allows Claude to generate new designs directly within Canva. Using MCP, Claude can connect to the tools Canva provides to generate designs on the canvas.Canva 连接器允许 Claude 直接在 Canva 内生成新设计。借助 MCP，Claude 可以连接到 Canva 提供的工具，在画布上生成设计。

![](https://www.youtube.com/watch?v=wXC2u36w2Rc)

### Notion and Linear in Claude Claude 中的 Notion 与 Linear

Using the Notion and Linear Connectors, Claude can access your pages in Notion and use them to update tickets in Linear. Here MCP creates a seamless transfer of unstructured context into organized tickets in a separate project management system.借助 Notion 和 Linear 连接器，Claude 可以访问你在 Notion 中的页面，并利用这些页面更新 Linear 中的工单。在此过程中，模型上下文协议（MCP）实现了将非结构化上下文无缝转换到独立项目管理系统中结构化工单的流程。

![](https://www.youtube.com/watch?v=xBV60h9_lbw)

### Figma in Claude Code Claude Code 中的 Figma

The Figma Connector allows Claude to access designs within Figma. This lets Claude Code create working prototypes of websites, applications, or user interfaces based on designs created in Figma.Figma 连接器允许 Claude 访问 Figma 中的设计稿。这让 Claude Code 能够根据在 Figma 中创建的设计稿，生成网站、应用或用户界面的可运行原型。

![](https://www.youtube.com/watch?v=dcKXca3Bs2o)

### Available Claude Connectors 可用的 Claude 连接器

Claude Connectors include integrations for:Claude 连接器包含以下集成：

- **Notion** for workspace documentation **Notion** 用于工作区文档
- **Linear** for issue tracking **Linear** 用于问题跟踪
- **Stripe** for payment data **Stripe** 用于支付数据
- **Canva** and **Figma** for design assistance **Canva** 和 **Figma** 用于设计辅助
- **Hubspot** for automating CRM tasks **Hubspot** 用于自动化客户关系管理任务
- **Sentry** for error tracking **Sentry** 用于错误跟踪
- ...and many more ……还有更多

Each connector takes just a few seconds to configure to become part of Claude's working context. Outside of Claude, there is an ecosystem of MCP servers on the [open-source MCP Registry](https://modelcontextprotocol.io/).每个连接器只需几秒钟即可完成配置，成为 Claude 工作上下文的一部分。在 Claude 之外， [开源 MCP 注册表](https://modelcontextprotocol.io/) 上存在一个 MCP 服务器生态系统。

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/68e948c50eec666207cdd811_2.png)

## Start exploring MCP 开始探索 MCP

Two paths exist based on your needs.根据你的需求，有两种路径可供选择。

### Connectors in Claude Claude 中的连接器

[Connectors](https://claude.com/partners/mcp) are pre-built, giving Claude instant access to tools, databases, and applications, and providing you with a new set of capabilities. Open [Claude](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2/directory), browse available connectors, and click to add them.[连接器](https://claude.com/partners/mcp) 是预先构建好的，能让 Claude 即时访问工具、数据库和应用程序，并为你提供一组新的功能。打开 [Claude](https://claude.ai/redirect/claudedotcom.v1.ab82fc0b-7619-451b-9c16-e658270364f2/directory) ，浏览可用的连接器，然后点击添加它们即可。

### Build custom MCP connections 构建自定义 MCP 连接

MCP is open-source, meaning that anyone can adopt MCP to connect AI to applications. The [Model Context Protocol documentation](https://modelcontextprotocol.io/) walks through how to build with MCP.

## Getting started 快速开始

If you want to try MCP, start by browsing for a Claude Connector you can immediately start using with Claude.如果你想尝试 MCP，首先浏览并找到一个 Claude 连接器，你就可以立即将其与 Claude 配合使用。

If an existing MCP server doesn't already exist, creating your own takes some work, but isn't too complex if you know TypeScript or Python. The [Model Context Protocol quickstart](https://modelcontextprotocol.io/quickstart) has working examples you can modify for your needs.如果现有的 MCP 服务器不存在，那么创建自己的服务器需要做一些工作，但如果你懂 TypeScript 或 Python，就不会太复杂。 [模型上下文协议快速入门](https://modelcontextprotocol.io/quickstart) 提供了可根据你的需求进行修改的可用示例。