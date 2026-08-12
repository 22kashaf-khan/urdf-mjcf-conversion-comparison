"""
compare_models.py

Compare the URDF model against the hand-written MJCF model from Project 1,
to quantify what a format conversion carries over and what it cannot.
"""

import mujoco

URDF_PATH = "../models/simple_leg.urdf"
MJCF_PATH = "C:/Projects/MuJoCo/models/simple_leg.xml"


def main():
    urdf_model = mujoco.MjModel.from_xml_path(URDF_PATH)
    mjcf_model = mujoco.MjModel.from_xml_path(MJCF_PATH)

    fields = [
        ("nbody   (bodies)", "nbody"),
        ("njnt    (joints)", "njnt"),
        ("ngeom   (geoms)", "ngeom"),
        ("nv      (DOFs)", "nv"),
        ("nu      (actuators)", "nu"),
        ("nsensor (sensors)", "nsensor"),
    ]

    print(f"{'Field':<22}| {'URDF':>5} | {'MJCF':>5}")
    print("-" * 38)
    for label, attr in fields:
        u = getattr(urdf_model, attr)
        m = getattr(mjcf_model, attr)
        print(f"{label:<22}| {u:>5} | {m:>5}")


if __name__ == "__main__":
    main()