# How fast can an infection spread?

![R0 vs serial interval](../../figures/epidemics.png)

Two numbers set how fast an outbreak grows:
- **R₀**, the number of people one case infects in a population with no immunity.
- **The serial interval**, the time between one case and the next.

Cases multiply by R₀ every serial interval, so the doubling time is t_d = T·ln 2/ln R₀.

**The threshold (blue).** When R₀ < 1, each generation is smaller than the last and outbreaks fizzle out. MERS sits there: dangerous for each patient, but unable to sustain human-to-human spread. This is a mathematical threshold (Kermack & McKendrick 1927), not a physical law, so it is shaded but not "forbidden".

**Doubling curves.** Diseases above the dotted amber curve double in under two days. Measles has the highest R₀ of any common infection (12–18), but its 12-day serial interval slows it. Pandemic influenza and COVID-19 grew fast because their serial intervals were short.

The curves ignore immunity, behaviour change and interventions, which is why real epidemics bend over.
