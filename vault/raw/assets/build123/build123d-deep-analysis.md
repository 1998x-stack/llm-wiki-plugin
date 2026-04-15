# build123d — 深度技术分析参考手册

> **Repository**: https://github.com/gumyr/build123d  
> **Version**: v0.10.0 (2025-11-05)  
> **License**: Apache 2.0  
> **Backend**: OpenCascade (OCC) / cadquery-ocp  
> **Python**: 3.10 ~ 3.13

---

## 目录

1. [架构概览](#1-架构概览)
2. [两种建模模式](#2-两种建模模式)
3. [拓扑类体系](#3-拓扑类体系)
4. [几何类体系](#4-几何类体系)
5. [1D 对象 — 曲线/线条](#5-1d-对象--曲线线条)
6. [2D 对象 — 草图/面](#6-2d-对象--草图面)
7. [3D 对象 — 实体](#7-3d-对象--实体)
8. [操作函数大全](#8-操作函数大全)
9. [拓扑选择器](#9-拓扑选择器)
10. [位置与变换系统](#10-位置与变换系统)
11. [Builder 上下文](#11-builder-上下文)
12. [孔特征工具](#12-孔特征工具)
13. [枚举类型参考](#13-枚举类型参考)
14. [导入/导出](#14-导入导出)
15. [装配体系统](#15-装配体系统)
16. [关节系统 Joints](#16-关节系统-joints)
17. [自定义对象扩展](#17-自定义对象扩展)
18. [运算符速查](#18-运算符速查)
19. [最佳实践 & Tips](#19-最佳实践--tips)
20. [常见陷阱 & FAQ](#20-常见陷阱--faq)

---

## 1. 架构概览

```
build123d
├── topology/              # 拓扑核心
│   ├── shape_core.py      # Shape 基类
│   ├── one_d.py           # Edge, Wire
│   ├── two_d.py           # Face, Shell
│   ├── three_d.py         # Solid
│   └── composite.py       # Compound, Part, Sketch, Curve
├── geometry.py            # Vector, Axis, Plane, Location
├── build_common.py        # Builder 基类, context stack
├── build_line.py          # BuildLine context
├── build_sketch.py        # BuildSketch context
├── build_part.py          # BuildPart context
├── objects_curve.py       # 1D 对象 (Line, Arc, ...)
├── objects_sketch.py      # 2D 对象 (Circle, Rectangle, ...)
├── objects_part.py        # 3D 对象 (Box, Cylinder, ...)
├── operations_generic.py  # 通用操作 (extrude, fillet, ...)
├── operations_sketch.py   # 草图操作 (make_face, trace, ...)
├── operations_part.py     # 零件操作 (draft, ...)
└── build_enums.py         # 枚举 (Mode, Align, GeomType, ...)
```

### 设计哲学

- **BREP**（边界表示法）建模，而非网格
- 底层使用 **OpenCascade** 几何核心
- 两种使用模式：**Builder Mode**（有状态上下文）和 **Algebra Mode**（无状态代数）
- 完全 Pythonic：选择器是列表，位置是可迭代对象
- 运算符驱动：`+`, `-`, `&`, `@`, `%`, `*`

---

## 2. 两种建模模式

### 2.1 Algebra Mode（代数模式）— 推荐用于复杂逻辑

无状态，每个对象显式管理，通过代数运算符组合。

```python
from build123d import *

# 创建草图并布尔运算
sketch = Rectangle(100, 60)
sketch -= Pos(0, 0) * Circle(20)          # 中心挖孔
sketch -= GridLocations(60, 30, 2, 2) * Circle(5)  # 四角孔

# 拉伸到3D
part = extrude(sketch, amount=10)

# 修改
part += Pos(0, 0, 10) * Cylinder(5, 20)   # 加圆柱
part = fillet(part.edges().filter_by(Axis.Z), radius=2)
```

### 2.2 Builder Mode（构建器模式）— 推荐用于结构化设计

有状态上下文管理，类似设计历史，嵌套 with 语句。

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch() as sk:
        Rectangle(100, 60)
        with Locations((0, 0)):
            Circle(20, mode=Mode.SUBTRACT)
        with GridLocations(60, 30, 2, 2):
            Circle(5, mode=Mode.SUBTRACT)
    extrude(amount=10)
    with Locations((0, 0, 10)):
        Cylinder(5, 20)
    fillet(edges().filter_by(Axis.Z), radius=2)

result = part.part   # 访问最终 Part
```

### 模式对比

| 特性 | Algebra Mode | Builder Mode |
|------|-------------|--------------|
| 状态管理 | 无状态，显式 | 有状态，隐式 |
| 可读性 | 代数表达式风格 | 嵌套上下文风格 |
| 调试 | 每步结果可直接打印 | 需访问 `.part` / `.sketch` |
| 混合使用 | ✅ 支持 | ✅ 支持 |
| 适合场景 | 参数化、函数式 | 结构化、设计历史 |

---

## 3. 拓扑类体系

### 继承关系

```
Shape (基类)
├── Vertex          # 0D — 点
├── Mixin1D
│   ├── Edge        # 1D — 边
│   └── Wire        # 1D — 线（多边连接）
├── Face            # 2D — 面
├── Shell           # 2D — 壳（多面连接）
├── Mixin3D
│   ├── Solid       # 3D — 实体
│   └── Compound    # 复合体（任意维度集合）
│       ├── Part    # Compound of Solids
│       ├── Sketch  # Compound of Faces
│       └── Curve   # Compound of Edges/Wires
```

### Shape 基类重要属性与方法

```python
# 属性
shape.volume           # 体积 (float)
shape.area             # 面积 (float)
shape.length           # 长度 (Edge/Wire)
shape.center()         # 重心 Vector
shape.bounding_box()   # BoundingBox 对象
shape.label            # 名称标签 (str)
shape.color            # 颜色 (Color)

# 拓扑访问（返回 ShapeList）
shape.vertices()
shape.edges()
shape.wires()
shape.faces()
shape.shells()
shape.solids()
shape.compounds()

# 几何属性
shape.is_valid         # bool
shape.geom_type        # GeomType 枚举
shape.location         # 当前 Location
shape.move(loc)        # 移动，返回新 Shape
shape.moved(loc)       # 不改变原对象
shape.locate(loc)      # 原地修改 Location
shape.clean()          # 去除冗余内部结构

# 变换
shape.mirror(plane)    # 镜像
shape.rotate(axis, angle)
shape.scale(factor)
shape.offset_3d(amount)

# 布尔运算（返回新对象）
shape.fuse(other)
shape.cut(other)
shape.intersect(other)
```

### ShapeList 方法

```python
shapes = part.edges()   # 返回 ShapeList

# 过滤
shapes.filter_by(Axis.Z)                        # 按轴向过滤
shapes.filter_by(GeomType.CIRCLE)               # 按几何类型过滤
shapes.filter_by(lambda e: e.length > 5)        # 自定义过滤

# 排序
shapes.sort_by(Axis.Z)                          # 按 Z 轴位置排序
shapes.sort_by(SortBy.LENGTH)                   # 按长度排序
shapes.sort_by(SortBy.RADIUS)                   # 按半径排序
shapes.sort_by(SortBy.AREA)                     # 按面积排序
shapes.sort_by(SortBy.DISTANCE)                 # 按距原点距离排序

# 分组
shapes.group_by(Axis.Z)                         # 按 Z 轴位置分组 → list of ShapeList
shapes.group_by(SortBy.RADIUS)                  # 按半径分组
shapes[-1]                                       # 最后一组（最大/最高）

# 集合运算
diff = shapes1 - shapes2                         # 差集
union = shapes1 | shapes2                        # 并集

# 特殊访问
shapes.first                                     # 第一个
shapes.last                                      # 最后一个
```

---

## 4. 几何类体系

### Vector

```python
v = Vector(1, 2, 3)
v = Vector((1, 2, 3))   # tuple 输入
v.X, v.Y, v.Z           # 分量访问

# 运算符
v1 + v2                  # 加法
v1 - v2                  # 减法
v1 * scalar              # 标量乘
v1 / scalar              # 标量除
abs(v)                   # 模长
-v                       # 取反
tuple(v)                 # 转 tuple

# 方法
v.normalized()           # 归一化
v.dot(v2)               # 点积
v.cross(v2)             # 叉积
v.distance_to(v2)       # 距离
v.angle_between(v2)     # 夹角（度）
v.rotate(axis, angle)   # 旋转
```

### Axis

```python
# 预定义轴
Axis.X     # (0,0,0) → (1,0,0)
Axis.Y     # (0,0,0) → (0,1,0)
Axis.Z     # (0,0,0) → (0,0,1)

# 自定义轴
ax = Axis((0,0,0), (1,1,0))    # 位置 + 方向

# 属性
ax.position   # Vector
ax.direction  # Vector
ax.reverse()  # 反向
```

### Plane

```python
# 预定义平面
Plane.XY    # Z=0 平面（默认工作平面）
Plane.XZ    # Y=0 平面
Plane.YZ    # X=0 平面
Plane.front, Plane.back, Plane.left, Plane.right, Plane.top, Plane.bottom

# 从 Face 创建
plane = Plane(face)

# 从位置+法向量创建
plane = Plane(origin=(0,0,5), z_dir=(0,0,1))

# 运算符 — 坐标系变换
plane * shape             # 将 shape 放置在 plane 坐标系
plane * Location(...)     # 组合变换
Plane.XZ * Pos(X=5)      # 偏移的平面

# 属性
plane.origin              # Vector
plane.x_dir, plane.y_dir, plane.z_dir
plane.to_location()       # 转 Location
```

### Location

```python
# 创建
loc = Location((10, 0, 5))                  # 纯平移
loc = Location((10, 0, 5), (45, 0, 0))      # 平移 + 欧拉角旋转

# 语法糖
pos = Pos(10, 0, 5)            # 位置
pos = Pos(X=10)                # 只指定 X
rot = Rot(0, 45, 0)            # 旋转（度）
rot = Rot(Z=90)                # 只绕 Z 旋转

# 组合
combined = Pos(10, 0) * Rot(Z=45)
applied = combined * Circle(5)    # 应用到 shape

# 位置查询运算符 (@, %)
point = edge @ 0.5          # 边上 t=0.5 处的 Vector
tangent = edge % 0.5        # 边上 t=0.5 处的切向 Vector
```

### BoundingBox

```python
bbox = shape.bounding_box()
bbox.min          # Vector (xmin, ymin, zmin)
bbox.max          # Vector (xmax, ymax, zmax)
bbox.size         # Vector (width, height, depth)
bbox.center       # Vector 中心点
bbox.diagonal     # 对角线长
bbox.add(other)   # 合并包围盒
```

---

## 5. 1D 对象 — 曲线/线条

在 `BuildLine` 上下文或 Algebra Mode 中使用。

### 基础线条对象

```python
# 直线
Line((0,0), (10,0))                        # 两点直线
PolarLine((0,0), 10, angle=45)            # 极坐标线
PolarLine(start, length, direction=vec)    # 方向向量线

# 折线
Polyline((0,0), (5,5), (10,0))            # 多点折线
FilletPolyline((0,0), (5,5), (10,0), radius=1)  # 带圆角折线

# 样条
Spline((0,0), (5,8), (10,0))                     # 通过点的样条
Spline(..., tangents=((1,0), (1,0)))              # 带切向量
Spline(..., tangent_scalars=(1.5, 1.0))           # 切向量缩放

# 贝塞尔曲线
Bezier((0,0), (2,5), (8,5), (10,0))       # 贝塞尔控制点
```

### 弧线对象

```python
# 圆弧（圆心方式）
CenterArc(center=(0,0), radius=5, start_angle=0, arc_size=90)

# 三点弧
RadiusArc(start, end, radius=5)           # 起终点+半径
SagittaArc(start, end, sagitta=2)         # 起终点+弦高
TangentArc(start, end, tangent=vec)       # 起终点+切向

# 椭圆弧
EllipticalCenterArc(center, x_radius, y_radius, start_angle, arc_size)

# 抛物线弧
ParabolicCenterArc(...)

# 双曲线弧
HyperbolicCenterArc(...)

# JernArc — 续接弧（从已有边的端点续接）
JernArc(start=line@1, tangent=line%1, radius=3, arc_size=180)
```

### 高级曲线

```python
# 螺旋线
Helix(pitch=5, height=20, radius=10)
Helix(pitch=5, height=20, radius=10, lefthand=True)   # 左旋

# 约束弧/线
ConstrainedArcs(...)
ConstrainedLines(...)

# 混合曲线（C2连续）
BlendCurve(edge1, edge2, continuity=2)

# 翼型轮廓
Airfoil(naca="2412", chord=100)

# 相交线
IntersectingLine(pt, direction, face)
```

### 线条操作

```python
# @ 和 % 运算符（重要！）
line = Line((0,0), (10,0))
arc  = JernArc(line @ 1, line % 1, radius=3, arc_size=90)
# @ t : 获取参数 t ∈ [0,1] 处的 Vector 点
# % t : 获取参数 t ∈ [0,1] 处的切向 Vector

# 链式续接
line = Line((0,-3), (6,-3))
line += JernArc(line@1, line%1, radius=3, arc_size=180)
line += PolarLine(line@1, 6, direction=line%1)
```

---

## 6. 2D 对象 — 草图/面

### 基础形状

```python
# 圆形
Circle(radius=10)
Ellipse(x_radius=10, y_radius=5)

# 矩形
Rectangle(width=20, height=10)
RectangleRounded(width=20, height=10, radius=2)
Square(size=10)

# 多边形
RegularPolygon(radius=10, side_count=6)       # 正六边形
Polygon(*pts)                                  # 任意多边形（点列表）

# 梯形
Trapezoid(width=20, height=10, left_side_angle=70)

# 文字
Text("build123d", font_size=10, font="Arial")

# 槽形
SlottedRectangle(width=20, height=10, slot_width=5)
```

### 从线条/路径创建面

```python
# 从闭合线段创建面（Builder Mode）
with BuildSketch():
    with BuildLine():
        Line((0,0), (10,0))
        Line((10,0), (10,10))
        Line((10,10), (0,0))
    make_face()

# Algebra Mode
wire = Wire.make_polygon([(0,0), (10,0), (10,10)])
face = Face(wire)

# 从非平面轮廓创建曲面
face = Face.make_surface_patch(wire)          # 边界约束曲面
face = Face.make_gordon_surface(...)          # Gordon 曲面
```

### 草图定位模式

```python
# align 参数控制草图原点对齐
Rectangle(10, 5, align=(Align.CENTER, Align.CENTER))  # 中心对齐（默认）
Rectangle(10, 5, align=(Align.MIN, Align.MIN))        # 左下角对齐
Rectangle(10, 5, align=(Align.MAX, Align.MAX))        # 右上角对齐
Box(10, 10, 10, align=(Align.MIN, Align.MIN, Align.MIN))  # 3D 对齐
```

---

## 7. 3D 对象 — 实体

### 基础几何体

```python
# 长方体
Box(length=10, width=8, height=5)
Box(10, 8, 5, align=(Align.MIN, Align.MIN, Align.MIN))   # 对齐到角

# 圆柱体
Cylinder(radius=5, height=10)
Cylinder(radius=5, height=10, arc_size=180)              # 半圆柱

# 圆锥体
Cone(bottom_radius=8, top_radius=3, height=10)
Cone(8, 0, 10)                                            # 完整锥

# 球体
Sphere(radius=10)
Sphere(radius=10, arc_size1=-45, arc_size2=90)            # 球扇形

# 圆环体
Torus(major_radius=20, minor_radius=5)

# 楔形体
Wedge(xsize=10, ysize=8, zsize=6, xminsize=2, zminsize=2)
```

### 高级几何体

```python
# 拉伸体
extrude(face_or_sketch, amount=10)
extrude(face_or_sketch, amount=10, taper=5)    # 锥形拉伸（度）
extrude(face_or_sketch, amount=10, both=True)  # 双向拉伸

# 旋转体
revolve(face_or_sketch, axis=Axis.Z, angle=360)
revolve(face_or_sketch, axis=Axis.Z, angle=180)   # 半旋转

# 放样体（过多个截面）
loft([sketch1, sketch2, sketch3])
loft([v1, sketch1, sketch2, v2])              # 顶点作为起止截面
loft([s1, s2], ruled=True)                   # 直纹面

# 扫掠体（截面沿路径）
sweep(profile, path)
sweep(profile, path, binormal=guide_wire)     # 双法矢控制
sweep(profile, path, transition=Transition.RIGHT)

# 加厚面
thicken(face, amount=2)                       # 薄壳加厚
thicken(face, amount=2, both=True)            # 双侧加厚
```

---

## 8. 操作函数大全

### 通用操作（1D/2D/3D）

```python
# 添加对象（Builder Mode）
add(shape, mode=Mode.ADD)

# 倒角
chamfer(edges_or_vertices, length=1)
chamfer(edges, length=1, length2=2)           # 非对称倒角
chamfer(edges, length=1, reference=face)      # 参考面指定长度方向

# 圆角
fillet(edges_or_vertices, radius=1)

# 镜像
mirror(shape, about=Plane.XY)
mirror(shape, about=Plane.YZ)

# 偏移
offset(shape, amount=2)                       # 向外偏移
offset(sketch, amount=-1, side=Side.LEFT)     # 方向控制

# 缩放
scale(shape, by=2.0)

# 投影
project(shape, onto_plane)

# 分割
split(shape, bisect_plane=Plane.XY)
split(shape, bisect_plane=Plane.XY, keep=Keep.TOP)  # 保留哪半
```

### 3D 专用操作

```python
# 偏移实体（抽壳）
offset(solid, amount=-2, openings=[top_face])   # 留开口抽壳

# 拔模角
draft(faces, plane, angle=5)

# 壳操作
shell(solid, amount=2)                        # 抽壳（同 offset）
```

### 草图专用操作

```python
# 从轮廓线创建面
make_face()                    # 封闭轮廓 → 面（Builder Mode）
make_hull(edges_or_wires)      # 凸包 → 面

# 追踪填充
trace(edges, stroke_width=1)   # 将线条转为带宽度的面

# 完整圆角
full_round(edge)               # Voronoi 圆角
```

### 孔操作（详见第12节）

```python
Hole(radius=3, depth=10)
CounterBoreHole(radius=3, counter_bore_radius=5, counter_bore_depth=3, depth=10)
CounterSinkHole(radius=3, counter_sink_radius=5, depth=10)
```

---

## 9. 拓扑选择器

build123d 最强大的功能之一：链式选择器语法。

### 访问器

```python
part.vertices()   # 所有顶点
part.edges()      # 所有边
part.wires()      # 所有线
part.faces()      # 所有面
part.solids()     # 所有实体（对 Compound）

# Builder Mode 中无需指定对象
edges()           # 当前上下文所有边
faces()           # 当前上下文所有面
```

### filter_by — 过滤

```python
# 按轴向（选择平行于该轴的边/面法向平行于该轴的面）
edges.filter_by(Axis.X)
edges.filter_by(Axis.Z)

# 按几何类型
edges.filter_by(GeomType.LINE)
edges.filter_by(GeomType.CIRCLE)
edges.filter_by(GeomType.ELLIPSE)
edges.filter_by(GeomType.BSPLINE)
faces.filter_by(GeomType.PLANE)
faces.filter_by(GeomType.CYLINDER)
faces.filter_by(GeomType.CONE)
faces.filter_by(GeomType.SPHERE)
faces.filter_by(GeomType.TORUS)

# 按自定义 lambda
edges.filter_by(lambda e: e.length > 5)
edges.filter_by(lambda e: e.length == 2)
faces.filter_by(lambda f: f.area > 100)
faces.filter_by(lambda f: f.radius == 5)    # 圆柱面半径

# Select.LAST — 选择最后一次操作创建的对象
part.edges(Select.LAST)
part.faces(Select.LAST)
```

### sort_by — 排序

```python
edges.sort_by(Axis.Z)          # 按 Z 坐标排序（升序）
edges.sort_by(Axis.X)
edges.sort_by(SortBy.LENGTH)   # 按长度
edges.sort_by(SortBy.RADIUS)   # 按半径
edges.sort_by(SortBy.AREA)     # 按面积（用于 faces）
edges.sort_by(SortBy.DISTANCE) # 按到原点距离
edges.sort_by(SortBy.VOLUME)   # 按体积（用于 solids）

# 结合列表索引
edges.sort_by(Axis.Z)[-1]      # Z 最高的边
edges.sort_by(Axis.Z)[0]       # Z 最低的边
edges.sort_by(Axis.Z)[-2:]     # 最高两条
```

### group_by — 分组

```python
# 返回 list of ShapeList，按属性值分组
groups = edges.group_by(Axis.Z)
groups[0]    # 最低 Z 的一组
groups[-1]   # 最高 Z 的一组

groups = faces.group_by(SortBy.AREA)
groups[-1]   # 面积最大的一组（通常是顶/底面）
groups[-1].sort_by(Axis.X)[-1]   # 最大面积组中 X 最右的面
```

### 链式组合示例

```python
# 选择 Z 方向的边且长度等于 2
part.edges().filter_by(Axis.Z).filter_by(lambda e: e.length == 2)

# 选择最顶层面的圆孔边
top_face = part.faces().sort_by(Axis.Z)[-1]
hole_edges = top_face.edges().filter_by(GeomType.CIRCLE)

# 选择 XY 平面上的圆柱面
cyl_faces = part.faces().filter_by(GeomType.CYLINDER).filter_by(lambda f: f.radius == 5)

# 选择最大面积组中 X 最大的面
target_face = part.faces().group_by(SortBy.AREA)[-1].sort_by(Axis.X)[-1]

# 差集选出新增边
before = part.edges()
part = fillet(...)
new_edges = part.edges() - before

# Select.LAST 用法
Hole(radius=3)
new_edges = edges(Select.LAST)
fillet(new_edges.sort_by(Axis.Z)[-1], radius=0.5)
```

---

## 10. 位置与变换系统

### 位置对象创建

```python
# Pos — 纯位移
Pos(10, 0, 5)
Pos(X=10)
Pos(Y=5, Z=2)

# Rot — 纯旋转（欧拉角，度）
Rot(0, 45, 0)         # 绕 Y 轴旋转 45°
Rot(Z=90)             # 绕 Z 轴 90°
Rot(X=30, Y=15)       # XY 复合旋转

# 组合
Pos(10,0) * Rot(Z=45)
```

### 位置上下文（Locations）

```python
# 单个位置
with Locations((10, 0, 0)):
    Circle(5)              # 在 (10,0,0) 放置圆

# 多个位置
with Locations([(10,0), (20,0), (30,0)]):
    Circle(5)              # 在三个位置各放一个圆

# 面上的位置
with Locations(top_face):
    Circle(5)              # 在面的中心放置

# 网格位置
GridLocations(x_spacing=10, y_spacing=8, x_count=3, y_count=2)

# 极坐标网格
PolarLocations(radius=20, count=6)           # 均匀分布
PolarLocations(radius=20, count=6, start_angle=30, angular_range=270)

# 六边形网格
HexLocations(apothem=6, x_count=5, y_count=5)

# 沿曲线的位置
CurveLocations(curve, count=10)
```

### Plane 作为坐标系

```python
# 在特定平面上作图
with BuildSketch(Plane.XZ):              # 在 XZ 平面上绘制
    Rectangle(10, 5)

with BuildSketch(Plane.YZ):
    Circle(8)

# 平面偏移
with BuildSketch(Plane.XY.offset(5)):    # Z=5 的 XY 平面
    Rectangle(10, 5)

# 从面创建平面
face = part.faces().sort_by(Axis.Z)[-1]
with BuildSketch(Plane(face)):
    Circle(3)

# 代数模式中的平面使用
sketch = Plane.XZ * Rectangle(10, 5)    # 放置在 XZ 平面上
```

---

## 11. Builder 上下文

### BuildLine

```python
with BuildLine() as bl:
    l1 = Line((0,0), (10,0))
    l2 = JernArc(l1@1, l1%1, radius=3, arc_size=90)

bl.wires    # 访问所有 Wire
bl.edges    # 访问所有 Edge
bl.line     # 主要 Wire
```

### BuildSketch

```python
with BuildSketch() as bs:
    Rectangle(10, 5)
    with Locations((5, 0)):
        Circle(2, mode=Mode.SUBTRACT)

bs.sketch   # 访问 Sketch（Compound of Faces）
bs.faces    # 访问所有 Face
```

### BuildPart

```python
with BuildPart() as bp:
    Box(10, 10, 5)
    Cylinder(3, 8)  # 自动 Mode.ADD

bp.part        # 访问最终 Part
bp.solids      # 所有 Solid
bp.faces       # 当前所有 Face（用于选择器）
bp.edges       # 当前所有 Edge
```

### Mode 枚举

```python
Mode.ADD        # 并（默认）
Mode.SUBTRACT   # 差
Mode.INTERSECT  # 交
Mode.REPLACE    # 替换当前上下文所有形状
Mode.PRIVATE    # 不参与上下文（用于辅助计算）
```

---

## 12. 孔特征工具

```python
# 基础通孔/盲孔
Hole(radius=3)                        # 通孔（穿透整个实体）
Hole(radius=3, depth=10)              # 盲孔（深度 10）

# 沉头孔
CounterBoreHole(
    radius=3,                         # 螺纹孔半径
    counter_bore_radius=5,            # 沉头半径
    counter_bore_depth=3,             # 沉头深度
    depth=10                          # 总深度
)

# 锥沉头孔
CounterSinkHole(
    radius=3,                         # 底孔半径
    counter_sink_radius=5,            # 锥面最大半径
    depth=10,                         # 总深度
    counter_sink_angle=82             # 锥角（度，默认 82°）
)

# 结合位置放置多个孔
with BuildPart() as plate:
    Box(100, 60, 10)
    with GridLocations(70, 40, 2, 2):
        CounterSinkHole(radius=2.5, counter_sink_radius=5, depth=10)
```

---

## 13. 枚举类型参考

```python
# Align — 对齐方式
Align.MIN     # 最小侧
Align.CENTER  # 中心
Align.MAX     # 最大侧

# Mode — 布尔操作模式
Mode.ADD
Mode.SUBTRACT
Mode.INTERSECT
Mode.REPLACE
Mode.PRIVATE

# GeomType — 几何类型
GeomType.LINE
GeomType.CIRCLE
GeomType.ELLIPSE
GeomType.BSPLINE
GeomType.BEZIER
GeomType.PLANE
GeomType.CYLINDER
GeomType.CONE
GeomType.SPHERE
GeomType.TORUS
GeomType.SURFACE_OF_REVOLUTION

# SortBy — 排序依据
SortBy.LENGTH
SortBy.RADIUS
SortBy.AREA
SortBy.VOLUME
SortBy.DISTANCE

# Select — 选择范围
Select.ALL    # 所有（默认）
Select.LAST   # 最后一次操作新增的

# Until — 拉伸终止条件
Until.FIRST   # 到第一个面
Until.LAST    # 到最后一个面
Until.NEXT    # 到下一个面
Until.PREVIOUS

# Keep — 分割保留哪部分
Keep.TOP
Keep.BOTTOM
Keep.BOTH

# Side — 偏移方向
Side.LEFT
Side.RIGHT
Side.BOTH
Side.INSIDE
Side.OUTSIDE

# Transition — 扫掠转角处理
Transition.RIGHT       # 直角连接
Transition.ROUND       # 圆角连接
Transition.TRANSFORMED # 变换（默认）

# AngularDirection — 旋转方向
AngularDirection.CLOCKWISE
AngularDirection.COUNTER_CLOCKWISE

# CenterOf — 中心计算方式
CenterOf.GEOMETRY
CenterOf.MASS
CenterOf.BOUNDING_BOX

# ApproxOption — 近似方式
ApproxOption.ARC
ApproxOption.NONE
ApproxOption.SPLINE
```

---

## 14. 导入/导出

```python
# 导入
step_shape = import_step("model.step")
svg_shape  = import_svg("drawing.svg")
dxf_shape  = import_dxf("drawing.dxf")
stl_shape  = import_stl("mesh.stl")

# 导出
export_step(part, "output.step")
export_stl(part, "output.stl")
export_stl(part, "output.stl", tolerance=0.001)      # 精度控制
export_gltf(part, "output.gltf")
export_brep(part, "output.brep")
export_svg(part, "output.svg")
export_svg(part, "output.svg", opt=svg_opts)
export_dxf(sketch, "output.dxf")
export_3mf(part, "output.3mf")

# SVG 选项
svg_opts = {
    "pixel_scale": 5,
    "show_axes": False,
    "show_hidden": True,
    "stroke_color": (0, 0, 0),
    "hidden_color": (128, 128, 128),
}

# CadQuery 互操作
import build123d as b3d
import cadquery as cq
b3d_solid = b3d.Solid.make_box(1, 1, 1)
cq_solid = cq.Shape(b3d_solid.wrapped)   # 转 CadQuery
```

---

## 15. 装配体系统

build123d 使用 `anytree` 实现层级装配，Shape 同时是 NodeMixin。

```python
from build123d import *
import copy

# 创建零件
base = Box(100, 80, 20)
cap  = Box(90, 70, 10)

# 设置父子关系（不复制 CAD 数据）
base.label = "base"
cap.label  = "cap"
cap.parent = base
cap.locate(Pos(0, 0, 20))    # 设置位置

# 构建 Compound 装配
assembly = Compound(children=[base, cap])

# 查看层次结构
print(assembly.show_topology())

# 深拷贝 vs 浅拷贝
deep_copy  = copy.deepcopy(part)   # 完整复制 CAD 数据
ref_copy   = copy.copy(part)       # 引用原 CAD 数据（更快）

# 大量重复零件的高效装配
screw = import_step("screw.step")
locs  = GridLocations(10, 10, 5, 5).local_locations
screw_instances = [copy.copy(screw).locate(loc) for loc in locs]
assembly = Compound(children=screw_instances)

# 访问装配件
assembly.children        # 直接子节点
assembly.descendants     # 所有后代
assembly["base"]         # 按名称访问
```

---

## 16. 关节系统 Joints

```python
from build123d import *

# 刚性关节（固定连接）
RigidJoint(label="base_attach", to_part=base, joint_location=Pos(0,0,20))

# 旋转关节（铰链）
RevoluteJoint(
    label="hinge",
    to_part=lid,
    axis=Axis((0,0,0), (0,1,0)),
    angular_range=(0, 120)
)

# 线性关节（滑动）
LinearJoint(
    label="slide",
    to_part=drawer,
    axis=Axis.X,
    linear_range=(0, 50)
)

# 螺旋关节
CylindricalJoint(
    label="screw",
    to_part=bolt,
    axis=Axis.Z,
    linear_range=(0, 30),
    angular_range=(0, 360 * 5)
)

# 连接关节
joint1.connect_to(joint2, angle=45)
joint1.connect_to(joint2, position=10)
```

---

## 17. 自定义对象扩展

通过继承基类实现可重用参数化对象：

```python
from build123d import *

# 自定义草图对象
class StarShape(BaseSketchObject):
    def __init__(self, outer_r: float, inner_r: float, points: int,
                 mode: Mode = Mode.ADD):
        with BuildSketch() as star:
            angles = [i * 360 / (2 * points) for i in range(2 * points)]
            radii  = [outer_r if i % 2 == 0 else inner_r for i in range(2*points)]
            pts = [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
                   for r, a in zip(radii, angles)]
            Polygon(*pts)
        super().__init__(obj=star.sketch, mode=mode)

# 自定义零件对象
class ParametricBracket(BasePartObject):
    def __init__(self, length: float, width: float, thickness: float,
                 hole_radius: float, mode: Mode = Mode.ADD):
        with BuildPart() as bracket:
            Box(length, width, thickness)
            with GridLocations(length - 20, width - 20, 2, 2):
                Hole(radius=hole_radius)
            fillet(bracket.edges().filter_by(Axis.Z), radius=2)
        super().__init__(obj=bracket.part, mode=mode)

# 使用自定义对象
with BuildPart() as assembly:
    ParametricBracket(100, 60, 5, 3)
    with Locations((120, 0, 0)):
        ParametricBracket(80, 50, 4, 2.5)
```

---

## 18. 运算符速查

### Shape 运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `+` | 布尔并（ADD） | `part1 + part2` |
| `-` | 布尔差（SUBTRACT） | `part - hole` |
| `&` | 布尔交（INTERSECT） | `part1 & part2` |
| `+=` | 原地并 | `sketch += Circle(5)` |
| `-=` | 原地差 | `sketch -= Pos(3,0)*Circle(2)` |

### 位置/平面运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `*` | 坐标系变换/应用 | `Plane.XZ * Circle(5)` |
| `*` | 位置组合 | `Pos(10,0) * Rot(Z=45)` |

### 曲线参数运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `@` | 参数 t ∈[0,1] 处的点 | `edge @ 0.5` → Vector |
| `%` | 参数 t ∈[0,1] 处的切向 | `edge % 0.0` → Vector |
| `@1` | 终点 | `line @ 1` |
| `@0` | 起点 | `line @ 0` |

### ShapeList 运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `-` | 差集（新边选择） | `new_edges = after - before` |
| `\|` | 并集 | `edges1 \| edges2` |
| `[]` | 索引/切片 | `edges[-1]`, `edges[-2:]` |

---

## 19. 最佳实践 & Tips

### 设计工作流

```
1. 确定对称轴 → 选择合适原点
2. 从最简截面开始（2D → 3D）
3. 先建主体，后加细节（孔/特征）
4. fillet/chamfer 放在最后
5. 用 Select.LAST 跟踪新边
6. 导出前调用 .clean() 优化
```

### 性能技巧

```python
# ✅ 使用 copy.copy() 而非 deepcopy() 处理大量重复零件
instances = [copy.copy(part).locate(loc) for loc in locs]

# ✅ 用 make_hull() 替代多次 union
face = make_hull([line1, line2, arc1])

# ✅ 将多个 Circle/Rectangle 合并后再拉伸，而非分别拉伸布尔
sketch = Rectangle(100, 60)
sketch -= GridLocations(40, 30, 2, 2) * Circle(5)
part = extrude(sketch, 10)  # 一次 Boolean

# ✅ 避免在 fillet 前进行不必要的 Boolean
```

### 选择器技巧

```python
# 选择最后操作新增的边（重要！）
before = part.edges()
part -= extrude(sketch, -5)
new_edges = part.edges() - before

# 选择圆孔所有边
hole_face = part.faces().filter_by(GeomType.CYLINDER).sort_by(SortBy.RADIUS)[0]
hole_edges = hole_face.edges()

# 按 Z 分层选择
layers = part.edges().group_by(Axis.Z)
top_edges = layers[-1]     # 最顶层
bot_edges = layers[0]      # 最底层
```

### 与 OCP / CadQuery 互操作

```python
# build123d → OCP (OpenCascade)
occ_shape = part.wrapped    # 访问底层 TopoDS_Shape

# build123d → CadQuery
import cadquery as cq
cq_obj = cq.Shape(part.wrapped)

# CadQuery → build123d
import build123d as b3d
b3d_shape = b3d.Shape.cast(cq_obj.val().wrapped)
```

---

## 20. 常见陷阱 & FAQ

### Q1: 拉伸方向意外

```python
# 问题：extrude 负值的方向与预期相反
# 原因：方向相对于面的法向量
# 解决：明确指定 dir 参数
extrude(sketch, amount=10, dir=(0, 0, -1))  # 显式指定方向
```

### Q2: fillet 失败

```python
# 原因：圆角半径过大，或选择了不适合的边
# 解决：
# 1. 减小 radius
# 2. 确认选择的边是正确的
# 3. 在 2D 阶段先 fillet，再拉伸
# 4. 复杂几何先 .clean() 再 fillet
```

### Q3: Mode.SUBTRACT 没有效果

```python
# 检查：待减对象是否与主体真正相交
# 检查：坐标系是否正确（plane/location）
# 检查：order — 必须在有主体之后执行
```

### Q4: Select.LAST 无法正确选择

```python
# Select.LAST 只能选择"最后一次 build123d 操作"新增的形状
# 正确做法：
snapshot = part.edges()    # 操作前拍快照
part -= Hole(radius=3)     # 执行操作
new = part.edges() - snapshot  # 差集得到新边
```

### Q5: Compound vs Part vs Solid

```python
Solid()     # 单个实体（不能包含其他形状）
Part()      # Compound of Solids（可包含多个 Solid）
Compound()  # 任意维度的集合（最通用）

# Part() + Part() 返回 Compound（如果有多个 Solid）
# Solid() + Solid() 可能返回 ShapeList（v0.9+）
# 解决方案：用 Compound() 包装
result = Compound([solid1, solid2])
```

### Q6: 升级 0.8 → 0.9+ 的破坏性变更

```python
# 旧 API                         # 新 API
shape.export_stl("file.stl")  →  export_stl(shape, "file.stl")
surface.thicken(amount)        →  Solid.thicken(surface, amount)
Shape.extrude()               →  extrude() 函数 / Edge.extrude(vertex)
```

---

## 附录：完整导入示例

```python
from build123d import *
# 包含：所有 Shape 类、操作函数、构建器、枚举、几何类
# 典型 build123d 脚本标准做法（尽管通配符导入不推荐用于库）

# 可视化（需安装 ocp_vscode）
from ocp_vscode import show, show_object

# 使用
part = Box(10, 10, 10)
show(part)                # 在 OCP Viewer 中显示

# 单位换算
MM = 1.0      # build123d 默认单位是 mm
from build123d import MM, CM, IN  # 单位常量
box = Box(1 * IN, 2 * IN, 0.5 * IN)   # 英寸单位输入
```

---

*本文档基于 build123d v0.10.0 编写，覆盖 Algebra Mode、Builder Mode、拓扑系统、选择器、装配体和关节系统。*
