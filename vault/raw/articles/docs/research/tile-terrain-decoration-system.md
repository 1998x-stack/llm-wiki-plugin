---
summary: "Reference documentation of the old SCE engine decoration proxy system for TileSetConverter migration"
last_updated: "2026-03-04"
---

# TileTerrain Decoration System (Old Engine)

This document describes the decoration proxy system from the old SCE engine's tile editor,
used as reference for the UrhoX TileSetConverter migration.

Source: `Editor/src/TileEditorModule/TilePool.h/cpp`, `DecorationProxyArchetype.h/cpp`, `Tile.cpp`

---

## Overview

Each tile prefab can define multiple **decoration proxy slots**. At runtime, the tile system
checks each slot's conditions against the actual terrain state (land/water at each corner),
and if conditions match, instantiates a random decoration from the referenced group.

---

## DecorationProxy Data Structure

In old engine .prefab files, decoration proxies are stored as archetype objects with `type = "decorationProxy"`:

```json
{
  "type": "decorationProxy",
  "position": { "x": 0.0, "y": 0.0, "z": 0.0 },
  "rotation": { "w_": 1.0, "x_": 0.0, "y_": 0.0, "z_": 0.0 },
  "scale": { "x": 1.0, "y": 1.0, "z": 1.0 },
  "slotName": "TreeSlot_01",
  "groupName": "deco.decal.decal_dg_big_b",
  "conditional": 1,
  "condition": {
    "bottomLeft": 0,
    "bottomRight": 0,
    "topLeft": 2,
    "topRight": 2
  },
  "uuid": "a1b2c3d4-..."
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `position/rotation/scale` | Transform | Where to place the decoration relative to tile origin |
| `slotName` | String | Display name for the slot (editor UI) |
| `groupName` | String | Decoration group reference (dot-separated path) |
| `conditional` | int (0/1) | Whether condition checking is enabled |
| `condition` | Object | Per-corner terrain type requirements |
| `uuid` | String | Unique identifier for this proxy slot |

---

## Condition Values (TileGrid enum)

The `condition` object has four corners, each with an integer value:

| Value | Name | Meaning |
|-------|------|---------|
| **0** | `TG_Land` | This corner must be **land/terrain** |
| **1** | `TG_Water` | This corner must be **water** |
| **2** | `TG_NotCare` | This corner can be **anything** (wildcard) |

Corner layout:

```
topLeft (TL)      topRight (TR)
    O-----------------O
    |                 |
    |     Tile        |
    |                 |
    O-----------------O
bottomLeft (BL)   bottomRight (BR)
```

### Conditional Flag

- `conditional = 1` (true): Check all four corner conditions against actual tile vertex marks. If ANY corner doesn't match, the decoration is NOT placed.
- `conditional = 0` (false): The decoration is placed **unconditionally** (conditions ignored).

### Rotation Adjustment

When a tile is rotated (0°/90°/180°/270°), the condition corners are rotated accordingly:

```cpp
condition[(cornerIndex + rotationMark + 4) % 4]
```

This ensures decorations with asymmetric conditions (e.g., "land on bottom, water on top") work correctly regardless of tile orientation.

---

## GroupName Construction

The `groupName` is derived from the decoration prefab's directory path relative to `Res/`:

```
Directory path:  deco/decal/decal_dg_big_b/model.prefab
                 ↓ strip filename, keep directory
                 deco/decal/decal_dg_big_b
                 ↓ replace '/' with '.'
