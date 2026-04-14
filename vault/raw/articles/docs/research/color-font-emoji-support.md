---
summary: "Color font and emoji rendering support via FreeType with fallback font mechanism"
last_updated: "2024-01-01"
---

# 彩色字体与 Emoji 支持

## 概述

UrhoX 引擎支持通过 FreeType 渲染彩色字体（如 Emoji），支持直接使用彩色字体或通过 fallback 机制混合使用普通字体和 Emoji 字体。

## 支持的字体格式

| 格式 | 描述 | 支持状态 |
|------|------|----------|
| **COLR/CPAL** | 向量分层格式，FreeType 原生支持 | ✅ 支持 |
| **CBDT/CBLC** | PNG 位图格式，需要 libpng | ❌ 不支持 |
| **SVG** | SVG 嵌入格式 | ❌ 不支持 |

### 推荐字体

- **Twemoji Mozilla** (COLR/CPAL 格式) - 推荐使用
  - 从 Mozilla Firefox 安装目录获取：`<Firefox安装目录>/fonts/TwemojiMozilla.ttf`
  - 或从 GitHub 搜索 "Twemoji Mozilla ttf" 下载

- **NotoColorEmoji** (CBDT/CBLC 格式) - 不支持（需要 libpng）

## 使用方式

### 方式1：直接使用 Emoji 字体

```lua
local text = ui.root:CreateChild("Text")
text:SetFont("Fonts/TwemojiMozilla.ttf", 32)
text:SetText("😀🎉🚀")
```

### 方式2：Fallback 机制（推荐）

混合使用普通文本字体和 Emoji 字体：

```lua
local cache = GetSubsystem("ResourceCache")

-- 加载主字体
-- 通过字体xml配置了fallback字体包括TwemojiMozilla.ttf
local mainFont = cache:GetResource("Font", "Fonts/Anonymous Pro.ttf")

-- 使用主字体
local text = ui.root:CreateChild("Text")
text:SetFont(mainFont, 24)
text:SetText("你好世界 😀🎉 Hello!")  -- 中文和英文用主字体，Emoji 用 fallback
```

### C++ 使用方式

```cpp
auto* cache = GetSubsystem<ResourceCache>();

// 加载字体
// 通过字体xml配置了fallback字体包括TwemojiMozilla.ttf
auto* mainFont = cache->GetResource<Font>("Fonts/Anonymous Pro.ttf");

// 创建文本
auto* text = ui->GetRoot()->CreateChild<Text>();
text->SetFont(mainFont, 24);
text->SetText("Hello 😀 世界!");
```

## 技术实现

### 架构概述

```
┌─────────────────────────────────────────────────────────────┐
│                         Text                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │ pageGlyphLocations_ │  │colorPageGlyphLocations_│        │
│  │   (灰度字形)         │  │   (彩色字形)          │         │
│  └─────────────────────┘  └─────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
                    │                       │
                    ▼                       ▼
┌─────────────────────────────────────────────────────────────┐
│                       FontFace                               │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │     textures_       │  │   colorTextures_    │           │
│  │  (Alpha8 纹理)      │  │   (RGBA8 纹理)      │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                              │
│  glyphMapping_: HashMap<charCode, FontGlyph>                │
│    └── FontGlyph::isColor_ 区分彩色/灰度                    │
└─────────────────────────────────────────────────────────────┘
```

### 修改的文件

| 文件 | 修改内容 |
|------|----------|
| `FontFace.h` | 添加 `FontGlyph::isColor_`、`colorTextures_`、`hasColorGlyphs_` |
| `FontFaceFreeType.h` | 添加 `SetupNextColorTexture()`、`colorAllocator_` |
| `FontFaceFreeType.cpp` | 彩色字体检测、BGRA 处理、fallback 支持 |
| `Text.h` | 添加 `colorPageGlyphLocations_` |
| `Text.cpp` | 分离彩色字形渲染逻辑 |

### 关键实现细节

#### 1. 彩色字体检测

