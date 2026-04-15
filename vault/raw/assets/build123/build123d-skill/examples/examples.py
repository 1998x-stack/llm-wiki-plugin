"""
build123d Examples Collection
Demonstrates: Builder Mode, Algebra Mode, Selectors, Assemblies
"""

# ============================================================
# Example 1: L-Bracket (Both Modes)
# ============================================================

from build123d import *

# --- Algebra Mode ---
def make_bracket_algebra(length=80, height=60, width=40,
                          thickness=5, hole_radius=3):
    """L型支架 - 代数模式"""
    with BuildSketch(Plane.XZ) as profile:
        with BuildLine() as outline:
            FilletPolyline(
                (0, 0), (length / 2, 0), (length / 2, height),
                radius=thickness
            )
            offset(amount=thickness, side=Side.LEFT)
        make_face()
        mirror(about=Plane.YZ)

    part = extrude(profile.sketch, amount=width / 2)
    part = part + mirror(part, about=Plane.XY)

    # 打孔
    top_face = part.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(Plane(top_face)):
        with GridLocations(length - 20, 0, 2, 1):
            Circle(hole_radius)
    holes = extrude(amount=-thickness - 1, mode=Mode.SUBTRACT)

    # 最后圆角
    corners = part.edges().filter_by(Axis.X).group_by(Axis.Y)[-1]
    part = fillet(corners, radius=3)
    return part


# --- Builder Mode ---
def make_bracket_builder(length=80, height=60, width=40,
                          thickness=5, hole_radius=3):
    """L型支架 - 构建器模式"""
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                FilletPolyline(
                    (0, 0), (length / 2, 0), (length / 2, height),
                    radius=thickness
                )
                offset(amount=thickness, side=Side.LEFT)
            make_face()
            mirror(about=Plane.YZ)
        extrude(amount=width / 2)
        mirror(about=Plane.XY)

        # 孔
        with BuildSketch(bp.faces().sort_by(Axis.Z)[-1]):
            with GridLocations(length - 20, 0, 2, 1):
                Circle(hole_radius)
        extrude(amount=-thickness - 1, mode=Mode.SUBTRACT)

        # 圆角
        corners = bp.edges().filter_by(Axis.X).group_by(Axis.Y)[-1]
        fillet(corners, radius=3)

    return bp.part


# ============================================================
# Example 2: Tea Cup (Revolve + Spline + Assembly)
# ============================================================

def make_tea_cup():
    """茶杯 — 旋转体 + 样条曲线 + 偏移抽壳"""
    wall = 3 * MM
    fillet_r = wall * 0.49

    with BuildPart() as cup:
        # 碗部旋转
        with BuildSketch(Plane.XZ):
            with BuildLine():
                s = Spline(
                    (30*MM, 10*MM), (69*MM, 105*MM),
                    tangents=((1, 0.5), (0.7, 1)),
                    tangent_scalars=(1.75, 1)
                )
                Polyline(s@0, s@0 + (10*MM, -10*MM),
                         (0, 0), (0, (s@1).Y), s@1)
            make_face()
        revolve(axis=Axis.Z)

        # 抽壳（顶面和底面开口）
        openings = cup.faces().filter_by(GeomType.PLANE)
        offset(amount=-wall, openings=openings)

        # 加底
        with Locations((0, 0, (s@0).Y)):
            Cylinder(radius=(s@0).X, height=wall)

        # 圆角所有边
        fillet(cup.edges(), radius=fillet_r)

    return cup.part


# ============================================================
# Example 3: Parametric Lego Brick (Full Builder Mode)
# ============================================================

