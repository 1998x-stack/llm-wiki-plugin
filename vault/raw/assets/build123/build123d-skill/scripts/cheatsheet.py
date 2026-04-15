#!/usr/bin/env python3
"""
build123d Quick Reference Cheat Sheet Script
Run this to see all key patterns in one place.
"""

CHEATSHEET = """
╔══════════════════════════════════════════════════════════════╗
║           build123d Quick Reference Cheat Sheet              ║
╚══════════════════════════════════════════════════════════════╝

━━━ SETUP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  pip install build123d ocp-vscode
  from build123d import *
  from ocp_vscode import show

━━━ ALGEBRA MODE (stateless) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  sketch = Rectangle(100, 60)
  sketch -= Circle(10)               # subtract
  part   = extrude(sketch, 10)       # → 3D
  part   = fillet(part.edges(), 2)   # round
  export_step(part, "out.step")

━━━ BUILDER MODE (context) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  with BuildPart() as bp:
    with BuildSketch():
      Rectangle(100, 60)
      Circle(10, mode=Mode.SUBTRACT)
    extrude(amount=10)
    fillet(edges(), radius=2)
  result = bp.part

━━━ 1D OBJECTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Line(start, end)
  PolarLine(start, length, angle=45)
  Polyline(*pts)
  FilletPolyline(*pts, radius=2)
  CenterArc(center, radius, start, arc_size)
  RadiusArc(start, end, radius)
  SagittaArc(start, end, sagitta)
  JernArc(start, tangent, radius, arc_size)  # continues an edge
  Spline(*pts, tangents=...)
  Bezier(*pts)
  Helix(pitch, height, radius)
  BlendCurve(e1, e2)                # C2 blend

━━━ 2D OBJECTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Circle(r)  Ellipse(rx, ry)
  Rectangle(w, h)  RectangleRounded(w, h, r)
  Square(s)  RegularPolygon(r, n)
  Trapezoid(w, h, angle)  Polygon(*pts)
  Text("txt", font_size=10)

━━━ 3D OBJECTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Box(l, w, h)  Cylinder(r, h)
  Cone(r1, r2, h)  Sphere(r)
  Torus(R, r)  Wedge(...)
  Hole(r, depth)
  CounterBoreHole(r, cbr, cbd, depth)
  CounterSinkHole(r, csr, depth, angle=82)

━━━ OPERATIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  extrude(sketch, amount=10)         # + taper, both, dir, until
  revolve(sketch, axis=Axis.Z)       # + angle
  loft([s1, s2, s3])                 # + ruled
  sweep(profile, path)               # + binormal, transition
  thicken(face, amount=2)
  fillet(edges, radius)
  chamfer(edges, length)
  mirror(shape, about=Plane.XY)
  offset(shape, amount)              # + openings for shell
  split(shape, bisect_plane)
  scale(shape, by=2.0)
  make_face()   make_hull()   trace()

━━━ OPERATORS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  part + part2    → union
  part - hole     → difference
  part & other    → intersection
  Plane.XZ * shape         → place on plane
  Pos(x,y,z) * shape       → translate
  Rot(X=45) * shape        → rotate
  edge @ t  → Vector at t∈[0,1]
  edge % t  → tangent at t∈[0,1]

━━━ SELECTORS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  part.edges()  .faces()  .vertices()  .solids()
  .filter_by(Axis.Z)            # parallel to Z
  .filter_by(GeomType.CIRCLE)   # circles only
  .filter_by(lambda e: e.length > 5)
  .sort_by(Axis.Z)[-1]          # topmost
  .sort_by(SortBy.RADIUS)[0]    # smallest radius
  .group_by(Axis.Z)[-1]         # highest group
  part.edges(Select.LAST)       # from last operation
  after - before                # new edges only

━━━ LOCATIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Pos(x, y, z)  Pos(X=10)
  Rot(x, y, z)  Rot(Z=90)
  GridLocations(dx, dy, nx, ny)
  PolarLocations(r, n, start=0, range=360)
  HexLocations(apothem, nx, ny)
  CurveLocations(curve, count)

━━━ EXPORT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  export_step(part, "out.step")
  export_stl(part, "out.stl", tolerance=0.01)
  export_gltf(part, "out.gltf")
  export_svg(part, "out.svg")
  export_brep(part, "out.brep")
  import_step("model.step")
  import_svg("drawing.svg")

━━━ KEY ENUMS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Mode:    ADD SUBTRACT INTERSECT REPLACE PRIVATE
  Align:   MIN CENTER MAX
  GeomType: LINE CIRCLE ELLIPSE CYLINDER PLANE TORUS ...
  SortBy:  LENGTH RADIUS AREA VOLUME DISTANCE
  Select:  ALL LAST
  Until:   FIRST LAST NEXT
  Keep:    TOP BOTTOM BOTH
"""

if __name__ == "__main__":
    print(CHEATSHEET)
