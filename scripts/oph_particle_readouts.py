#!/usr/bin/env python3
"""Fixed-window finite correlator screening; no particle-name inference.

An accepted output is a single-cosh *shape candidate*, not a spectral theorem,
physical pole, or clean no-pole exclusion. Input intervals are propagated as
rectangular envelopes; no simultaneous statistical coverage is inferred.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Mapping


@dataclass(frozen=True)
class ScreenPolicy:
    """Engineering screening thresholds frozen before the fixture evaluation."""

    centers: tuple[int, ...] = (2, 3, 4)
    max_relative_gap_spread: float = 0.05
    max_relative_envelope_width: float = 0.25

    def validate(self) -> None:
        if len(self.centers) < 3 or any(type(t) is not int or t < 2 for t in self.centers):
            raise ValueError("Require at least three centers >=2; contact lag is excluded")
        if tuple(range(self.centers[0], self.centers[-1] + 1)) != self.centers:
            raise ValueError("The frozen centers must be a contiguous increasing window")
        for value in (self.max_relative_gap_spread, self.max_relative_envelope_width):
            if not math.isfinite(value) or value <= 0:
                raise ValueError("Screen tolerances must be finite and positive")


DEFAULT_POLICY = ScreenPolicy()
PHYSICAL_OBLIGATIONS = [
    "source-selected operator and action, with revision-pinned derivation",
    "reflection positivity and transfer reconstruction for this operator parity",
    "spin/statistics and charge representation, including gauge invariance",
    "multi-operator and multi-volume spectral separation from thresholds",
    "controlled interacting continuum and physical clock calibration",
    "target-independent agreement with independently measured observables",
]


def screen_channel(
    correlator: Mapping[int, tuple[float, float, float]],
    *,
    period: int,
    policy: ScreenPolicy = DEFAULT_POLICY,
    source: str = "unspecified finite model",
) -> dict:
    """Screen values ``lag: (estimate, lower, upper)`` in transfer-site units.

    All lags are nonnegative integers, and finite input intervals must contain
    their point estimate. Missing data and insufficient precision fail closed.
    A valid finite-volume cosh identity alone cannot select a particle species.
    """
    policy.validate()
    if type(period) is not int or period < 4 or period % 2:
        raise ValueError("Require an even integer transfer period >=4")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("A nonempty source description is required")
    values = {}
    for lag, row in correlator.items():
        if type(lag) is not int or lag < 0 or lag > period // 2:
            raise ValueError("Lags must be integers in [0, period/2]")
        if len(row) != 3 or not all(math.isfinite(float(x)) for x in row):
            raise ValueError("Correlator values and interval endpoints must be finite triples")
        point, lower, upper = (float(x) for x in row)
        if not lower <= point <= upper:
            raise ValueError("Every interval must contain its point estimate")
        values[lag] = (point, lower, upper)

    required = sorted({t + delta for t in policy.centers for delta in (-1, 0, 1)})
    reasons: list[str] = []
    missing = [t for t in required if t not in values]
    if missing:
        reasons.append("missing_required_lags")
    if required[-1] > period // 2:
        reasons.append("transfer_extent_too_small_for_frozen_window")
    nonpositive = [t for t in required if t in values and values[t][1] <= 0]
    if nonpositive:
        reasons.append("positive_separated_signal_unresolved")

    gaps = []
    if not reasons:
        for t in policy.centers:
            left, center, right = values[t - 1], values[t], values[t + 1]
            ratio = (left[0] + right[0]) / (2 * center[0])
            ratio_low = (left[1] + right[1]) / (2 * center[2])
            ratio_high = (left[2] + right[2]) / (2 * center[1])
            if not all(math.isfinite(x) for x in (ratio, ratio_low, ratio_high)):
                reasons.append("nonfinite_effective_gap_ratio")
                break
            if ratio < 1 or ratio_high < 1:
                reasons.append("positive_real_cosh_gap_not_supported")
                break
            gap = math.acosh(ratio)
            lower = math.acosh(max(1.0, ratio_low))
            upper = math.acosh(ratio_high)
            gaps.append({"lag": t, "gap": gap, "lower_envelope": lower,
                         "upper_envelope": upper})
        if len(gaps) == len(policy.centers):
            point_mean = sum(row["gap"] for row in gaps) / len(gaps)
            if point_mean <= 0 or any(row["lower_envelope"] <= 0 for row in gaps):
                reasons.append("gap_not_separated_from_zero")
            else:
                spread = (max(row["gap"] for row in gaps)
                          - min(row["gap"] for row in gaps)) / point_mean
                width = (max(row["upper_envelope"] for row in gaps)
                         - min(row["lower_envelope"] for row in gaps)) / point_mean
                if spread > policy.max_relative_gap_spread:
                    reasons.append("effective_gap_not_stable_in_frozen_window")
                if width > policy.max_relative_envelope_width:
                    reasons.append("effective_gap_envelope_too_wide")

    candidate = not reasons
    result = {
        "schema_version": 1,
        "source": source,
        "period_transfer_sites": period,
        "policy": asdict(policy),
        "required_lags": required,
        "contact_lag_used": False,
        "finite_channel_status": "single_cosh_shape_candidate" if candidate else "unresolved",
        "evidence_status": "supported but incomplete" if candidate else "unresolved",
        "reasons": reasons,
        "missing_lags": missing,
        "nonpositive_lower_envelope_lags": nonpositive,
        "effective_gaps": gaps,
        "gap_units": "dimensionless per declared transfer lattice step",
        "candidate_gap": sum(x["gap"] for x in gaps) / len(gaps) if candidate else None,
        "interval_interpretation": "rectangular propagation of supplied envelopes; no joint confidence level asserted",
        "physical_particle_identification": "unresolved",
        "physical_particle_name": None,
        "no_pole_exclusion": False,
        "physical_obligations": PHYSICAL_OBLIGATIONS,
    }
    if gaps:
        result["gap_envelope"] = [min(x["lower_envelope"] for x in gaps),
                                  max(x["upper_envelope"] for x in gaps)]
    else:
        result["gap_envelope"] = None
    return result


def periodic_cosh_values(period: int, terms: list[tuple[float, float]]) -> dict:
    """Exact synthetic sum A*(exp(-E*t)+exp(-E*(T-t))) for controls only."""
    return {t: sum(a * (math.exp(-e*t) + math.exp(-e*(period-t))) for a, e in terms)
            for t in range(period // 2 + 1)}


def summarize_stage3(path: Path) -> list[dict]:
    """Replay the published CSV without fabricating unavailable raw chains."""
    groups: dict[tuple, dict] = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            key = (int(row["N"]), int(row["L"]), row["estimator"])
            lag = int(row["separation"])
            group = groups.setdefault(key, {})
            if lag in group:
                raise ValueError("Duplicate lag in a Stage 3 channel")
            group[lag] = (float(row["estimate"]), float(row["ci_low_block_envelope"]),
                          float(row["ci_high_block_envelope"]))
    results = []
    for (n, size, estimator), data in sorted(groups.items()):
        result = screen_channel(data, period=size,
            source=f"legacy Stage 3 CSV: N={n}, L={size}, {estimator}")
        # The November audit found the old code's axes differed from its
        # documented F01 / axis-3 definition. Retain numbers only as a legacy
        # implementation regression, never as a certified intended correlator.
        result["provenance_status"] = "quarantined_axis_mismatch"
        result["provenance_limitation"] = (
            "Historical sampler rolled component-selected links along axes 1,2 "
            "and averaged axes 1,2,3; documented F01 needs axes 0,1 and an "
            "axis-3 separation needs averaging axes 0,1,2. No corrected rerun "
            "or raw-chain recovery is inferred from this legacy CSV.")
        if "legacy_operator_provenance_mismatch" not in result["reasons"]:
            result["reasons"].append("legacy_operator_provenance_mismatch")
        result["finite_channel_status"] = "unresolved"
        result["evidence_status"] = "unresolved"
        result["candidate_gap"] = None
        results.append(result)
    return results


def receipt(stage3_path: Path) -> dict:
    """Deterministic controls and retrospective screen of the frozen old study."""
    period = 16
    single = periodic_cosh_values(period, [(1.0, 0.4)])
    mixture = periodic_cosh_values(period, [(1.0, 0.15), (8.0, 1.2)])
    fixtures = {
        "exact_single_cosh": {t: (x, x, x) for t, x in single.items()},
        "two_gap_mixture": {t: (x, x, x) for t, x in mixture.items()},
        "zero_signal": {t: (0.0, -0.01, 0.01) for t in single},
        "negative_signal": {t: (-x, -1.01*x, -0.99*x) for t, x in single.items()},
        "imprecise_positive_signal": {t: (x, 0.5*x, 1.5*x) for t, x in single.items()},
    }
    controls = {name: screen_channel(data, period=period, source=f"synthetic control: {name}")
                for name, data in fixtures.items()}
    return {
        "schema_version": 1,
        "date": "2026-11-05",
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "finite single-cosh shape screening, not discovery of nature's particles",
        "policy_frozen_for": "synthetic implementation checks; retrospective for October Stage 3 data",
        "input_sha256": hashlib.sha256(stage3_path.read_bytes()).hexdigest(),
        "synthetic_controls": controls,
        "stage3_channels": summarize_stage3(stage3_path),
        "nonidentification_witness": {
            "statement": "The same correlator can be assigned different spectator charge labels without changing this screen.",
            "consequence": "Correlator shape alone does not identify spin, statistics, charge, or physical species.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage3-csv", type=Path,
        default=Path(__file__).resolve().parents[1]/"docs/data/oph_n2_flux_stage3_summary.csv")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = receipt(args.stage3_csv)
    encoded = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
