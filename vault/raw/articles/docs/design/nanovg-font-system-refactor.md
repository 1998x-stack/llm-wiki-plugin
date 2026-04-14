---
summary: "NanoVG font system refactor to use engine Font system via NANOVG_USE_URHO_FONT macro"
related_paths:
  - engine/Source/ThirdParty/bgfx-all/bgfx/examples/common/nanovg/**
last_updated: "2026-01-10"
---

# NanoVG 字体系统重构计划

## 目标

将 NanoVG 的字形获取改为使用引擎的 Font 系统，通过 `NANOVG_USE_URHO_FONT` 宏完全隔离两套实现。

## 核心策略

```
NANOVG_USE_URHO_FONT 未定义时（原路径）:
NanoVG API → fontstash → FreeType → fontstash atlas → bgfx 纹理 → NanoVG shader

NANOVG_USE_URHO_FONT 定义时（Urho 路径）:
NanoVG API → Font::GetFace/GetFaceByPixel → FontFace::GetGlyph → FontFace 纹理 → NanoVG shader
                                                    ↑
                                        (完全复用引擎 Font 系统)
                                        (Texture::GetGPUObjectIdx 获取 bgfx handle)
```

**关键特性**：
- 编译时隔离，不支持运行时切换
- Urho 路径完全不使用 fontstash
- 代码干净，无特判逻辑

---

## NVGcontext 结构修改

```cpp
struct NVGcontext {
    NVGparams params;
    float* commands;
    int ccommands;
    int ncommands;
    float commandx, commandy;
    NVGstate states[NVG_MAX_STATES];
    int nstates;
    NVGpathCache* cache;
    float tessTol;
    float distTol;
    float fringeWidth;
    float devicePxRatio;
    INVGFileSystem* fileSystem;
    int drawCallCount;
    int fillTriCount;
    int strokeTriCount;
    int textTriCount;

#if NANOVG_USE_URHO_FONT
    Urho3D::Font* urhoFonts[NVG_MAX_URHO_FONTS];
    char urhoFontNames[NVG_MAX_URHO_FONTS][64];  // 存储字体名字，用于 nvgFindFont
    int nUrhoFonts;
    int fontSizeMethod;  // 0 = point size (GetFace), 1 = pixel size (GetFaceByPixel)
#else
    struct FONScontext* fs;
    int fontImages[NVG_MAX_FONTIMAGES];
    int fontImageIdx;
    int colorFontImages[NVG_MAX_FONTIMAGES];
    int colorFontImageIdx;
#endif
};
```

---

## 需要宏隔离的函数

### 完整列表

| 函数 | 原实现 | Urho 路径实现 |
|------|--------|--------------|
| `nvgCreateInternal` | 创建 fontstash context | 初始化 `urhoFonts` 数组 |
| `nvgDeleteInternal` | 删除 fontstash context | 释放 `urhoFonts`（ReleaseRef） |
| `nvgCreateFont` | `nvg__fonsAddFont` | 不支持，返回 -1 |
| `nvgCreateFontMem` | `fonsAddFontMem` | 不支持，返回 -1 |
| `nvgCreateFontUrho` | `fonsAddFontUrho` | 直接存入 `urhoFonts` 数组 |
| `nvgFindFont` | `fonsGetFontByName` | 遍历 `urhoFontNames` 查找 |
| `nvgAddFallbackFontId` | `fonsAddFallbackFont` | 空实现，返回 0（Urho 内部处理） |
| `nvgAddFallbackFont` | `nvgFindFont` | 空实现，返回 0 |
| `nvgForceAutoHint` | `fonsSetForceAutoHint` | 空实现（Urho 不需要） |
| `nvgGetForceAutoHint` | `fonsGetForceAutoHint` | 返回 0 |
| `nvgFontSizeMethod` | `fonsSetSizeMethod` | 设置 `ctx->fontSizeMethod` |
| `nvgGetFontSizeMethod` | `fonsGetSizeMethod` | 返回 `ctx->fontSizeMethod` |
| `nvgFontFace` | `fonsGetFontByName` | 调用 `nvgFindFont` 设置 `state->fontId` |
| `nvg__flushTextTexture` | `fonsValidateTexture` | 空实现（FontFace 管理纹理） |
| `nvg__allocTextAtlas` | `fonsResetAtlas` | 空实现 |
| `nvg__renderText` | 用 `ctx->fontImages` | 使用传入的纹理 handle |
| `nvg__renderColorText` | 用 `ctx->colorFontImages` | 使用传入的纹理 handle |
| `nvgText` | `fonsTextIterInit/Next` | **核心实现** |
| `nvgTextBox` | `nvgText` 等 | 复用 Urho 版 |
| `nvgTextGlyphPositions` | `fonsTextIterInit/Next` | 遍历 UTF-8 → GetGlyph → 返回位置 |
| `nvgTextBreakLines` | `fonsTextIterInit/Next` | 遍历 UTF-8 → GetGlyph → 计算换行 |
| `nvgTextBounds` | `fonsTextBounds` | 遍历 UTF-8 → GetGlyph → 计算边界 |
| `nvgTextBoxBounds` | `nvgTextBreakLines` | 复用 Urho 版 |
| `nvgTextMetrics` | `fonsVertMetrics` | 从 FontFace 获取度量信息 |

### 不需要宏隔离的函数（只操作 NVGstate）

- `nvgFontSize` - 只设置 `state->fontSize`
- `nvgFontBlur` - 只设置 `state->fontBlur`
- `nvgTextLetterSpacing` - 只设置 `state->letterSpacing`
- `nvgTextLineHeight` - 只设置 `state->lineHeight`
- `nvgTextAlign` - 只设置 `state->textAlign`
- `nvgFontFaceId` - 只设置 `state->fontId`

---

## 核心实现细节

### 1. 获取 FontFace 逻辑

```cpp
// 根据 fontSizeMethod 选择接口
Urho3D::FontFace* face;
float fontSize = state->fontSize * scale;

if (ctx->fontSizeMethod == 0) {
    // Point size (default) - 使用 FT_Set_Char_Size
    face = font->GetFace(fontSize);
} else {
    // Pixel size - 使用 FT_Set_Pixel_Sizes
    face = font->GetFaceByPixel(fontSize);
}
```

### 2. 多 Page 渲染合批

FontFace 有两套独立的纹理数组：
- `face->GetTextures()` - 灰度纹理（普通字形）
- `face->GetColorTextures()` - RGBA 纹理（Emoji 等彩色字形）

每套纹理可能有多个 page（当一张纹理装不下时自动扩展）。

**关键点**：
1. `glyph->page_` 是在**对应纹理数组内**的索引
2. 灰度 page 0 和彩色 page 0 是**完全不同的纹理**
3. 分批的 key 是 `(isColor, page)` 的组合

```cpp
// 纹理结构示意
face->GetTextures():       [Tex0_Gray, Tex1_Gray, ...]      // 灰度纹理数组
face->GetColorTextures():  [Tex0_Color, Tex1_Color, ...]    // 彩色纹理数组

// 字形引用
glyph A: isColor_=false, page_=0  → GetTextures()[0]
glyph B: isColor_=false, page_=1  → GetTextures()[1]
glyph C: isColor_=true,  page_=0  → GetColorTextures()[0]  // 不同的纹理！
```

**分批逻辑**：

```cpp
int currentPage = -1;
int currentIsColor = -1;
bgfx::TextureHandle currentTexHandle = BGFX_INVALID_HANDLE;

for each glyph:
    int glyphPage = glyph->page_;
    int glyphIsColor = glyph->isColor_ ? 1 : 0;

    // page 或 isColor 任一变化 → flush
    if (glyphPage != currentPage || glyphIsColor != currentIsColor) {
        if (nverts > 0) {
            nvg__renderTextBatch(ctx, currentTexHandle, currentIsColor, verts, nverts);
            nverts = 0;
        }
        currentPage = glyphPage;
        currentIsColor = glyphIsColor;

        // 从正确的纹理数组获取 handle
        if (currentIsColor) {
            Texture* tex = face->GetColorTextures()[currentPage];
            currentTexHandle = { (uint16_t)tex->GetGPUObjectIdx() };
        } else {
            Texture* tex = face->GetTextures()[currentPage];
            currentTexHandle = { (uint16_t)tex->GetGPUObjectIdx() };
        }
    }

    // 添加顶点到当前批次
    addGlyphVertices(glyph, ...);
    nverts += 6;

// 渲染最后一批
if (nverts > 0) {
    nvg__renderTextBatch(ctx, currentTexHandle, currentIsColor, verts, nverts);
}
```

**渲染时的颜色处理**：

```cpp
void nvg__renderTextBatch(NVGcontext* ctx, bgfx::TextureHandle tex, int isColor,
                          NVGvertex* verts, int nverts)
{
    NVGstate* state = nvg__getState(ctx);

    if (isColor) {
        // 彩色字形（Emoji）：使用白色，保留纹理原色
        nvg__renderTriangles(ctx, tex, verts, nverts, NVG_WHITE);
    } else {
        // 灰度字形：使用当前填充色
        nvg__renderTriangles(ctx, tex, verts, nverts, state->fill.innerColor);
    }
}
```

**为什么不能简单地只按 page 分批？**

因为灰度和彩色使用不同的纹理数组，即使 page 相同也是不同的纹理：

```
文本: "Hello 😀 World"

字形序列:
H(gray,p0) e(gray,p0) l(gray,p0) l(gray,p0) o(gray,p0)  → batch 1 (gray tex 0)
😀(color,p0)                                             → batch 2 (color tex 0) ← 不同纹理！
W(gray,p0) o(gray,p0) r(gray,p0) l(gray,p0) d(gray,p0)  → batch 3 (gray tex 0)
```

如果只按 page 分批，😀 会错误地使用灰度纹理渲染。

### 3. 对齐方式（复刻原算法）

**水平对齐**：
```cpp
if (align & NVG_ALIGN_LEFT) {
    // 不调整
} else if (align & NVG_ALIGN_RIGHT) {
    float width = nvgTextBounds(...);  // 先计算总宽度
    x -= width;
} else if (align & NVG_ALIGN_CENTER) {
    float width = nvgTextBounds(...);
    x -= width * 0.5f;
}
```

**垂直对齐**（FONS_ZERO_TOPLEFT 模式）：
```cpp
float ascender = face->GetAscender();
float descender = face->GetAscender() - face->GetRowHeight();  // descender 为负值

if (align & NVG_ALIGN_TOP) {
    y += ascender;
} else if (align & NVG_ALIGN_MIDDLE) {
    y += (ascender + descender) / 2.0f;
} else if (align & NVG_ALIGN_BASELINE) {
    y += 0;
} else if (align & NVG_ALIGN_BOTTOM) {
    y += descender;
}
```

### 4. Kerning（字距调整）

**fontstash 原实现**：
```c
if (prevGlyphIndex != -1 && glyph->index != -1)
    x += fons__tt_getGlyphKernAdvance(&font->font, prevGlyphIndex, glyph->index) * scale;
```

**Urho 路径**：
```cpp
unsigned int prevCodepoint = 0;
for each glyph:
    if (prevCodepoint != 0)
        curX += face->GetKerning(prevCodepoint, codepoint);
    // ... 渲染字形 ...
    prevCodepoint = codepoint;
```

### 5. letterSpacing 支持

```cpp
curX += glyph->advanceX_ + state->letterSpacing * scale;
```

### 6. 颜色字形判断

使用 `glyph->isColor_` 判断是否为彩色字形（Emoji）：
- 灰度字形：使用 `face->GetTextures()`
- 彩色字形：使用 `face->GetColorTextures()`，渲染时设置白色以保留原色

---

## nvgText 核心流程（Urho 路径）

```cpp
float nvgText(NVGcontext* ctx, float x, float y, const char* string, const char* end)
{
    NVGstate* state = nvg__getState(ctx);
    if (string == NULL || state->fontId < 0) return x;
    if (end == NULL) end = string + strlen(string);

    // 1. 获取 Font 和 FontFace
    Urho3D::Font* font = ctx->urhoFonts[state->fontId];
    if (!font) return x;

    float scale = nvg__getFontScale(state) * ctx->devicePxRatio;
    float fontSize = state->fontSize * scale;

    Urho3D::FontFace* face;
    if (ctx->fontSizeMethod == 0)
        face = font->GetFace(fontSize);
    else
        face = font->GetFaceByPixel(fontSize);
    if (!face) return x;

    float invscale = 1.0f / scale;

    // 2. 处理水平对齐
    if (state->textAlign & NVG_ALIGN_CENTER) {
        float width = nvgTextBounds(ctx, 0, 0, string, end, NULL);
        x -= width * 0.5f;
    } else if (state->textAlign & NVG_ALIGN_RIGHT) {
        float width = nvgTextBounds(ctx, 0, 0, string, end, NULL);
        x -= width;
    }

    // 3. 处理垂直对齐
    float ascender = face->GetAscender();
    float descender = face->GetAscender() - face->GetRowHeight();
    if (state->textAlign & NVG_ALIGN_TOP)
        y += ascender * invscale;
    else if (state->textAlign & NVG_ALIGN_MIDDLE)
        y += (ascender + descender) * 0.5f * invscale;
    else if (state->textAlign & NVG_ALIGN_BOTTOM)
        y += descender * invscale;

    // 4. 分配顶点缓冲
    int cverts = nvg__maxi(2, (int)(end - string)) * 6;
    NVGvertex* verts = nvg__allocTempVerts(ctx, cverts);
    if (!verts) return x;

    int nverts = 0;
    float curX = x * scale;
    float curY = y * scale;

    // 合批状态
    int currentPage = -1;
    int currentIsColor = -1;
    unsigned int currentTexHandle = 0;

    // 5. 遍历 UTF-8 字符
    unsigned int codepoint;
    unsigned int utf8state = 0;
    unsigned int prevCodepoint = 0;  // 用于 kerning

    for (const char* s = string; s < end; s++) {
        if (nvg__decodeUTF8(&utf8state, &codepoint, *(unsigned char*)s))
            continue;

        const Urho3D::FontGlyph* glyph = face->GetGlyph(codepoint);
        if (!glyph) {
            prevCodepoint = 0;
            continue;
        }

        // Kerning
        if (prevCodepoint != 0)
            curX += face->GetKerning(prevCodepoint, codepoint);

        // 检查是否需要 flush（page 或 isColor 变化）
        int glyphPage = glyph->page_;
        int glyphIsColor = glyph->isColor_ ? 1 : 0;

        if (glyphPage != currentPage || glyphIsColor != currentIsColor) {
            if (nverts > 0) {
                nvg__renderTextBatch(ctx, currentTexHandle, currentIsColor, verts, nverts);
                nverts = 0;
            }
            currentPage = glyphPage;
            currentIsColor = glyphIsColor;

            // 获取纹理 handle
            const auto& textures = currentIsColor ? face->GetColorTextures() : face->GetTextures();
            if (currentPage < textures.Size() && textures[currentPage])
                currentTexHandle = textures[currentPage]->GetGPUObjectIdx();
        }

        // 计算顶点
        float gx = curX + glyph->offsetX_;
        float gy = curY + glyph->offsetY_;
        float gw = (float)glyph->texWidth_;
        float gh = (float)glyph->texHeight_;

        // 获取纹理尺寸计算 UV
        const auto& textures = currentIsColor ? face->GetColorTextures() : face->GetTextures();
        Urho3D::Texture* tex = textures[currentPage];
        float texW = (float)tex->GetWidth();
        float texH = (float)tex->GetHeight();

        float u0 = glyph->x_ / texW;
        float v0 = glyph->y_ / texH;
        float u1 = (glyph->x_ + glyph->texWidth_) / texW;
        float v1 = (glyph->y_ + glyph->texHeight_) / texH;

        // 变换到屏幕坐标
        float c[8];
        nvgTransformPoint(&c[0], &c[1], state->xform, gx*invscale, gy*invscale);
        nvgTransformPoint(&c[2], &c[3], state->xform, (gx+gw)*invscale, gy*invscale);
        nvgTransformPoint(&c[4], &c[5], state->xform, (gx+gw)*invscale, (gy+gh)*invscale);
        nvgTransformPoint(&c[6], &c[7], state->xform, gx*invscale, (gy+gh)*invscale);

        // 添加三角形顶点
        if (nverts + 6 <= cverts) {
            nvg__vset(&verts[nverts++], c[0], c[1], u0, v0);
            nvg__vset(&verts[nverts++], c[4], c[5], u1, v1);
            nvg__vset(&verts[nverts++], c[2], c[3], u1, v0);
            nvg__vset(&verts[nverts++], c[0], c[1], u0, v0);
            nvg__vset(&verts[nverts++], c[6], c[7], u0, v1);
            nvg__vset(&verts[nverts++], c[4], c[5], u1, v1);
        }

        curX += glyph->advanceX_ + state->letterSpacing * scale;
        prevCodepoint = codepoint;
    }

    // 6. 渲染最后一批
    if (nverts > 0) {
        nvg__renderTextBatch(ctx, currentTexHandle, currentIsColor, verts, nverts);
    }

    return curX / scale;
}
```

---

## nvgTextBounds 核心流程（Urho 路径）

**fontstash 原实现关键点**：
1. bounds 计算使用 `glyph->xoff/yoff` 和 `(x1-x0)/(y1-y0)`
2. 水平对齐是在**返回前调整 bounds**，不是调整起始 x
3. 返回值是 advance（文本总宽度）

```cpp
float nvgTextBounds(NVGcontext* ctx, float x, float y, const char* string, const char* end, float* bounds)
{
    NVGstate* state = nvg__getState(ctx);
    if (string == NULL || state->fontId < 0) return 0;
    if (end == NULL) end = string + strlen(string);

    Urho3D::Font* font = ctx->urhoFonts[state->fontId];
    if (!font) return 0;

    float scale = nvg__getFontScale(state) * ctx->devicePxRatio;
    float invscale = 1.0f / scale;
    float fontSize = state->fontSize * scale;

    Urho3D::FontFace* face;
    if (ctx->fontSizeMethod == 0)
        face = font->GetFace(fontSize);
    else
        face = font->GetFaceByPixel(fontSize);
    if (!face) return 0;

    // 垂直对齐偏移（与 nvgText 一致）
    float ascender = face->GetAscender();
    float descender = ascender - face->GetRowHeight();  // descender 为负值
    if (state->textAlign & NVG_ALIGN_TOP)
        y += ascender * invscale;
    else if (state->textAlign & NVG_ALIGN_MIDDLE)
        y += (ascender + descender) * 0.5f * invscale;
    else if (state->textAlign & NVG_ALIGN_BOTTOM)
        y += descender * invscale;

    // 初始化 bounds
    float minx = x, maxx = x;
    float miny = y, maxy = y;

    float curX = x * scale;
    unsigned int prevCodepoint = 0;
    unsigned int codepoint;
    unsigned int utf8state = 0;

    for (const char* s = string; s < end; s++) {
        if (nvg__decodeUTF8(&utf8state, &codepoint, *(unsigned char*)s))
            continue;

        const Urho3D::FontGlyph* glyph = face->GetGlyph(codepoint);
        if (!glyph) {
            prevCodepoint = 0;
            continue;
        }

        // Kerning
        if (prevCodepoint != 0)
            curX += face->GetKerning(prevCodepoint, codepoint);

        // 计算字形边界（关键：使用 offsetX/Y 和 texWidth/texHeight）
        float gx = curX + glyph->offsetX_;
        float gy = y * scale + glyph->offsetY_;

        // 只有非空字形才更新 bounds
        if (glyph->texWidth_ > 0 && glyph->texHeight_ > 0) {
            minx = nvg__minf(minx, gx * invscale);
            miny = nvg__minf(miny, gy * invscale);
            maxx = nvg__maxf(maxx, (gx + glyph->texWidth_) * invscale);
            maxy = nvg__maxf(maxy, (gy + glyph->texHeight_) * invscale);
        }

        curX += glyph->advanceX_ + state->letterSpacing * scale;
        prevCodepoint = codepoint;
    }

    float advance = curX * invscale - x;

    // 水平对齐调整 bounds（不是调整起始位置！）
    if (state->textAlign & NVG_ALIGN_CENTER) {
        minx -= advance * 0.5f;
        maxx -= advance * 0.5f;
    } else if (state->textAlign & NVG_ALIGN_RIGHT) {
        minx -= advance;
        maxx -= advance;
    }

    if (bounds) {
        bounds[0] = minx;
        bounds[1] = miny;
        bounds[2] = maxx;
        bounds[3] = maxy;
    }

    return advance;
}
```

---

## nvgTextGlyphPositions 核心流程（Urho 路径）

返回每个字形的位置信息，用于光标定位、文本选择等。

```cpp
int nvgTextGlyphPositions(NVGcontext* ctx, float x, float y, const char* string, const char* end,
                          NVGglyphPosition* positions, int maxPositions)
{
    NVGstate* state = nvg__getState(ctx);
    if (string == NULL || state->fontId < 0) return 0;
    if (end == NULL) end = string + strlen(string);

    Urho3D::Font* font = ctx->urhoFonts[state->fontId];
    if (!font) return 0;

    float scale = nvg__getFontScale(state) * ctx->devicePxRatio;
    float invscale = 1.0f / scale;
    float fontSize = state->fontSize * scale;

    Urho3D::FontFace* face;
    if (ctx->fontSizeMethod == 0)
        face = font->GetFace(fontSize);
    else
        face = font->GetFaceByPixel(fontSize);
    if (!face) return 0;

    float curX = x * scale;
    unsigned int prevCodepoint = 0;
    unsigned int codepoint;
    unsigned int utf8state = 0;
    int npos = 0;

    for (const char* s = string; s < end && npos < maxPositions; s++) {
        if (nvg__decodeUTF8(&utf8state, &codepoint, *(unsigned char*)s))
            continue;

        const Urho3D::FontGlyph* glyph = face->GetGlyph(codepoint);

        // Kerning
        if (prevCodepoint != 0 && glyph)
            curX += face->GetKerning(prevCodepoint, codepoint);

        // 记录位置（即使 glyph 为空也记录，用于光标定位）
        positions[npos].str = s;
        positions[npos].x = curX * invscale;

        if (glyph) {
            float gx = curX + glyph->offsetX_;
            positions[npos].minx = gx * invscale;
            positions[npos].maxx = (gx + glyph->texWidth_) * invscale;

            curX += glyph->advanceX_ + state->letterSpacing * scale;
            prevCodepoint = codepoint;
        } else {
            positions[npos].minx = curX * invscale;
            positions[npos].maxx = curX * invscale;
            prevCodepoint = 0;
        }

        npos++;
    }

    return npos;
}
```

---

## nvgTextBreakLines 核心流程（Urho 路径）

将文本按指定宽度分成多行，用于 `nvgTextBox` 等换行渲染。

**关键逻辑**：
1. 遍历字符，累计宽度
2. 遇到空格/标点时记录为潜在换行点
3. 超过 breakRowWidth 时在最近的换行点断开
4. CJK 字符可以在任意位置换行
5. 强制换行符（`\n`, `\r`）直接断开

```cpp
// 字符类型定义（与 nanovg 原实现一致）
enum NVGcodepointType {
    NVG_SPACE,      // 空格
    NVG_NEWLINE,    // 换行符
    NVG_CHAR,       // 普通字符
    NVG_CJK_CHAR,   // CJK 字符（可任意位置换行）
};

static int nvg__isSpace(unsigned int codepoint) {
    return codepoint == ' ' || codepoint == '\t';
}

static int nvg__isNewline(unsigned int codepoint) {
    return codepoint == '\n' || codepoint == '\r';
}

static int nvg__isCJK(unsigned int codepoint) {
    // CJK 统一表意文字范围
    return (codepoint >= 0x4E00 && codepoint <= 0x9FFF) ||   // CJK Unified Ideographs
           (codepoint >= 0x3000 && codepoint <= 0x303F) ||   // CJK Symbols and Punctuation
           (codepoint >= 0x3040 && codepoint <= 0x309F) ||   // Hiragana
           (codepoint >= 0x30A0 && codepoint <= 0x30FF) ||   // Katakana
           (codepoint >= 0xFF00 && codepoint <= 0xFFEF) ||   // Halfwidth and Fullwidth Forms
           (codepoint >= 0xAC00 && codepoint <= 0xD7AF);     // Hangul Syllables
}

static int nvg__getCodepointType(unsigned int codepoint) {
    if (nvg__isNewline(codepoint)) return NVG_NEWLINE;
    if (nvg__isSpace(codepoint)) return NVG_SPACE;
    if (nvg__isCJK(codepoint)) return NVG_CJK_CHAR;
    return NVG_CHAR;
}

int nvgTextBreakLines(NVGcontext* ctx, const char* string, const char* end,
                      float breakRowWidth, NVGtextRow* rows, int maxRows)
{
    NVGstate* state = nvg__getState(ctx);
    if (string == NULL || state->fontId < 0) return 0;
    if (end == NULL) end = string + strlen(string);
    if (maxRows == 0) return 0;

    Urho3D::Font* font = ctx->urhoFonts[state->fontId];
    if (!font) return 0;

    float scale = nvg__getFontScale(state) * ctx->devicePxRatio;
    float invscale = 1.0f / scale;
    float fontSize = state->fontSize * scale;

    Urho3D::FontFace* face;
    if (ctx->fontSizeMethod == 0)
        face = font->GetFace(fontSize);
    else
        face = font->GetFaceByPixel(fontSize);
    if (!face) return 0;

    int nrows = 0;
    float rowStartX = 0;
    float rowWidth = 0;
    float rowMinX = 0;
    float rowMaxX = 0;
    const char* rowStart = NULL;
    const char* rowEnd = NULL;
    const char* wordStart = NULL;
    float wordStartX = 0;
    float wordMinX = 0;
    const char* breakEnd = NULL;
    float breakWidth = 0;
    float breakMaxX = 0;
    int type = NVG_SPACE;
    int prevType = NVG_SPACE;

    unsigned int codepoint;
    unsigned int utf8state = 0;
    unsigned int prevCodepoint = 0;

    for (const char* s = string; s < end; s++) {
        if (nvg__decodeUTF8(&utf8state, &codepoint, *(unsigned char*)s))
            continue;

        prevType = type;
        type = nvg__getCodepointType(codepoint);

        // 强制换行
        if (type == NVG_NEWLINE) {
            // 结束当前行
            if (rowStart != NULL) {
                rows[nrows].start = rowStart;
                rows[nrows].end = rowEnd != NULL ? rowEnd : s;
                rows[nrows].width = rowWidth * invscale;
                rows[nrows].minx = rowMinX * invscale;
                rows[nrows].maxx = rowMaxX * invscale;
                rows[nrows].next = s + 1;
                nrows++;
                if (nrows >= maxRows)
                    return nrows;
            }
            // 重置行状态
            rowStart = NULL;
            rowEnd = NULL;
            rowWidth = 0;
            rowMinX = 0;
            rowMaxX = 0;
            wordStart = NULL;
            breakEnd = NULL;
            prevCodepoint = 0;
            continue;
        }

        const Urho3D::FontGlyph* glyph = face->GetGlyph(codepoint);
        if (!glyph) {
            prevCodepoint = 0;
            continue;
        }

        // Kerning
        float kerning = 0;
        if (prevCodepoint != 0)
            kerning = face->GetKerning(prevCodepoint, codepoint);

        float advance = glyph->advanceX_ + state->letterSpacing * scale + kerning;
        float gx = rowStartX + rowWidth + kerning + glyph->offsetX_;
        float gw = (float)glyph->texWidth_;

        // 开始新行
        if (rowStart == NULL) {
            // 跳过行首空格
            if (type == NVG_SPACE) {
                prevCodepoint = codepoint;
                continue;
            }
            rowStart = s;
            rowStartX = 0;
            rowWidth = 0;
            rowMinX = gx;
            rowMaxX = gx + gw;
            wordStart = s;
            wordStartX = 0;
            wordMinX = gx;
            breakEnd = NULL;
        }

        // 记录潜在换行点
        if (prevType == NVG_SPACE && type == NVG_CHAR) {
            // 空格后的普通字符 - 单词开始
            wordStart = s;
            wordStartX = rowWidth;
            wordMinX = gx;
        }
        if (prevType == NVG_CHAR && type == NVG_SPACE) {
            // 普通字符后的空格 - 可以在这里换行
            breakEnd = s;
            breakWidth = rowWidth;
            breakMaxX = rowMaxX;
        }
        if (type == NVG_CJK_CHAR) {
            // CJK 字符可以在任意位置换行
            breakEnd = s;
            breakWidth = rowWidth;
            breakMaxX = rowMaxX;
            wordStart = s;
            wordStartX = rowWidth;
            wordMinX = gx;
        }

        // 更新行宽度
        rowWidth += advance;
        if (glyph->texWidth_ > 0)
            rowMaxX = nvg__maxf(rowMaxX, gx + gw);
        rowEnd = s + 1;  // 指向下一个字符

        // 检查是否超过宽度限制
        if (type != NVG_SPACE && rowWidth > breakRowWidth * scale) {
            if (breakEnd != NULL) {
                // 在最近的换行点断开
                rows[nrows].start = rowStart;
                rows[nrows].end = breakEnd;
                rows[nrows].width = breakWidth * invscale;
                rows[nrows].minx = rowMinX * invscale;
                rows[nrows].maxx = breakMaxX * invscale;
                rows[nrows].next = breakEnd;
                nrows++;
                if (nrows >= maxRows)
                    return nrows;

                // 从单词开始位置继续
                rowStart = wordStart;
                rowStartX = wordStartX;
                rowWidth -= wordStartX;
                rowMinX = wordMinX;
                rowMaxX = gx + gw;
                rowEnd = s + 1;
                wordStart = NULL;
                breakEnd = NULL;
            } else {
                // 没有换行点，强制在当前位置断开
                rows[nrows].start = rowStart;
                rows[nrows].end = s;
                rows[nrows].width = (rowWidth - advance) * invscale;
                rows[nrows].minx = rowMinX * invscale;
                rows[nrows].maxx = rowMaxX * invscale;
                rows[nrows].next = s;
                nrows++;
                if (nrows >= maxRows)
                    return nrows;

                // 从当前字符开始新行
                rowStart = s;
                rowStartX = 0;
                rowWidth = advance;
                rowMinX = glyph->offsetX_;
                rowMaxX = glyph->offsetX_ + gw;
                rowEnd = s + 1;
                wordStart = s;
                wordStartX = 0;
                wordMinX = glyph->offsetX_;
                breakEnd = NULL;
            }
        }

        prevCodepoint = codepoint;
    }

    // 处理最后一行
    if (rowStart != NULL) {
        rows[nrows].start = rowStart;
        rows[nrows].end = rowEnd;
        rows[nrows].width = rowWidth * invscale;
        rows[nrows].minx = rowMinX * invscale;
        rows[nrows].maxx = rowMaxX * invscale;
        rows[nrows].next = end;
        nrows++;
    }

    return nrows;
}
```

**NVGtextRow 结构**：
```cpp
struct NVGtextRow {
    const char* start;  // 行起始指针
    const char* end;    // 行结束指针（不含）
    const char* next;   // 下一行起始指针
    float width;        // 行宽度（不含尾部空格）
    float minx, maxx;   // 行的 x 边界
};
```

**关键点**：
1. **单词边界检测**：空格→字符 = 单词开始，字符→空格 = 可换行点
2. **CJK 处理**：每个 CJK 字符都是潜在换行点
3. **强制换行**：`\n` 和 `\r` 立即断行
4. **行首空格跳过**：新行开始时跳过前导空格
5. **宽度计算**：包含 kerning 和 letterSpacing

---

## nvgTextMetrics 核心流程（Urho 路径）

```cpp
void nvgTextMetrics(NVGcontext* ctx, float* ascender, float* descender, float* lineh)
{
    NVGstate* state = nvg__getState(ctx);
    if (state->fontId < 0) return;

    Urho3D::Font* font = ctx->urhoFonts[state->fontId];
    if (!font) return;

    float scale = nvg__getFontScale(state) * ctx->devicePxRatio;
    float invscale = 1.0f / scale;
    float fontSize = state->fontSize * scale;

    Urho3D::FontFace* face;
    if (ctx->fontSizeMethod == 0)
        face = font->GetFace(fontSize);
    else
        face = font->GetFaceByPixel(fontSize);
    if (!face) return;

    if (ascender)
        *ascender = face->GetAscender() * invscale;
    if (descender)
        *descender = (face->GetAscender() - face->GetRowHeight()) * invscale;
    if (lineh)
        *lineh = face->GetRowHeight() * invscale * state->lineHeight;
}
```

---

## 一致性保证检查清单

| 项目 | fontstash 原实现 | Urho 路径实现 | 状态 |
|------|-----------------|--------------|------|
| **字形前进量** | `glyph->xadv / 10.0f` | `glyph->advanceX_` | ✅ 单位一致 |
| **字形偏移** | `glyph->xoff/yoff` (像素) | `glyph->offsetX_/offsetY_` (像素) | ✅ 单位一致 |
| **字形尺寸** | `x1-x0`, `y1-y0` (纹理像素) | `texWidth_`, `texHeight_` (纹理像素) | ✅ 单位一致 |
| **Kerning** | `getKernAdvance() * scale` | `face->GetKerning()` | ✅ 已实现 |
| **letterSpacing** | `+ spacing` | `+ state->letterSpacing * scale` | ✅ 已实现 |
| **垂直对齐** | `ascender/descender * isize/10` | `face->GetAscender()` 等 (已是像素) | ✅ 逻辑一致 |
| **水平对齐** | bounds 计算后调整 | bounds 计算后调整 | ✅ 逻辑一致 |
| **多 page 合批** | N/A (fontstash 单 atlas) | 按 page + isColor flush | ✅ 已实现 |
| **换行算法** | 单词边界 + CJK 任意断 | 完全复刻原逻辑 | ✅ 已实现 |
| **行首空格** | 跳过 | 跳过 | ✅ 逻辑一致 |
| **强制换行** | `\n`/`\r` 立即断行 | `\n`/`\r` 立即断行 | ✅ 逻辑一致 |

---

## 引擎层修改（Font / FontFaceFreeType）

### Font.h 修改

```cpp
class URHO3D_API Font : public Resource
{
public:
    // ... 现有接口 ...

    /// Get font face by point size (uses FT_Set_Char_Size with 96 DPI)
    FontFace* GetFace(float pointSize, int blur = 0);

    /// Get font face by pixel size (uses FT_Set_Pixel_Sizes)
    FontFace* GetFaceByPixel(float pixelSize, int blur = 0);

private:
    /// Make face cache key from size and blur
    /// key = (size * 10) | (blur << 16)
    inline int MakeFaceKey(float size, int blur)
    {
        return ((int)(size * 10)) | (blur << 16);
    }

    /// Return font face using FreeType (point size). Called internally.
    FontFace* GetFaceFreeType(float pointSize, int blur = 0);

    /// Return font face using FreeType (pixel size). Called internally.
    FontFace* GetFaceFreeTypeByPixel(float pixelSize, int blur = 0);

    /// Return bitmap font face. Called internally.
    FontFace* GetFaceBitmap(float pointSize);

    /// Point size font faces (key = (pointSize * 10) | (blur << 16))
    HashMap<int, SharedPtr<FontFace>> faces_;

    /// Pixel size font faces (key = (pixelSize * 10) | (blur << 16))
    HashMap<int, SharedPtr<FontFace>> pixelFaces_;
};
```

### Font.cpp 实现

```cpp
FontFace* Font::GetFace(float pointSize, int blur)
{
    int key = MakeFaceKey(pointSize, blur);
    auto it = faces_.Find(key);
    if (it != faces_.End())
    {
        it->second_->AddUsedTimes();
        return it->second_;
    }

    switch (fontType_)
    {
    case FONT_FREETYPE:
#ifdef URHO3D_FREETYPE
        {
            auto face = GetFaceFreeType(pointSize, blur);
            if (face)
            {
                face->AddUsedTimes();
                return face;
            }
        }
#endif
        break;

    case FONT_BITMAP:
        // Bitmap font 不支持 blur
        if (blur == 0)
        {
            auto face = GetFaceBitmap(pointSize);
            if (face)
            {
                face->AddUsedTimes();
                return face;
            }
        }
        break;

    default:
        break;
    }

    return nullptr;
}

FontFace* Font::GetFaceByPixel(float pixelSize, int blur)
{
    int key = MakeFaceKey(pixelSize, blur);
    auto it = pixelFaces_.Find(key);
    if (it != pixelFaces_.End())
    {
        it->second_->AddUsedTimes();
        return it->second_;
    }

    switch (fontType_)
    {
    case FONT_FREETYPE:
#ifdef URHO3D_FREETYPE
        {
            auto face = GetFaceFreeTypeByPixel(pixelSize, blur);
            if (face)
            {
                face->AddUsedTimes();
                return face;
            }
        }
#endif
        break;

    default:
        // Bitmap font 不支持 pixel size
        break;
    }

    return nullptr;
}

FontFace* Font::GetFaceFreeType(float pointSize, int blur)
{
#ifdef URHO3D_FREETYPE
    SharedPtr<FontFaceFreeType> newFace(new FontFaceFreeType(this));
    if (loadAllGlyph_)
        newFace->SetLoadAllGlyph();
    if (!newFace->Load(&fontData_[0], fontDataSize_, pointSize, FONT_SIZE_POINT, blur))
        return nullptr;

    int key = MakeFaceKey(pointSize, blur);
    faces_[key] = newFace;
    return newFace;
#else
    return nullptr;
#endif
}

FontFace* Font::GetFaceFreeTypeByPixel(float pixelSize, int blur)
{
#ifdef URHO3D_FREETYPE
    SharedPtr<FontFaceFreeType> newFace(new FontFaceFreeType(this));
    if (loadAllGlyph_)
        newFace->SetLoadAllGlyph();
    if (!newFace->Load(&fontData_[0], fontDataSize_, pixelSize, FONT_SIZE_PIXEL, blur))
        return nullptr;

    int key = MakeFaceKey(pixelSize, blur);
    pixelFaces_[key] = newFace;
    return newFace;
#else
    return nullptr;
#endif
}
```

### FontFaceFreeType 修改

#### FontSizeMethod 枚举（FontDefs.h）

```cpp
enum FontSizeMethod
{
    FONT_SIZE_POINT = 0,  // FT_Set_Char_Size (point size + 96 DPI)
    FONT_SIZE_PIXEL = 1,  // FT_Set_Pixel_Sizes (pixel size)
};
```

#### Load 方法签名

```cpp
// FontFaceFreeType.h
class URHO3D_API FontFaceFreeType : public FontFace
{
public:
    bool Load(const unsigned char* fontData, unsigned fontDataSize,
              float size, FontSizeMethod sizeMethod = FONT_SIZE_POINT, int blur = 0) override;

private:
    FontSizeMethod sizeMethod_{FONT_SIZE_POINT};
    int blur_{0};
};
```

#### FreeType 调用

```cpp
// FontFaceFreeType.cpp - Load 中
if (sizeMethod_ == FONT_SIZE_PIXEL)
    FT_Set_Pixel_Sizes(face, 0, (FT_UInt)(size + 0.5f));
else
    FT_Set_Char_Size(face, 0, (FT_F26Dot6)(size * 64), 96, 96);
```

#### Blur Padding

blur 需要额外的 padding 来容纳模糊后扩散的像素（与 fontstash 一致）：

```cpp
// fontstash 中的 padding 计算
int pad = blur + 2;
```

**影响**：
1. **位图尺寸扩大**：`width + pad*2`, `height + pad*2`
2. **offset 调整**：`offsetX - pad`, `offsetY - pad`
3. **atlas 空间**：需要分配更大区域

#### Blur 算法（从 fontstash 移植）

```cpp
// FontFaceFreeType.cpp - LoadCharGlyph 中

if (blur_ > 0)
{
    int pad = blur_ + 2;

    // 1. 原始字形尺寸
    int origWidth = ftBitmap.width;
    int origHeight = ftBitmap.rows;

    // 2. 扩展后的尺寸（包含 padding）
    int newWidth = origWidth + pad * 2;
    int newHeight = origHeight + pad * 2;

    // 3. 分配扩展后的位图（初始化为 0）
    unsigned char* expandedBitmap = new unsigned char[newWidth * newHeight]();

    // 4. 将原始字形复制到中心位置
    for (int y = 0; y < origHeight; y++)
    {
        unsigned char* src = ftBitmap.buffer + y * ftBitmap.pitch;
        unsigned char* dst = expandedBitmap + (y + pad) * newWidth + pad;
        memcpy(dst, src, origWidth);
    }

    // 5. 应用模糊
    ApplyBlur(expandedBitmap, newWidth, newHeight, blur_);

    // 6. 调整 offset（向左上偏移 pad 像素）
    offsetX -= pad;
    offsetY -= pad;

    // 7. 使用扩展后的位图
    // ...
}

// ApplyBlur 实现（Exponential blur, from fontstash, Jani Huhtanen 2006）
#define APREC 16
#define ZPREC 7

void FontFaceFreeType::ApplyBlur(unsigned char* dst, int w, int h, int blur)
{
    if (blur < 1) return;
    float sigma = blur * 0.57735f;  // 1 / sqrt(3)
    int alpha = (int)((1 << APREC) * (1.0f - expf(-2.3f / (sigma + 1.0f))));
    BlurRows(dst, w, h, w, alpha);
    BlurCols(dst, w, h, w, alpha);
    BlurRows(dst, w, h, w, alpha);
    BlurCols(dst, w, h, w, alpha);
}

void FontFaceFreeType::BlurRows(unsigned char* dst, int w, int h, int stride, int alpha)
{
    for (int y = 0; y < h; y++)
    {
        int z = 0;
        for (int x = 1; x < w; x++)
        {
            z += (alpha * (((int)dst[x] << ZPREC) - z)) >> APREC;
            dst[x] = (unsigned char)(z >> ZPREC);
        }
        dst[w-1] = 0;
        z = 0;
        for (int x = w-2; x >= 0; x--)
        {
            z += (alpha * (((int)dst[x] << ZPREC) - z)) >> APREC;
            dst[x] = (unsigned char)(z >> ZPREC);
        }
        dst[0] = 0;
        dst += stride;
    }
}

void FontFaceFreeType::BlurCols(unsigned char* dst, int w, int h, int stride, int alpha)
{
    for (int x = 0; x < w; x++)
    {
        int z = 0;
        for (int y = stride; y < h * stride; y += stride)
        {
            z += (alpha * (((int)dst[y] << ZPREC) - z)) >> APREC;
            dst[y] = (unsigned char)(z >> ZPREC);
        }
        dst[(h-1) * stride] = 0;
        z = 0;
        for (int y = (h-2) * stride; y >= 0; y -= stride)
        {
            z += (alpha * (((int)dst[y] << ZPREC) - z)) >> APREC;
            dst[y] = (unsigned char)(z >> ZPREC);
        }
        dst[0] = 0;
        dst++;
    }
}
```

### Size 精度与 Cache Key

| | 计算方式 | 精度 |
|--|----------|------|
| 引擎（修改后） | `size * 10` | 0.1 像素 |
| NanoVG | `size * 10` | 0.1 像素 |

Cache Key 编码：
```cpp
// key = (size * 10) | (blur << 16)
int key = ((int)(size * 10)) | (blur << 16);
```

---

## 实现步骤

### Phase 1: 文件头部和结构修改
1. [ ] 添加 `#if NANOVG_USE_URHO_FONT` 条件编译 fontstash.h 包含
2. [ ] 定义 `NVG_MAX_URHO_FONTS` 常量
3. [ ] 修改 `NVGcontext` 结构，添加 Urho 专用字段

### Phase 2: 初始化和销毁
4. [ ] 修改 `nvgCreateInternal` - Urho 路径初始化
5. [ ] 修改 `nvgDeleteInternal` - Urho 路径清理

### Phase 3: 字体管理函数
6. [ ] 修改 `nvgCreateFontUrho` - 直接存入数组
7. [ ] 修改 `nvgCreateFont` / `nvgCreateFontMem` - Urho 路径返回 -1
8. [ ] 修改 `nvgFindFont` - 遍历 `urhoFontNames` 查找
9. [ ] 修改 `nvgFontFace` - 调用 `nvgFindFont`
10. [ ] 修改 `nvgFontSizeMethod` / `nvgGetFontSizeMethod` - 操作 `ctx->fontSizeMethod`
11. [ ] 修改 `nvgAddFallbackFontId` / `nvgForceAutoHint` 等 - 空实现

### Phase 4: 核心渲染函数
12. [ ] 实现 `nvg__renderTextBatch` - 支持传入纹理 handle
13. [ ] 修改 `nvgText` - Urho 路径完整实现
14. [ ] 修改 `nvgTextBounds` - Urho 路径实现
15. [ ] 修改 `nvgTextGlyphPositions` - Urho 路径实现
16. [ ] 修改 `nvgTextBreakLines` - Urho 路径实现
17. [ ] 修改 `nvgTextMetrics` - 从 FontFace 获取度量

### Phase 5: 辅助函数
18. [ ] 修改 `nvg__flushTextTexture` - Urho 路径空实现
19. [ ] 修改 `nvg__allocTextAtlas` - Urho 路径空实现
20. [ ] 修改 `nvgTextBox` / `nvgTextBoxBounds` - 复用其他函数

### Phase 6: 测试验证
21. [ ] 基本文本渲染测试
22. [ ] 中文/Emoji 测试
23. [ ] 对齐方式测试
24. [ ] letterSpacing 测试
25. [ ] 多 page 纹理测试

---

## 验证方案

```lua
-- 基本文本
nvgText(ctx, 100, 100, "Hello World")

-- 中文
nvgText(ctx, 100, 150, "你好世界")

-- Emoji
nvgText(ctx, 100, 200, "Hello 😀🎉")

-- 不同对齐方式
nvgTextAlign(ctx, NVG_ALIGN_LEFT | NVG_ALIGN_TOP)
nvgText(ctx, 200, 100, "Left Top")

nvgTextAlign(ctx, NVG_ALIGN_CENTER | NVG_ALIGN_MIDDLE)
nvgText(ctx, 200, 150, "Center Middle")

nvgTextAlign(ctx, NVG_ALIGN_RIGHT | NVG_ALIGN_BOTTOM)
nvgText(ctx, 200, 200, "Right Bottom")

-- 字间距
nvgTextLetterSpacing(ctx, 5)
nvgText(ctx, 100, 300, "Spaced Text")

-- 不同字号
for size = 12, 48, 12 do
    nvgFontSize(ctx, size)
    nvgText(ctx, 100, 350 + size, "Size " .. size)
end
```

---

## 风险与缓解

| 风险 | 缓解措施 |
|------|---------|
| 多 page 渲染顺序错乱 | 按 page + isColor 分批，保持顺序 |
| 对齐结果与原版不一致 | 完全复刻原算法，逐行对比 |
| letterSpacing 单位不一致 | 确保乘以 scale |
| 纹理 handle 无效 | 检查 page 范围和纹理指针 |

---

*最后更新: 2026-01-10*
