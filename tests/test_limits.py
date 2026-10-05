"""Each bound against a value computed by hand (see the comments for the arithmetic)."""

import math

import pytest

from allowed_universe import constants as k
from allowed_universe import limits as L

rel = pytest.approx


# --- spin (spec acceptance values) -------------------------------------------


def test_spin_light_at_one_metre():
    # c / pi = 299792458 / 3.14159 = 9.5426e7
    assert L.spin_light(1.0) == rel(9.54e7, rel=1e-3)


def test_spin_quantum_at_one_angstrom():
    # 12 hbar / (pi^2 rho d^5) = 1.2655e-33 / (9.8696 * 22590 * 1e-50) = 5.68e11
    assert L.spin_quantum(1e-10) == rel(5.7e11, rel=0.01)


def test_spin_quantum_prefactor():
    # spec: f_min ~ 5.7e-39 / d^5
    assert L.spin_quantum(1.0) == rel(5.7e-39, rel=0.01)


def test_spin_age_floor():
    # 1 / (13.787e9 * 3.15576e7 s) = 2.30e-18 Hz
    assert L.spin_age() == rel(2.3e-18, rel=0.01)


def test_spin_material_is_light_scaled():
    assert L.spin_material(2.0) / L.spin_light(2.0) == rel(3000 / k.c)


def test_spin_gravity_rock():
    # sqrt(4 pi G 2000 / 3) / 2pi = 1.19e-4 Hz, about one turn per 2.3 h
    f = L.spin_gravity(2000)
    assert f == rel(1.19e-4, rel=0.01)
    assert 1 / f / 3600 == rel(2.33, rel=0.01)


def test_black_hole_max_spin_10_msun():
    # c^3 / (4 pi G M) with M = 10 Msun: 2.694e25 / 1.668e22 = 1615.6 Hz
    assert L.spin_black_hole_max(10 * k.M_SUN) == rel(1615.6, rel=1e-3)


def test_black_hole_spin_tends_to_max():
    m = 10 * k.M_SUN
    assert L.spin_black_hole(m, 0.999999) == rel(float(L.spin_black_hole_max(m)), rel=2e-3)


def test_maximal_black_hole_rim_moves_at_light_speed():
    # a = 1 horizon frequency equals c/(pi d) with d = 4GM/c^2: the cap sits on the light line
    m = 10 * k.M_SUN
    d = 4 * k.G * m / k.c**2
    assert L.spin_black_hole_max(m) == rel(float(L.spin_light(d)))


def test_kepler_earth_orbit():
    # one year
    f = L.orbit_frequency(k.M_SUN, k.AU)
    assert 1 / f / k.YEAR == rel(1.0, rel=1e-3)


# --- mass ---------------------------------------------------------------------


def test_mass_black_hole_sun():
    # Sun's Schwarzschild radius is 2.95 km, so d = 5.9 km holds one solar mass
    assert L.mass_black_hole(5906.0) == rel(k.M_SUN, rel=1e-3)


def test_mass_compton_electron():
    # h / (c * lambda_C) returns the electron mass at its Compton wavelength 2.4263e-12 m
    assert L.mass_compton(2.42631e-12) == rel(k.m_e, rel=1e-5)


def test_black_hole_and_compton_meet_near_planck_scale():
    # c^2 d / 4G = h / cd  ->  d = sqrt(4 G h / c^3) = 2 sqrt(2 pi) l_P
    d = math.sqrt(4 * k.G * k.h / k.c**3)
    assert d / k.l_planck == rel(2 * math.sqrt(2 * math.pi))
    assert L.mass_black_hole(d) == rel(float(L.mass_compton(d)))


# --- speed, temperature, density, acceleration, lifetime -----------------------


def test_sound_speed_bound():
    # Trachenko et al. 2020: 36.1 km/s
    assert L.speed_sound_max() == rel(3.61e4, rel=0.01)


def test_planck_temperature():
    assert L.temperature_planck() == rel(1.4168e32, rel=1e-3)


def test_collapse_temperature_one_metre():
    # (3 c^4 / (2 pi G a))^(1/4) = (7.64e58)^(1/4) = 5.26e14 K
    assert L.temperature_collapse(1.0) == rel(5.26e14, rel=0.01)


def test_hawking_temperature_solar_mass():
    # T = hbar c^3 / (8 pi G M k_B) = 6.17e-8 K for one solar mass
    d = 4 * k.G * k.M_SUN / k.c**2
    assert L.temperature_hawking(d) == rel(6.17e-8, rel=0.01)


def test_black_hole_density_sun():
    # Sun squeezed to d = 5.9 km: M / (pi d^3 / 6) = 1.84e19 kg/m^3
    d = 4 * k.G * k.M_SUN / k.c**2
    assert L.density_black_hole(d) == rel(k.M_SUN / (math.pi * d**3 / 6))
    assert L.density_black_hole(d) == rel(1.84e19, rel=0.01)


