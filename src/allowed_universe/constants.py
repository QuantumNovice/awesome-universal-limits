"""Physical constants used by every chart.

Fundamental constants come from ``scipy.constants`` (CODATA 2022 in SciPy >= 1.15).
Astronomical and material values that are not CODATA constants are defined here
once, each with its source, so every limit and test uses the same numbers.
"""

from __future__ import annotations

import math

import scipy.constants as _sc

# --- CODATA 2022 (via scipy.constants) --------------------------------------
c = _sc.c  # speed of light in vacuum, m/s (exact)
G = _sc.G  # Newtonian constant of gravitation, m^3 kg^-1 s^-2
h = _sc.h  # Planck constant, J s (exact)
hbar = _sc.hbar  # reduced Planck constant, J s
k_B = _sc.k  # Boltzmann constant, J/K (exact)
e = _sc.e  # elementary charge, C (exact)
epsilon_0 = _sc.epsilon_0  # vacuum permittivity, F/m
m_e = _sc.m_e  # electron mass, kg
m_p = _sc.m_p  # proton mass, kg
sigma_SB = _sc.Stefan_Boltzmann  # W m^-2 K^-4
a_rad = 4 * sigma_SB / c  # radiation constant, J m^-3 K^-4
eV = _sc.electron_volt  # J
N_A = _sc.Avogadro  # 1/mol

# Planck units
l_planck = math.sqrt(hbar * G / c**3)  # m
t_planck = math.sqrt(hbar * G / c**5)  # s
m_planck = math.sqrt(hbar * c / G)  # kg
T_planck = math.sqrt(hbar * c**5 / G) / k_B  # K
a_planck = math.sqrt(c**7 / (hbar * G))  # m/s^2

# --- Time --------------------------------------------------------------------
YEAR = 365.25 * 86400.0  # Julian year, s (IAU)
# Age of the universe: 13.787 +/- 0.020 Gyr, Planck 2018 VI (A&A 641, A6), Table 2.
T0 = 13.787e9 * YEAR  # s
# Hubble constant, Planck 2018 VI: 67.4 km/s/Mpc
H0 = 67.4e3 / 3.0857e22  # 1/s

# --- Astronomy (IAU 2015 Resolution B3 nominal values) -----------------------
GM_SUN = 1.3271244e20  # m^3/s^2
M_SUN = GM_SUN / G  # kg
R_SUN = 6.957e8  # m
GM_EARTH = 3.986004e14  # m^3/s^2
R_EARTH = 6.3781e6  # equatorial, m
SIDEREAL_DAY = 86164.0905  # s
R_GEO = (GM_EARTH * (SIDEREAL_DAY / (2 * math.pi)) ** 2) ** (1 / 3)  # m
AU = 1.495978707e11  # m (exact)
PC = 3.0856775814913673e16  # m
LY = c * YEAR  # m

# --- Matter ------------------------------------------------------------------
# Osmium, densest element at room conditions: 22,590 kg/m^3 (Arblaster 1989,
# Platinum Metals Rev. 33, 14). The spec rounds this to 22,600.
RHO_OSMIUM = 22_590.0
# Nuclear saturation density: n0 = 0.16 fm^-3 -> rho = n0 * m_n = 2.7e17 kg/m^3.
RHO_NUCLEAR = 0.16e45 * _sc.m_n
# Typical rock / rubble-pile asteroid bulk density (Carry 2012, P&SS 73, 98).
RHO_ROCK = 2_000.0
RHO_WATER = 1_000.0
# Rim speed ~ sqrt(sigma/rho) of the strongest bulk engineering materials.
V_RIM_MATERIAL = 3_000.0  # m/s
