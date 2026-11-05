#!/usr/bin/env python3
"""Controlled classical phi^4 readouts in three space dimensions and model time.

The action, periodic carrier, clock, and coupling are supplied. This program
does not derive an interacting quantum continuum or identify nature's particles.
All quantities below use declared dimensionless model units.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Callable

import numpy as np


def _number(value: float, name: str, *, positive: bool = False) -> float:
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a finite real number")
    value = float(value)
    if not math.isfinite(value) or (value <= 0 if positive else value < 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'nonnegative'}")
    return value


def _field(value: np.ndarray, name: str) -> np.ndarray:
    raw = np.asarray(value)
    if np.iscomplexobj(raw):
        raise ValueError(f"{name} must be real")
    field = np.asarray(raw, dtype=float)
    if field.ndim != 3 or min(field.shape) < 4 or len(set(field.shape)) != 1:
        raise ValueError(f"{name} must be a cubic three-dimensional grid, N>=4")
    if not np.all(np.isfinite(field)):
        raise ValueError(f"{name} must contain only finite values")
    return field


def laplacian(field: np.ndarray, spacing: float) -> np.ndarray:
    """Centered periodic Laplacian; each of the three axes contributes."""
    field = _field(field, "field")
    spacing = _number(spacing, "spacing", positive=True)
    return sum(np.roll(field, 1, axis=i) - 2 * field + np.roll(field, -1, axis=i)
               for i in range(3)) / spacing**2


def energy_components(field: np.ndarray, velocity: np.ndarray, spacing: float,
                      speed: float = 1.0, mass_squared: float = 0.7,
                      coupling: float = 2.0) -> dict[str, float]:
    """Hamiltonian of the supplied semi-discrete action, in model energy units.

    E = h^3 sum [v^2/2 + c^2 sum_i(D_i^+ phi)^2/2
                + m0^2 phi^2/2 + lambda phi^4/4].
    The bare coefficient m0^2 is not a measured physical pole mass.
    """
    field, velocity = _field(field, "field"), _field(velocity, "velocity")
    if field.shape != velocity.shape:
        raise ValueError("field and velocity must have the same shape")
    spacing = _number(spacing, "spacing", positive=True)
    speed = _number(speed, "speed", positive=True)
    mass_squared = _number(mass_squared, "mass_squared")
    coupling = _number(coupling, "coupling")
    volume = spacing**3
    result = {
        "kinetic": float(volume * np.sum(velocity**2) / 2),
        "gradient": float(volume * speed**2 * sum(
            np.sum(((np.roll(field, -1, axis=i) - field) / spacing)**2)
            for i in range(3)) / 2),
        "quadratic": float(volume * mass_squared * np.sum(field**2) / 2),
        "quartic": float(volume * coupling * np.sum(field**4) / 4),
    }
    result["total"] = sum(result.values())
    if not all(math.isfinite(v) for v in result.values()):
        raise ValueError("energy overflow")
    return result


def evolve(field: np.ndarray, velocity: np.ndarray, *, spacing: float,
           final_time: float, time_step: float, speed: float = 1.0,
           mass_squared: float = 0.7, coupling: float = 2.0,
           source: Callable[[float], np.ndarray] | None = None) -> dict:
    """Velocity-Verlet integration with retained energy/readout records.

    The guard dt*sqrt(12*c^2/h^2+m0^2+3*lambda*max(phi^2)) < 1.8 is
    checked at both ends of every step. It is an instantaneous conservative
    linearized frequency guard, not a proof of nonlinear global stability.
    An exact final-time hit uses dt=final_time/ceil(final_time/time_step).
    """
    u, v = _field(field, "field").copy(), _field(velocity, "velocity").copy()
    if u.shape != v.shape:
        raise ValueError("field and velocity must have the same shape")
    spacing = _number(spacing, "spacing", positive=True)
    final_time = _number(final_time, "final_time", positive=True)
    time_step = _number(time_step, "time_step", positive=True)
    speed = _number(speed, "speed", positive=True)
    mass_squared = _number(mass_squared, "mass_squared")
    coupling = _number(coupling, "coupling")
    steps = math.ceil(final_time / time_step)
    dt = final_time / steps

    def force(x: np.ndarray, t: float) -> tuple[np.ndarray, np.ndarray]:
        frequency_guard = dt * math.sqrt(12 * speed**2 / spacing**2 + mass_squared
                                        + 3 * coupling * float(np.max(x**2)))
        if not math.isfinite(frequency_guard) or frequency_guard >= 1.8:
            raise ValueError("time step violates the declared frequency guard")
        j = np.zeros_like(x) if source is None else _field(source(t), "source")
        if j.shape != x.shape:
            raise ValueError("source must have the field shape")
        return speed**2 * laplacian(x, spacing) - mass_squared * x - coupling * x**3 + j, j

    acceleration, j = force(u, 0.0)
    source_work = 0.0
    records = []

    def record(t: float) -> None:
        e = energy_components(u, v, spacing, speed, mass_squared, coupling)
        records.append({"model_time": t, **e, "source_work": source_work,
                        "field_rms": float(np.sqrt(np.mean(u**2))),
                        "velocity_rms": float(np.sqrt(np.mean(v**2)))})

    record(0.0)
    for step in range(steps):
        old_power = spacing**3 * float(np.sum(j * v))
        next_u = u + dt * v + 0.5 * dt**2 * acceleration
        next_acceleration, next_j = force(next_u, (step + 1) * dt)
        next_v = v + 0.5 * dt * (acceleration + next_acceleration)
        new_power = spacing**3 * float(np.sum(next_j * next_v))
        source_work += 0.5 * dt * (old_power + new_power)
        u, v, acceleration, j = next_u, next_v, next_acceleration, next_j
        record((step + 1) * dt)
    return {"field": u, "velocity": v, "records": records,
            "steps": steps, "time_step": dt, "final_time": final_time}


def manufactured_case(n: int, *, omit_interaction: bool = False) -> dict:
    """Verification against an analytic forced nonlinear solution.

    phi=.4 sin(x)sin(y)sin(z)cos(1.7t) on [0,2*pi)^3.
    J=(3+m0^2-1.7^2)phi+lambda*phi^3, with lambda=2 fixed even
    in the interaction-omission negative control.
    """
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n < 4:
        raise ValueError("n must be an integer >=4")
    length, omega, amplitude, mass_squared, coupling = 2 * math.pi, 1.7, 0.4, 0.7, 2.0
    h = length / n
    s = np.sin(np.arange(n) * h)
    spatial = amplitude * s[:, None, None] * s[None, :, None] * s[None, None, :]

    def exact(t: float) -> np.ndarray:
        return spatial * math.cos(omega * t)

    def source(t: float) -> np.ndarray:
        x = exact(t)
        return (3 + mass_squared - omega**2) * x + coupling * x**3

    result = evolve(spatial, np.zeros_like(spatial), spacing=h, final_time=0.6,
                    time_step=0.1 * h, mass_squared=mass_squared,
                    coupling=0.0 if omit_interaction else coupling, source=source)
    error = float(np.sqrt(np.mean((result["field"] - exact(0.6))**2)))
    v_exact = -omega * spatial * math.sin(omega * 0.6)
    v_error = float(np.sqrt(np.mean((result["velocity"] - v_exact)**2)))
    return {"n": n, "spacing": h, "time_step": result["time_step"],
            "steps": result["steps"], "final_time": 0.6,
            "field_rms_error": error, "velocity_rms_error": v_error,
            "interaction_in_equation": not omit_interaction}


def build_receipt() -> dict:
    """Run a frozen verification suite; no claim of empirical prediction."""
    resolutions = [12, 18, 24, 36]
    cases = [manufactured_case(n) for n in resolutions]
    orders = [math.log(a["field_rms_error"] / b["field_rms_error"]) /
              math.log(b["n"] / a["n"]) for a, b in zip(cases[:-1], cases[1:])]
    negative = manufactured_case(resolutions[-1], omit_interaction=True)
    n, length = 16, 2 * math.pi
    h = length / n
    x = np.arange(n) * h
    field = 0.4 * np.sin(x[:, None, None]) * np.sin(x[None, :, None]) * np.sin(x[None, None, :])
    unforced = evolve(field, np.zeros_like(field), spacing=h, final_time=2.0,
                      time_step=0.025 * h)
    initial = unforced["records"][0]["total"]
    drift = max(abs(row["total"] - initial) / initial for row in unforced["records"])
    unforced_half_step = evolve(field, np.zeros_like(field), spacing=h,
                                final_time=2.0, time_step=0.0125 * h)
    half_drift = max(abs(row["total"] - initial) / initial
                     for row in unforced_half_step["records"])
    controls = {
        "min_observed_field_order": 1.8,
        "max_relative_energy_drift": 0.0005,
        "min_energy_drift_improvement_under_half_step": 3.0,
        "min_interaction_omission_error_ratio": 3.0,
    }
    ratio = negative["field_rms_error"] / cases[-1]["field_rms_error"]
    checks = {
        "refinement": all(order > controls["min_observed_field_order"] for order in orders),
        "unforced_energy_drift": drift < controls["max_relative_energy_drift"],
        "energy_drift_time_refinement": drift / half_drift > controls["min_energy_drift_improvement_under_half_step"],
        "interaction_omission_detected": ratio > controls["min_interaction_omission_error_ratio"],
    }
    return {
        "schema_version": 1,
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "demonstrated" if all(checks.values()) else "rejected",
        "scope": "numerical verification of a supplied classical nonlinear scalar model",
        "model": {"spatial_dimensions": 3, "time_kind": "supplied_model_time",
                  "boundary": "periodic", "length": length, "speed": 1.0,
                  "mass_squared": 0.7, "coupling": 2.0,
                  "potential": "mass_squared*phi^2/2 + coupling*phi^4/4",
                  "units": "dimensionless model length, time, field, and energy"},
        "criteria": controls,
        "checks": checks,
        "manufactured_refinement": cases,
        "observed_field_orders": orders,
        "interaction_omission_control": {**negative, "error_ratio": ratio},
        "unforced": {"n": n, "final_time": 2.0, "time_step": unforced["time_step"],
                     "relative_energy_drift": drift,
                     "half_time_step": unforced_half_step["time_step"],
                     "half_step_relative_energy_drift": half_drift,
                     "energy_drift_improvement": drift / half_drift,
                     "readout_records": unforced["records"]},
        "unresolved": ["OPH source-to-action and field/observer readout bridge",
                       "physical clock and dimensional calibration",
                       "interacting quantum continuum and renormalization",
                       "spin/statistics, particle identity, and empirical validation",
                       "uniform nonlinear continuum error theorem"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write a deterministic verification receipt")
    args = parser.parse_args()
    result = build_receipt()
    text = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    else:
        print(text, end="")
    if not all(result["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
