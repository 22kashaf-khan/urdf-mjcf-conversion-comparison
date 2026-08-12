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

## Project structure
