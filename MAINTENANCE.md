# MNik-EV profile and live lab

The profile README and interactive GitHub Pages site share one visual identity.
The cover is a capture of the same Three.js motor that visitors can control in
the lab. The former vector car has been removed. The Persian Gazelle card states
the owner's previous role without depicting an invented team vehicle.

## Existing components

- Three.js 0.186.1, OrbitControls and RoomEnvironment: locally vendored, with MIT
  license. RoomEnvironment is converted to a PMREM environment for PBR materials.
- Platane/snk through `generate-snake-animation` 3.5.0: the actual GitHub
  contribution calendar, animated as a snake. `npm ci && npm run refresh`.
- Lucide Static 1.50.0: project icons; ISC license in `docs/vendor/lucide/`.
- Space Grotesk and JetBrains Mono: local fonts, with OFL licenses.
- Skill Icons: the language/tool strip, from
  https://skillicons.dev/icons?i=c,cpp,python,arduino,raspberrypi,git,linux&theme=dark.
- The PCB image is the original isometric render from the owner's
  [Robot Shield repository](https://github.com/MNik-EV/Robot-Shield-ATmega328).

The motor geometry, experiment logic, typography/layouts and small SVG cards
are project code. Image generation was attempted but returned network errors;
no generated image is included.

## Build and preview

```sh
python scripts/build_profile_assets.py
python -m http.server 8766 --bind 127.0.0.1
```

Open `http://127.0.0.1:8766/docs/` for the live lab.

To regenerate the animated covers, install Playwright and ffmpeg, keep that
server running, then use `python scripts/capture_art.py --browser PATH_TO_CHROMIUM`.
The capture script writes its temporary frames to ignored `.preview/` directories.
The README selects mobile and reduced-motion variants through `<picture>`.

GitHub Pages serves `/docs` from `main`, with `.nojekyll`. All fonts, scripts and
site images are local; the live lab makes no API calls and has no trackers or keys.

## Activity refresh

Run `npm ci` and `npm run refresh`. Locally the script obtains the existing GitHub
CLI token in memory; in Actions it uses `GITHUB_TOKEN`. Credentials are never
written to the output. The published JSON records the snapshot timestamp.
The prepared daily workflow is in `automation/update-activity.yml`; it is only
active once installed as `.github/workflows/update-activity.yml` with GitHub's
required `workflow` scope. The profile does not claim it is live or scheduled.

## Model boundaries

- The motor is an illustrative 12-slot / 8-pole model. Visual rotation is slowed
  60 times. The three phase signals are ideal sinusoids, not measured currents or
  an implemented FOC simulation. Speed follows a simple first-order response.
- Passive balancing only decreases higher cell voltages. It is an accelerated
  visual explanation, not an electrochemical battery model.
- DC UPS transfer is idealized. A 24 V, 8 Ah model supplies the selected load at
  90% conversion efficiency, with discharge time accelerated 600 times. Charging
  is not simulated; the reset button restores the battery state.
- Sound is off until explicitly enabled. Reduced motion pauses motor rotation
  and disables CSS animations; users can explicitly resume it.
- WebGL failure leaves a 2D fallback and the controls available.