groupName:       deco.decal.decal_dg_big_b
```

Logic from `TilePool.cpp`:
```cpp
String GetGroupName(const String& path)
{
    auto pos = path.FindLast("/");
    String groupName = path.Substring(0, pos);  // strip filename
    groupName.Replace('/', '.');                 // dots instead of slashes
    return groupName;
}
```

### Examples

| Prefab Path | groupName |
|-------------|-----------|
| `deco/decal/decal_dg_big_b/model.prefab` | `deco.decal.decal_dg_big_b` |
| `deco/Tiles/me_basemesh_hope/cracks/xxx/model.prefab` | `deco.Tiles.me_basemesh_hope.cracks.xxx` |

---

## Decoration Group Lookup

At runtime, decoration groups are populated from all non-tile prefabs in the resource tree:

1. **Loading**: Each .prefab file in `deco/` (and other non-tile directories) is scanned.
2. **Grouping**: Prefabs are grouped by their `groupName` (derived from directory path).
3. **Selection**: `RandomTileByGroup(groupName)` picks a random prefab from the group, weighted by `selectionRate` (from `basicInfo` archetype).

```
group_["deco.decal.decal_dg_big_b"] = [
    { path: "deco/decal/decal_dg_big_b/model.prefab", weight: 1.0 },
    { path: "deco/decal/decal_dg_big_b/model2.prefab", weight: 0.5 },
    ...
]
```

---

## Runtime Decoration Placement (Tile::Adjust)

When a tile is placed or its surroundings change:

1. **Get vertex marks**: Determine land/water status at each of the tile's 4 corners.
2. **For each decorationProxy in the tile prefab**:
   a. If `conditional == false`: always match.
   b. If `conditional == true`: check each corner condition (accounting for tile rotation):
      - `TG_NotCare (2)`: skip (always ok)
      - `TG_Land (0)`: actual vertex must be land
      - `TG_Water (1)`: actual vertex must be water
      - If ANY corner fails → skip this proxy
   c. If matched:
      - `pool->RandomTileByGroup(groupName)` → pick a random decoration prefab
      - Create a `ProxyDecoration` node as child of the tile
      - Apply proxy's position/rotation/scale transform
   d. If previously matched but now doesn't: remove the decoration node.
3. **User removal tracking**: If user manually removed a proxy decoration (tracked by UUID), it won't be re-added even if conditions match again.

---

## Relationship to Decal Directories

In the TileSet input directory (e.g., `tiles/me_tiles_field/`):

| Directory | Purpose |
|-----------|---------|
| `decal/` | Main decoration prefabs (grouped by subdirectory: A, B, C, ...) |
| `decal_path/` | Path-specific decorations |
| `decal_path_2/` | Additional path decorations |

These directories contain decoration prefabs that are referenced by `groupName` in tile prefabs.
However, note that `groupName` references `deco/...` paths (global resource paths), not the
local `decal/` directories within the TileSet. The `decal/` directories within a TileSet are
a local convenience — the actual decoration prefabs live under `Res/deco/`.

---

## Mapping to UrhoX TileSet Format

### Old → New Condition Mapping

| Old Value | Old Name | New Value |
|-----------|----------|-----------|
| 0 | `TG_Land` | `"land"` |
| 1 | `TG_Water` | `"water"` |
| 2 | `TG_NotCare` | `"any"` |

### Old → New Structure Mapping

Old `decorationProxy` → New `DecoSlot`:

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `groupName` | `DecoSlot.group` | Dot-separated → keep as-is for lookup |
| `condition.bottomLeft` | `DecoCondition.marks[0]` (BL) | 0→"land", 1→"water", 2→"any" |
| `condition.bottomRight` | `DecoCondition.marks[1]` (BR) | Same mapping |
| `condition.topRight` | `DecoCondition.marks[2]` (TR) | Same mapping |
| `condition.topLeft` | `DecoCondition.marks[3]` (TL) | Same mapping |
| `position` | `DecoSlot.position` | Convert Z-up cm → Y-up meters |
| `rotation` | `DecoSlot.rotation` | Convert coordinate system |
| `scale` | `DecoSlot.scale` | Direct copy |

When `conditional == 0`, set all four marks to `"any"` (unconditional placement).

### GroupName in New Format

The `DecoSlot.group` field stores the `groupName` as-is (dot-separated).
The `decorationGroups` in the TileSet JSON must use matching keys.

Currently `BuildDecorationGroups` generates keys like `"decal_A"` from local directories,
but these should instead match the `groupName` format used by decoration proxies.

---

## Statistics (me_tiles_field)

- **948 decorationProxy entries** across **326 prefab files**
- Decoration groups from `decal/`, `decal_path/`, `decal_path_2/` directories
- groupNames reference `deco/...` paths from the global `Res/` resource tree

---

*Last updated: 2026-03-04*
