---
summary: "WebGL-compatible SSAO implementation using fragment shaders (rasterization) based on Intel ASSAO"
status: in_progress
last_updated: "2024-11-26"
read_when:
  - "implementing SSAO for WebGL"
  - "modifying screen-space rendering passes"
  - "working on rasterization-based post-processing"
---

# SSAORasterize Implementation Guide

## Overview

SSAORasterize is a WebGL-compatible implementation of Screen Space Ambient Occlusion (SSAO) based on Intel's ASSAO algorithm. Unlike the original compute shader version (`SSAO.cpp`), this implementation uses fragment shaders (rasterization) to support platforms without compute shader capabilities, such as WebGL.

## Architecture

### Render Passes

1. **Prepare Depths** (`fs_prepare_depths.glsl`) - Downscale depth buffer to half resolution
2. **Prepare Normals** (`fs_prepare_normals.glsl`) - Reconstruct view-space normals from depth (optional)
3. **Generate AO** (`fs_generate_ao.glsl`) - Main SSAO calculation with quality levels
4. **Blur** (`fs_blur.glsl`) - Edge-aware blur passes (0-4 passes)
5. **Apply** (`fs_apply.glsl`) - Upsample to full resolution

### Key Files

```
engine/Source/Urho3D/Graphics/
├── SSAORasterize.cpp      # C++ implementation
├── SSAORasterize.h        # Header with settings and uniforms

Res/Shaders/BLGL/SSAORasterize/
├── vs_fullscreen.glsl     # Fullscreen quad vertex shader
├── fs_prepare_depths.glsl # Depth preparation
├── fs_prepare_normals.glsl# Normal reconstruction
├── fs_generate_ao.glsl    # AO generation
├── fs_blur.glsl           # Edge-aware blur
├── fs_apply.glsl          # Final apply/upsample
├── uniforms.sh            # Shared uniform definitions
└── varying.def.sc         # Varying definitions
```

## Critical: Platform-Specific UV and View Space Handling

### The Problem

OpenGL and D3D have different conventions for:
1. **Texture UV origin**: OpenGL has Y=0 at bottom, D3D has Y=0 at top
2. **NDC (Normalized Device Coordinates)**: Both have Y=-1 at bottom, Y=+1 at top
3. **Clip space to UV mapping**: Requires different formulas per platform

### The Solution

The implementation must use **platform-specific handling** in multiple places to ensure correct behavior. This matches the original `SSAO.cpp` compute shader implementation.

#### 1. Vertex Shader UV Calculation (`vs_fullscreen.glsl`)

```glsl
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
    // OpenGL: UV.y=0 at bottom, use clipPos.y directly
    v_texcoord0 = vec2(
        gl_Position.x / gl_Position.w * 0.5 + 0.5,
        gl_Position.y / gl_Position.w * 0.5 + 0.5);
#else
    // D3D: UV.y=0 at top, negate clipPos.y
    v_texcoord0 = vec2(
        gl_Position.x / gl_Position.w * 0.5 + 0.5,
        -gl_Position.y / gl_Position.w * 0.5 + 0.5);
#endif
```

#### 2. C++ NDC to View Space Conversion (`SSAORasterize.cpp`)

```cpp
if (bgfx::getRendererType() == bgfx::RendererType::OpenGL)
{
    // OpenGL: positive Y multiplier (UV.y=0 at bottom maps to negative view Y)
    Vec2Set(uniforms_.ndcToViewMul, tanHalfFOVX * 2.0f, tanHalfFOVY * 2.0f);
    Vec2Set(uniforms_.ndcToViewAdd, tanHalfFOVX * -1.0f, tanHalfFOVY * -1.0f);
}
else
{
    // D3D: negative Y multiplier (UV.y=0 at top maps to positive view Y)
    Vec2Set(uniforms_.ndcToViewMul, tanHalfFOVX * 2.0f, tanHalfFOVY * -2.0f);
    Vec2Set(uniforms_.ndcToViewAdd, tanHalfFOVX * -1.0f, tanHalfFOVY * 1.0f);
}
```

