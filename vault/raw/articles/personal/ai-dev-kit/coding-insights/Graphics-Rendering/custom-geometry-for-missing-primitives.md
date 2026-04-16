# 使用 CustomGeometry 模拟内置模型缺失的基础形状

**日期**: 2025-12-23
**分类**: Graphics-Rendering
**严重程度**: Medium
**游戏/项目**: 通用（水果忍者、切割效果、特殊几何体等）
**引擎版本**: UrhoX (Based on Urho3D)

---

## 🎯 应用场景 (Use Cases)

当需要使用**基础几何形状**，但**引擎内置模型不支持**时，应使用 `CustomGeometry` 来程序化生成。

### 典型场景

| 需求 | 内置模型 | 解决方案 |
|------|---------|---------|
| 半球（水果切开效果） | ❌ 不支持 | ✅ CustomGeometry |
| 圆锥台/截锥体 | ❌ 不支持 | ✅ CustomGeometry |
| 楔形/斜面 | ❌ 不支持 | ✅ CustomGeometry |
| 扇形/弧形 | ❌ 不支持 | ✅ CustomGeometry |
| 胶囊体（非物理用途） | ❌ 不支持 | ✅ CustomGeometry |
| 任意多边形柱体 | ❌ 不支持 | ✅ CustomGeometry |

### 内置模型列表（供参考）

引擎内置的基础模型（详见 `engine-docs/built-in-models.md`）：
- Box（立方体）
- Sphere（球体）
- Cylinder（圆柱体）
- Cone（圆锥体）
- Plane（平面）
- Torus（圆环）
- TeaPot（茶壶）

---

## ✅ 解决方案：CustomGeometry 半球示例

### 创建半球（水果切开效果）

```lua
--- 创建半球几何体
---@param node Node 要附加几何体的节点
---@param radius number 半球半径
---@param segments number 分段数（越大越平滑，推荐 16-32）
---@param materialPath string 材质路径
---@param isUpperHalf boolean true=上半球, false=下半球
---@return CustomGeometry
local function CreateHemisphere(node, radius, segments, materialPath, isUpperHalf)
    local geom = node:CreateComponent("CustomGeometry")
    geom:BeginGeometry(0, TRIANGLE_LIST)
    
    local rings = math.floor(segments / 2)  -- 半球只需要一半的环数
    
    -- 生成顶点
    for ring = 0, rings do
        -- 半球的纬度范围：上半球 0~90°，下半球 90°~180°
        local phi
        if isUpperHalf then
            phi = (ring / rings) * (math.pi / 2)  -- 0 到 π/2
        else
            phi = (math.pi / 2) + (ring / rings) * (math.pi / 2)  -- π/2 到 π
        end
        
        for seg = 0, segments do
            local theta = (seg / segments) * math.pi * 2
            
            -- 球面坐标转笛卡尔坐标
            local x = radius * math.sin(phi) * math.cos(theta)
            local y = radius * math.cos(phi)
            local z = radius * math.sin(phi) * math.sin(theta)
            
            -- 法线 = 归一化的位置向量
            local nx, ny, nz = x / radius, y / radius, z / radius
            
            -- UV 坐标
            local u = seg / segments
            local v = ring / rings
            
            geom:DefineVertex(Vector3(x, y, z))
            geom:DefineNormal(Vector3(nx, ny, nz))
            geom:DefineTexCoord(Vector2(u, v))
            
            -- 生成三角形（除了最后一行和最后一列）
            if ring < rings and seg < segments then
                local current = ring * (segments + 1) + seg
                local next = current + 1
                local below = current + (segments + 1)
                local belowNext = below + 1
                
                -- 两个三角形组成一个四边形
                -- 注意：根据 isUpperHalf 调整绕序保证正确的面朝向
                if isUpperHalf then
                    geom:DefineTriangle(current, below, next)
                    geom:DefineTriangle(next, below, belowNext)
                else
                    geom:DefineTriangle(current, next, below)
                    geom:DefineTriangle(next, belowNext, below)
                end
            end
        end
    end
    
    -- 添加底面（切面）
    local centerY = isUpperHalf and 0 or 0
    local normalY = isUpperHalf and -1 or 1
    
    -- 底面中心点
    local centerIndex = (rings + 1) * (segments + 1)
    geom:DefineVertex(Vector3(0, centerY, 0))
    geom:DefineNormal(Vector3(0, normalY, 0))
    geom:DefineTexCoord(Vector2(0.5, 0.5))
    
    -- 底面边缘点
    for seg = 0, segments do
        local theta = (seg / segments) * math.pi * 2
        local x = radius * math.cos(theta)
        local z = radius * math.sin(theta)
        
        geom:DefineVertex(Vector3(x, centerY, z))
        geom:DefineNormal(Vector3(0, normalY, 0))
        geom:DefineTexCoord(Vector2(0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)))
        
        if seg < segments then
            local edgeCurrent = centerIndex + 1 + seg
            local edgeNext = centerIndex + 1 + seg + 1
            if isUpperHalf then
                geom:DefineTriangle(centerIndex, edgeNext, edgeCurrent)
            else
                geom:DefineTriangle(centerIndex, edgeCurrent, edgeNext)
            end
        end
    end
    
    geom:Commit()
    
    -- 设置材质
    local material = cache:GetResource("Material", materialPath)
    geom:SetMaterial(material)
    
    return geom
end

-- 使用示例：创建切开的水果效果
function CreateSlicedFruit(position)
    -- 上半部分
    local upperNode = scene_:CreateChild("FruitUpper")
    upperNode.position = position + Vector3(0, 0.05, 0)  -- 略微分开
    CreateHemisphere(upperNode, 0.5, 24, "Materials/FruitSkin.xml", true)
    
    -- 下半部分
    local lowerNode = scene_:CreateChild("FruitLower")
    lowerNode.position = position - Vector3(0, 0.05, 0)  -- 略微分开
    CreateHemisphere(lowerNode, 0.5, 24, "Materials/FruitSkin.xml", false)
    
    -- 可以给切面添加不同材质（果肉颜色）
    -- 通过多 Geometry 或贴花实现
    
    return upperNode, lowerNode
end
```

