# Objects Reference — build123d

## 1D 对象 (BuildLine / Curve)

### 直线族

```python
Line(start, end)
PolarLine(start, length, angle=None, direction=None)
IntersectingLine(pt, direction, face_or_plane)
```

### 弧线族

```python
CenterArc(center, radius, start_angle, arc_size,
          angular_direction=AngularDirection.COUNTER_CLOCKWISE)
RadiusArc(start_point, end_point, radius)
SagittaArc(start_point, end_point, sagitta)
TangentArc(start_point, end_point, tangent, tangent_from_first=True)
EllipticalCenterArc(center, x_radius, y_radius, start_angle, arc_size, rotation=0)
ParabolicCenterArc(center, start_vertex, end_vertex)
HyperbolicCenterArc(...)

# JernArc — 续接弧（接续已有边）
JernArc(start, tangent, radius, arc_size,
        angular_direction=AngularDirection.COUNTER_CLOCKWISE)

# ArcArc 族
ArcArcTangentArc(arc1, arc2)
ArcArcTangentLine(arc1, pt)
PointArcTangentArc(pt, arc)
PointArcTangentLine(pt1, arc, pt2)
DoubleTangentArc(pt, tangent, arc)
ConstrainedArcs(...)
```

### 复合曲线

```python
Polyline(*pts, close=False)
FilletPolyline(*pts, radius, close=False)
Spline(*pts, tangents=None, tangent_scalars=None, periodic=False)
Bezier(*pts)                              # 贝塞尔
Helix(pitch, height, radius, center=(0,0,0), lefthand=False, cone_angle=0)
BlendCurve(edge1, edge2, continuity=2)    # C0/C1/C2 混合曲线 v0.10+
Airfoil(naca="2412", chord=100, ...)      # NACA 翼型
ConstrainedLines(...)
```

---

## 2D 对象 (BuildSketch / Sketch)

### 圆形族

```python
Circle(radius, align=CENTER)
Ellipse(x_radius, y_radius, rotation=0, align=CENTER)
```

### 矩形族

```python
Rectangle(width, height, align=CENTER, rotation=0)
RectangleRounded(width, height, radius, align=CENTER)
Square(size, align=CENTER, rotation=0)
SlottedRectangle(width, height, slot_width, align=CENTER)
```

### 多边形族

```python
RegularPolygon(radius, side_count, align=CENTER,
               major_radius=False, rotation=0)
Polygon(*pts, align=CENTER)
Trapezoid(width, height, left_side_angle, right_side_angle=None,
          align=CENTER, rotation=0)
```

### 文字/其他

```python
Text(txt, font_size, font="Arial", font_path=None,
     font_style=FontStyle.REGULAR, align=CENTER,
     path=None, position_on_path=0)
```

---

## 3D 对象 (BuildPart / Part)

### 基础几何体

```python
Box(length, width, height, align=CENTER)
Cylinder(radius, height, arc_size=360, align=CENTER)
Cone(bottom_radius, top_radius, height, arc_size=360, align=CENTER)
Sphere(radius, arc_size1=-90, arc_size2=90, arc_size3=360, align=CENTER)
Torus(major_radius, minor_radius, minor_start_angle=-180,
      minor_end_angle=180, major_angle=360, align=CENTER)
Wedge(xsize, ysize, zsize, xminsize=0, zminsize=0, align=MIN)
```

### 孔特征

```python
Hole(radius, depth=None, mode=Mode.SUBTRACT)
CounterBoreHole(radius, counter_bore_radius, counter_bore_depth,
                depth=None, mode=Mode.SUBTRACT)
CounterSinkHole(radius, counter_sink_radius, depth=None,
                counter_sink_angle=82, mode=Mode.SUBTRACT)
```

### 位置模式（Locations 上下文）

所有对象在 `with Locations(...)` 内自动多实例化：

```python
with BuildPart() as bp:
    Box(100, 60, 10)
    with GridLocations(70, 40, 2, 2):
        Hole(radius=3)    # 自动在4个位置打孔
```

---

## Locations 上下文对象

```python
Locations(*locs_or_planes)           # 单个或多个位置
GridLocations(x_spacing, y_spacing, x_count, y_count, align=CENTER)
PolarLocations(radius, count, start_angle=0, angular_range=360,
               rotate_children=True)
HexLocations(apothem, x_count, y_count, major_radius=False, align=CENTER)
CurveLocations(curve, count)         # 沿曲线均匀分布

# 访问 local_locations（不含父级变换）
locs = GridLocations(10, 10, 3, 3).local_locations  # list[Location]
```
