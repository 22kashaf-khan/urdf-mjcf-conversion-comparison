# URDF → MJCF Conversion & Format Comparison

A hand-built robot leg, written independently in both URDF and MJCF, used
to quantify exactly what a format conversion carries over and what it
silently loses — rather than assuming a converted file is equivalent to
the original.

## What this project demonstrates

- Hand-authored URDF (links, joints, inertial/visual/collision blocks)
  from scratch, not copied from an existing robot
- MuJoCo's native URDF import, and its automatic conversion to MJCF
- A structured, evidence-based comparison of what survives conversion
  and what doesn't
- Real findings about format-specific defaults that silently change
  model behavior

## The core question

URDF and MJCF can both describe a robot, but they aren't equivalent
formats — one is a strict subset of the other. Rather than assume this,
this project tests it directly: the same leg, written by hand in both
formats, then compared field by field.

## What survives conversion perfectly

| Field | URDF | MJCF |
|---|---|---|
| Joints (`njnt`) | 2 | 2 |
| Degrees of freedom (`nv`) | 2 | 2 |

The kinematic chain — joint count, degrees of freedom, structure —
converts exactly. URDF's flat link/joint list gets correctly rebuilt into
MJCF's nested body tree.

## What doesn't survive

| Field | URDF | MJCF |
|---|---|---|
| Bodies (`nbody`) | 3 | 5 |
| Geoms (`ngeom`) | 3 | 5 |
| Actuators (`nu`) | **0** | 2 |
| Sensors (`nsensor`) | **0** | 3 |

**Actuators and sensors have no URDF representation at all.** URDF
describes a robot's physical structure — mass, joints, geometry — but has
no syntax for control (position/velocity/torque actuators) or sensing
(touch, joint position, joint velocity). Converting MJCF → URDF would
silently discard all of it.

The body and geom count differences trace to two further findings:

- **A link with no joint connecting it to the world gets welded into the
  world body and loses its identity.** The hand-authored `base_link` in
  the URDF disappears entirely in the converted output — no name, no
  separate body, just a bare geom.
- **`discardvisual` defaults differently by format.** URDF import
  discards visual-only geoms by default; MJCF does not. The same file,
  loaded as URDF vs. MJCF, produces different geometry counts for this
  reason alone.

## Other format-specific traps found

- **URDF is radians-only. MJCF's angle units depend on a compiler
  setting** you choose (`angle="degree"` or `angle="radian"`). Copying a
  joint range between the two formats without accounting for this is an
  easy, silent ~57x error.
- **Cylinder length is stored as half-length internally** in MJCF — a
  URDF `length="0.5"` becomes `size="0.05 0.25"` after conversion, which
  looks like a bug if you don't know the convention.
- **URDF's `effort` limit becomes `actuatorfrcrange`** in the converted
  MJCF — a symmetric force range generated from a single input number.
  `velocity` limits have no MJCF equivalent and are dropped entirely.

## The practical conclusion

The skeleton (joints, DOF, kinematic structure) survives conversion
cleanly. The simulation setup (actuators, sensors, contact tuning) does
not — it only exists in MJCF, and has to be added after conversion, not
assumed to carry over. This is the basis for treating URDF as a robot's
canonical source description, and MJCF as a build artifact you configure
on top of it for a specific simulator — not two interchangeable files.
