---
title: "C++ 游戏引擎搭建指南"
source: "https://chatgpt.com/c/69d71319-51f4-8321-b19e-4c072159389e"
author:
published:
created: 2026-04-09
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
用 C++ 搭建游戏引擎，核心不是“一次写完一个大系统”，而是先定 **目标类型** ，再按模块逐步拼起来。

如果你是第一次做，最推荐的是：

**先做一个 2D / 轻量 3D 引擎原型** ，目标是能跑场景、渲染精灵或模型、处理输入、播放声音、加载资源、驱动 ECS/组件，而不是一开始就做 Unreal 那种全家桶。

---

## 一、先决定你要做哪种引擎

不同目标，架构差很多。

### 1\. 练手型

适合学习图形学、架构、C++工程化。

目标：

- 窗口创建
- 输入系统
- 渲染三角形 / 精灵 / 模型
- 简单场景树
- 资源加载
- 简单物理或碰撞

### 2\. 独立游戏工具型

适合自己做游戏。

目标：

### 3\. 商业级通用引擎

不建议一开始就碰。

因为它需要：

- 多线程任务系统
- 跨平台抽象
- 完整渲染管线
- 资源管线
- 编辑器生态
- 脚本系统
- 网络同步
- 性能分析工具

---

## 二、推荐的最小模块划分

一个 C++ 游戏引擎，通常可以拆成这几层：

### 1\. Platform 平台层

负责和操作系统打交道：

常见库：

- **SDL2 / SDL3**
- GLFW
- 原生 Win32 / Cocoa / X11

新手建议：

- 用 **SDL** 或 **GLFW** 起步，不要自己手搓窗口层。

---

### 2\. Core 核心层

负责基础设施：

- 日志系统
- 断言
- 内存管理
- 事件系统
- Job System（后期）
- 配置系统
- UUID / Handle

建议先有：

- `Log`
- `Assert`
- `Timer`
- `EventBus`
- `FileSystem`

---

### 3\. Render 渲染层

这是最核心的技术模块。

你需要决定图形 API：

- **OpenGL** ：上手快，适合学习
- **DirectX 11/12** ：Windows 方向
- **Vulkan** ：现代、高性能，但复杂
- **Metal** ：macOS/iOS

初学搭建建议：

- 先 **OpenGL**
- 以后再抽象成 Render Hardware Interface（RHI）

渲染层最小功能：

- Shader 编译/加载
- Vertex / Index Buffer
- Texture
- Camera
- Mesh
- Material
- Render Queue

---

### 4\. Scene 场景层

负责“游戏世界怎么组织”。

常见两种思路：

#### 场景树

适合：

- UI
- 层级关系明确的物体

#### ECS（Entity Component System）

适合：

- 游戏对象多
- 组件化管理
- 性能友好

新手建议：

- 一开始用 **Entity + Component** 的轻量方案
- 不要急着做特别纯粹的 ECS

例如：

- Transform
- SpriteRenderer
- MeshRenderer
- Camera
- Rigidbody

---

### 5\. Resource 资源系统

处理：

- 模型
- 纹理
- 音频
- Shader
- 配置文件

需要解决：

- 路径管理
- 缓存
- 引用计数 / Handle
- 异步加载（后期）

常见格式：

- 图片：stb\_image
- 模型：Assimp
- 音频：OpenAL / FMOD / miniaudio

---

### 6\. Physics 物理层

初期不建议自己从零写完整物理引擎。

可以接：

- **Box2D** （2D）
- **Bullet** （3D）
- PhysX（复杂）

先做：

- AABB 碰撞
- 简单射线检测
- 基础刚体封装

---

### 7\. Audio 音频层

功能包括：

- 播放音效
- 背景音乐
- 音量控制
- 3D 音频（后期）

推荐：

- **miniaudio** ：轻量
- OpenAL
- FMOD（成熟但更重）

---

### 8\. Scripting 脚本层

C++ 引擎常见做法：

- Lua
- C#（像 Unity）
- Python（工具向，不常用于运行时）
- 自己的反射 + 热重载系统

