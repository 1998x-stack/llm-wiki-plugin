# UrhoX Lua Development Documentation

AI coding assistant reference for UrhoX Lua game development.

---

## Core Documentation

### [principles.md](principles.md) ⭐
Development principles, design philosophy, and best practices for AI-assisted development.

### [gotchas/](gotchas/index.md) ⚠️
常见陷阱与注意事项 - **只记录实际遇到并验证过的问题**（当前 8 个）。
- [物理系统](gotchas/physics.md)：Rolling Friction 不兼容、Collision Margin 过大
- [相机系统](gotchas/camera.md)：orthoSize 的 0.5 因子、GetScreenRay 无缓存、正交投影公式

### [API Reference](api/index.md)
Complete Lua 5.4 API reference (20 files, ~276KB total, avg 13.8KB/file).

**Quick links**:
- [Core](api/core.md) - Scene, Node, Component
- [Graphics](api/graphics.md) - StaticModel, Camera, Light, Material
- [Physics](api/physics.md) - RigidBody, CollisionShape
- [Physics 2D](api/physics-2d.md) - RigidBody2D, CollisionShape2D
- [UI](api/ui.md) - UIElement, Button, Text
- [Audio](api/audio.md) - Sound, SoundSource
- [Input](api/input.md) - Keyboard, Mouse, Touch
- [Math](api/math.md) - Vector3, Quaternion, Color
- [Enums](api/enums.md) - All enumerations
- [Globals](api/globals.md) - Global functions and properties

---

## Recipes (Solutions)

### Ready
- [recipes/ui.md](recipes/ui.md) - **UI 开发指南（Yoga + NanoVG，40+ 控件）** ⭐
- [recipes/materials.md](recipes/materials.md) - 材质列表和参数
- [recipes/rendering.md](recipes/rendering.md) - 渲染配置（灯光组）
- [recipes/nanovg_bloom_glow_guide.md](recipes/nanovg_bloom_glow_guide.md) - NanoVG Bloom 发光特效

### Planned
- `recipes/create-menu.md` - Complete menu system with code
- `recipes/save-game.md` - Save/load game data
- `recipes/spawn-enemies.md` - Enemy spawn system
- `recipes/camera-follow.md` - Camera following
- `recipes/character-movement.md` - Character controller
- `recipes/collision-detection.md` - Collision handling
- `recipes/optimize-performance.md` - Performance optimization
- `recipes/debug-lua.md` - Debugging techniques

---

## Tutorials (Planned)

1. `tutorials/01-first-game.md` - 30min first game
2. `tutorials/02-scene-nodes.md` - Scene tree, node hierarchy
3. `tutorials/03-components.md` - Component system
4. `tutorials/04-input.md` - Keyboard, mouse, touch input
5. `tutorials/05-ui.md` - UI system basics
6. `tutorials/06-physics.md` - Physics system
7. `tutorials/07-animations.md` - Animation system
8. `tutorials/08-particles.md` - Particle effects
9. `tutorials/09-audio.md` - Audio system
10. `tutorials/10-multiplayer.md` - Multiplayer basics

---

## Keyword Index

| Need | File |
|------|------|
| **Development principles** | **principles.md** |
| **常见陷阱/坑** | **gotchas/index.md** |
| API reference | api/index.md |
| Create scene | api/core.md#scene |
| Add model | api/graphics.md#staticmodel |
| Camera | api/graphics.md#camera |
| Lighting | api/graphics.md#light |
| Physics (3D) | api/physics.md#rigidbody |
| Physics (2D) | api/Physics2D.md#rigidbody2d |
| Collision | api/physics.md#collisionshape |
| **UI system (Yoga + NanoVG)** | **recipes/ui.md** |
| Audio | api/audio.md#sound |
| Input | api/input.md |
| Math types | api/math.md |
| Enumerations | api/enums.md |
| Global functions | api/globals.md |
| Menu system | recipes/create-menu.md |
| **材质列表** | **recipes/materials.md** |
| **渲染/灯光组** | **recipes/rendering.md** |
| **瓦片地形生成/加载** | **recipes/tile-terrain-guide.md** |

---

**Version**: v0.1.0-alpha  
**Status**: Core framework ready, content in development
