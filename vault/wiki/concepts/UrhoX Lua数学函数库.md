---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["UrhoX", "Lua", "数学", "API", "向量", "游戏开发"]
aliases: [UrhoX数学API, Lua数学工具函数, vector math utilities]
relates_to: [UrhoX全局子系统, UrhoX Lua开发准则]
supersedes: null
---
# UrhoX Lua数学函数库

## 概述
[[UrhoX引擎|UrhoX]] 全局作用域提供完整的数学工具函数集，涵盖标量运算、向量逐分量操作、类型转换和随机数生成，全部在 Lua 全局作用域直接调用。

## 关键内容

### 标量数学函数

与标准数学库对应，但作用于 float 类型：

```lua
-- 基础运算
Abs(x), Ceil(x), Floor(x), Round(x), Sqrt(x)
Sin(angle), Cos(angle), Tan(angle)   -- angle 单位：度
Asin(x), Acos(x), Atan(x), Atan2(y, x)
Pow(x, y), Ln(x), Mod(x, y), Fract(x)

-- 数值限制与插值
Clamp(value, min, max)
Lerp(lhs, rhs, t)
InverseLerp(lhs, rhs, x)
SmoothStep(lhs, rhs, t)

-- 符号与比较
Sign(value)
Equals(a, b)   -- 浮点数近似相等
IsNaN(value)
Max(a, b), Min(a, b)
```

### 向量逐分量操作

UrhoX 为 Vector2/3/4 和 IntVector2/3 提供批量运算函数：

```lua
-- 逐分量算术（Vector2/3/4 通用）
VectorCeil(vec), VectorFloor(vec), VectorRound(vec)
VectorMax(a, b), VectorMin(a, b)
VectorLerp(lhs, rhs, t)

-- 整数向量转换
VectorCeilToInt(vec2),  VectorFloorToInt(vec2),  VectorRoundToInt(vec2)
VectorMax(iv2a, iv2b),  VectorMin(iv2a, iv2b)
```

### 随机数函数

```lua
Random()               -- [0, 1)
Random(range)          -- [0, range)
Random(min, max)       -- [min, max)
RandomInt(range)       -- 整数 [0, range)
RandomInt(min, max)    -- 整数 [min, max)
RandStandardNormal()   -- 标准正态分布
RandomNormal(mean, variance)

-- 可复现随机（种子固定输出固定）
StableRandom(seed_float)
StableRandom(seed_Vector2)
StableRandom(seed_Vector3)

SetRandomSeed(seed)
GetRandomSeed()
```

### 类型字符串转换

从字符串反序列化向量/颜色（常用于配置加载）：

```lua
ToVector2("1 2"), ToVector3("1 2 3"), ToVector4("1 2 3 4")
ToIntVector2("1 2"), ToIntVector3("1 2 3")
ToIntRect("0 0 100 100"), ToRect("0 0 1 1")
ToQuaternion("0 0 0 1"), ToMatrix3x4("..."), ToMatrix4("...")
ToColor("1 0 0 1")
```

### 整数工具函数

```lua
AbsInt(n), ClampInt(n, min, max)
CeilToInt(f), FloorToInt(f), RoundToInt(f)
MaxInt(a, b), MinInt(a, b)
ToInt(str), ToUInt(str), ToInt64(str)

-- 位操作
CountSetBits(n), IsPowerOfTwo(n)
NextPowerOfTwo(n), LogBaseTwo(n)
SDBMHash(hash, c)
```

### 重要数学常量

```lua
M_PI         -- π
M_HALF_PI    -- π/2
M_DEGTORAD   -- π/180（度转弧度）
M_RADTODEG   -- 180/π（弧度转度）
M_EPSILON    -- 浮点最小精度
M_INFINITY   -- 无穷大
M_MAX_INT, M_MIN_INT
M_MAX_UNSIGNED, M_MIN_UNSIGNED
```

> 注意：[[UrhoX引擎|UrhoX]] 三角函数的角度参数单位是**度**而非弧度，与标准数学库不同。

## 来源
- [[raw/articles/personal/ai-dev-kit/engine-docs/api/globals.md]] — UrhoX Lua API Global Scope 文档

## 相关
- [[UrhoX全局子系统]] — relates_to，数学函数与全局子系统同属全局作用域
- [[UrhoX Lua开发准则]] — relates_to，坐标系与单位规则（度/米）
