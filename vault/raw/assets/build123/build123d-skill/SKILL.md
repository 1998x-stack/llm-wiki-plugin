---
name: build123d
description: >
  Expert build123d Python CAD programming skill. Triggers when users want to:
  create 3D/2D CAD models in Python, write build123d scripts, design parametric
  parts for 3D printing / CNC / laser cutting, use BREP modeling with OpenCascade,
  convert CadQuery workflows to build123d, work with topology selectors (filter_by,
  sort_by, group_by), use Builder Mode (BuildPart/BuildSketch/BuildLine) or Algebra
  Mode, perform boolean operations, extrude/revolve/loft/sweep shapes, create
  assemblies and joints, export STEP/STL/SVG files, or debug build123d errors.
  Also trigger for: "CAD as code", "parametric 3D model", "OpenCascade Python",
  "BREP modeling", "build123d how do I...", "ocp_vscode viewer setup",
  "fillet/chamfer edges", or any mention of build123d objects (Box, Cylinder,
  Sketch, Part, Face, Edge, etc.).
---

# build123d Expert Skill

build123d is a Python BREP CAD library built on OpenCascade. This skill covers both
**Algebra Mode** (stateless, operator-driven) and **Builder Mode** (context-managed).

## Quick Decision: Which Mode?

| Situation | Use |
|-----------|-----|
| Functional/parametric scripts | Algebra Mode |
| Structured design history | Builder Mode |
| Mixing logic with geometry | Algebra Mode |
| Teaching / readable code | Builder Mode |

Both modes can be mixed freely.

## Setup

```python
pip install build123d
# Viewer (highly recommended):
pip install ocp-vscode

from build123d import *
from ocp_vscode import show   # optional viewer
```

---

## Core Patterns

### Algebra Mode (stateless)

```python
from build123d import *

sketch = Rectangle(100, 60)
sketch -= GridLocations(70, 40, 2, 2) * Circle(5)
part = extrude(sketch, amount=10)
part = fillet(part.edges().filter_by(Axis.Z), radius=2)
export_step(part, "output.step")
```

### Builder Mode (context)

```python
from build123d import *

with BuildPart() as bp:
    with BuildSketch():
        Rectangle(100, 60)
        with GridLocations(70, 40, 2, 2):
            Circle(5, mode=Mode.SUBTRACT)
    extrude(amount=10)
    fillet(edges().filter_by(Axis.Z), radius=2)

result = bp.part
```

---

## Key Concepts to Apply

### 1. Topology Selectors (Most Important Pattern)

```python
# Chain selectors fluently
part.edges().filter_by(Axis.Z)                         # Z-parallel edges
part.edges().filter_by(GeomType.CIRCLE)                # circular edges
part.edges().filter_by(lambda e: e.length > 5)         # custom filter
part.faces().sort_by(Axis.Z)[-1]                       # topmost face
part.faces().group_by(SortBy.AREA)[-1]                 # largest area group
part.edges(Select.LAST)                                 # edges from last op

# Diff to find new edges
before = part.edges()
part -= Hole(radius=3)
new_edges = part.edges() - before
```

### 2. Location & Positioning

```python
Pos(10, 0, 5) * Circle(3)         # translate
Rot(Z=90) * Rectangle(10, 5)      # rotate
Plane.XZ * Rectangle(10, 5)       # on XZ plane
Plane(face) * Circle(3)           # on a face's plane
GridLocations(10, 8, 3, 2)        # grid pattern
PolarLocations(radius=20, count=6) # polar pattern
```

### 3. Curve Parameter Operators

```python
line = Line((0,0), (10,5))
pt = line @ 0.5    # midpoint Vector
t  = line % 0.0    # start tangent Vector
arc = JernArc(line @ 1, line % 1, radius=3, arc_size=90)
```

### 4. Boolean Operations

```python
# Algebra Mode
result = part1 + part2    # union
result = part1 - part2    # difference  
result = part1 & part2    # intersection

# Builder Mode (via mode=)
Circle(5, mode=Mode.ADD)
Circle(3, mode=Mode.SUBTRACT)
Circle(2, mode=Mode.INTERSECT)
```

### 5. Common 3D Operations

```python
extrude(sketch, amount=10)                    # basic extrude
extrude(sketch, amount=10, taper=5)          # tapered
extrude(sketch, amount=10, both=True)        # bidirectional
revolve(sketch, axis=Axis.Z, angle=360)      # revolve
loft([sketch1, sketch2, sketch3])            # loft sections
sweep(profile, path)                          # sweep
fillet(part.edges(), radius=1)               # round edges
chamfer(part.edges(), length=0.5)            # bevel edges
offset(solid, amount=-2, openings=[face])    # shell/hollow
```

---

## Reference Files

For comprehensive details, read the appropriate reference file:

- **`references/topology.md`** — Full Shape class API, ShapeList methods, Mixin1D/3D
- **`references/objects.md`** — All 1D/2D/3D object classes with parameters
- **`references/operations.md`** — All operation functions with signatures
- **`references/locations.md`** — Location, Pos, Rot, Plane, GridLocations, etc.
- **`references/enums.md`** — All enums: Mode, GeomType, SortBy, Align, etc.
- **`references/assembly.md`** — Compound, Joint system, anytree integration
- **`references/import_export.md`** — import_step/export_stl/export_step etc.
- **`references/tips.md`** — Best practices, performance, common pitfalls, FAQ

## Example Scripts

- **`examples/bracket.py`** — L-bracket with holes and fillets (both modes)
- **`examples/tea_cup.py`** — Complex revolve + spline + handle
- **`examples/lego_brick.py`** — Parametric Lego brick (full builder mode)
- **`examples/assembly.py`** — Multi-part assembly with joints
- **`examples/selector_demo.py`** — Selector chaining demos

---

## When to Read Reference Files

- User asks about a **specific object** (e.g., Helix, BlendCurve) → `references/objects.md`
- User asks about **selectors** → `references/topology.md`
- User needs **enums** list → `references/enums.md`
- User building **assembly** → `references/assembly.md`
- User exporting files → `references/import_export.md`
- User hitting **errors** or asking best practices → `references/tips.md`

---

## Common Mistakes to Avoid

1. **fillet/chamfer too early** — always do last, after all booleans
2. **Wrong extrude direction** — use `dir=` param or flip sign
3. **Select.LAST misuse** — only works for the immediately preceding operation
4. **Solid + Solid in v0.9+** returns ShapeList, not Compound — wrap with `Compound()`
5. **Deprecated API** (v0.8→v0.9): use `export_stl(shape, "file")` not `shape.export_stl()`
