# Operations Reference — build123d

## 通用操作 (1D/2D/3D)

```python
# 添加形状到上下文
add(shape, rotation=None, locations=None, mode=Mode.ADD)

# 圆角
fillet(objects, radius)          # objects: Edge|Vertex 或其列表
# Vertex fillet → 圆角顶点（2D）；Edge fillet → 圆角边（3D）

# 倒角
chamfer(objects, length, length2=None, angle=None, reference=None)
# length2: 非对称倒角第二长度
# reference: Face — 指定长度测量方向的参考面

# 镜像
mirror(shapes, about=Plane.XY, mode=Mode.ADD)

# 偏移
offset(objects, amount, openings=None, kind=Kind.ARC, side=Side.BOTH,
       closed=True, mode=Mode.REPLACE)
# openings: list[Face] — 抽壳时的开口面

# 缩放
scale(objects, by)

# 投影
project(objects, workplane, projection=..., mode=Mode.ADD)

# 分割
split(objects, bisect_plane, keep=Keep.TOP, mode=Mode.REPLACE)
```

## 草图专用操作

```python
# 从封闭轮廓创建面
make_face(lines=None, mode=Mode.ADD)

# 凸包
make_hull(objects=None, mode=Mode.ADD)

# 线条加宽 → 面
trace(lines=None, stroke_width=1, side=Side.BOTH, mode=Mode.ADD)

# Voronoi 完整圆角
full_round(edge, invert=False, voronoi_point_count=100, mode=Mode.REPLACE)
# → (Sketch, Vector center, float radius)
```

## 3D 专用操作

```python
# 拉伸
extrude(to_extrude=None, amount=None, dir=None,
        until=None, target=None,
        both=False, taper=0.0, clean=True, mode=Mode.ADD)
# until: Until.FIRST / LAST / NEXT / PREVIOUS

# 旋转
revolve(profiles=None, axis=Axis.Z, angle=360, clean=True, mode=Mode.ADD)

# 放样
loft(sections=None, ruled=False, clean=True, mode=Mode.ADD)
# sections: list[Vertex | Face | Sketch]

# 扫掠
sweep(sections=None, path=None, multisection=False,
      is_frenet=False, transition=Transition.TRANSFORMED,
      normal=None, binormal=None, clean=True, mode=Mode.ADD)

# 加厚（面 → 实体）
thicken(to_thicken=None, amount=None, normal_override=None,
        both=False, clean=True, mode=Mode.ADD)

# 线转面扫掠（管道截面）
# Builder Mode: pending edges → faces
sweep_line(...)

# 拔模角
draft(faces=None, plane=None, angle=5, mode=Mode.REPLACE)
```

---

# Enums Reference — build123d

```python
from build123d import *

# Align
Align.MIN / CENTER / MAX

# Mode
Mode.ADD / SUBTRACT / INTERSECT / REPLACE / PRIVATE

# GeomType
GeomType.LINE / CIRCLE / ELLIPSE / BSPLINE / BEZIER
GeomType.PLANE / CYLINDER / CONE / SPHERE / TORUS
GeomType.SURFACE_OF_REVOLUTION / OFFSET_SURFACE / OTHER

# SortBy
SortBy.LENGTH / RADIUS / AREA / VOLUME / DISTANCE

# Select
Select.ALL / LAST

# Until (extrude)
Until.FIRST / LAST / NEXT / PREVIOUS

# Keep (split)
Keep.TOP / BOTTOM / BOTH / INSIDE / OUTSIDE

# Side (offset)
Side.LEFT / RIGHT / BOTH / INSIDE / OUTSIDE

# Transition (sweep)
Transition.RIGHT / ROUND / TRANSFORMED

# AngularDirection
AngularDirection.CLOCKWISE / COUNTER_CLOCKWISE

# CenterOf
CenterOf.GEOMETRY / MASS / BOUNDING_BOX

# ApproxOption
ApproxOption.ARC / NONE / SPLINE

# FontStyle
FontStyle.REGULAR / BOLD / ITALIC

# Kind (offset joint)
Kind.ARC / INTERSECTION / TANGENT

# LengthMode
LengthMode.DIAGONAL / HORIZONTAL / VERTICAL

# Units (常量)
MM = 1.0
CM = 10.0
IN = 25.4
FT = 304.8
```

---

# Tips & Best Practices — build123d

## 工作流推荐顺序

```
1. 规划对称轴，选择原点（减少后续变换）
2. 创建主要轮廓（2D Sketch）
3. 拉伸/旋转/放样 → 3D
4. 添加主要特征（孔、凸台）
5. 最后执行 fillet/chamfer
6. 调用 .clean() 优化拓扑
7. 导出
```

## 性能优化

```python
# ✅ 多实例用 copy.copy（浅拷贝引用 OCC TShape）
import copy
instances = [copy.copy(part).locate(loc) for loc in locs]

# ✅ 合并 sketch 后一次拉伸，避免多次 boolean
sketch = Rectangle(100, 60)
sketch -= GridLocations(50, 40, 2, 2) * Circle(5)
part = extrude(sketch, 10)  # 一次操作

# ✅ 复杂 boolean 前先 make_hull 简化轮廓
face = make_hull([line1, arc1, line2])

# ❌ 避免：多次独立 boolean union
part += Box(...)
part += Box(...)  # 可以，但大量时效率低
```

## 选择器最佳实践

