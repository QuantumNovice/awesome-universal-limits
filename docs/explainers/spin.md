# How fast can things spin?

![Spin rate vs size](../../figures/spin.png)

Every chart in this repo has three layers. Here is what they mean for spin.

## 1. Hard bounds (red and blue, shaded)

**Faster than light (red).** A spinning object's rim moves at speed π·d·f. That speed cannot reach c, so the spin rate must stay below f = c/(πd). A 1 m wheel would have to turn about 95 million times a second to hit this line.

**Below one quantum (blue, solid).** Angular momentum comes in units of ħ. The slowest nonzero spin happens when the object is as heavy as possible for its size (we use osmium, the densest element, with the mass at the rim): f = 12ħ/(π²ρd⁵). This line only matters for molecules. A hydrogen molecule in its first rotational state sits right next to it.

**Slower than the universe is old (blue, dashed).** One turn in 13.8 billion years is 2.3×10⁻¹⁸ Hz. Nothing stops something from spinning slower, but nobody could ever see it complete a turn. **This is an observability floor, not a law of physics.** That is why it is dashed.

## 2. Practical limits (thin lines)

**Material strength (dotted amber).** A rim tears apart once its speed passes roughly √(σ/ρ), about 3 km/s for the strongest bulk materials. Drills, centrifuges and the laser-spun nanoparticle all stop near this line.

**Self-gravity (dashed grey).** Anything held together by its own gravity flies apart when the spin at its equator beats gravity. That depends only on density, so the line is flat: about one turn per 2.3 hours for rock. Rubble-pile asteroids pile up right at this "spin barrier".

## 3. Real objects

Each marker is a real object. The solid bar runs from the slowest known member of its class to the fastest. The dotted bar continues up to that class's own breakup limit, marked with a black cap. Black holes have a cap of their own: a maximally spinning hole's horizon moves at exactly light speed, so their caps touch the red line. Pink curves are orbits, from Mercury to Neptune, the last orbits of the GW150914 black-hole merger, and the Milky Way's rotation.

Data: [`data/spin.csv`](../../data/spin.csv), [`data/spin_orbits.csv`](../../data/spin_orbits.csv). Formulas: [`src/allowed_universe/limits.py`](../../src/allowed_universe/limits.py).