```cpp
// FontFaceFreeType.cpp - Load()
if (FT_HAS_COLOR(face))
{
    hasColorGlyphs_ = true;
    loadMode_ |= FT_LOAD_COLOR;
}
```

#### 2. Bitmap-Only 字体支持

某些 Emoji 字体（如 NotoColorEmoji）是纯位图字体，不支持 `FT_Set_Char_Size`：

```cpp
if (FT_HAS_FIXED_SIZES(face) && !FT_IS_SCALABLE(face))
{
    // 选择最接近请求大小的 strike
    int bestStrikeIndex = 0;
    int bestDiff = INT_MAX;
    for (int i = 0; i < face->num_fixed_sizes; ++i)
    {
        int diff = abs(face->available_sizes[i].height - requestedPixelHeight);
        if (diff < bestDiff)
        {
            bestDiff = diff;
            bestStrikeIndex = i;
        }
    }
    FT_Select_Size(face, bestStrikeIndex);
}
```

#### 3. BGRA → RGBA 转换

FreeType 返回 BGRA 格式，需要转换为引擎使用的 RGBA：

```cpp
if (slot->bitmap.pixel_mode == FT_PIXEL_MODE_BGRA)
{
    for (unsigned col = 0; col < width; ++col)
    {
        dest[col * 4 + 0] = src[col * 4 + 2];  // R ← B
        dest[col * 4 + 1] = src[col * 4 + 1];  // G ← G
        dest[col * 4 + 2] = src[col * 4 + 0];  // B ← R
        dest[col * 4 + 3] = src[col * 4 + 3];  // A ← A
    }
}
```

#### 4. Fallback 机制支持

`LoadCharGlyphFrom()` 需要切换 fallback 字体的完整状态：

```cpp
bool FontFaceFreeType::LoadCharGlyphFrom(FontFace* face, const unsigned c)
{
    auto* ftFace = static_cast<FontFaceFreeType*>(face);

    // 保存当前状态
    const auto oldFace = face_;
    const auto oldLoadMode = loadMode_;
    const auto oldHasColorGlyphs = hasColorGlyphs_;

    // 使用 fallback 字体的设置
    face_ = ftFace->face_;
    loadMode_ = ftFace->loadMode_;           // 关键：使用 FT_LOAD_COLOR
    hasColorGlyphs_ = ftFace->hasColorGlyphs_;

    const auto success = LoadCharGlyph(c);

    // 恢复原状态
    face_ = oldFace;
    loadMode_ = oldLoadMode;
    hasColorGlyphs_ = oldHasColorGlyphs;

    return success && !glyphMapping_[c].isNotDef_;
}
```

#### 5. 彩色字形渲染

彩色字形使用白色渲染以保留原始颜色：

```cpp
// Text.cpp - GetBatches()
for (auto& colorPageGlyphLocation : colorPageGlyphLocations_)
{
    // 彩色字形使用白色，不应用文本颜色
    Color white(1.0f, 1.0f, 1.0f, 1.0f);
    ConstructBatch(colorBatch, colorPageGlyphLocation, 0, 0, &white);
}
```

## 已知限制

1. **不支持 PNG 嵌入格式** - CBDT/CBLC 格式需要 libpng，当前引擎使用 STB 图像库
2. **不支持 SVG 格式** - 需要 SVG 渲染库
3. **Bitmap 字体尺寸固定** - 纯位图 Emoji 字体只能使用预设的尺寸

## 故障排除

### Emoji 不显示

1. 检查字体格式是否为 COLR/CPAL
2. 确认 fallback 字体已正确添加
3. 检查日志是否有 `FT_Load_Char` 错误

### Emoji 显示为方块

1. 字体可能不包含该 Emoji 字符
2. 尝试使用更完整的 Emoji 字体

### 崩溃：face->size == nullptr

1. 可能是 bitmap-only 字体未正确处理
2. 确认使用的是最新版本的引擎代码

---

*最后更新: 2024*
