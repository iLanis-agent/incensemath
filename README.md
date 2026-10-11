# Incense math

How long a stick really burns, how many a room takes, and what the weekly ritual costs in packs a year. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/incensemath/

## The three tools

- **Burn plan** - `burnPlan(lengthCm, minPerCm, packCount)`: minutes per stick and hours per pack.
- **Room plan** - `roomPlan(roomM2, m2PerStick, packSize)`: sticks per session and sessions per pack.
- **Year plan** - `yearPlan(sessionsWeek, sticksEach, packPrice, packSize)`: sticks, packs and cost per year.

## Labeled norms (illustrative references, not rules)

- Burn rate: 2 minutes per centimeter. Stick: 21 cm. Coverage: one stick scents about 15 m². Pack: 20 sticks. Your sticks, rooms and ritual decide the real numbers.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (47 cases, 133 checks)

Regenerate the oracle expectations: `python3 oracle.py`
