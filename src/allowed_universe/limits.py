"""Every limit line in the repo, as a pure function.

Sizes ``d`` are diameters in metres. All functions accept floats or numpy arrays.
Each function's docstring gives the formula; ``tests/test_limits.py`` checks it
against a hand-computed value.
"""

from __future__ import annotations

import math

import numpy as np

from allowed_universe import constants as k

# =============================================================================
# Chart 1: spin rate (Hz) vs size
# =============================================================================


def spin_light(d):
    """Rim at light speed: f_max = c / (pi d)."""
    return k.c / (np.pi * np.asarray(d, dtype=float))


def spin_quantum(d, rho=k.RHO_OSMIUM):
    """One quantum of spin, mass at the rim: f_min = 12 hbar / (pi^2 rho d^5)."""
    return 12 * k.hbar / (np.pi**2 * rho * np.asarray(d, dtype=float) ** 5)


def spin_age():
    """One turn in the age of the universe: f = 1 / t0 (an observability floor)."""
    return 1.0 / k.T0


def spin_material(d, v_rim=k.V_RIM_MATERIAL):
    """Material strength: rim speed v ~ sqrt(sigma/rho), f = v / (pi d)."""
    return v_rim / (np.pi * np.asarray(d, dtype=float))


def spin_gravity(rho=k.RHO_ROCK):
    """Self-gravity breakup: f = (1/2pi) sqrt(4 pi G rho / 3)."""
    return math.sqrt(4 * math.pi * k.G * rho / 3) / (2 * math.pi)


def spin_black_hole_max(mass_kg):
    """Horizon frequency of a maximally spinning (a = 1) black hole: c^3 / (4 pi G M)."""
    return k.c**3 / (4 * np.pi * k.G * np.asarray(mass_kg, dtype=float))


def spin_black_hole(mass_kg, a):
    """Horizon frequency for spin parameter a: a c / (4 pi r+), r+ = GM/c^2 (1 + sqrt(1-a^2))."""
    r_plus = k.G * mass_kg / k.c**2 * (1 + np.sqrt(1 - a**2))
    return a * k.c / (4 * np.pi * r_plus)


def orbit_frequency(mass_kg, semi_major_m):
    """Kepler's third law: f = (1/2pi) sqrt(G M / a^3)."""
    return np.sqrt(k.G * mass_kg / np.asarray(semi_major_m, dtype=float) ** 3) / (2 * np.pi)


# =============================================================================
# Chart 2: mass (kg) vs size
# =============================================================================


def mass_black_hole(d):
    """Schwarzschild: diameter d = 2 r_s = 4 G M / c^2, so M = c^2 d / (4 G)."""
    return k.c**2 * np.asarray(d, dtype=float) / (4 * k.G)


def mass_compton(d):
    """Quantum: an object cannot be smaller than its Compton wavelength h/(Mc): M = h / (c d)."""
    return k.h / (k.c * np.asarray(d, dtype=float))


def mass_at_density(d, rho):
    """Sphere of diameter d and density rho: M = rho pi d^3 / 6."""
    return rho * np.pi * np.asarray(d, dtype=float) ** 3 / 6


# =============================================================================
# Chart 3: speed (m/s) vs size
# =============================================================================


def speed_light():
    """Nothing with mass reaches c."""
    return k.c


def speed_age(d):
    """Observability floor: moving one's own size in the age of the universe, v = d / t0."""
    return np.asarray(d, dtype=float) / k.T0


def speed_escape(mass_kg, d):
    """Surface escape speed of a body of mass M and diameter d: sqrt(4 G M / d)."""
    return np.sqrt(4 * k.G * mass_kg / np.asarray(d, dtype=float))


# =============================================================================
# Chart 4: temperature (K) vs size
# =============================================================================


def temperature_planck():
    """Planck temperature sqrt(hbar c^5 / G) / k_B ~ 1.42e32 K."""
    return k.T_planck


