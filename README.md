# Casper Excalibur G770 — Dolby Audio Profiles for EasyEffects

Dolby Audio profiles converted from the official Windows driver for use with EasyEffects on Linux.

## Profiles
- **Dolby-Music** — Best for everyday listening
- **Dolby-Movie** — Enhanced surround for films
- **Dolby-Dynamic** — Adaptive for mixed content
- **Dolby-Game** — Optimized for gaming
- **Dolby-Voice** — Clear dialog enhancement

## Installation

1. Install [EasyEffects](https://flathub.org/apps/com.github.wwmm.easyeffects) via Flatpak
2. Copy `.json` files to `~/.local/share/easyeffects/output/`
3. Open EasyEffects → Output → Presets → select a profile

## Hardware
- **Device:** Casper Excalibur G770
- **Audio Codec:** Realtek ALC255 (Subsystem: 152D:1295)
- **Source:** Official Casper Windows driver (DAX3 XML)

## Conversion
Profiles were extracted from the DAX3 XML using `dolby_casper_convert.py` included in this repo.

If you have a different Casper model with a similar DAX3 XML, you can run:
```bash
python3 dolby_casper_convert.py path/to/DEV_XXXX.xml
```

## Tested On
- Bazzite (Fedora-based, immutable)
- EasyEffects 8.x (Flatpak)

## Contributing
If you test this on another Casper model, open an issue with your results!
