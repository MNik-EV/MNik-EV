# Profile artwork

The profile uses original SVG artwork stored in this repository. The rotating
motor and three-phase waveforms are decorative illustrations, not live data.
The vehicle is a conceptual solar car, not a technical drawing of a particular
Persian Gazelle generation.

The assets need no external image service, fonts, tracking pixels, JavaScript,
GitHub Actions, or API keys. They keep a complete static composition when motion
is disabled and respect `prefers-reduced-motion`.

Regenerate the SVG files with Python 3:

```sh
python scripts/build_assets.py
```

`README.md` contains the editable profile copy and project links. Its `<picture>`
element selects the taller hero on narrow screens. Project descriptions refer to
the linked public repositories; BMS and DC UPS are presented as areas of focus.
