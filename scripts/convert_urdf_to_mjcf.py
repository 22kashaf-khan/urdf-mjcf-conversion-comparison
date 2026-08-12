"""
convert_urdf_to_mjcf.py

Load the hand-written URDF and save MuJoCo's compiled interpretation
of it as MJCF, so the conversion can be inspected directly.
"""

import mujoco

URDF_PATH = "../models/simple_leg.urdf"
OUTPUT_PATH = "../models/converted_from_urdf.xml"


def main():
    model = mujoco.MjModel.from_xml_path(URDF_PATH)
    mujoco.mj_saveLastXML(OUTPUT_PATH, model)
    print(f"Converted {URDF_PATH} -> {OUTPUT_PATH}")
    print()
    print(f"nbody: {model.nbody}, njnt: {model.njnt}, ngeom: {model.ngeom}, nv: {model.nv}")
    print()
    with open(OUTPUT_PATH) as f:
        print(f.read())


if __name__ == "__main__":
    main()