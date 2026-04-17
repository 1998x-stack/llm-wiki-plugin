# 渲染配置说明

> UrhoX 渲染系统的关键配置

---

## 灯光组 (LightGroup)

使用预设的灯光组替代手动创建 Zone 和 Light，推荐用于快速配置场景光照环境。

```lua
-- 加载灯光组
local lightGroupFile = cache:GetResource("XMLFile", "LightGroup/Daytime.xml")
local lightGroup = scene_:CreateChild("LightGroup")
lightGroup:LoadXML(lightGroupFile:GetRoot())
```

### 可用预设

| 文件 | 说明 |
|------|------|
| `LightGroup/Daytime.xml` | 白天 |
| `LightGroup/Dusk.xml` | 黄昏 |
| `LightGroup/Night.xml` | 夜晚 |

---

## 灯光亮度

| 灯光类型 | 亮度单位 |
|----------|----------|
| 方向光 (Directional) | 勒克斯 (lux) |
| 点光 (Point) | 坎德拉 (cd) |
| 锥光 (Spot) | 坎德拉 (cd) |


## 相关文档

- [材质列表](./materials.md)

---

[返回 Recipes](./README.md)

