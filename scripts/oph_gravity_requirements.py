#!/usr/bin/env python3
"""Exact finite null tomography and an evidence contract for OPH gravity.

This module audits supplied evidence; it does not validate physical premises.
The tomography uses a supplied Minkowski interface (-,+,+,+), not a metric
derived from repairs. Run without arguments to reproduce the frozen receipt.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


F = Fraction
PAIRS = tuple((i, j) for i in range(4) for j in range(i, 4))
METRIC = tuple(tuple(F((-1 if i == 0 else 1) if i == j else 0)
                     for j in range(4)) for i in range(4))
NULL_DIRECTIONS = (
    (1, 1, 0, 0), (1, -1, 0, 0),
    (1, 0, 1, 0), (1, 0, -1, 0),
    (1, 0, 0, 1), (1, 0, 0, -1),
    (1, F(3, 5), F(4, 5), 0),
    (1, F(3, 5), 0, F(4, 5)),
    (1, 0, F(3, 5), F(4, 5)),
)

# These are local audit IDs, not canonical upstream theorem identifiers.
REQUIREMENTS = {
    "finite_tensor_interface": "A same-source symmetric 3+1 tensor interface and Lorentz metric",
    "nine_direction_balances": "Nine spanning source-derived null-direction balances",
    "ward_bianchi_conservation": "Compatible Ward/Bianchi conservation for the same tensors",
    "connectedness": "Connected event domain with the required regularity",
    "event_signal_clock": "Physical event, signal, volume, and clock identification",
    "stress_vacuum": "Independently reconstructed physical stress and vacuum subtraction",
    "coupling_scale": "Same-family coupling normalization and physical scale calibration",
    "tensor_curvature_limit": "Controlled same-family rank-two tensor-curvature convergence",
    "small_ball_null_balance": "Independent continuum small-ball/null-balance identification",
    "null_modular_bridge": "Physical null-stress/modular-charge identification",
    "bounded_interval_transport": "Bounded-interval transport and projective compatibility",
    "entropy_stationarity": "Fixed-cap generalized-entropy stationarity on the variation class",
    "bw_realized_cap_pair": "Canonical scaling cap-pair realization from transported marginals",
    "bw_rigidity": "Independent BW rigidity on the realized limit",
    "bw_collar_floor": "Eventual fixed local collar common floor on transport marginals",
    "capacity_carrier": "Source-selected positive capacity carrier",
    "same_invariant_capacity": "Construction/readback identify the same capacity invariant",
    "horizon_saturation": "Physical horizon-record attachment and saturation",
    "independent_gravity_test": "Frozen comparison with independent gravitational observations",
}
FINITE = ("finite_tensor_interface", "nine_direction_balances",
          "ward_bianchi_conservation", "connectedness")
PHYSICAL = ("event_signal_clock", "stress_vacuum", "coupling_scale")
ROUTES = {
    "tensor_limit": ("tensor_curvature_limit",),
    "null_balance": ("small_ball_null_balance",),
    "bw_null_balance": ("small_ball_null_balance", "null_modular_bridge",
                        "bounded_interval_transport", "entropy_stationarity",
                        "bw_realized_cap_pair", "bw_rigidity", "bw_collar_floor"),
}
CAPACITY = ("capacity_carrier", "same_invariant_capacity", "horizon_saturation")
EVIDENCE_STATUSES = {"demonstrated", "supported_but_incomplete", "hypothesis",
                     "unresolved", "rejected"}


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("Booleans are not tensor coefficients")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Coefficients must be finite")
    try:
        return F(value)
    except (ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("Expected a finite rational-compatible coefficient") from exc


def _tensor(tensor):
    if len(tensor) != 4 or any(len(row) != 4 for row in tensor):
        raise ValueError("Expected a 4 by 4 tensor")
    result = tuple(tuple(_fraction(x) for x in row) for row in tensor)
    if any(result[i][j] != result[j][i] for i, j in PAIRS):
        raise ValueError("The supplied tensor must be exactly symmetric")
    return result


def _rref(rows):
    """Exact row reduction; returns reduced rows and pivot column indices."""
    matrix = [list(map(_fraction, row)) for row in rows]
    if not matrix:
        return [], []
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("Ragged matrix")
    pivots = []
    row = 0
    for column in range(width):
        pivot = next((i for i in range(row, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][column]
        matrix[row] = [x / scale for x in matrix[row]]
        for i in range(len(matrix)):
            if i != row:
                scale = matrix[i][column]
                matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[row])]
        pivots.append(column)
        row += 1
        if row == len(matrix):
            break
    return matrix, pivots


def null_design(directions=NULL_DIRECTIONS):
    """Rows map the ten independent covariant H_ab entries to H_ab k^a k^b."""
    rows = []
    for vector in directions:
        if len(vector) != 4:
            raise ValueError("Expected four-component null vectors")
        k = tuple(map(_fraction, vector))
        if not any(k) or -k[0] ** 2 + sum(x ** 2 for x in k[1:]) != 0:
            raise ValueError("Each direction must be a nonzero exact Minkowski-null vector")
        rows.append([k[i] * k[j] * (1 if i == j else 2) for i, j in PAIRS])
    return rows


def null_contractions(tensor, directions=NULL_DIRECTIONS):
    matrix = _tensor(tensor)
    entries = [matrix[i][j] for i, j in PAIRS]
    return [sum(a * b for a, b in zip(row, entries)) for row in null_design(directions)]


def tomography_rank(directions=NULL_DIRECTIONS):
    rows = null_design(directions)
    rank = len(_rref(rows)[1])
    return {"directions": len(rows), "rank": rank, "symmetric_tensor_dimension": 10,
            "nullity": 10 - rank, "identifies_tensor_modulo_metric": rank == 9,
            "identifies_full_tensor": False}


def reconstruct_modulo_metric(readings):
    """Reconstruct the H_00=0 representative from the canonical nine readings.

    The gauge is a reporting convention, not a determination of Lambda.
    Every tensor H + lambda*eta has the same readings.
    """
    if len(readings) != 9:
        raise ValueError("Exactly nine canonical-direction readings are required")
    design = null_design()
    augmented = [row + [_fraction(y)] for row, y in zip(design, readings)]
    augmented.append([F(1)] + [F(0)] * 10)  # H_00 = 0
    reduced, pivots = _rref(augmented)
    if pivots != list(range(10)):
        raise ValueError("The declared tomography interface is not invertible modulo metric")
    entries = [row[-1] for row in reduced]
    tensor = [[F(0)] * 4 for _ in range(4)]
    for (i, j), value in zip(PAIRS, entries):
        tensor[i][j] = tensor[j][i] = value
    return tensor


def add_metric(tensor, coefficient):
    tensor = _tensor(tensor)
    coefficient = _fraction(coefficient)
    return [[tensor[i][j] + coefficient * METRIC[i][j] for j in range(4)]
            for i in range(4)]


def conservation_diagnostic(values, edges):
    """Exact incidence test d(lambda)=0 on a supplied finite undirected graph.

    This is the scalar remnant of a supplied conservation identity. It does
    not derive discrete Bianchi/Ward identities or a physical stress tensor.
    """
    values = list(map(_fraction, values))
    if not values:
        raise ValueError("A nonempty finite domain is required")
    adjacency = [set() for _ in values]
    residuals = []
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("An edge must contain two vertex indices")
        i, j = edge
        if (isinstance(i, bool) or isinstance(j, bool) or not isinstance(i, int)
                or not isinstance(j, int) or not 0 <= i < len(values)
                or not 0 <= j < len(values)):
            raise ValueError("Invalid vertex index")
        adjacency[i].add(j)
        adjacency[j].add(i)
        residuals.append(values[j] - values[i])
    remaining = set(range(len(values)))
    components = []
    while remaining:
        pending = [min(remaining)]
        component = set()
        while pending:
            vertex = pending.pop()
            if vertex in component:
                continue
            component.add(vertex)
            pending.extend(adjacency[vertex] - component)
        remaining -= component
        components.append(sorted(component))
    return {"status": "PASS" if all(x == 0 for x in residuals) else "FAIL",
            "edge_residuals": [str(x) for x in residuals],
            "components": components, "connected": len(components) == 1,
            "undetermined_constants": len(components),
            "determines_constant_value": False,
            "scope": "finite scalar incidence check after a supplied conservation reduction"}


def evaluate_requirements(evidence=None, route="tensor_limit", require_lambda=True):
    """Fail-closed manifest audit, never a scientific proof verifier.

    A qualifying record has status 'demonstrated', a nonempty artifact locator,
    an explicit same-family assertion and target-independent assertion. Even a
    complete manifest only licenses independent review of the referenced work.
    """
    if route not in ROUTES:
        raise ValueError("Unknown continuum route")
    if not isinstance(require_lambda, bool):
        raise ValueError("require_lambda must be boolean")
    evidence = {} if evidence is None else evidence
    if not isinstance(evidence, dict) or set(evidence) - set(REQUIREMENTS):
        raise ValueError("Evidence must be a mapping of known local requirement IDs")
    for name, record in evidence.items():
        if not isinstance(record, dict) or record.get("status") not in EVIDENCE_STATUSES:
            raise ValueError(f"Malformed evidence record: {name}")
    required = FINITE + PHYSICAL + ROUTES[route]
    if require_lambda:
        required += CAPACITY
    required += ("independent_gravity_test",)
    rows = []
    for name in required:
        record = evidence.get(name, {"status": "unresolved"})
        reasons = []
        if record["status"] != "demonstrated":
            reasons.append("evidence_not_demonstrated")
        if not isinstance(record.get("artifact"), str) or not record["artifact"].strip():
            reasons.append("missing_artifact")
        if record.get("same_family") is not True:
            reasons.append("same_family_not_attested")
        if record.get("target_independent") is not True:
            reasons.append("target_independence_not_attested")
        rows.append({"id": name, "requirement": REQUIREMENTS[name],
                     "evidence_status": record["status"], "missing": reasons})
    failed = any(row["evidence_status"] == "rejected" for row in rows)
    blockers = [row["id"] for row in rows if row["missing"]]
    return {"status": "REJECTED" if failed else "UNRESOLVED" if blockers else "READY_FOR_REVIEW",
            "route": route, "lambda_required": require_lambda,
            "requirements": rows, "blockers": blockers,
            "manifest_complete": not blockers,
            "physical_gravity_established": False,
            "G_SI": None, "Lambda_m_minus_2": None,
            "boundary": "Manifest fields are attestations, not machine-verified physical evidence. "
                        "A no-G scale certificate is a supplied calibration until independently attached."}


def demo_receipt():
    original = [[2, 1, -2, 3], [1, 5, 4, -1], [-2, 4, 7, 2], [3, -1, 2, 11]]
    readings = null_contractions(original)
    shifted = add_metric(original, F(7, 3))
    reconstructed = reconstruct_modulo_metric(readings)
    return {
        "schema": "oph-gravity-readout-v1", "metric_signature": "-+++",
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "evidence_status": "demonstrated_finite_algebra; physical_gravity_unresolved",
        "tomography": {**tomography_rank(),
                       "directions": [[str(x) for x in k] for k in NULL_DIRECTIONS],
                       "readings": [str(x) for x in readings],
                       "metric_shift": "7/3",
                       "shifted_readings_identical": readings == null_contractions(shifted),
                       "reconstructed_H00_zero": [[str(x) for x in row] for row in reconstructed],
                       "reconstruction_readings_identical": null_contractions(reconstructed) == readings,
                       "only_axes_rank": tomography_rank(NULL_DIRECTIONS[:6])["rank"]},
        "conservation": {
            "constant_connected": conservation_diagnostic([2, 2, 2], [(0, 1), (1, 2)]),
            "varying_connected": conservation_diagnostic([2, 3, 2], [(0, 1), (1, 2)]),
            "disconnected": conservation_diagnostic([2, 2, 9], [(0, 1)])},
        "requirements": evaluate_requirements(),
        "not_established": ["source-derived physical tensor", "Einstein dynamics",
                            "measured Newton coupling", "source-selected cosmological constant"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(demo_receipt(), indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