---

## 💡 关键知识点 (Key Insights)

### 1. CustomGeometry 工作流程

```lua
local geom = node:CreateComponent("CustomGeometry")
geom:BeginGeometry(0, TRIANGLE_LIST)  -- 开始定义几何体

-- 定义顶点（必须按顺序）
geom:DefineVertex(Vector3(x, y, z))    -- 位置
geom:DefineNormal(Vector3(nx, ny, nz)) -- 法线（用于光照）
geom:DefineTexCoord(Vector2(u, v))     -- UV 坐标

-- 定义三角形（顶点索引）
geom:DefineTriangle(idx0, idx1, idx2)

geom:Commit()  -- 提交几何数据
geom:SetMaterial(material)  -- 设置材质
```

### 2. ⚠️ TRIANGLE_LIST 核心规则

**每 3 个顶点 = 1 个三角形**，顶点必须逐个定义：

```lua
-- ✅ 正确：每个三角形单独定义 3 个顶点
geom:BeginGeometry(0, TRIANGLE_LIST)

-- 三角形 1
geom:DefineVertex(Vector3(0, 1, 0))   -- 顶点 0
geom:DefineVertex(Vector3(-1, 0, 0))  -- 顶点 1  
geom:DefineVertex(Vector3(1, 0, 0))   -- 顶点 2

-- 三角形 2
geom:DefineVertex(Vector3(0, 0, 1))   -- 顶点 3
geom:DefineVertex(Vector3(-1, 0, 0))  -- 顶点 4 (可以和顶点1相同位置，但必须重新定义)
geom:DefineVertex(Vector3(1, 0, 0))   -- 顶点 5

geom:Commit()
```

```lua
-- ❌ 错误：只定义顶点，期望自动组成三角形
for i = 1, 100 do
    geom:DefineVertex(vertices[i])  -- 没用！必须每3个连续顶点才能组成三角形
end
-- 结果：100 个顶点 = 33 个三角形（最后1个顶点被丢弃）
```

**绕序规则**：从正面看，顶点按**逆时针(CCW)**顺序 = 正面朝外

### 3. 注意事项

| 要点 | 说明 |
|------|------|
| **顶点顺序** | 逆时针绕序 = 正面朝外（默认剔除背面） |
| **法线方向** | 必须指向外部，否则光照错误 |
| **性能考虑** | 分段数越高越平滑，但顶点越多；推荐 16-32 |
| **材质双面** | 如需显示背面，材质设置 `<cull value="none"/>` |

### 4. 常用几何体计算公式

```lua
-- 球面坐标（phi: 纬度 0~π, theta: 经度 0~2π）
x = radius * sin(phi) * cos(theta)
y = radius * cos(phi)
z = radius * sin(phi) * sin(theta)

-- 圆柱侧面
x = radius * cos(theta)
y = height * t  -- t: 0~1
z = radius * sin(theta)

-- 圆锥侧面
x = radius * (1 - t) * cos(theta)  -- t: 0=底面, 1=顶点
y = height * t
z = radius * (1 - t) * sin(theta)
```

---

## 🔗 相关资源 (Related Resources)

### 引擎文档
- `engine-docs/built-in-models.md` - 内置模型尺寸参考
- `examples/07-minecraft-voxel-world.lua` - CustomGeometry 大规模使用示例
- `examples/12-fruit-ninja-3d-game.lua` - 半球切割效果实际应用 ⭐

### 参考示例
- **FruitNinja3D** - 水果切割效果（半球 + 切面，带 PBR 材质和 NanoVG UI）
- Minecraft 体素世界（立方体批量生成）
- 程序化地形生成

---

## 🤖 AI 局限性分析 (AI Limitations Analysis)

### 问题性质分类

- [ ] LLM 根本局限（数学推理、空间想象等）
- [x] **知识/经验不足（可通过学习改进）**
- [ ] 上下文理解错误

### 分析

**这是典型的"知识盲区"问题**：
- AI 可能不知道引擎缺少哪些基础模型
- AI 可能不知道 CustomGeometry 是解决方案
- 通过本文档补充后，AI 可以正确应对此类需求

### 改进建议

**对 AI**：当用户需要基础几何形状时：
1. 先检查 `engine-docs/built-in-models.md` 是否有内置支持
2. 如果没有，使用 CustomGeometry 程序化生成
3. 参考本文档的代码模板

---

**最后更新**: 2025-12-23
**贡献者**: Human Developer

