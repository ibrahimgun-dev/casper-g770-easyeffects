#!/usr/bin/env python3
"""
Casper Excalibur G770 — Dolby DAX3 XML → EasyEffects JSON
Converts tuning-vlldp audio-optimizer-bands to parametric EQ preset.
"""

import xml.etree.ElementTree as ET
import json
import sys
import os

# Frequencies at 48000 Hz (from XML band_20_freq)
FREQS_48K = [47,141,234,328,469,656,844,1031,1313,1688,2250,3000,3750,4688,5813,7125,9000,11250,13875,19688]

# Dolby unit → dB conversion (192 units = 12 dB)
SCALE = 12.0 / 192.0

def parse_gains(value_str):
    return [int(v) for v in value_str.split(',')]

def gains_to_db(gains):
    return [round(g * SCALE, 2) for g in gains]

def build_eq_bands(gains_db, freqs):
    bands = {}
    for i, (freq, gain) in enumerate(zip(freqs, gains_db)):
        bands[f"band{i}"] = {
            "frequency": float(freq),
            "gain": gain,
            "mode": "APO (DR)",
            "mute": False,
            "q": 1.41,
            "slope": "x1",
            "solo": False,
            "type": "Bell"
        }
    return bands

def convert_profile(xml_path, profile_name, output_dir):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    endpoint = root.find(".//endpoint[@type='internal_speaker']")
    if endpoint is None:
        print("ERROR: internal_speaker endpoint not found")
        return False

    profile = endpoint.find(f".//profile[@type='{profile_name}']")
    if profile is None:
        print(f"ERROR: profile '{profile_name}' not found")
        return False

    vlldp = profile.find("tuning-vlldp")
    if vlldp is None:
        print(f"ERROR: tuning-vlldp not found in '{profile_name}'")
        return False

    aob = vlldp.find("audio-optimizer-bands")
    if aob is None:
        print(f"ERROR: audio-optimizer-bands not found")
        return False

    gain_l_el = aob.find("gain_l")
    gain_r_el = aob.find("gain_r")

    if gain_l_el is None or gain_r_el is None:
        print("ERROR: gain_l or gain_r not found")
        return False

    gains_l = gains_to_db(parse_gains(gain_l_el.get("value")))
    gains_r = gains_to_db(parse_gains(gain_r_el.get("value")))

    bands_l = build_eq_bands(gains_l, FREQS_48K)
    bands_r = build_eq_bands(gains_r, FREQS_48K)

    preset = {
        "output": {
            "blocklist": [],
            "plugins_order": ["equalizer#0"],
            "equalizer#0": {
                "balance": 0.0,
                "bypass": False,
                "input-gain": 0.0,
                "output-gain": 0.0,
                "mode": "IIR",
                "num-bands": len(FREQS_48K),
                "split-channels": True,
                "left": bands_l,
                "right": bands_r
            }
        }
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"Dolby-{profile_name.capitalize()}.json")
    with open(out_path, "w") as f:
        json.dump(preset, f, indent=2)

    print(f"✅ Saved: {out_path}")
    return True

if __name__ == "__main__":
    xml_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not xml_path:
        print("Usage: python3 dolby_casper_convert.py <path/to/DEV_0255.xml>")
        sys.exit(1)

    output_dir = os.path.expanduser("~/.local/share/easyeffects/output/")
    profiles = ["dynamic", "movie", "music", "game", "voice"]

    print(f"Converting {len(profiles)} profiles → {output_dir}\n")
    for p in profiles:
        convert_profile(xml_path, p, output_dir)

    print("\nDone! Open EasyEffects → Output → Presets to select.")