def temperature_collapse(d):
    """Radiation hotter than this inside a sphere of diameter d would form a black hole.

    a T^4 (pi d^3 / 6) = c^4 d / (4 G)  ->  T = (3 c^4 / (2 pi G a d^2))^(1/4).
    """
    d = np.asarray(d, dtype=float)
    return (3 * k.c**4 / (2 * np.pi * k.G * k.a_rad * d**2)) ** 0.25


def temperature_hawking(d):
    """Hawking temperature of a black hole of diameter d: T = hbar c / (2 pi k_B d)."""
    return k.hbar * k.c / (2 * np.pi * k.k_B * np.asarray(d, dtype=float))


# =============================================================================
# Chart 5: density (kg/m^3) vs size
# =============================================================================


def density_black_hole(d):
    """Mean density inside a horizon of diameter d: 3 c^2 / (2 pi G d^2)."""
    return 3 * k.c**2 / (2 * np.pi * k.G * np.asarray(d, dtype=float) ** 2)


# =============================================================================
# Chart 6: acceleration (m/s^2) vs size
# =============================================================================


def accel_rindler(d):
    """A rigid body of length d cannot accelerate faster than c^2 / d (Rindler horizon).

    The same value is the surface gravity of a black hole of diameter d (kappa = c^4 / 4GM).
    """
    return k.c**2 / np.asarray(d, dtype=float)


def accel_planck():
    """Planck acceleration sqrt(c^7 / (hbar G)) ~ 5.6e51 m/s^2."""
    return k.a_planck


def accel_age(d):
    """Observability floor: covering one's own size in the age of the universe, a = d / t0^2."""
    return np.asarray(d, dtype=float) / k.T0**2


def accel_material(d, v_rim=k.V_RIM_MATERIAL):
    """Centripetal acceleration at a rim spinning at the material limit: a = 2 v^2 / d."""
    return 2 * v_rim**2 / np.asarray(d, dtype=float)


# =============================================================================
# Chart 7: lifetime (s) vs size
# =============================================================================


def lifetime_planck():
    """Planck time sqrt(hbar G / c^5) ~ 5.4e-44 s."""
    return k.t_planck


def lifetime_age():
    """Age of the universe, t0. Longer lifetimes can be inferred but never watched."""
    return k.T0


def lifetime_light_crossing(d):
    """Light-crossing time d / c."""
    return np.asarray(d, dtype=float) / k.c


def lifetime_hawking(d):
    """Evaporation time of a black hole of diameter d: 5120 pi G^2 M^3 / (hbar c^4)."""
    m = mass_black_hole(d)
    return 5120 * np.pi * k.G**2 * m**3 / (k.hbar * k.c**4)


# =============================================================================
# Materials: tensile strength (Pa) vs density
# =============================================================================


def strength_energy_condition(rho):
    """Dominant energy condition: tension cannot exceed energy density, sigma <= rho c^2."""
    return np.asarray(rho, dtype=float) * k.c**2


def strength_for_speed(rho, v):
    """Strength whose characteristic speed sqrt(sigma/rho) equals v: sigma = rho v^2."""
    return np.asarray(rho, dtype=float) * v**2


def space_elevator_specific_strength():
    """Specific strength (J/kg) for a uniform cable from Earth's equator to geostationary orbit.

    Integral of (GM/r^2 - omega^2 r) dr from R_E to R_GEO:
    GM (1/R_E - 1/R_GEO) - omega^2 (R_GEO^2 - R_E^2) / 2.
    """
    omega = 2 * math.pi / k.SIDEREAL_DAY
    return k.GM_EARTH * (1 / k.R_EARTH - 1 / k.R_GEO) - omega**2 * (k.R_GEO**2 - k.R_EARTH**2) / 2


# =============================================================================
# Chemistry: binding energy (J) vs size
# =============================================================================


def coulomb_energy(d):
    """Electrostatic energy of two unit charges a distance d apart: e^2 / (4 pi eps0 d)."""
    return k.e**2 / (4 * np.pi * k.epsilon_0 * np.asarray(d, dtype=float))


