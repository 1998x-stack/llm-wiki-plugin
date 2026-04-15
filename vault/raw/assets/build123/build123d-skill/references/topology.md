# Topology Reference — build123d

## Shape 基类

```python
# 属性
shape.volume           # float — 体积
shape.area             # float — 面积
shape.length           # float — 长度 (Edge/Wire)
shape.center()         # Vector — 重心 (CenterOf.MASS default)
shape.center(CenterOf.BOUNDING_BOX)
shape.bounding_box()   # BoundingBox
shape.label            # str — 名称标签
shape.color            # Color
shape.is_valid         # bool
shape.geom_type        # GeomType enum
shape.location         # Location

# 拓扑访问 → ShapeList
shape.vertices()
shape.edges()
shape.wires()
shape.faces()
shape.shells()
shape.solids()
shape.compounds()
shape.get_top_level_shapes()  # v0.10+

# 变换（返回新对象）
shape.move(location)
shape.moved(location)
shape.locate(location)     # 原地修改
shape.mirror(plane)
shape.rotate(axis, angle)
shape.scale(factor)
shape.clean()
shape.fix()

# 布尔运算（Shape 级，无上下文）
shape.fuse(other)
shape.cut(other)
shape.intersect(other)     # 可能返回 None（无交集）

# 属性查询
shape.is_inside(point)     # 点在内部？
shape.find_intersection(point, direction)
shape.project_to_shape(other)
```

## Mixin1D (Edge / Wire 专用)

```python
edge.length              # float
edge.radius              # float (圆弧)
edge.start_point()       # Vector
edge.end_point()         # Vector
edge.tangent_at(t)       # Vector (t ∈ [0,1])
edge.position_at(t)      # Vector
edge @ t                 # position_at(t) 简写
edge % t                 # tangent_at(t) 简写
edge.close()             # 闭合 Edge → Wire
edge.make_wire()         # Edge → Wire
wire.close()             # 闭合 Wire
wire.order_edges()       # 重排边顺序
wire.project_to_shape(solid, direction)
```

## Mixin3D (Solid / Compound 专用)

```python
solid.shell(amount, faces)        # 抽壳
solid.is_inside(point)            # bool
solid.max_fillet(edges, tolerance)  # 最大可用圆角半径
solid.make_loft(...)              # 放样
```

## Face 专用属性

```python
face.area                # float
face.normal_at(point)    # Vector — 法向量
face.center()            # Vector
face.outer_wire()        # Wire — 外轮廓
face.inner_wires()       # list[Wire] — 孔轮廓
face.is_planar           # bool
face.radius              # float (圆柱面)
face.radii               # tuple (椭圆面 x/y 半径) v0.10+
face.is_circular_convex  # bool v0.10+
face.is_circular_concave # bool v0.10+
face.axis_of_rotation    # Axis (旋转面) v0.10+
face.make_surface_patch(wire, ...) # 约束曲面
face.make_gordon_surface(...)      # Gordon 曲面 v0.10+
```

## ShapeList 完整方法

```python
sl = part.edges()   # ShapeList

# 过滤
sl.filter_by(Axis.X)                       # 轴向
sl.filter_by(Axis.Y)
sl.filter_by(Axis.Z)
sl.filter_by(GeomType.LINE)               # 几何类型
sl.filter_by(GeomType.CIRCLE)
sl.filter_by(GeomType.CYLINDER)
sl.filter_by(lambda s: s.length > 5)      # 自定义 predicate

# 排序（升序，用[-1]取最大）
sl.sort_by(Axis.X)
sl.sort_by(Axis.Y)
sl.sort_by(Axis.Z)
sl.sort_by(SortBy.LENGTH)
sl.sort_by(SortBy.RADIUS)
sl.sort_by(SortBy.AREA)
sl.sort_by(SortBy.VOLUME)
sl.sort_by(SortBy.DISTANCE)

# 分组（按坐标或属性聚类）
groups = sl.group_by(Axis.Z)    # list of ShapeList
groups = sl.group_by(SortBy.RADIUS)

# 属性
sl.first    # 第一个 Shape
sl.last     # 最后一个 Shape

# 集合运算
new = after_sl - before_sl   # 差集（新增的）
union = sl1 | sl2             # 并集
```

## BoundingBox

```python
bbox = shape.bounding_box()
bbox.min          # Vector(xmin, ymin, zmin)
bbox.max          # Vector(xmax, ymax, zmax)
bbox.size         # Vector(w, h, d)
bbox.center       # Vector
bbox.diagonal     # float
bbox.is_inside(point)  # bool
bbox.add(other_bbox)   # 合并返回新 BoundingBox
```

## Compound / Part / Sketch

```python
# Compound — 通用容器
c = Compound([shape1, shape2, shape3])
c.children        # anytree 子节点
c.show_topology() # 打印树状结构
c.get_top_level_shapes()   # v0.10+

# Part = Compound of Solids
p = Part()
p += Box(10,10,10)

# Sketch = Compound of Faces
s = Sketch()
s += Circle(5)

# Curve = Compound of Edges/Wires (v0.10 replaces old Curve)
```