新手建议：

- 前期先全部 C++
- 后期再接 **Lua**

---

### 9\. Editor 编辑器层

很多人做引擎，最后卡死在编辑器。

编辑器通常包括：

- Hierarchy
- Inspector
- Scene View
- Asset Browser
- Console

快速方案：

- 用 **Dear ImGui** 做工具 UI

这是最现实的路线：

- Runtime 和 Editor 分离
- Editor 本质上是 Runtime + 调试面板

---

## 三、推荐的开发顺序

最稳的顺序不是按“模块完整度”，而是按“能跑起来”的链路推进。

### 第 1 阶段：先让程序跑起来

- CMake 工程
- SDL/GLFW 创建窗口
- 主循环
- 输入响应
- 清屏 + 绘制三角形

目标：  
**看到第一个三角形**

---

### 第 2 阶段：做渲染基础

- Shader 类
- Texture 类
- Mesh 类
- Camera
- 2D Sprite 或 3D Mesh 渲染

目标：  
**能显示贴图和基本模型**

---

### 第 3 阶段：做场景系统

- GameObject / Entity
- Transform
- Renderer Component
- Scene 管理

目标：  
**能在场景中放多个对象**

---

### 第 4 阶段：做资源系统

- 纹理加载
- 模型加载
- Shader 管理
- 资源缓存

目标：  
**资源不再散乱硬编码**

---

### 第 5 阶段：做编辑器雏形

- Dear ImGui 接入
- Inspector
- 场景层级
- 调试面板

目标：  
**开始从“代码驱动”过渡到“工具驱动”**

---

### 第 6 阶段：扩展高级能力

- 物理
- 动画
- 粒子
- 脚本
- 多线程
- 热重载
- 序列化
- Prefab

---

## 四、一个比较合理的目录结构

```markdown
Engine/
├── CMakeLists.txt
├── ThirdParty/
├── Engine/
│   ├── Core/
│   ├── Platform/
│   ├── Renderer/
│   ├── Scene/
│   ├── Resource/
│   ├── Audio/
│   ├── Physics/
│   ├── Scripting/
│   └── Editor/
├── Runtime/
│   └── main.cpp
├── Sandbox/
│   └── TestScene.cpp
└── Assets/
```

你可以把它理解成：