def confinement_energy(d, mass_kg=k.m_e):
    """Ground-state energy of a particle in a box of width d: h^2 / (8 m d^2)."""
    return k.h**2 / (8 * mass_kg * np.asarray(d, dtype=float) ** 2)


def thermal_energy(temperature_k):
    """k_B T."""
    return k.k_B * temperature_k


# =============================================================================
# AI: compute-optimal training (Hoffmann et al. 2022)
# =============================================================================

CHINCHILLA_TOKENS_PER_PARAM = 20.0


def chinchilla_compute(n_params):
    """Training FLOP for a compute-optimal model: C = 6 N D with D = 20 N."""
    n = np.asarray(n_params, dtype=float)
    return 6 * n * CHINCHILLA_TOKENS_PER_PARAM * n


# =============================================================================
# Human cognition
# =============================================================================


def landauer_bit_rate(power_w, temperature_k):
    """Maximum irreversible bit erasures per second for a given power: P / (k_B T ln 2)."""
    return power_w / (k.k_B * temperature_k * math.log(2))


def reading_ceiling(hours_per_paper):
    """Papers per year one person could read with no sleep: (hours in a year) / (hours per paper)."""
    return k.YEAR / 3600 / hours_per_paper


def speed_sound_max():
    """Upper bound on the speed of sound in condensed matter (Trachenko et al. 2020):
    v = alpha sqrt(m_e / (2 m_p)) c ~ 36 km/s."""
    alpha = k.e**2 / (4 * math.pi * k.epsilon_0 * k.hbar * k.c)
    return alpha * math.sqrt(k.m_e / (2 * k.m_p)) * k.c


# =============================================================================
# Energy, power and radio
# =============================================================================


def specific_energy_mc2():
    """Mass-energy: no store can release more than c^2 joules per kilogram."""
    return k.c**2


def power_planck():
    """Planck power c^5 / G ~ 3.6e52 W: the most any system can radiate (gravitational waves included)."""
    return k.c**5 / k.G


SIGMA_THOMSON = 6.6524587321e-29  # m^2, CODATA 2018/2022


def eddington_luminosity(mass_kg):
    """Radiation pressure on electrons balances gravity on protons: 4 pi G M m_p c / sigma_T."""
    return 4 * np.pi * k.G * np.asarray(mass_kg, dtype=float) * k.m_p * k.c / SIGMA_THOMSON


def shannon_isotropic_power(distance_m, bit_rate, freq_hz=2.4e9, noise_k=290.0):
    """Transmit power for `bit_rate` at the Shannon limit (Eb/N0 = ln 2) between isotropic antennas.

    P = k_B T ln2 R (4 pi r f / c)^2 (free-space path loss, no antenna gain).
    """
    r = np.asarray(distance_m, dtype=float)
    return k.k_B * noise_k * math.log(2) * bit_rate * (4 * np.pi * r * freq_hz / k.c) ** 2


# =============================================================================
# Electromagnetism
# =============================================================================

E_SCHWINGER = k.m_e**2 * k.c**3 / (k.e * k.hbar)  # V/m, ~1.32e18
B_QUANTUM = k.m_e**2 * k.c**2 / (k.e * k.hbar)  # T, ~4.41e9
E_AIR_BREAKDOWN = 3.0e6  # V/m at sea level, cm-scale gaps
MU_0 = 1.25663706127e-6  # vacuum permeability, CODATA 2022


def charge_for_field(d, field_v_m):
    """Charge on a sphere of diameter d whose surface field is E: 4 pi eps0 (d/2)^2 E."""
    r = np.asarray(d, dtype=float) / 2
    return 4 * np.pi * k.epsilon_0 * r**2 * field_v_m


def voltage_for_field(gap_m, field_v_m):
    """Voltage across a gap at uniform field E: V = E d."""
    return np.asarray(gap_m, dtype=float) * field_v_m