```python
# 追踪新增边（最可靠方式）
snapshot = part.edges()
part -= extrude(inner_sketch, -depth)
new_edges = part.edges() - snapshot
fillet(new_edges, radius=1)

# 从面的角度选择关联边
top = part.faces().sort_by(Axis.Z)[-1]   # 顶面
rim_edges = top.edges().filter_by(GeomType.CIRCLE)  # 孔边

# 不要依赖边的顺序（拓扑操作后可能变化）
# ✅ 用属性描述，而非索引
```

## 常见错误与修复

### fillet 失败
```python
# 原因：半径过大 / 相邻边冲突
# 修复1：减小 radius
# 修复2：先 .clean() 再 fillet
part = part.clean()
part = fillet(part.edges(), radius=1)

# 查询最大可用半径
max_r = solid.max_fillet(edges, tolerance=0.001)
```

### extrude 方向错误
```python
# 原因：face 法向量与预期相反
# 修复：显式指定方向
extrude(sketch, amount=10, dir=(0, 0, -1))
# 或：用负值 + mode 控制
extrude(sketch, amount=-10, mode=Mode.SUBTRACT)
```

### Solid + Solid → ShapeList (v0.9+)
```python
# 旧行为（v0.8）：Solid + Solid = Compound
# 新行为（v0.9+）：Solid + Solid = ShapeList
# 修复：
result = Compound([solid1 + solid2])
# 或使用 Part:
result = Part() + solid1 + solid2
```

### 升级迁移 v0.8 → v0.9+
```python
# 旧                              # 新
shape.export_stl("f.stl")    →   export_stl(shape, "f.stl")
shape.export_step("f.step")  →   export_step(shape, "f.step")
surface.thicken(amt)         →   Solid.thicken(surface, amt)
Shape.intersect()            →   extrude() 或 Edge.extrude(vertex)
Curve 对象                   →   Wire / Edge (v0.10)
first_level_shapes           →   get_top_level_shapes() (v0.10)
```

---

# Assembly Reference — build123d

```python
import copy
from build123d import *

## 基础装配
base = Box(100, 80, 20)
base.label = "base"

cap = Box(90, 70, 10)
cap.label = "cap"
cap.parent = base              # 设置父节点（anytree）
cap.locate(Pos(0, 0, 20))

# 构建 Compound 装配
assembly = Compound(children=[base, cap])
print(assembly.show_topology())

## 高效重复零件
screw = import_step("screw.step")
locs = GridLocations(15, 15, 4, 4).local_locations
# 浅拷贝：共享 OCC 数据，更快更省内存
copies = [copy.copy(screw).locate(loc) for loc in locs]
assy = Compound(children=copies)

## 关节系统
from build123d import *

# 刚性关节
RigidJoint("base_mount", to_part=base,
           joint_location=Pos(0, 0, 20))

# 旋转关节
RevoluteJoint("hinge", to_part=lid,
              axis=Axis((0,0,0), (0,1,0)),
              angular_range=(0, 120))

# 线性关节
LinearJoint("slide", to_part=drawer,
            axis=Axis.X, linear_range=(0, 50))

# 圆柱关节（旋转+线性）
CylindricalJoint("screw_joint", to_part=bolt,
                 axis=Axis.Z,
                 linear_range=(0, 30),
                 angular_range=(0, 1800))

# 连接关节
joint_a = base.joints["base_mount"]
joint_b = arm.joints["arm_mount"]
joint_a.connect_to(joint_b, angle=45)

## anytree 属性
shape.parent           # 父节点
shape.children         # 子节点 tuple
shape.ancestors        # 所有祖先
shape.descendants      # 所有后代
shape.root             # 根节点
```

---

# Import/Export Reference — build123d

```python
# === 导入 ===
import_step("model.step")         # → Part/Compound
import_svg("drawing.svg")         # → Sketch (Compound of Faces)
import_dxf("drawing.dxf")         # → Sketch
import_stl("mesh.stl")            # → Solid (tessellated)
import_brep("shape.brep")         # → Shape

# === 导出 ===
export_step(shape, "output.step")
export_stl(shape, "output.stl")
export_stl(shape, "output.stl", tolerance=0.001,  # 精度
           angular_tolerance=0.1)                  # 角度精度

export_gltf(shape, "output.gltf")
export_gltf(shape, "output.gltf", binary=True)    # .glb

export_brep(shape, "output.brep")
export_svg(shape, "output.svg")
export_svg(shape, "output.svg", opt=svg_opts)

export_dxf(sketch, "output.dxf")
export_3mf(shape, "output.3mf")

# SVG 选项
svg_opts = {
    "pixel_scale": 5,
    "show_axes": False,
    "show_hidden": True,
    "stroke_color": (0, 0, 0),
    "hidden_color": (160, 160, 160),
    "stroke_width": 0.25,
    "line_type": "iso",              # 投影类型
}

# 单位
from build123d import MM, CM, IN, FT
box = Box(1 * IN, 2 * IN, 0.5 * IN)   # 英寸

# CadQuery 互操作
import cadquery as cq, build123d as b3d
# b3d → cq
cq_shape = cq.Shape(b3d_part.wrapped)
# cq → b3d
b3d_shape = b3d.Shape.cast(cq_shape.val().wrapped)

# OCP 底层访问
occ_topo = shape.wrapped    # TopoDS_Shape
```
