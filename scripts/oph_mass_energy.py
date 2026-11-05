#!/usr/bin/env python3
"""Mass/energy readouts of the *declared* anchored Gaussian lattice model.

The transfer gap is dimensionless. Physical units are conditional on a supplied
clock and spectral bridge; neither is derived or verified by this module.
Sampler sweeps and bare action parameters are never reported as particle masses.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from numbers import Real
from pathlib import Path
import platform
from typing import Sequence

import numpy as np

# Exact defining SI values; hbar is derived from h with floating-point pi.
# https://www.bipm.org/en/measurement-units/si-defining-constants
PLANCK_J_S = 6.62607015e-34
HBAR_J_S = PLANCK_J_S / (2 * math.pi)
LIGHT_SPEED_M_S = 299792458.0
ELEMENTARY_CHARGE_C = 1.602176634e-19
JOULES_PER_GEV = 1e9 * ELEMENTARY_CHARGE_C


def _finite(value: float, name: str, *, positive: bool = False) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number, not a boolean or string")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite real number") from exc
    if not math.isfinite(result) or (positive and result <= 0):
        raise ValueError(f"{name} must be finite" + (" and positive" if positive else ""))
    return result


def lattice_omega(kappa: float, spatial_couplings: Sequence[float],
                  momentum_angles: Sequence[float]) -> float:
    """Return omega = kappa + 4 sum J_i sin(theta_i/2)^2, dimensionless.

    Exactly three spatial directions; kappa > 0 ensures a normalizable finite
    Gaussian measure without an additional zero-mode prescription. Angles are
    lattice momenta, not momenta in SI units. On a finite spatial torus they
    must separately be chosen from its allowed 2*pi*n/L modes.
    """
    kappa = _finite(kappa, "kappa", positive=True)
    if len(spatial_couplings) != 3 or len(momentum_angles) != 3:
        raise ValueError("Require exactly three spatial couplings and momentum angles")
    js = [_finite(j, "spatial coupling", positive=True) for j in spatial_couplings]
    angles = [_finite(a, "momentum angle") for a in momentum_angles]
    try:
        result = math.fsum([kappa] + [4 * j * math.sin(a / 2) ** 2
                                      for j, a in zip(js, angles)])
    except OverflowError as exc:
        raise ValueError("Spatial symbol exceeds floating-point range") from exc
    return _finite(result, "spatial symbol", positive=True)


def transfer_gap(kappa: float, transfer_coupling: float,
                 spatial_couplings: Sequence[float],
                 momentum_angles: Sequence[float]) -> float:
    """Dimensionless Gaussian transfer gap, using a cancellation-safe formula."""
    omega = lattice_omega(kappa, spatial_couplings, momentum_angles)
    j0 = _finite(transfer_coupling, "transfer coupling", positive=True)
    ratio = _finite(omega / j0, "omega / transfer coupling", positive=True)
    return 2 * math.asinh(math.sqrt(ratio) / 2)


def transfer_precision(omega: float, transfer_coupling: float,
                       extent: int) -> np.ndarray:
    """Build Q directly from sum_t [j0(q[t+1]-q[t])^2+omega*q[t]^2]/2.

    This construction does not use the transfer-gap or spectral formula.
    """
    omega = _finite(omega, "omega", positive=True)
    j0 = _finite(transfer_coupling, "transfer coupling", positive=True)
    if isinstance(extent, (bool, np.bool_)) or not isinstance(extent, (int, np.integer)) or extent < 3:
        raise ValueError("Periodic transfer extent must be an integer >= 3")
    if not math.isfinite(omega + 2 * j0):
        raise ValueError("Precision diagonal exceeds floating-point range")
    precision = np.eye(extent) * omega
    for t in range(extent):
        nxt = (t + 1) % extent
        precision[t, t] += j0
        precision[nxt, nxt] += j0
        precision[t, nxt] -= j0
        precision[nxt, t] -= j0
    return precision


def finite_mode_covariance(omega: float, transfer_coupling: float,
                           extent: int) -> np.ndarray:
    """Return C(t)=Q^{-1}[t,0] by an independent finite linear solve."""
    precision = transfer_precision(omega, transfer_coupling, extent)
    source = np.zeros(extent)
    source[0] = 1
    try:
        covariance = np.linalg.solve(precision, source)
    except np.linalg.LinAlgError as exc:
        raise ValueError("Precision solve failed at this floating-point scale") from exc
    if not np.all(np.isfinite(covariance)) or np.any(covariance <= 0):
        raise ValueError("Covariance lost positivity or finiteness at this floating-point scale")
    residual = np.linalg.norm(precision @ covariance - source, ord=np.inf)
    if residual > 1e-10:
        raise ValueError("Precision solve residual exceeds 1e-10")
    return covariance


def periodic_effective_gaps(correlator: Sequence[float]) -> list[float | None]:
    """Local cosh estimates; None for contact, nonpositive, or invalid ratios.

    This is a numerical diagnostic, not a pole classifier. Finite inputs are
    required globally, but an inadmissible local triplet is withheld, not clipped
    into a mass. Sampling errors and autocorrelation need a separate analysis.
    """
    if len(correlator) < 3:
        raise ValueError("Need a full periodic correlator with at least three entries")
    values = [_finite(c, "correlator entry") for c in correlator]
    gaps: list[float | None] = [None]  # t=0 contains the precision contact source.
    for t in range(1, len(values)):
        left, mid, right = values[t - 1], values[t], values[(t + 1) % len(values)]
        if min(left, mid, right) <= 0:
            gaps.append(None)
            continue
        # Halve first to avoid overflow in left + right.
        ratio = (0.5 * left + 0.5 * right) / mid
        gaps.append(math.acosh(ratio) if math.isfinite(ratio) and ratio >= 1 else None)
    return gaps


@dataclass(frozen=True)
class ClockCalibration:
    """A caller-supplied calibration contract, never a verified physics proof.

    Example-only reference strings still produce only a conditional conversion.
    To promote a physical claim, a human/reviewer must verify the cited clock,
    spectral reconstruction, and target independence outside this module.
    """

    seconds_per_transfer_step: float
    clock_reference: str
    spectral_bridge_reference: str
    independent_of_mass_target: bool
    coordinate_kind: str = "equilibrium_transfer"

    def validate(self) -> None:
        _finite(self.seconds_per_transfer_step, "seconds per transfer step", positive=True)
        for name, ref in (("clock_reference", self.clock_reference),
                          ("spectral_bridge_reference", self.spectral_bridge_reference)):
            if not isinstance(ref, str) or not ref.strip():
                raise ValueError(f"{name} must name a supplied provenance reference")
        if self.independent_of_mass_target is not True:
            raise ValueError("Target-fitted scale cannot be used as an independent mass readout")
        if self.coordinate_kind != "equilibrium_transfer":
            raise ValueError("Only the equilibrium transfer coordinate is supported; sampler sweeps are not time")


def conditional_physical_readout(gap: float, calibration: ClockCalibration | None,
                                 *, zero_momentum: bool) -> dict:
    """Convert gap via E=hbar*gap/a_t and, at rest only, m=E/c^2.

    No physical value is emitted without calibration. Supplying references
    changes the arithmetic availability, not the evidence status of the theory.
    """
    gap = _finite(gap, "transfer gap", positive=True)
    if type(zero_momentum) is not bool:
        raise ValueError("zero_momentum must be an explicit boolean")
    result = {
        "status": "unresolved", "energy_J": None, "energy_GeV": None,
        "rest_mass_kg": None, "rest_mass_GeV_per_c2": None,
        "physical_particle_identification": "unresolved",
        "evidence_verified_by_code": False,
        "reason": "No clock calibration and spectral bridge supplied",
    }
    if calibration is None:
        return result
    if not isinstance(calibration, ClockCalibration):
        raise ValueError("calibration must be a ClockCalibration contract")
    calibration.validate()
    energy = _finite(HBAR_J_S * (gap / calibration.seconds_per_transfer_step),
                     "conditional energy", positive=True)
    gev = _finite(energy / JOULES_PER_GEV, "conditional GeV energy", positive=True)
    mass = _finite(energy / LIGHT_SPEED_M_S ** 2, "conditional rest mass", positive=True) if zero_momentum else None
    result.update({
        "status": "conditional_unit_conversion", "energy_J": energy,
        "energy_GeV": gev, "rest_mass_kg": mass,
        "rest_mass_GeV_per_c2": gev if zero_momentum else None,
        "calibration": asdict(calibration),
        "reason": "Arithmetic conditional on caller-supplied clock and spectral bridge; references not verified",
    })
    return result


def gaussian_readout(kappa: float = 0.25, transfer_coupling: float = 1.2,
                     spatial_couplings: Sequence[float] = (1.0, 0.8, 1.1),
                     momentum_angles: Sequence[float] = (0.0, 0.0, 0.0),
                     calibration: ClockCalibration | None = None) -> dict:
    gap = transfer_gap(kappa, transfer_coupling, spatial_couplings, momentum_angles)
    angles = [_finite(a, "momentum angle") for a in momentum_angles]
    zero_momentum = all(math.remainder(a, 2 * math.pi) == 0.0 for a in angles)
    return {
        "model": "uniformly anchored periodic Gaussian; 3 transverse dimensions",
        "status": "demonstrated_conditional_model_formula",
        "supplied_parameters": {"kappa": float(kappa), "J0": float(transfer_coupling),
                                "J_spatial": [float(j) for j in spatial_couplings],
                                "momentum_angles": angles},
        "omega_dimensionless": lattice_omega(kappa, spatial_couplings, angles),
        "transfer_gap_dimensionless": gap,
        "zero_momentum": zero_momentum,
        "bare_kappa_is_particle_mass": False,
        "sampler_sweeps_are_physical_time": False,
        "physical": conditional_physical_readout(gap, calibration, zero_momentum=zero_momentum),
    }


def benchmark_receipt() -> dict:
    """Frozen deterministic direct-covariance checks, no parameter fitting."""
    cases = []
    # Frozen before execution; 15 cases test anchors, temporal coupling, and modes.
    for kappa in (0.05, 0.1, 0.25, 0.5, 1.0):
        for j0, mode in ((0.5, (0, 0, 0)), (1.0, (1, 0, 0)), (2.0, (1, 1, 0))):
            angles = tuple(2 * math.pi * n / 8 for n in mode)
            omega = lattice_omega(kappa, (1.0, 0.8, 1.1), angles)
            predicted = transfer_gap(kappa, j0, (1.0, 0.8, 1.1), angles)
            corr = finite_mode_covariance(omega, j0, 16)
            estimates = periodic_effective_gaps(corr)
            observed = [x for x in estimates[1:] if x is not None]
            error = max((abs(x - predicted) for x in observed), default=math.inf)
            cases.append({"kappa": kappa, "J0": j0, "spatial_extent": 8,
                          "mode_numbers": list(mode), "transfer_extent": 16,
                          "analytic_gap": predicted, "direct_covariance": corr.tolist(),
                          "max_gap_absolute_error": error,
                          "passed": len(observed) == 15 and error < 1e-10})
    return {
        "schema_version": 1, "model_scope": "declared finite Gaussian model only",
        "provenance": {
            "source_path": "scripts/oph_mass_energy.py",
            "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "baseline_commit": "d498af3926c98889531bca425565867409103a99",
            "source_pin_semantics": "SHA256 pins the current implementation; baseline is historical context",
        },
        "method": "assemble precision from link differences; solve Q*C=delta; local cosh readback",
        "frozen_acceptance": {"absolute_gap_error_lt": 1e-10, "all_noncontact_lags_required": True},
        "cases": cases, "passed": all(c["passed"] for c in cases),
        "uncalibrated_zero_momentum_readout": gaussian_readout(),
        "scientific_boundary": "No physical clock, particle identity, continuum interaction, or measured mass is derived",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = benchmark_receipt()
    text = json.dumps(receipt, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
    if not receipt["passed"]:
        raise SystemExit("Finite Gaussian mass/energy benchmark failed")


if __name__ == "__main__":
    main()