def field_collapse(d):
    """Magnetic field whose energy, filling a sphere of diameter d, would form a black hole.

    B^2/(2 mu0) * pi d^3/6 = c^4 d/(4G)  ->  B = sqrt(3 mu0 / (pi G)) c^2 / d.
    """
    return math.sqrt(3 * MU_0 / (math.pi * k.G)) * k.c**2 / np.asarray(d, dtype=float)


def pulsar_dipole_field(period_s, pdot):
    """Surface dipole field from spin-down: B ~ 3.2e15 T sqrt(P Pdot) (3.2e19 G)."""
    return 3.2e15 * np.sqrt(np.asarray(period_s, dtype=float) * pdot)


def pdot_for_field(period_s, field_t):
    """Period derivative of a pulsar with dipole field B: Pdot = (B / 3.2e15)^2 / P."""
    return (field_t / 3.2e15) ** 2 / np.asarray(period_s, dtype=float)


def pdot_for_age(period_s, age_s):
    """Characteristic spin-down age tau = P / (2 Pdot)  ->  Pdot = P / (2 tau)."""
    return np.asarray(period_s, dtype=float) / (2 * age_s)


def min_spin_period(d):
    """A body of diameter d cannot spin faster than its rim reaching c: P = pi d / c."""
    return math.pi * d / k.c


# =============================================================================
# Pressure, flow, oscillation
# =============================================================================


def pressure_black_hole(d):
    """Dominant energy condition with black-hole density: P <= rho_BH c^2 = 3 c^4 / (2 pi G d^2)."""
    return density_black_hole(d) * k.c**2


def flow_at_speed(d, v):
    """Volumetric flow through a circular channel of diameter d at mean speed v: v pi d^2 / 4."""
    return v * np.pi * np.asarray(d, dtype=float) ** 2 / 4


def oscillation_light(d):
    """Swinging to and fro across its own size d, the peak speed pi f d must stay below c."""
    return k.c / (np.pi * np.asarray(d, dtype=float))


def oscillation_sound(d, v=None):
    """Fundamental mechanical mode of a solid of size d: f = v / (2 d), v at most ~36 km/s."""
    v = speed_sound_max() if v is None else v
    return v / (2 * np.asarray(d, dtype=float))


SOUND_SPEED_WATER = 1482.0  # m/s at 20 C


# =============================================================================
# Light, sound, numbers
# =============================================================================

K_M = 683.0  # lm/W, maximum luminous efficacy (SI definition of the candela)


def luminous_intensity_for_power(power_w):
    """Isotropic luminous intensity if all of `power_w` were emitted at 555 nm: 683 P / (4 pi)."""
    return K_M * power_w / (4 * math.pi)


def spl_db(pressure_pa, ref_pa=20e-6):
    """Sound pressure level, dB re ref."""
    return 20 * math.log10(pressure_pa / ref_pa)


P_ATM = 101325.0


def holographic_bits(radius_m):
    """Maximum information in a sphere of radius R: area / (4 l_P^2 ln 2) bits."""
    return 4 * math.pi * radius_m**2 / (4 * k.l_planck**2 * math.log(2))


OBSERVABLE_RADIUS = 46.5e9 * k.LY


# =============================================================================
# Epidemics, structures, volumes
# =============================================================================


def r0_for_doubling(serial_days, doubling_days):
    """Reproduction number that doubles case counts every `doubling_days`: R = 2^(T / t_d)."""
    return 2.0 ** (np.asarray(serial_days, dtype=float) / doubling_days)


G_EARTH = 9.80665


def crushing_height(strength_pa, density):
    """Tallest uniform column before its base crushes: h = sigma / (rho g)."""
    return strength_pa / (density * G_EARTH)


def mass_black_hole_volume(volume_m3):
    """Black-hole mass for a sphere of the given volume: M = c^2 d / 4G, d = (6V/pi)^(1/3)."""
    d = (6 * np.asarray(volume_m3, dtype=float) / np.pi) ** (1 / 3)
    return mass_black_hole(d)


BP_LENGTH_M = 0.34e-9  # rise per base pair of B-DNA
