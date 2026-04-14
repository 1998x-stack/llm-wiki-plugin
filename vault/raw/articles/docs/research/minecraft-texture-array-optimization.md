---
summary: "Texture Array optimization to fix seam artifacts in Minecraft texture atlas sampling"
last_updated: "2026-01-25"
---

# Minecraft 纹理采样优化：Texture Array 方案

## 问题描述

在 `Hand-picked/Minecraft` 项目中，使用 Texture Atlas（纹理图集）时，方块之间会出现明显的接缝问题：

1. **近处接缝**：UV 边界处采样到相邻 tile 的像素
2. **远处接缝更明显**：mipmap 低级别会把整个 atlas 压缩，相邻 tile 的像素完全混合

## 当前解决方案（2026-01-25）

### 已实施的优化

1. **周期性噪声生成**（`HDPack.lua`）
   - 使用 `periodicSmoothNoise()` 确保纹理四方连续
   - 法线计算使用周期性边界采样

2. **禁用 mipmap**（`TexturePackBase.lua`）
   ```lua
   texture:SetNumLevels(1)  -- 只有 1 级，禁用 mipmap
   ```

3. **半像素 UV 偏移**（`TexturePackBase.lua`）
   ```lua
   local halfPixel = 0.5 / self.atlasSize
   ```

### 当前效果
- 接缝明显减轻
- 远处会有轻微闪烁（没有 mipmap 的 aliasing）
- **可接受的折中方案**

## 彻底解决方案：Texture Array

### 原理

使用 `Texture2DArray` 代替 `Texture2D` atlas：
- 每个方块类型是独立的一"层"（layer）
- GPU 采样时只在当前层内采样，永远不会采到其他层
- 每层可独立生成 mipmap，不会和其他纹理混合

### UrhoX 支持情况

**Lua API 已完整支持**：

```lua
local texArray = Texture2DArray:new()
texArray:SetLayers(9)  -- 9 种方块类型
texArray:SetSize(9, 32, 32, graphics:GetRGBAFormat(), TEXTURE_STATIC)
texArray:SetData(0, grassTopImage)   -- 层 0: 草地顶部
texArray:SetData(1, grassSideImage)  -- 层 1: 草地侧面
-- ...
```

### 实现步骤

#### 1. 新建 Shader（~50 行）

复制 `CoreData/Shaders/GLSL/PBRLitSolid.glsl`，修改采样方式：

```glsl
// 原来
uniform sampler2D sDiffMap;
vec4 diffInput = texture2D(sDiffMap, vTexCoord.xy);

// 改为
uniform sampler2DArray sDiffMap;
varying float vTexLayer;  // 从顶点着色器传入层索引
vec4 diffInput = texture(sDiffMap, vec3(vTexCoord.xy, vTexLayer));
```

#### 2. 新建 Technique（~20 行）

```xml
<technique vs="PBRLitSolidArray" ps="PBRLitSolidArray" 
           vsdefines="NORMALMAP VERTEXCOLOR TEXTUREARRAY" 
           psdefines="NORMALMAP DIFFMAP METALLIC ROUGHNESS PBR IBL VERTEXCOLOR TEXTUREARRAY">
    <!-- ... -->
</technique>
```

#### 3. 修改 HDPack.lua

```lua
function HDPack:generate()
    local texArray = Texture2DArray:new()
    texArray:SetLayers(9)
    texArray:SetSize(9, self.tileSize, self.tileSize, ...)
    
    -- 每个方块类型生成独立的 Image
    local grassTopImg = self:generateGrassTopImage()
    texArray:SetData(0, grassTopImg)
    -- ...
    
    return {
        diffuse = texArray,
        normal = normalTexArray,
        specular = specTexArray,
    }
end
```

#### 4. 修改 ChunkMeshBuilder.lua

传递层索引（可用顶点颜色的 alpha 通道或额外的顶点属性）：

```lua
-- 在 buildFace 中
local layerIndex = BLOCK_TEXTURE_LAYERS[blockType][faceType]
geometry:DefineColor(Color(1, 1, 1, layerIndex / 255.0))  -- 用 alpha 传递层索引
```

#### 5. 修改材质绑定

```lua
material:SetTexture(TU_DIFFUSE, texArray)  -- 绑定 Texture2DArray
```

### 工作量估计

| 任务 | 预计时间 |
|------|----------|
| 新建 shader | 1-2 小时 |
| 新建 technique | 30 分钟 |
| 修改 HDPack.lua | 1 小时 |
| 修改 ChunkMeshBuilder.lua | 1 小时 |
| 调试和测试 | 1-2 小时 |
| **总计** | **4-6 小时** |

### 预期效果

- ✅ 彻底消除接缝（不同方块类型完全隔离）
- ✅ 支持 mipmap（远处不闪烁）
- ✅ 纹理质量最佳

## 相关文件

- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/rendering/texturepacks/HDPack.lua`
- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/rendering/texturepacks/TexturePackBase.lua`
- `engine/bin/Data/LuaScripts/Hand-picked/Minecraft/scripts/world/ChunkMeshBuilder.lua`
- `engine/bin/CoreData/Shaders/GLSL/PBRLitSolid.glsl`

## 参考资料

- [Texture Arrays in OpenGL](https://www.khronos.org/opengl/wiki/Array_Texture)
- UrhoX Lua API: `Texture2DArray.pkg`
