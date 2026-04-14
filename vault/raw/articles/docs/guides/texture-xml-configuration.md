---
summary: "Texture XML configuration format for sampling parameters and compression settings"
last_updated: "2025-12-18"
---

# UrhoX 纹理 XML 配置规范

本文档描述 UrhoX 引擎中纹理资源的 XML 配置格式。

## 概述

纹理 XML 配置文件用于定义纹理的采样参数和压缩设置。配置文件与纹理文件同名，扩展名为 `.xml`。

**示例**: `MyTexture.png` 对应的配置文件为 `MyTexture.xml`

## 加载机制

引擎加载纹理时会自动查找对应的 XML 配置文件 (`Texture.cpp:287-315`):

1. 首先查找与纹理同名的 `.xml` 文件
2. 如果不存在，使用默认配置 `EngineRes/Textures/Default.xml`

---

## 配置类型

### 1. 2D 纹理 (`<texture>`)

用于普通 2D 纹理的配置。

```xml
<?xml version="1.0"?>
<texture>
    <!-- 寻址模式 -->
    <address coord="u" mode="clamp" />
    <address coord="v" mode="clamp" />

    <!-- 边界颜色 (当 mode="border" 时使用) -->
    <border color="1 1 1 1" />

    <!-- 过滤模式 -->
    <filter mode="trilinear" anisotropy="4" />

    <!-- 质量级别 mip 跳过数 -->
    <quality low="2" medium="1" high="0" />

    <!-- sRGB 色彩空间 -->
    <srgb enable="true" />

    <!-- 平台特定压缩配置 -->
    <platform name="windows">
        <compress format="BC7" quality="medium" />
    </platform>
    <platform name="android">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>
    <platform name="ios">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>
    <platform name="web">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>

    <!-- 旧格式压缩 (无平台区分，优先级低于 platform) -->
    <compress format="BC7" quality="medium" />
</texture>
```

### 2. Cubemap (`<cubemap>`)

用于立方体贴图的配置，指定 6 个面的纹理文件。

```xml
<cubemap name="output.ktx">
    <face name="PosX.dds" />
    <face name="NegX.dds" />
    <face name="PosY.dds" />
    <face name="NegY.dds" />
    <face name="PosZ.dds" />
    <face name="NegZ.dds" />
    <quality low="0" />
</cubemap>
```

**Face 顺序**: +X, -X, +Y, -Y, +Z, -Z

### 3. 单图 Cubemap (`<image>`)

从单张图片生成立方体贴图，支持多种布局格式。

```xml
<texture>
    <image name="skybox.hdr" layout="horizontal" />
</texture>
```

**支持的布局 (layout)**:
| 值 | 说明 |
|---|---|
| `horizontal` | 水平排列 6 面 (1x6) |
| `horizontalnvidia` | NVIDIA 水平格式 |
| `horizontalcross` | 水平十字 (4x3) |
| `verticalcross` | 垂直十字 (3x4) |
| `blender` | Blender 格式 (3x2) |

### 4. 3D 纹理 / LUT (`<texture3d>`)

用于 3D 纹理和颜色查找表 (LUT)。

```xml
<texture3d>
    <colorlut name="LUTIdentity.png" />
    <mipmap enable="false" />
    <quality low="0" />
</texture3d>
```

### 5. Texture Array (`<texturearray>`)

用于纹理数组的配置。

```xml
<texturearray>
    <layer name="layer0.png" />
    <layer name="layer1.png" />
    <layer name="layer2.png" />
    <layer name="layer3.png" />
</texturearray>
```

---

## 配置参数详解

### 寻址模式 (`<address>`)

控制纹理坐标超出 [0,1] 范围时的行为。

```xml
<address coord="u" mode="clamp" />
<address coord="v" mode="wrap" />
<address coord="w" mode="mirror" />  <!-- 3D 纹理 -->
```

| 属性 | 说明 |
|---|---|
| `coord` | 纹理坐标轴: `u`, `v`, `w` |
| `mode` | 寻址模式 (见下表) |

| mode 值 | 说明 |
|---|---|
| `wrap` | 重复平铺 (默认) |
| `mirror` | 镜像重复 |
| `clamp` | 钳制到边缘 |
| `border` | 使用边界颜色 |

### 边界颜色 (`<border>`)

当寻址模式为 `border` 时使用的颜色。

```xml
<border color="1 1 1 1" />  <!-- RGBA, 范围 0-1 -->
```

### 过滤模式 (`<filter>`)

控制纹理采样的过滤方式。

```xml
<filter mode="trilinear" anisotropy="8" />
```

| 属性 | 说明 |
|---|---|
| `mode` | 过滤模式 (见下表) |
| `anisotropy` | 各向异性过滤级别 (1-16) |

| mode 值 | 说明 |
|---|---|
| `nearest` | 最近邻采样 |
| `bilinear` | 双线性过滤 |
| `trilinear` | 三线性过滤 (带 mipmap 混合) |
| `anisotropic` | 各向异性过滤 |
| `nearestanisotropic` | 最近邻 + 各向异性 |
| `default` | 使用引擎默认设置 |