def make_lego(pip_count=4, pip_rows=2):
    """参数化乐高积木"""
    UNIT = 8
    PIP_H = 1.8
    PIP_D = 4.8
    BASE_H = 9.6
    WALL = 1.2
    SUPPORT_OD = 6.5
    SUPPORT_ID = 4.8

    W = UNIT * pip_count
    D = UNIT * pip_rows
    H = BASE_H + PIP_H

    with BuildPart() as lego:
        # 外壳
        with BuildSketch():
            Rectangle(W, D)
            offset(amount=-WALL, mode=Mode.SUBTRACT)
        extrude(amount=BASE_H)

        # 顶板
        with BuildSketch(lego.faces().sort_by(Axis.Z)[-1]):
            Rectangle(W, D)
        extrude(amount=WALL)

        # 内支撑柱（底部）
        if pip_count > 1 and pip_rows > 1:
            with BuildSketch():
                with GridLocations(UNIT, UNIT, pip_count-1, pip_rows-1):
                    Circle(SUPPORT_OD / 2)
                    Circle(SUPPORT_ID / 2, mode=Mode.SUBTRACT)
            extrude(amount=BASE_H - WALL)

        # 顶部 Pips
        with BuildSketch(lego.faces().sort_by(Axis.Z)[-1]):
            with GridLocations(UNIT, UNIT, pip_count, pip_rows):
                Circle(PIP_D / 2)
        extrude(amount=PIP_H)

    return lego.part


# ============================================================
# Example 4: Selector Chaining Demo
# ============================================================

def selector_demo():
    """选择器链式操作演示"""
    part = Part() + Box(80, 60, 20)

    # 打4个孔
    hole_sketch = Plane(part.faces().sort_by(Axis.Z)[-1]) * (
        GridLocations(50, 30, 2, 2) * Circle(4)
    )
    part -= extrude(hole_sketch, -20)

    # 选择顶面圆形边（孔边）
    top_face = part.faces().sort_by(Axis.Z)[-1]
    hole_edges = top_face.edges().filter_by(GeomType.CIRCLE)
    part = chamfer(hole_edges, length=1)

    # 选择 Z 方向竖边（角边）
    vertical_edges = part.edges().filter_by(Axis.Z)
    part = fillet(vertical_edges, radius=3)

    # 选择最顶层边（顶面外轮廓）
    top_layer = part.edges().group_by(Axis.Z)[-1]
    long_edges = top_layer.filter_by(lambda e: e.length > 10)
    part = fillet(long_edges, radius=2)

    return part


# ============================================================
# Example 5: Simple Assembly
# ============================================================

def make_assembly():
    """简单装配体示例"""
    import copy

    # 底座
    base = Part() + Box(100, 80, 10)
    base.label = "base"

    # 立柱（4个）
    post = Part() + Cylinder(radius=5, height=40)
    post.label = "post"

    locs = GridLocations(70, 50, 2, 2).local_locations
    post_instances = []
    for i, loc in enumerate(locs):
        p = copy.copy(post)
        p.label = f"post_{i}"
        p.locate(loc * Pos(0, 0, 10))
        post_instances.append(p)

    # 顶板
    top = Part() + Box(100, 80, 8)
    top.label = "top"
    top.locate(Pos(0, 0, 50))

    assembly = Compound(children=[base, *post_instances, top])
    return assembly


# ============================================================
# Example 6: Import/Export Pipeline
# ============================================================

def import_export_demo():
    """导入导出示例"""
    from build123d import *

    # 创建零件
    part = Part() + Box(50, 40, 20)
    part -= Cylinder(radius=10, height=20)

    # 导出多种格式
    export_step(part, "/tmp/part.step")
    export_stl(part, "/tmp/part.stl", tolerance=0.01)
    export_brep(part, "/tmp/part.brep")

    # SVG 工程图导出
    svg_opts = {
        "pixel_scale": 5,
        "show_axes": True,
        "show_hidden": True,
    }
    export_svg(part, "/tmp/part.svg", opt=svg_opts)

    # 重新导入 STEP
    imported = import_step("/tmp/part.step")
    print(f"Imported volume: {imported.volume:.2f} mm³")
    print(f"Faces: {len(imported.faces())}")


if __name__ == "__main__":
    # 快速测试所有示例
    print("Making bracket (algebra)...")
    b1 = make_bracket_algebra()
    print(f"  Volume: {b1.volume:.1f}")

    print("Making bracket (builder)...")
    b2 = make_bracket_builder()
    print(f"  Volume: {b2.volume:.1f}")

    print("Making Lego brick...")
    lego = make_lego(4, 2)
    print(f"  Volume: {lego.volume:.1f}")

    print("Selector demo...")
    sd = selector_demo()
    print(f"  Faces: {len(sd.faces())}")

    print("Assembly demo...")
    assy = make_assembly()
    print(assy.show_topology())

    print("All examples complete!")