#### 3. Fragment Shader Pixel Size Flip

In both `fs_prepare_normals.glsl` and `fs_generate_ao.glsl`:

```glsl
vec2 pixelSize = u_viewportPixelSize; // or u_halfViewportPixelSize
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
    pixelSize.y = -pixelSize.y;
#endif
```

#### 4. Sample Offset Flip (`fs_generate_ao.glsl`)

```glsl
sampleOffset = round(sampleOffset);

#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
    sampleOffset.y = -sampleOffset.y;
#endif
```

#### 5. Detail AO Delta Signs (`fs_generate_ao.glsl`)

```glsl
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
    vec3 pixTDelta = vec3(0.0,  pixelDirRBViewspaceSizeAtCenterZ.y, 0.0) + ...;
    vec3 pixBDelta = vec3(0.0, -pixelDirRBViewspaceSizeAtCenterZ.y, 0.0) + ...;
#else
    vec3 pixTDelta = vec3(0.0, -pixelDirRBViewspaceSizeAtCenterZ.y, 0.0) + ...;
    vec3 pixBDelta = vec3(0.0,  pixelDirRBViewspaceSizeAtCenterZ.y, 0.0) + ...;
#endif
```

## Common Mistakes to Avoid

### 1. DO NOT Unify UV Convention

**Wrong approach**: Trying to use a unified D3D-style UV convention for all platforms.

This fails because:
- The `ndcToViewMul/Add` values depend on the UV convention
- If UV convention doesn't match the multiplier/add values, view-space positions are wrong
- Results in inverted normals (Y=0 instead of Y=1 for horizontal surfaces)

### 2. Always Check Both GLSL Macros

When checking for OpenGL/GLSL platform, always use:
```glsl
#if BGFX_SHADER_LANGUAGE_GLSL || BGFX_SHADER_LANGUAGE_GLSL_HLSLCC
```

Not just:
```glsl
#if BGFX_SHADER_LANGUAGE_GLSL  // WRONG - misses HLSLCC
```

`BGFX_SHADER_LANGUAGE_GLSL_HLSLCC` is used when HLSL shaders are cross-compiled to GLSL.

### 3. Reference Original SSAO.cpp

The original compute shader implementation (`SSAO.cpp`) contains the correct platform-specific handling. When in doubt, check how the original handles:
- `ndcToViewMul` / `ndcToViewAdd` (lines 563-572)
- `perPassFullResCoordOffset` / `perPassFullResUVOffset` (lines 611-620)

## Debugging Tips

### Normal Map Verification

For a horizontal floor viewed from above:
- **Correct**: Normal Y component should be close to 1.0 (pointing up)
- **Wrong**: Normal Y component is 0 or negative (pointing sideways or down)

If normals appear inverted, check:
1. UV calculation in vertex shader matches platform
2. `ndcToViewMul.y` sign matches platform convention
3. `pixelSize.y` flip is applied for OpenGL

### Visual Comparison

Compare the generated normal map with the original `SSAO.cpp` output:
- Details (edges, corners) should match
- Overall direction (color tint) should match
- If details match but direction is wrong, it's a sign flip issue

## Quality Levels

| Level | Define | Samples | Use Case |
|-------|--------|---------|----------|
| 0 | `QUALITY_LOW` | 3 | Mobile/WebGL |
| 1 | `QUALITY_MEDIUM` | 5 | Default |
| 2 | `QUALITY_HIGH` | 12 | Desktop |

Note: Quality level 3 (Adaptive) from original SSAO is not supported in rasterize version.

## Performance Notes

- Rasterize version is slower than compute shader version on desktop
- Rasterize version produces slightly stronger AO (compensated with 0.5x multiplier)
- Half-resolution AO with bilinear upsample provides good quality/performance balance

## References

- Intel ASSAO: https://github.com/GameTechDev/ASSAO
- Original implementation: `engine/Source/Urho3D/Graphics/SSAO.cpp`
- bgfx examples: https://github.com/bkarber/bgfx/tree/master/examples/39-assao

---

*Last updated: 2024-11-26*
