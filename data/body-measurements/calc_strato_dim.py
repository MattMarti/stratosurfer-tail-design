import re

import yaml
import numpy as np
from scipy.spatial.transform import Rotation

IN_2_MM = 25.4
CENTER_OF_GRAVITY_OFFSET = 67.5

def extract_scales_angles(measurements:dict):
    ruler_0_mark = measurements[0]
    scales = []
    angles = []
    for key, ruler_mark in measurements.items():
        if key == 0:
            continue
        length_cm = key
        vector = ruler_mark - ruler_0_mark
        length_px = np.linalg.norm(vector)
        px2unit = length_cm / length_px
        scales.append(px2unit)
        angle = np.rad2deg(np.arctan2(vector[1], vector[0]))
        if angle < 0: angle += 360
        angles.append(angle)
        print(f"key {key}, vector {vector}: {angle:.3f} deg")
    return scales, angles


def get_scale(data):
    ruler_cm_measurements = {}
    ruler_in_measurements = {}
    for k, v in data.items():
        regexp_match = re.compile(r"ruler \d+").match(k)
        if regexp_match is None:
            continue
        ruler_value = int(regexp_match[0].split()[-1])
        if re.compile(r"ruler \d+ cm").search(k) is not None:
            ruler_cm_measurements[ruler_value] = v
        if re.compile(r"ruler \d+ in").search(k) is not None:
            ruler_in_measurements[ruler_value] = v

    scales_px_cm, angles_cm = extract_scales_angles(ruler_cm_measurements)
    scales_px_in, angles_in = extract_scales_angles(ruler_in_measurements)

    scales_px_cm_mm = [10.0 * s for s in scales_px_cm]
    scales_px_in_mm = [IN_2_MM * s for s in scales_px_in]
    scales = [*scales_px_cm_mm, *scales_px_in_mm]

    scale_px_mm = np.mean(scales)
    scale_res = 100 * (np.array(scales) - scale_px_mm) / scale_px_mm

    angles_cm = [a for a in angles_cm]
    angles_in = [180 - a for a in angles_in]
    angles = [*angles_cm, *angles_in]

    angle = np.sum(np.array(angles) * np.array(scales)) / np.sum(scales)
    angle_res = np.array(angles) - angle

    print("--- Get px to mm scale ---")
    print(f"Scale px to mm: {scale_px_mm:.4f}")
    print(f"Residuals (%): {scale_res}")
    print(f"Ruler orientation: {np.mean(angles):.4f} deg")
    print(f"Residuals (deg): {angle_res}")

    return scale_px_mm, angle


def get_wing_le_position(data, scale_px_mm):
    return data["wing leading edge"] * scale_px_mm


def get_wing_te_position(data, scale_px_mm):
    top_pos_px = data["wing trailing edge top"]
    bot_pos_px = data["wing trailing edge bottom"]

    te_vector_px = top_pos_px - bot_pos_px
    te_unit_vector = te_vector_px / np.linalg.norm(te_vector_px)

    return bot_pos_px * scale_px_mm + te_unit_vector


def get_deck_orientation(data):
    deck_le = data["deck leading edge"]
    deck_te = data["deck trailing edge"]

    vector = deck_le - deck_te
    angle_global = np.rad2deg(np.arctan2(vector[1], vector[0]))
    if angle_global < 0: angle_global += 360
    pitch = 180 - angle_global

    return pitch


def get_chord_orientation(data, scale_px_mm):
    wing_le_mm = get_wing_le_position(data, scale_px_mm)
    wing_te_mm = get_wing_te_position(data, scale_px_mm)

    vector = wing_le_mm - wing_te_mm
    angle_global = np.rad2deg(np.arctan2(vector[1], vector[0]))
    if angle_global < 0: angle_global += 360
    pitch = 180 - angle_global

    return pitch


def get_design_positions(data, scale_px_mm, deck_pitch, design_aoa):
    print(" ")

    nose = scale_px_mm * data["nose"]
    wing_le_pic = scale_px_mm * data["wing leading edge"]
    tail_cr_pic = scale_px_mm * data["tail spike crux"]
    tail_st_pic = scale_px_mm * data["tail spike tip"]
    deck_le_pic = scale_px_mm * data["deck leading edge"]
    deck_te_pic = scale_px_mm * data["deck trailing edge"]
    gnss_le_pic = scale_px_mm * data["gnss leading screw"]
    gnss_te_pic = scale_px_mm * data["gnss trailing screw"]

    ref = deck_le_pic

    deck_vector = deck_te_pic - deck_le_pic
    orientation = np.arctan2(deck_vector[1], deck_vector[0])
    r = Rotation.from_euler('z', -orientation).as_matrix()[0:2, 0:2]

    deck_te = r @ (deck_te_pic - ref)
    wing_le = r @ (wing_le_pic - ref)
    tail_cr = r @ (tail_cr_pic - ref)
    tail_st = r @ (tail_st_pic - ref)
    gnss_le = r @ (gnss_le_pic - ref)
    gnss_te = r @ (gnss_te_pic - ref)

    gnss = gnss_le + 0.5 * (gnss_te - gnss_le)

    cog = np.zeros((2,))
    cog[0] = wing_le[0] + CENTER_OF_GRAVITY_OFFSET
    cog[1] = np.NaN # Can't tell where it is in y, we'll figure that out later

    with np.printoptions(precision=2, suppress=True):
        print(f"Deck trailing edge  {deck_te}")
        print(f"Wing leading edge   {wing_le}")
        print(f"Tail crux           {tail_cr}")
        print(f"Tail spike tip      {tail_st}")
        print(f"Center of Gravity:  {cog}")
        print(f"GNSS position:      {gnss}")
        print(" ")


def preprocess_data(data):
    for key, points in data.items():
        converted_points = []
        for p in points:
            p = [float(s) for s in p.split(",")]
            p[1] = -p[1]
            converted_points.append(p)
        converted_points = np.array(converted_points)
        data[key] = np.mean(converted_points, 0)
    return data


def load_data(path):
    with open(path, 'r') as fid:
        for line in fid:
            if line.strip() == "--- YAML ---":
                break
        raw_data = yaml.safe_load(fid)
    return preprocess_data(raw_data)


def main():
    fname = "strato-body-measurements.txt"
    data = load_data(fname)
    
    scale_px_mm, ruler_angle_deg = get_scale(data)

    deck_pitch = get_deck_orientation(data)
    print(f"Deck pitch: {deck_pitch:.3f}")
    chord_pitch = get_chord_orientation(data, scale_px_mm)
    print(f"Chord pitch: {chord_pitch:.3f}")

    design_aoa = chord_pitch - deck_pitch
    print(f"\nDesign AoA: {design_aoa:.6f}")
    
    get_design_positions(data, scale_px_mm, deck_pitch, design_aoa)


if __name__ == "__main__":
    main()
