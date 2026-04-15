---
summary: "NanoVG BGFX backend draw call batching optimization to reduce bgfx::submit() calls"
related_paths:
  - engine/Source/ThirdParty/bgfx-all/bgfx/examples/common/nanovg/**
last_updated: "2026-04-02"
---

# NanoVG Draw Call Batching Design

NanoVG BGFX 后端的 Draw Call (DC) 合批优化架构，通过减少 `bgfx::submit()` 调用次数提升渲染性能。

**相关文件**: `engine/Source/ThirdParty/bgfx-all/bgfx/examples/common/nanovg/nanovg_bgfx.cpp`

## 合批方案总览

| 方案 | 目标场景 | DC 减少 | 实现日期 |
|------|----------|---------|----------|
| TRIANGLES 跨 call 合批 | 大量文本渲染 | 50-90% | 2024-12-03 |
| ConvexFill 跨 call 合批 | UI 矩形/按钮 | 45-90% | 2024-12-03 |
| Fill 内部多 path 合批 | 非凸多边形 | ~99% | 2024-12-04 |
| ConvexFill 内部多 path 合批 | 凸多边形 | ~99% | 2024-12-04 |
| Stroke 内部多 path 合批 | 描边 | ~99% | 2024-12-04 |

---

## 调试开关

### NVG_BATCH_ENABLED 宏

提供了一个编译时宏 `NVG_BATCH_ENABLED` 用于控制合批优化的开关，方便调试和性能对比：

```cpp
// 在 nanovg_bgfx.cpp 文件顶部定义
// Enable/disable draw call batching optimization
// Set to 0 to disable batching for debugging/comparison
#ifndef NVG_BATCH_ENABLED
#define NVG_BATCH_ENABLED 1
#endif
```

**使用方法**:

| 设置 | 效果 |
|------|------|
| `NVG_BATCH_ENABLED 1` (默认) | 启用所有合批优化 |
| `NVG_BATCH_ENABLED 0` | 禁用合批，每个 path 单独渲染 |

**控制范围**:

- `glnvg__fill()`: Stencil Pass 和 Fringe Pass 的内部合批
- `glnvg__convexFill()`: Fill Pass 和 Fringe Pass 的内部合批
- `glnvg__stroke()`: Stroke tristrip 的内部合批
- `nvgRenderFlush()`: CONVEXFILL 和 TRIANGLES 的跨 call 合批

**用途**:
1. **调试**: 禁用合批后可以更容易定位渲染问题
2. **性能对比**: 对比优化前后的 DC 数量和帧率
3. **回归测试**: 验证合批逻辑的正确性

---

## 当前渲染架构分析

### Draw Call 产生位置

| 函数 | DC 产生原因 | 代码位置 |
|------|-------------|----------|
| `glnvg__fill()` | 非凸多边形: stencil fill + fringe + final fill | 618-689 行 |
| `glnvg__convexFill()` | 凸多边形: 每个 path 1 DC + fringe DC | 691-722 行 |
| `glnvg__stroke()` | 描边: 每个 path 1 DC | 724-742 行 |
| `glnvg__triangles()` | 三角形(文本): 每个 call 1 DC | 744-756 行 |

### 无法合批的原因

1. **状态变化频繁**: 每个绘制可能有不同的 blend mode、uniform、texture
2. **Stencil Fill 多 Pass**: 非凸多边形使用 stencil buffer，必须分步渲染
3. **图元类型不同**: Fill 用 triangle fan，Stroke 用 triangle strip

### 可合批的场景

1. **连续的 TRIANGLES 调用**: 文本渲染，属性相同时可合并
2. **连续的 CONVEXFILL 调用**: UI 矩形/圆角矩形，属性相同时可合并

---

## 方案 1: TRIANGLES Call 合批

### 目标场景

文本渲染。每次 `nvgText()` 产生一个 `GLNVG_TRIANGLES` call，连续相同属性的文本可合并。

```
优化前:
nvgText("Hello")  → call[0]: TRIANGLES, verts[0..17]   → DC 1
nvgText("World")  → call[1]: TRIANGLES, verts[18..35]  → DC 2
nvgText("!")      → call[2]: TRIANGLES, verts[36..41]  → DC 3
                                                总计: 3 DC

优化后:
nvgText("Hello")  → call[0]: TRIANGLES, verts[0..17]
nvgText("World")  → call[1]: TRIANGLES, verts[18..35]  → 合并
nvgText("!")      → call[2]: TRIANGLES, verts[36..41]
                  → 单次渲染 verts[0..41]              → DC 1
                                                总计: 1 DC
```

### 合批条件

两个连续的 TRIANGLES call 可合并，当且仅当：

1. `call[i].type == call[i+1].type == GLNVG_TRIANGLES`
2. `call[i].image == call[i+1].image` (相同纹理，通常是字体纹理)
3. `call[i].blendFunc == call[i+1].blendFunc` (相同混合模式)
4. `uniformOffset` 指向的 uniform 数据相同 (scissor、颜色等)
5. 顶点在 buffer 中连续 (vertex offset 连续)

### 实现代码

#### 1. 添加合批条件检查函数

```cpp
static bool glnvg__canMergeTriangles(struct GLNVGcontext* gl,
    struct GLNVGcall* a, struct GLNVGcall* b)
{
    // 类型必须都是 TRIANGLES
    if (a->type != GLNVG_TRIANGLES || b->type != GLNVG_TRIANGLES)
        return false;

    // 纹理必须相同
    if (a->image != b->image)
        return false;

    // 混合模式必须相同
    if (a->blendFunc.srcRGB != b->blendFunc.srcRGB ||
        a->blendFunc.dstRGB != b->blendFunc.dstRGB ||
        a->blendFunc.srcAlpha != b->blendFunc.srcAlpha ||
        a->blendFunc.dstAlpha != b->blendFunc.dstAlpha)
        return false;

    // 比较 uniform 数据 (scissor, paint, color 等)
    struct GLNVGfragUniforms* ua = nvg__fragUniformPtr(gl, a->uniformOffset);
    struct GLNVGfragUniforms* ub = nvg__fragUniformPtr(gl, b->uniformOffset);
    return bx::memCmp(ua, ub, sizeof(struct GLNVGfragUniforms)) == 0;
}
```

#### 2. 添加合批渲染函数

```cpp
static void glnvg__trianglesBatched(struct GLNVGcontext* gl,
    int vertexOffset, int vertexCount, int uniformOffset, int image)
{
    if (vertexCount < 3)
        return;

    nvgRenderSetUniforms(gl, uniformOffset, image);
    bgfx::setState(gl->state);
    bgfx::setVertexBuffer(0, &gl->tvb, vertexOffset, vertexCount);
    bgfx::setTexture(0, gl->s_tex, gl->th);
    bgfx::submit(gl->viewId, gl->prog);
    gl->nsubmits++;
}
```

#### 3. 修改 nvgRenderFlush() 中 TRIANGLES 的处理

```cpp
case GLNVG_TRIANGLES:
{
    // 尝试合批连续的 TRIANGLES
    int mergedVertexOffset = call->vertexOffset;
    int mergedVertexCount = call->vertexCount;
    int uniformOffset = call->uniformOffset;
    int image = call->image;

    // 向后查找可合并的 calls
    uint32_t jj = ii + 1;
    while (jj < (uint32_t)gl->ncalls)
    {
        struct GLNVGcall* next = &gl->calls[jj];

        // 检查是否可合并
        if (!glnvg__canMergeTriangles(gl, call, next))
            break;

        // 检查顶点是否连续 (关键!)
        if (next->vertexOffset != mergedVertexOffset + mergedVertexCount)
            break;

        mergedVertexCount += next->vertexCount;
        jj++;
    }

    // 一次性渲染合并后的顶点
    glnvg__trianglesBatched(gl, mergedVertexOffset,
        mergedVertexCount, uniformOffset, image);

    ii = jj; // 跳过已合并的 calls
}
break;
```

### 预期收益

| 场景 | 优化前 DC | 优化后 DC | 减少比例 |
|------|-----------|-----------|----------|
| 10 段连续文本 | 10 | 1 | 90% |
| 文本穿插其他绘制 | 10 | 3-5 | 50-70% |
| 不同颜色文本 | 10 | 10 | 0% |

---

## 方案 3: Convex Fill 合批

### 目标场景

UI 界面的矩形、圆角矩形等凸多边形。`glnvg__convexFill()` 当前每个 path 单独渲染。

```
优化前:
nvgFillRect(r1)  → path[0]: fillCount=4  → DC 1 (+ fringe DC)
nvgFillRect(r2)  → path[1]: fillCount=4  → DC 2 (+ fringe DC)
nvgFillRect(r3)  → path[2]: fillCount=4  → DC 3 (+ fringe DC)
                                    总计: 3 DC (不含 fringe)

优化后:
nvgFillRect(r1)  → path[0]: fillCount=4
nvgFillRect(r2)  → path[1]: fillCount=4  → 合并 index buffer
nvgFillRect(r3)  → path[2]: fillCount=4
                 → 单次渲染                → DC 1
                                    总计: 1 DC (不含 fringe)
```

### 技术难点

Convex fill 使用 **triangle fan** 拓扑:

```cpp
// fan() 函数生成索引
// 顶点: [0, 1, 2, 3, 4]
// 索引: [0,1,2], [0,2,3], [0,3,4]
//       中心点始终是 0
```

**问题**: 不同 path 的 fan 中心点不同，无法简单合并。

**解决方案**: 预先将所有 fan 转换为 triangle list，合并到同一个 index buffer。

### 合批条件

```cpp
static bool glnvg__canMergeConvexFill(struct GLNVGcontext* gl,
    struct GLNVGcall* a, struct GLNVGcall* b)
{
    // 类型必须都是 CONVEXFILL
    if (a->type != GLNVG_CONVEXFILL || b->type != GLNVG_CONVEXFILL)
        return false;

    // 纹理必须相同
    if (a->image != b->image)
        return false;

    // 混合模式必须相同
    if (a->blendFunc.srcRGB != b->blendFunc.srcRGB ||
        a->blendFunc.dstRGB != b->blendFunc.dstRGB ||
        a->blendFunc.srcAlpha != b->blendFunc.srcAlpha ||
        a->blendFunc.dstAlpha != b->blendFunc.dstAlpha)
        return false;

    // 比较 uniform 数据
    struct GLNVGfragUniforms* ua = nvg__fragUniformPtr(gl, a->uniformOffset);
    struct GLNVGfragUniforms* ub = nvg__fragUniformPtr(gl, b->uniformOffset);
    return bx::memCmp(ua, ub, sizeof(struct GLNVGfragUniforms)) == 0;
}
```

### 实现代码

#### 1. 合批渲染函数

```cpp
static void glnvg__convexFillBatched(struct GLNVGcontext* gl,
    struct GLNVGcall* calls, uint32_t startIdx, uint32_t endIdx)
{
    // 1. 计算总三角形数量
    int totalTris = 0;
    for (uint32_t i = startIdx; i < endIdx; i++)
    {
        struct GLNVGcall* call = &calls[i];
        struct GLNVGpath* paths = &gl->paths[call->pathOffset];
        for (int j = 0; j < call->pathCount; j++)
        {
            if (paths[j].fillCount >= 3)
                totalTris += paths[j].fillCount - 2;
        }
    }

    if (totalTris == 0)
        return;

    // 2. 分配合并的 index buffer
    bgfx::TransientIndexBuffer tib;
    if (!bgfx::allocTransientIndexBuffer(&tib, totalTris * 3))
    {
        // 回退到非合批渲染
        for (uint32_t i = startIdx; i < endIdx; i++)
        {
            glnvg__convexFill(gl, &calls[i]);
        }
        return;
    }

    uint16_t* indices = (uint16_t*)tib.data;
    int idxOffset = 0;

    // 3. 为每个 path 生成 fan → triangle list 索引
    for (uint32_t i = startIdx; i < endIdx; i++)
    {
        struct GLNVGcall* call = &calls[i];
        struct GLNVGpath* paths = &gl->paths[call->pathOffset];
        for (int j = 0; j < call->pathCount; j++)
        {
            int fillOffset = paths[j].fillOffset;
            int fillCount = paths[j].fillCount;
            if (fillCount < 3)
                continue;

            // Fan to triangle list 转换
            // fan: center=fillOffset, vertices=[fillOffset+1, fillOffset+2, ...]
            // 实际上 NanoVG 的 fan 是 [0,1,2], [0,2,3], ...
            for (int k = 0; k < fillCount - 2; k++)
            {
                indices[idxOffset++] = (uint16_t)fillOffset;
                indices[idxOffset++] = (uint16_t)(fillOffset + k + 1);
                indices[idxOffset++] = (uint16_t)(fillOffset + k + 2);
            }
        }
    }

    // 4. 设置 uniform (使用第一个 call 的)
    struct GLNVGcall* firstCall = &calls[startIdx];
    nvgRenderSetUniforms(gl, firstCall->uniformOffset, firstCall->image);

    // 5. 单次提交
    bgfx::setState(gl->state);
    bgfx::setVertexBuffer(0, &gl->tvb);
    bgfx::setIndexBuffer(&tib);
    bgfx::setTexture(0, gl->s_tex, gl->th);
    bgfx::submit(gl->viewId, gl->prog);
    gl->nsubmits++;
}
```

#### 2. Fringe 单独渲染函数

```cpp
static void glnvg__renderFringes(struct GLNVGcontext* gl, struct GLNVGcall* call)
{
    struct GLNVGpath* paths = &gl->paths[call->pathOffset];
    int npaths = call->pathCount;

    for (int i = 0; i < npaths; i++)
    {
        if (paths[i].strokeCount == 0)
            continue;

        bgfx::setState(gl->state | BGFX_STATE_PT_TRISTRIP);
        bgfx::setVertexBuffer(0, &gl->tvb, paths[i].strokeOffset, paths[i].strokeCount);
        bgfx::setTexture(0, gl->s_tex, gl->th);
        bgfx::submit(gl->viewId, gl->prog);
        gl->nsubmits++;
    }
}
```

#### 3. 修改 nvgRenderFlush() 中 CONVEXFILL 的处理

```cpp
case GLNVG_CONVEXFILL:
{
    // 查找可合批的连续 convex fill
    uint32_t batchEnd = ii + 1;
    while (batchEnd < (uint32_t)gl->ncalls &&
           glnvg__canMergeConvexFill(gl, call, &gl->calls[batchEnd]))
    {
        batchEnd++;
    }

    uint32_t batchSize = batchEnd - ii;

    if (batchSize > 1)
    {
        // 合批渲染 fill
        glnvg__convexFillBatched(gl, gl->calls, ii, batchEnd);

        // 单独处理 fringe (如果启用 edge AA)
        if (gl->edgeAntiAlias)
        {
            for (uint32_t k = ii; k < batchEnd; k++)
            {
                glnvg__renderFringes(gl, &gl->calls[k]);
            }
        }
    }
    else
    {
        // 单个 call，使用原逻辑
        glnvg__convexFill(gl, call);
    }

    ii = batchEnd;
}
break;
```

### Index Buffer 16-bit 限制

当顶点数量超过 65535 时，16-bit index buffer 会溢出。需要添加检查:

```cpp
// 在 glnvg__convexFillBatched 开头添加检查
int maxVertexIndex = 0;
for (uint32_t i = startIdx; i < endIdx; i++)
{
    struct GLNVGcall* call = &calls[i];
    struct GLNVGpath* paths = &gl->paths[call->pathOffset];
    for (int j = 0; j < call->pathCount; j++)
    {
        int endIdx = paths[j].fillOffset + paths[j].fillCount;
        if (endIdx > maxVertexIndex)
            maxVertexIndex = endIdx;
    }
}

if (maxVertexIndex > 65535)
{
    // 回退到非合批渲染
    for (uint32_t i = startIdx; i < endIdx; i++)
    {
        glnvg__convexFill(gl, &calls[i]);
    }
    return;
}
```

### 预期收益

| 场景 | 优化前 DC | 优化后 DC | 减少比例 |
|------|-----------|-----------|----------|
| 10 个相同颜色矩形 | 10 | 1 | 90% |
| 带 edge AA | 20 | 11 | 45% |
| 不同颜色矩形 | 10 | 10 | 0% |

---

## 完整的 nvgRenderFlush() 修改

```cpp
static void nvgRenderFlush(void* _userPtr)
{
    struct GLNVGcontext* gl = (struct GLNVGcontext*)_userPtr;

    gl->nsubmits = 0;  // Reset submit counter

    if (gl->ncalls > 0 && gl->nverts > 0)
    {
        bgfx::allocTransientVertexBuffer(&gl->tvb, gl->nverts, s_nvgLayout);

        int allocated = gl->tvb.size / gl->tvb.stride;
        if (allocated < gl->nverts)
        {
            gl->nverts = allocated;
            BX_WARN(true, "Vertex number truncated due to transient vertex buffer overflow");
        }

        bx::memCopy(gl->tvb.data, gl->verts, gl->nverts * sizeof(struct NVGvertex));
        bgfx::setUniform(gl->u_viewSize, gl->view);

        uint32_t ii = 0;
        while (ii < (uint32_t)gl->ncalls)
        {
            struct GLNVGcall* call = &gl->calls[ii];
            const GLNVGblend* blend = &call->blendFunc;
            gl->state = BGFX_STATE_BLEND_FUNC_SEPARATE(
                    blend->srcRGB, blend->dstRGB,
                    blend->srcAlpha, blend->dstAlpha)
                | BGFX_STATE_WRITE_RGB
                | BGFX_STATE_WRITE_A;

            switch (call->type)
            {
            case GLNVG_FILL:
                glnvg__fill(gl, call);
                ii++;
                break;

            case GLNVG_CONVEXFILL:
                {
                    // 方案 3: Convex Fill 合批
                    uint32_t batchEnd = ii + 1;
                    while (batchEnd < (uint32_t)gl->ncalls &&
                           glnvg__canMergeConvexFill(gl, call, &gl->calls[batchEnd]))
                    {
                        batchEnd++;
                    }

                    if (batchEnd - ii > 1)
                    {
                        glnvg__convexFillBatched(gl, gl->calls, ii, batchEnd);
                        if (gl->edgeAntiAlias)
                        {
                            for (uint32_t k = ii; k < batchEnd; k++)
                            {
                                glnvg__renderFringes(gl, &gl->calls[k]);
                            }
                        }
                    }
                    else
                    {
                        glnvg__convexFill(gl, call);
                    }
                    ii = batchEnd;
                }
                break;

            case GLNVG_STROKE:
                glnvg__stroke(gl, call);
                ii++;
                break;

            case GLNVG_TRIANGLES:
                {
                    // 方案 1: TRIANGLES 合批
                    int mergedVertexOffset = call->vertexOffset;
                    int mergedVertexCount = call->vertexCount;
                    int uniformOffset = call->uniformOffset;
                    int image = call->image;

                    uint32_t jj = ii + 1;
                    while (jj < (uint32_t)gl->ncalls)
                    {
                        struct GLNVGcall* next = &gl->calls[jj];
                        if (!glnvg__canMergeTriangles(gl, call, next))
                            break;
                        if (next->vertexOffset != mergedVertexOffset + mergedVertexCount)
                            break;
                        mergedVertexCount += next->vertexCount;
                        jj++;
                    }

                    glnvg__trianglesBatched(gl, mergedVertexOffset,
                        mergedVertexCount, uniformOffset, image);
                    ii = jj;
                }
                break;

            default:
                ii++;
                break;
            }
        }
    }

    // Reset calls
    gl->nverts = 0;
    gl->npaths = 0;
    gl->ncalls = 0;
    gl->nuniforms = 0;
}
```

---

## 测试与验证

### 使用 nvgGetStats() 监控

```cpp
// 在每帧结束时调用
int numDC, numVerts;
nvgGetStats(vg, &numDC, &numVerts);
printf("NanoVG: DC=%d, Verts=%d\n", numDC, numVerts);
```

### 测试用例

1. **文本合批测试**: 连续绘制 100 个相同颜色的文本，验证 DC 从 100 降到 1
2. **矩形合批测试**: 连续绘制 50 个相同颜色的矩形，验证 DC 减少
3. **混合场景测试**: 文本、矩形交替绘制，验证不会错误合批
4. **不同属性测试**: 不同颜色/纹理的绘制，验证不会错误合批

### 回归测试

- 确保视觉效果与优化前一致
- 确保 edge AA 效果正常
- 确保 scissor 裁剪正常
- 确保不同 blend mode 正常

---

## 进一步优化方向

### Fringe 合批 (未来)

当前 fringe (edge AA) 仍然逐个渲染。可以考虑:

1. **Degenerate triangles**: 用退化三角形连接多个 triangle strip
2. **Primitive restart**: 使用特殊索引值分隔不同 strip (需要硬件支持)

### Instancing (未来)

将 uniform 数据放入 instance buffer，单次 submit 渲染多个不同属性的图元。

**难点**:
- 需要修改 shader
- 不同纹理需要 texture array 或 bindless texture
- BGFX instance buffer 有大小限制

### 排序优化 (未来)

在 `nvgRenderFlush()` 前对 calls 进行排序，将相同属性的 calls 聚合在一起，增加合批机会。

**注意**: 可能影响渲染顺序，需要考虑透明度和遮挡关系。

---

## 总结

| 方案 | 复杂度 | 主要收益场景 | DC 减少 |
|------|--------|--------------|---------|
| TRIANGLES 合批 | 低 | 大量文本渲染 | 50-90% |
| ConvexFill 合批 | 中 | UI 矩形/按钮 | 45-90% |

**实现优先级**: 方案 1 > 方案 3

**风险**: 低。合批失败时自动回退到原逻辑，不影响正确性。

---

## 更新日志

- **2024-12-04**: 添加 NVG_BATCH_ENABLED 调试开关
  - 新增编译时宏 `NVG_BATCH_ENABLED` 控制合批优化开关
  - 默认值为 1 (启用)，设为 0 可禁用所有合批优化
  - 支持控制的范围:
    - `glnvg__fill()`: Stencil Pass 和 Fringe Pass 内部合批
    - `glnvg__convexFill()`: Fill Pass 和 Fringe Pass 内部合批
    - `glnvg__stroke()`: Stroke tristrip 内部合批
    - `nvgRenderFlush()`: CONVEXFILL 和 TRIANGLES 跨 call 合批
  - 用途: 调试、性能对比、回归测试

- **2024-12-04**: 实现 16-bit index buffer 分块处理 (Chunking) - 修复版
  - 解决问题: 合批后索引数量超过 65535 或顶点偏移超过 65535 导致的 bug
  - **核心策略**: 使用相对索引 + 顶点偏移
    - `batchVertexBase`: 当前 batch 的顶点起始位置
    - `batchVertexCount`: 当前 batch 需要的顶点数量
    - 索引值使用相对偏移 (0 ~ 65535 范围内)
    - 提交时通过 `setVertexBuffer(0, &tvb, vertexOffset, numVertices)` 设置顶点偏移
  - **重要**: 只有使用索引的 pass 才需要限制，纯顶点 pass 无限制
  - 新增辅助函数:
    - `glnvg__submitStencilBatchWithOffset(gl, indices, numIndices, vertexOffset, numVertices)`
    - `glnvg__submitConvexFillBatchWithOffset(gl, indices, numIndices, vertexOffset, numVertices)`
  - 修改 `glnvg__fill()`: Stencil Pass 支持分块 (索引+顶点偏移)，Fringe Pass 无限制 (顶点)
  - 修改 `glnvg__convexFill()`: Fill Pass 支持分块 (索引+顶点偏移)，Fringe Pass 无限制 (顶点)
  - 修改 `glnvg__convexFillBatched()`: 跨 call 合批支持分块 (索引+顶点偏移)
  - 修改 `glnvg__stroke()`: Stroke Pass 无限制 (顶点)
  - 策略: 无论顶点总数多大，只要每个 batch 内的相对索引不超过 65535，就可以合批

- **2024-12-04**: 实现内部多 path 合批优化
  - 修改 `glnvg__fill()`: 合批 Stencil Pass 和 Fringe Pass
    - Stencil: 将所有 path 的三角形合并到一个 index buffer
    - Fringe: 使用 degenerate triangles 连接多个 tristrip
    - DC 从 `2N+1` 降至 `3` (N = path 数量)
  - 修改 `glnvg__convexFill()`: 合批 Fill 和 Fringe Pass
    - Fill: 将所有 path 的三角形合并到一个 index buffer
    - Fringe: 使用 degenerate triangles 连接多个 tristrip
    - DC 从 `2N` 降至 `2` (开启 AA 时)
  - 修改 `glnvg__stroke()`: 合批所有 stroke tristrip
    - 使用 degenerate triangles 连接多个 tristrip
    - DC 从 `N` 降至 `1`

- **2024-12-03**: 实现方案 3 (ConvexFill 跨 call 合批)
  - 新增 `glnvg__canMergeConvexFill()` 函数
  - 新增 `glnvg__convexFillBatched()` 函数
  - 新增 `glnvg__renderFringes()` 函数
  - 修改 `nvgRenderFlush()` 支持 CONVEXFILL 合批

- **2024-12-03**: 实现方案 1 (TRIANGLES 跨 call 合批)
  - 新增 `glnvg__canMergeTriangles()` 函数
  - 新增 `glnvg__trianglesBatched()` 函数
  - 修改 `nvgRenderFlush()` 支持 TRIANGLES 合批

---

## 方案 4/5/6: 内部多 Path 合批

### 问题背景

统计发现单个 call 内部可能包含大量 path:
```
NVG Stats: calls=23, paths=7914, maxPaths/call=2823
```

原始实现每个 path 单独渲染，导致上万个 DC。

### 优化原理

**Stencil/Fill Pass**: 将所有 path 的 fan 拓扑转换为 triangle list，合并到一个 index buffer。

**Fringe/Stroke Pass**: 使用 degenerate triangles 连接多个 tristrip:
```
Strip1: [A, B, C, D]
Strip2: [E, F, G, H]
合并:   [A, B, C, D, D, E, E, F, G, H]
                    ↑   ↑
              退化三角形 (面积为0，不渲染)
```

### 16-bit Index Buffer 限制处理

由于 BGFX 使用 16-bit index buffer，**只有使用索引的渲染 pass 才需要 65535 限制**。

**限制策略**:

| 渲染 Pass | 使用方式 | 是否需要限制 |
|-----------|---------|-------------|
| Stencil Pass (glnvg__fill) | **索引** | ✅ 需要 65535 限制 |
| Fill Pass (glnvg__convexFill) | **索引** | ✅ 需要 65535 限制 |
| Fringe Pass | 顶点 | ❌ 无限制 |
| Stroke Pass | 顶点 | ❌ 无限制 |

**分块处理** (仅对索引 pass):

1. **MAX_INDICES_PER_BATCH = 65535**: 索引数量上限
2. **MAX_TRIS_PER_BATCH = 21845**: 三角形数量上限 (65535 / 3)

当合批后索引数量超过限制时，自动分割成多个 batch 分别提交。
Fringe 和 Stroke 只使用顶点缓冲，无需分块。

**核心算法**: 使用相对索引 + 顶点偏移

```cpp
const int MAX_INDICES_PER_BATCH = 65535;
const int MAX_TRIS_PER_BATCH = MAX_INDICES_PER_BATCH / 3;

uint16_t* tempIndices = BX_ALLOC(...);
int idxOffset = 0;
int currentBatchTris = 0;
int batchVertexBase = 0;   // 当前 batch 的顶点起始位置
int batchVertexCount = 0;  // 当前 batch 需要的顶点数量

for (i = 0; i < npaths; i++)
{
    int fillOffset = paths[i].fillOffset;
    int fillCount = paths[i].fillCount;
    int pathTris = fillCount - 2;

    // 计算相对于 batch base 的偏移
    int relativeOffset = fillOffset - batchVertexBase;

    // 检查是否需要开始新 batch:
    // 1. 相对偏移为负 (path 在 base 之前)
    // 2. 相对索引超出 16-bit 范围
    // 3. 三角形数量超出限制
    bool needNewBatch = (relativeOffset < 0) ||
                        (relativeOffset + fillCount > 65535) ||
                        (currentBatchTris + pathTris > MAX_TRIS_PER_BATCH);

    if (needNewBatch && idxOffset > 0)
    {
        // Flush 当前 batch
        glnvg__submitStencilBatchWithOffset(gl, tempIndices, idxOffset,
                                            batchVertexBase, batchVertexCount);
        idxOffset = 0;
        currentBatchTris = 0;
        batchVertexBase = fillOffset;  // 新 batch 从当前 path 开始
        batchVertexCount = 0;
        relativeOffset = 0;
    }
    else if (idxOffset == 0)
    {
        // 第一个 path，设置 base
        batchVertexBase = fillOffset;
        batchVertexCount = 0;
        relativeOffset = 0;
    }

    // 更新顶点数量
    int requiredVertexCount = relativeOffset + fillCount;
    if (requiredVertexCount > batchVertexCount)
        batchVertexCount = requiredVertexCount;

    // 添加三角形到当前 batch (使用相对索引)
    for (int k = 0; k < pathTris; k++)
    {
        tempIndices[idxOffset++] = (uint16_t)relativeOffset;
        tempIndices[idxOffset++] = (uint16_t)(relativeOffset + k + 1);
        tempIndices[idxOffset++] = (uint16_t)(relativeOffset + k + 2);
    }
    currentBatchTris += pathTris;
}

// Flush 剩余 batch
if (idxOffset > 0)
{
    glnvg__submitStencilBatchWithOffset(gl, tempIndices, idxOffset,
                                        batchVertexBase, batchVertexCount);
}
```

### 新增辅助函数

| 函数 | 用途 |
|------|------|
| `glnvg__submitStencilBatchWithOffset()` | 提交 stencil fill batch (索引+顶点偏移) |
| `glnvg__submitConvexFillBatchWithOffset()` | 提交 convex fill batch (索引+顶点偏移) |

### 预期收益

| 场景 | 优化前 DC | 优化后 DC | 减少比例 |
|------|-----------|-----------|----------|
| FILL (2823 paths, AA) | 5647 | ~3 | 99.9% |
| CONVEXFILL (100 paths, AA) | 200 | ~2 | 99% |
| STROKE (100 paths) | 100 | ~1 | 99% |

注：当 path 数量超大时，DC 数量会随 batch 数量增加，但仍远低于逐 path 渲染。

---

*最后更新: 2026-04-02*