### 质量级别 (`<quality>`)

根据画质设置跳过的 mipmap 层数，用于优化低端设备性能。

```xml
<quality low="2" medium="1" high="0" />
```

| 属性 | 说明 |
|---|---|
| `low` | 低画质跳过的 mip 层数 |
| `medium` / `med` | 中画质跳过的 mip 层数 |
| `high` | 高画质跳过的 mip 层数 |

### sRGB (`<srgb>`)

指定纹理是否使用 sRGB 色彩空间。

```xml
<srgb enable="true" />
```

- **Diffuse/Albedo 贴图**: `enable="true"`
- **Normal/Roughness/Metallic 贴图**: `enable="false"`

### Mipmap (`<mipmap>`)

控制是否生成 mipmap。

```xml
<mipmap enable="true" />
```

> **注意**: 此选项在运行时加载代码中已被注释，主要在资源烘焙时使用。

---

## 压缩配置

### 平台特定压缩 (`<platform>`)

为不同平台指定不同的压缩格式。

```xml
<platform name="windows">
    <compress format="BC7" quality="medium" />
</platform>
<platform name="android">
    <compress format="ASTC_6X6" quality="medium" />
</platform>
```

**支持的平台 (name)**:
- `windows`
- `android`
- `ios`
- `web`

### 压缩格式 (`<compress>`)

```xml
<compress format="BC7" quality="medium" />
```

| 属性 | 说明 |
|---|---|
| `format` | 压缩格式 (见下表) |
| `quality` | 压缩质量 (见下表) |

#### 支持的压缩格式

| 格式 | 块大小 | 平台 | 说明 |
|---|---|---|---|
| `ASTC_4X4` | 4x4 | Mobile/Web | 高质量，支持 sRGB |
| `ASTC_5X5` | 5x5 | Mobile/Web | 中等质量 |
| `ASTC_6X6` | 6x6 | Mobile/Web | 较低质量，文件更小 |
| `BC1` | 4x4 | Windows | DXT1，无 Alpha 或 1-bit Alpha |
| `BC3` | 4x4 | Windows | DXT5，带 Alpha |
| `BC7` | 4x4 | Windows | 高质量，支持 sRGB |
| `BC6H` | 4x4 | Windows | HDR 纹理专用 |

#### 压缩质量

| 值 | 说明 | 速度 |
|---|---|---|
| `fastest` | 最快 | 极快 |
| `fast` | 快速 | 快 |
| `medium` | 中等 (推荐) | 中等 |
| `thorough` | 精细 | 慢 |
| `exhaustive` | 极致 | 极慢 |

### 默认压缩格式

如果未指定压缩格式，AssetsCooking 工具会根据平台使用默认值：

| 平台 | 默认格式 |
|---|---|
| Windows | BC7 |
| Android | ASTC_6X6 |
| iOS | ASTC_6X6 |
| Web | ASTC_6X6 |

---

## 完整示例

### Diffuse 贴图 (需要 sRGB)

```xml
<?xml version="1.0"?>
<texture>
    <quality low="1" medium="0" high="0" />
    <srgb enable="true" />
    <platform name="windows">
        <compress format="BC7" quality="medium" />
    </platform>
    <platform name="android">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>
    <platform name="ios">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>
    <platform name="web">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>
</texture>
```

### Normal 贴图 (线性空间)

```xml
<?xml version="1.0"?>
<texture>
    <quality low="1" medium="0" high="0" />
    <srgb enable="false" />
    <platform name="windows">
        <compress format="BC7" quality="medium" />
    </platform>
    <platform name="android">
        <compress format="ASTC_6X6" quality="medium" />
    </platform>
</texture>
```

### UI 贴图 (无 mipmap，点采样)

```xml
<texture>
    <mipmap enable="false" />
    <filter mode="nearest" />
    <address coord="u" mode="clamp" />
    <address coord="v" mode="clamp" />
    <quality low="0" />
</texture>
```

### Skybox Cubemap

```xml
<cubemap name="Skybox.ktx">
    <face name="Sky_PosX.dds" />
    <face name="Sky_NegX.dds" />
    <face name="Sky_PosY.dds" />
    <face name="Sky_NegY.dds" />
    <face name="Sky_PosZ.dds" />
    <face name="Sky_NegZ.dds" />
    <quality low="0" />
</cubemap>
```

---

## 相关源码

| 文件 | 说明 |
|---|---|
| `Urho3D/Graphics/Texture.cpp:237-284` | 运行时参数解析 |
| `Urho3D/Graphics/Texture.cpp:287-315` | XML 文件加载逻辑 |
| `Urho3D/Graphics/TextureCube.cpp:110-223` | Cubemap 配置解析 |
| `Tools/AssetsCooking/main.cpp:60-120` | 压缩配置解析 |
| `Tools/AssetsCooking/CookingCubemap.cpp` | Cubemap 烘焙 |
| `Tools/AssetsCooking/CookingTextureArray.cpp` | TextureArray 烘焙 |
| `Tools/TextureCompression/TextureCompression.cpp:37-45` | 压缩格式定义 |

---

*最后更新: 2025-12-18*