def test_rindler_equals_horizon_gravity():
    # kappa = c^4 / (4 G M) and d = 4GM/c^2  ->  kappa = c^2 / d
    m = k.M_SUN
    d = 4 * k.G * m / k.c**2
    assert L.accel_rindler(d) == rel(k.c**4 / (4 * k.G * m))


def test_planck_acceleration():
    assert L.accel_planck() == rel(5.56e51, rel=0.01)


def test_planck_time():
    assert L.lifetime_planck() == rel(5.391e-44, rel=1e-3)


def test_hawking_lifetime_solar_mass():
    # 5120 pi G^2 M^3 / (hbar c^4) = 6.6e74 s = 2.1e67 yr for one solar mass
    d = 4 * k.G * k.M_SUN / k.c**2
    assert L.lifetime_hawking(d) / k.YEAR == rel(2.1e67, rel=0.02)


# --- materials, chemistry, AI, cognition --------------------------------------


def test_energy_condition_water():
    assert L.strength_energy_condition(1000) == rel(8.988e19, rel=1e-3)


def test_space_elevator_breaking_length():
    # about 48.5 MJ/kg, i.e. a breaking length of ~4,940 km at 1 g
    s = L.space_elevator_specific_strength()
    assert s == rel(4.84e7, rel=0.01)
    assert s / 9.80665 / 1e3 == rel(4940, rel=0.01)


def test_geostationary_radius():
    assert k.R_GEO == rel(4.2164e7, rel=1e-4)


def test_coulomb_hydrogen():
    # Coulomb energy at two Bohr radii equals the 13.6 eV binding energy
    assert L.coulomb_energy(2 * 0.529177e-10) / k.eV == rel(13.6, rel=1e-3)


def test_thermal_energy_room():
    assert L.thermal_energy(300) / k.eV == rel(0.02585, rel=1e-3)


def test_chinchilla_compute():
    # 70B parameters, 1.4T tokens: 6 * 7e10 * 1.4e12 = 5.88e23 FLOP
    assert L.chinchilla_compute(7e10) == rel(5.88e23)


def test_landauer_brain():
    # 20 W / (k_B * 310 K * ln 2) = 6.7e21 bit/s
    assert L.landauer_bit_rate(20, 310) == rel(6.74e21, rel=0.01)


def test_reading_ceiling():
    assert L.reading_ceiling(1.0) == rel(8766, rel=1e-3)


# --- electromagnetism -----------------------------------------------------------


def test_schwinger_field():
    # m_e^2 c^3 / (e hbar) = 1.3233e18 V/m
    assert L.E_SCHWINGER == rel(1.3233e18, rel=1e-3)


def test_charge_collapse_per_metre():
    # c^2 sqrt(4 pi eps0 / G) = 8.988e16 * sqrt(1.1127e-10 / 6.6743e-11) = 1.1605e17 C per metre of radius
    assert L.charge_collapse(2.0) == rel(1.1605e17, rel=1e-3)


def test_charged_sphere_at_collapse_has_planck_voltage():
    # V = Q / (4 pi eps0 r) at the collapse charge is c^2 / sqrt(4 pi eps0 G) = 1.043e27 V, for any size
    for d in (1e-10, 1.0, 1e10):
        v = L.charge_collapse(d) / (4 * math.pi * k.epsilon_0 * d / 2)
        assert v == rel(L.PLANCK_VOLTAGE)
    assert L.PLANCK_VOLTAGE == rel(1.043e27, rel=1e-3)


def test_gravity_beats_schwinger_above_sun_size():
    # 4 pi eps0 r^2 E_S = r c^2 sqrt(4 pi eps0 / G)  ->  r = c^2 / (E_S sqrt(4 pi eps0 G)) = 7.9e8 m
    r = k.c**2 / (L.E_SCHWINGER * math.sqrt(4 * math.pi * k.epsilon_0 * k.G))
    assert r == rel(7.9e8, rel=0.01)
    assert L.charge_collapse(4 * r) < L.charge_for_field(4 * r, L.E_SCHWINGER)


def test_planck_charge_is_e_over_sqrt_alpha():
    alpha = k.e**2 / (4 * math.pi * k.epsilon_0 * k.hbar * k.c)
    assert L.PLANCK_CHARGE == rel(k.e / math.sqrt(alpha))
    assert L.PLANCK_CHARGE / k.e == rel(11.7, rel=0.01)


def test_rayleigh_limit_millimetre_water_drop():
    # 8 pi sqrt(8.854e-12 * 0.072 * (1e-3)^3) = 25.13 * 2.525e-11 = 6.35e-10 C
    assert L.charge_rayleigh(2e-3) == rel(6.35e-10, rel=0.01)