- **Engine/** ：引擎代码
- **Runtime/** ：真正运行程序的入口
- **Sandbox/** ：测试功能的小游戏/测试场景
- **Assets/** ：资源

---

## 五、主循环大概长这样

游戏引擎本质上都离不开主循环：

```markdown
while (running)
{
    PollEvents();
    UpdateTime();

    ProcessInput();
    Update();
    PhysicsStep();
    Render();

    Present();
}
```

更规范一点会拆成：

```markdown
while (running)
{
    platform.PollEvents();

    float dt = timer.GetDeltaTime();

    engine.BeginFrame();
    engine.Update(dt);
    engine.Render();
    engine.EndFrame();
}
```

---

## 六、推荐技术栈

如果你想快速做出一个像样的 C++ 引擎，建议这套：

- **C++17 / C++20**
- **CMake**
- **SDL2/SDL3** 或 GLFW
- **OpenGL** （入门）或 Vulkan（进阶）
- **GLM** ：数学库
- **stb\_image** ：图片加载
- **Assimp** ：模型导入
- **Dear ImGui** ：编辑器 UI
- **spdlog** ：日志
- **entt** ：ECS 可选
- **Box2D / Bullet** ：物理

非常适合练手。

---

## 七、几个关键设计建议

### 1\. 不要一开始就过度抽象

很多人一上来就想做：

- 通用 RHI
- 反射系统
- 资源热重载
- 全平台适配

结果半年都没有画出一个场景。

更好的思路是：  
**先跑通，再抽象。**

---

### 2\. 不要先写编辑器

编辑器是放大器，不是发动机。

先有 Runtime：

- 能渲染
- 能加载资源
- 能组织场景

再做编辑器，否则你会一直在做 UI 壳子。

---

### 3\. 引擎开发本质是“工具链开发”

难点不只是渲染，而是：

- 资源导入
- 场景保存
- 调试能力
- 工作流效率

所以真正有价值的是：  
**Runtime + Editor + Asset Pipeline**

---

### 4\. 先做“窄而深”，不要做“大而全”

例如：

- 做一个很稳的 2D 引擎，比做一个半残的 3D 通用引擎更有价值
- 做一个完整的 forward renderer，比做一半 deferred + 一半 PBR 更好

---

## 八、学习路线建议

### 路线 A：偏工程实现

1. C++ 基础和现代 C++
2. CMake
3. OpenGL
4. 数学基础（向量、矩阵、四元数）
5. 场景系统
6. 资源系统
7. 编辑器工具

### 路线 B：偏图形学

1. 线性代数
2. 渲染管线
3. Shader
4. 阴影 / PBR / 后处理
5. 渲染架构抽象

### 路线 C：偏游戏架构

1. ECS
2. 事件系统
3. 资源管理
4. 状态机
5. 脚本系统
6. 网络同步

---

## 九、一个现实可行的 3 个月目标

如果你是个人项目，可以定这个版本目标：

### V0.1

- 窗口
- 输入
- OpenGL 渲染
- Shader / Texture
- 2D Sprite

### V0.2

- Scene / Entity / Component
- 摄像机
- 资源管理
- 场景保存加载

### V0.3

- Dear ImGui 编辑器
- 层级面板
- 属性检查器
- Gizmo
- 简单物理

做到这里，已经是一个“真的能做小游戏”的雏形了。

---

## 十、最常见的坑

### 坑 1：什么都想自己写

窗口、音频、模型导入、UI 都自己写，效率极低。

### 坑 2：架构过度设计

接口抽象 100 层，功能 0 层。

### 坑 3：没有 Sandbox

没有测试场景，改一个模块全局爆炸。

### 坑 4：不做资源管理

最后全是路径硬编码、重复加载、内存泄漏。

### 坑 5：不做日志和断言

出了问题完全没法定位。

---

## 十一、如果你要我给一个最推荐的起步方案

我会建议你这样搭：

**第一版技术选型：**

- C++20
- CMake
- SDL2
- OpenGL
- GLM
- stb\_image
- Dear ImGui
- spdlog

**第一版功能目标：**

- 创建窗口
- 主循环
- 输入
- 画三角形
- 画纹理
- 相机
- 场景 + Transform
- ImGui 调试面板

这是最稳、最容易成型的路线。

---

## 十二、你可以直接照着做的开发顺序

1. 建 CMake 项目
2. 接 SDL2 / GLFW
3. 跑出 OpenGL 窗口
4. 写 Shader 封装
5. 写 VertexBuffer / Texture
6. 画三角形和纹理
7. 加 Camera 和 Transform
8. 做 Entity / Component
9. 做资源加载器
10. 接 Dear ImGui
11. 做场景保存
12. 接物理和脚本

---

如果你愿意，我下一条可以直接给你一份：

- **“C++ 游戏引擎最小可运行项目结构”**
- 或者 **“从 0 到 1 的 CMake + SDL2 + OpenGL 示例代码”**

可以。 **场景树（Scene Graph）** 本质上就是：  
把场景里的对象按 **父子层级** 组织起来，让对象之间能自然表达“跟随关系”“局部坐标”“整体变换传播”。

最典型的例子：

- 角色 是一个节点
	- 右手 是角色的子节点
		- 剑 是右手的子节点
- UI 根节点
	- 面板
		- 按钮
				- 文本

这样一来，只要角色移动，右手和剑都会一起动；面板缩放，按钮和文本也一起缩放。

---

## 一、场景树到底解决什么问题

它主要解决 4 件事：

## 1\. 层级关系

表示“谁挂在谁下面”。

例如：

- 摄像机挂在车辆上
- 武器挂在角色手上
- UI 控件挂在窗口上

## 2\. 局部坐标与世界坐标

每个节点一般都有：

- **Local Transform** ：相对父节点的位置/旋转/缩放
- **World Transform** ：最终在世界中的位置/旋转/缩放

公式可以理解成：

```markdown
World = ParentWorld * Local
```

这就是场景树最核心的价值。

---

## 3\. 递归更新

父节点变了，子节点自动跟着更新。

例如：

- 飞机转向
- 机翼、导弹挂点、驾驶舱都跟着变

---

## 4\. 遍历管理

你可以统一遍历整棵树来做：

- Update
- Render
- UI 布局
- 可见性裁剪
- 删除子树
- 序列化

---

## 二、场景树的基本结构

一个最小节点通常长这样：

```markdown
class SceneNode
{
public:
    SceneNode* parent = nullptr;
    std::vector<SceneNode*> children;

    Transform localTransform;
    Mat4 worldMatrix;

    std::string name;
    bool active = true;
};
```

这里的关键字段：

- `parent` ：父节点
- `children` ：孩子列表
- `localTransform` ：本地变换
- `worldMatrix` ：世界矩阵
- `active` ：节点是否启用

---

## 三、Transform 怎么设计

通常一个 Transform 包含：

```markdown
struct Transform
{
    Vec3 position;
    Vec3 rotation;   // 或 Quaternion
    Vec3 scale = {1, 1, 1};
};
```

然后提供一个函数，把它转成矩阵：

```markdown
Mat4 Transform::ToMatrix() const
{
    Mat4 T = Translate(position);
    Mat4 R = Rotate(rotation);
    Mat4 S = Scale(scale);
    return T * R * S;
}
```

更严谨的 3D 推荐：

- 旋转不要长期用欧拉角存核心逻辑
- 用 **Quaternion**

例如：

```markdown
struct Transform
{
    Vec3 position {0, 0, 0};
    Quaternion rotation;
    Vec3 scale {1, 1, 1};
};
```

---

## 四、世界矩阵怎么更新

最基本写法：

```markdown
void SceneNode::UpdateWorldMatrix()
{
    Mat4 local = localTransform.ToMatrix();

    if (parent)
        worldMatrix = parent->worldMatrix * local;
    else
        worldMatrix = local;

    for (SceneNode* child : children)
        child->UpdateWorldMatrix();
}
```

这就是标准递归传播。

---

## 五、为什么 UI 特别适合场景树

因为 UI 天然就是层级结构。

例如：

- Canvas
	- Window
		- Title
				- Content
			- ButtonA
						- ButtonB

UI 里父节点通常控制子节点的：

- 位置偏移
- 裁剪区域
- 可见性
- 缩放
- 透明度

所以 UI 系统几乎天然就是场景树。

---

## 六、游戏对象为什么也适合场景树

因为很多对象存在明显挂载关系：

- 角色
	- 头
		- 手
		- 武器
		- 特效挂点
- 车
	- 车轮 FL
		- 车轮 FR
		- 车轮 RL
		- 车轮 RR
- 摄像机
	- 跟随点
		- HUD 锚点

这类结构如果不用树，你就得手写很多“跟随同步逻辑”。  
用了树之后，父节点变换自动传递。

---

## 七、一个更完整的节点设计

你可以把节点分成“层级部分 + 功能部分”。

例如：

```markdown
class SceneNode
{
public:
    SceneNode(const std::string& nodeName = "Node")
        : name(nodeName) {}

    void AddChild(SceneNode* child);
    void RemoveChild(SceneNode* child);
    void SetParent(SceneNode* newParent);

    void UpdateWorldRecursive();
    void Update(float dt);
    void Render();

    const Mat4& GetWorldMatrix() const { return worldMatrix; }

public:
    std::string name;

    SceneNode* parent = nullptr;
    std::vector<SceneNode*> children;

    Transform localTransform;
    Mat4 worldMatrix = Mat4::Identity();

    bool active = true;
    bool visible = true;
};
```

父子管理：

```markdown
void SceneNode::AddChild(SceneNode* child)
{
    if (!child) return;

    child->parent = this;
    children.push_back(child);
}
```

更严谨一点，要先从旧父节点移除，再挂到新父节点。

---

## 八、SetParent 时有一个关键问题

切换父节点时， **是否保持世界坐标不变** ？

这是引擎里非常关键的设计点。

例如：

- 一把枪原本在地上
- 玩家捡起后挂到手上

这时通常希望：

- 挂上去的一瞬间，枪不要突然跳位置
- 或者明确按挂点规则重算

所以常见接口会这样设计：

```markdown
void SetParent(SceneNode* newParent, bool keepWorldTransform);
```

如果 `keepWorldTransform = true` ，就要先保存旧的世界矩阵，再反推出新的 local transform。

逻辑大概是：

```markdown
newLocal = inverse(newParentWorld) * oldWorld
```

---

## 九、场景树的更新一般分两类

## 1\. 逻辑更新

例如 AI、运动、动画状态机：

```markdown
void SceneNode::Update(float dt)
{
    if (!active) return;

    // 自己的逻辑
    // ...

    for (SceneNode* child : children)
        child->Update(dt);
}
```

---

## 2\. 变换更新

先统一刷新整个树的世界矩阵：

```markdown
root->UpdateWorldRecursive();
```

通常顺序会是：

```markdown
UpdateLogic(dt);
UpdateTransforms();
Render();
```

---

## 十、渲染时怎么和场景树配合

场景树不一定直接等于渲染队列。

通常流程是：

1. 遍历场景树
2. 收集可渲染节点
3. 把世界矩阵、材质、网格丢进渲染队列
4. 排序并渲染

比如：

```markdown
void CollectRenderables(SceneNode* node, RenderQueue& queue)
{
    if (!node || !node->visible) return;

    if (node->HasMeshRenderer())
    {
        queue.Add(node->GetMesh(), node->GetMaterial(), node->GetWorldMatrix());
    }

    for (SceneNode* child : node->children)
        CollectRenderables(child, queue);
}
```

这点很重要：

**场景树负责组织世界，渲染器负责真正绘制。**

不要把两者耦合死。

---

## 十一、场景树和 ECS 的关系

这两个经常被误以为是二选一，其实不是。

## 方案 A：纯场景树

每个节点自己带组件、逻辑、渲染信息。

优点：

- 直观
- 好理解
- 容易做编辑器
- 很适合 UI 和中小项目

缺点：

- 大量对象时，数据局部性不一定好
- 系统化批处理不如 ECS 自然

---

## 方案 B：ECS + 场景树混合

这是更常见也更实用的方案。

比如：

- Entity 存在 ECS 里
- Transform 组件里有 parent/children
- 层级关系还是树
- 渲染、物理、动画系统按 ECS 批处理

也就是说：

**“树”描述关系，ECS 描述数据和系统执行。**

这是很常见的现代做法。

---

## 十二、场景树最常见的几个坑

## 1\. 循环引用

不能让 A 是 B 的父节点，同时 B 又直接或间接成为 A 的父节点。

所以 `SetParent` 时必须检查祖先链。

---

## 2\. 内存管理混乱

如果全是裸指针，很容易删父节点时把子节点搞挂。

更稳的方式：

- 用 `unique_ptr` 管子节点所有权
- 父节点只拥有孩子
- 子节点保存非 owning 的 `parent` 指针

例如：

```markdown
class SceneNode
{
public:
    SceneNode* parent = nullptr;
    std::vector<std::unique_ptr<SceneNode>> children;
};
```

这是很常见的写法。

---

## 3\. 变换重复计算

每帧整棵树全量更新可以先接受，但后面会浪费。

优化办法：

- dirty flag

例如：

- local transform 改了，标记 dirty
- 父节点 dirty，子节点也 dirty
- 只更新脏节点

---

## 4\. 更新顺序不清晰

有时候你先逻辑更新，再变换更新；  
有时候动画系统要先改骨骼，再更新附着点。

所以引擎里最好明确阶段：

- PreUpdate
- Update
- LateUpdate
- TransformPropagation
- Render

---

## 5\. 删除节点时子树处理不清楚

删父节点时：

- 是连孩子一起删？
- 还是把孩子提升到父节点上？
- 还是先 detach？

要提前定义规则。

一般默认：  
**删父节点 = 整个子树一起删。**

---

## 十三、推荐一个“够用”的场景树实现思路

如果你现在在做自己的引擎，我建议你先做这个版本：

## 节点只负责：

- 名字
- 父子关系
- Transform
- 激活/显示
- 遍历接口

## 组件负责：

- MeshRenderer
- Camera
- Light
- Rigidbody
- Script

也就是：

```markdown
class SceneNode
{
public:
    Transform localTransform;
    Mat4 worldMatrix;

    SceneNode* parent;
    std::vector<std::unique_ptr<SceneNode>> children;
    std::vector<std::unique_ptr<Component>> components;
};
```

这样不会把节点做成上帝对象。

---

## 十四、一个很实用的遍历方式

通常会有两种遍历：

## 深度优先遍历 DFS

最常见，适合树结构更新：

```markdown
void Traverse(SceneNode* node)
{
    if (!node) return;

    // 处理当前节点

    for (auto& child : node->children)
        Traverse(child.get());
}
```

---

## 广度优先遍历 BFS

适合某些 UI、层级统计、调试可视化。

但引擎里多数场景更新还是 DFS 为主。

---

## 十五、一个最小可运行伪代码

```markdown
class SceneNode
{
public:
    std::string name;
    SceneNode* parent = nullptr;
    std::vector<std::unique_ptr<SceneNode>> children;

    Transform localTransform;
    Mat4 worldMatrix = Mat4::Identity();

    void UpdateWorldRecursive(const Mat4& parentWorld)
    {
        worldMatrix = parentWorld * localTransform.ToMatrix();

        for (auto& child : children)
            child->UpdateWorldRecursive(worldMatrix);
    }

    SceneNode* CreateChild(const std::string& childName)
    {
        auto child = std::make_unique<SceneNode>();
        child->name = childName;
        child->parent = this;

        SceneNode* ptr = child.get();
        children.push_back(std::move(child));
        return ptr;
    }
};
```

使用：

```markdown
SceneNode root;
root.name = "Root";

SceneNode* player = root.CreateChild("Player");
SceneNode* weapon = player->CreateChild("Weapon");

player->localTransform.position = {10, 0, 0};
weapon->localTransform.position = {1, 0, 0};

root.UpdateWorldRecursive(Mat4::Identity());
```

最后：

- `player` 世界坐标是 `(10, 0, 0)`
- `weapon` 世界坐标是 `(11, 0, 0)`

---

## 十六、什么时候不该过度依赖场景树

有些数据并不天然适合树：

- 大量粒子
- 海量子弹
- 大规模 NPC
- 纯批处理对象

这些对象更适合：

- ECS 数组
- 批量实例渲染
- Job System

所以场景树最适合的是：

- 明确层级关系的对象
- 需要父子变换传播的对象
- 编辑器里要直观看层级的对象
- UI

---

## 十七、你可以怎么落地

如果你现在就开始写，我建议按这个顺序：

1. 先写 `Transform`
2. 再写 `SceneNode`
3. 支持 `AddChild / RemoveChild / SetParent`
4. 做 `UpdateWorldRecursive`
5. 做 `dirty flag`
6. 给节点挂 `Component`
7. 编辑器里显示 Hierarchy 面板

这样你很快就能有一个能用的场景系统。

---

## 十八、一句话总结

**场景树 = 用树结构管理对象层级，并通过父子关系传播变换。**

它最适合：

它的核心不是“树”本身，  
而是这三个东西：

- **父子关系**
- **局部变换 -> 世界变换**
- **递归遍历与传播**

---

你要的话，我下一条可以直接继续给你：

1. **一份完整的 C++ SceneNode 实现**
2. **场景树 + 组件系统怎么结合**
3. **场景树和 ECS 混合架构怎么设计**

我更建议下一步看第 2 个。

你喜欢此风格吗？