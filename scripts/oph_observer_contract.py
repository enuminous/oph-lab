#!/usr/bin/env python3
"""Inspect the implemented OPH readout contract without importing the simulator.

Source inspection and finite-model observable closure do not establish physical
completeness. The finite checker assumes a supplied, exhaustive deterministic
state/transition table and a known sequence of scheduler labels.
"""
from __future__ import annotations

import argparse
import ast
from collections import deque
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "oph-observer-contract-v1"
LEGACY_REVISION = "d498af3926c98889531bca425565867409103a99"
SAMPLER = "scripts/oph_n2_flux_mc.py"
WAVE = "scripts/oph_efmw_continuum_demo.py"
SUMMARY = "scripts/summarize_oph_flux.py"


def _canonical(value: Any) -> str:
    """Reject non-JSON and nonfinite evidence; equality is explicit JSON equality."""
    def validate(item: Any) -> None:
        if isinstance(item, dict):
            if any(not isinstance(key, str) for key in item):
                raise ValueError("JSON object keys must be strings")
            for child in item.values():
                validate(child)
        elif isinstance(item, list):
            for child in item:
                validate(child)
        elif item is not None and type(item) not in (str, int, float, bool):
            raise ValueError("observable values must be JSON values")

    try:
        validate(value)
        return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError("observable values must be finite JSON values") from exc


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _function(tree: ast.AST, qualified_name: str) -> ast.FunctionDef:
    current = tree
    for name in qualified_name.split("."):
        matches = [node for node in getattr(current, "body", [])
                   if isinstance(node, ast.FunctionDef) and node.name == name]
        if len(matches) != 1:
            raise ValueError(f"expected one function {qualified_name}")
        current = matches[0]
    if not isinstance(current, ast.FunctionDef):
        raise ValueError(f"not a function: {qualified_name}")
    return current


def _expression(expr: str) -> str:
    return ast.dump(ast.parse(expr, mode="eval").body, include_attributes=False)


def _return_expr(function: ast.FunctionDef) -> ast.AST:
    matches = [n.value for n in function.body if isinstance(n, ast.Return)]
    if len(matches) != 1 or matches[0] is None:
        raise ValueError("expected exactly one top-level return expression")
    return matches[0]


def _assignment(function: ast.FunctionDef, name: str) -> ast.AST:
    matches = [node.value for node in function.body if isinstance(node, ast.Assign)
               and any(isinstance(target, ast.Name) and target.id == name
                       for target in node.targets)]
    if len(matches) != 1:
        raise ValueError(f"expected one assignment to {name}")
    return matches[0]


def _default(function: ast.FunctionDef, name: str) -> Any:
    names = [arg.arg for arg in function.args.args]
    defaults = dict(zip(names[len(names) - len(function.args.defaults):],
                        function.args.defaults))
    if name not in defaults:
        raise ValueError(f"missing default for {name}")
    return ast.literal_eval(defaults[name])


def audit_flux_geometry(source: str) -> dict[str, Any]:
    """Check a deliberately restricted AST contract for the shared F01 readout.

    This is a source-shape regression gate, not an arbitrary-Python semantics
    proof. Independent indexing and gauge tests are still required. Algebraic
    rewrites outside this contract fail closed and require review.
    """
    expected = {
        "oriented_product": "links[mu] * np.roll(links[nu], -1, axis=mu) * "
                            "np.conj(np.roll(links[mu], -1, axis=nu)) * np.conj(links[nu])",
        "averaged_axes": "tuple(axis for axis in range(4) if axis != transfer_axis)",
        "slice_readout": "np.imag(plaquette_product(links)).mean(axis=spatial_axes)",
        "direct_delegate": "spatial_flux_slices(np.exp(1j * theta))",
        "conditional_delegate": "spatial_flux_slices(r)",
    }
    checks: dict[str, bool] = {}
    observed: dict[str, Any] = {}
    try:
        tree = ast.parse(source)
        product = _function(tree, "plaquette_product")
        slices = _function(tree, "spatial_flux_slices")
        actual = {
            "oriented_product": _return_expr(product),
            "averaged_axes": _assignment(slices, "spatial_axes"),
            "slice_readout": _return_expr(slices),
            "direct_delegate": _return_expr(_function(tree, "run.flux_slice")),
            "conditional_delegate": _return_expr(_function(tree, "run.rb_flux_slice")),
        }
        for name, expression in actual.items():
            observed[name] = ast.unparse(expression)
            checks[name] = ast.dump(expression, include_attributes=False) == _expression(expected[name])
        defaults = [_default(product, "mu"), _default(product, "nu"),
                    _default(slices, "transfer_axis")]
        observed["default_mu_nu_transfer_axis"] = defaults
        checks["default_plane_and_separation"] = defaults == [0, 1, 3]
    except (SyntaxError, ValueError, TypeError) as exc:
        return {"status": "FAIL", "checks": checks, "observed": observed,
                "reason": str(exc), "scope": "restricted_static_readout_geometry"}
    return {"status": "PASS" if all(checks.values()) else "FAIL",
            "checks": checks, "observed": observed,
            "scope": "restricted_static_readout_geometry",
            "scope_limit": "Does not execute Python, prove estimator validity, or identify physical time."}


def inspect_source(root: Path, path: str, symbols: list[str]) -> dict[str, Any]:
    """Read only repository-relative regular files and fingerprint exact bytes."""
    root = root.resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        raise ValueError("source path leaves the repository")
    if not target.is_file():
        return {"path": path, "status": "UNRESOLVED", "reason": "source file absent"}
    raw = target.read_bytes()
    result: dict[str, Any] = {"path": path, "sha256": _sha(raw), "bytes": len(raw),
                              "status": "PASS", "symbols": []}
    try:
        source = raw.decode("utf-8")
        tree = ast.parse(source)
        for qualified_name in symbols:
            function = _function(tree, qualified_name)
            segment = ast.get_source_segment(source, function)
            if segment is None:
                raise ValueError(f"no source span for {qualified_name}")
            result["symbols"].append({"name": qualified_name, "line_start": function.lineno,
                                      "line_end": function.end_lineno,
                                      "source_sha256": _sha(segment.encode("utf-8"))})
    except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
        result.update(status="UNRESOLVED", reason=str(exc))
    return result


def _validate_finite_model(states: list[str], readback: dict[str, Any],
                           observables: dict[str, dict[str, Any]],
                           transitions: dict[str, dict[str, str]]) -> None:
    if (not isinstance(states, list) or not states
            or any(not isinstance(s, str) or not s for s in states)
            or len(set(states)) != len(states)):
        raise ValueError("states must be a nonempty list of unique nonempty strings")
    state_set = set(states)
    if not isinstance(readback, dict) or set(readback) != state_set:
        raise ValueError("readback must cover exactly the declared state set")
    if not isinstance(observables, dict) or not observables:
        raise ValueError("at least one declared observable is required")
    if not isinstance(transitions, dict) or not transitions:
        raise ValueError("at least one scheduler-labelled transition is required")
    for name, values in observables.items():
        if (not isinstance(name, str) or not name or not isinstance(values, dict)
                or set(values) != state_set):
            raise ValueError("each named observable must cover exactly the declared state set")
    for name, transition in transitions.items():
        if (not isinstance(name, str) or not name or not isinstance(transition, dict)
                or set(transition) != state_set
                or any(not isinstance(s, str) or s not in state_set for s in transition.values())):
            raise ValueError("each scheduler transition must be total and remain inside the state set")
    for values in [readback, *observables.values()]:
        for value in values.values():
            _canonical(value)


def audit_finite_observable_closure(states: list[str], readback: dict[str, Any],
                                   observables: dict[str, dict[str, Any]],
                                   transitions: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Decide all-finite-horizon observable determinacy in a supplied finite model.

    Partition refinement computes observational equivalence under all finite
    words in the known scheduler labels. A PASS means equal current readbacks
    imply equal future declared observables for every such common word. It does
    not say the readback determines the next readback, that the schedule is
    observable, or that these observables exhaust reality.
    """
    _validate_finite_model(states, readback, observables, transitions)
    states = sorted(states)
    names, labels = sorted(observables), sorted(transitions)
    values = {s: tuple(_canonical(observables[name][s]) for name in names) for s in states}

    def classify(signatures: dict[str, Any]) -> dict[str, int]:
        ids: dict[Any, int] = {}
        return {s: ids.setdefault(signatures[s], len(ids)) for s in states}

    partition = classify(values)
    rounds = 0
    while True:
        refined = classify({s: (partition[s], tuple(partition[transitions[label][s]]
                                                     for label in labels)) for s in states})
        if refined == partition:
            break
        partition = refined
        rounds += 1
    readback_classes: dict[str, list[str]] = {}
    for state in states:
        readback_classes.setdefault(_canonical(readback[state]), []).append(state)

    conflicts = []
    for group in readback_classes.values():
        anchor = group[0]
        for other in group[1:]:
            if partition[anchor] == partition[other]:
                continue
            # An explicit shortest distinguishing word, including length zero.
            queue = deque([(anchor, other, [])])
            seen = {(anchor, other)}
            while queue:
                left, right, word = queue.popleft()
                differing = [name for name in names
                             if _canonical(observables[name][left]) != _canonical(observables[name][right])]
                if differing:
                    conflicts.append({"same_readback_states": [anchor, other],
                                      "scheduler_word": word, "terminal_states": [left, right],
                                      "differing_observables": differing,
                                      "values": {name: [observables[name][left], observables[name][right]]
                                                 for name in differing}})
                    break
                for label in labels:
                    pair = (transitions[label][left], transitions[label][right])
                    if pair not in seen:
                        seen.add(pair)
                        queue.append((*pair, word + [label]))
            else:
                raise RuntimeError("refinement found a conflict without a distinguishing word")
    model = {"states": states, "readback": readback, "observables": observables,
             "transitions": transitions}
    return {"status": "PASS" if not conflicts else "FAIL",
            "scope": "all_finite_scheduler_words_of_declared_deterministic_model",
            "states": len(states), "observable_names": names, "scheduler_labels": labels,
            "model_sha256": _sha(_canonical(model).encode("utf-8")),
            "refinement_rounds": rounds, "behavior_classes": len(set(partition.values())),
            "counterexamples": conflicts, "physical_completeness": "UNRESOLVED",
            "assumptions": ["state table is exhaustive", "transition functions are supplied and total",
                            "future scheduler-label sequence is known", "declared observables are the tested scope"]}


def memory_counterexample() -> dict[str, Any]:
    """Four authored states show that law access is distinct from state access."""
    states = ["00", "01", "10", "11"]
    visible = {state: int(state[0]) for state in states}
    transitions = {"tick": {state: state[1] * 2 for state in states}}
    observables = {"visible_bit": visible}
    return {"model": "authored four-state illustration; not an OPH microscopic memory law",
            "law": "(visible,memory) -> (memory,memory)",
            "specification_is_known_in_both_cases": True,
            "visible_only": audit_finite_observable_closure(states, visible, observables, transitions),
            "declared_full_state_readback": audit_finite_observable_closure(
                states, {state: [int(state[0]), int(state[1])] for state in states}, observables, transitions)}


def build_contract(root: Path) -> dict[str, Any]:
    """Create a deterministic content-pinned receipt; no simulation is executed."""
    sources = [inspect_source(root, SAMPLER, ["run", "run.sweep", "run.flux_slice", "run.rb_flux_slice",
                                            "plaquette_product", "spatial_flux_slices"]),
               inspect_source(root, WAVE, ["test_resolution", "test_resolution.lap", "test_resolution.S"]),
               inspect_source(root, SUMMARY, ["estimate", "block_bootstrap"])]
    sampler_source = (root / SAMPLER).read_text() if (root / SAMPLER).is_file() else ""
    geometry = audit_flux_geometry(sampler_source)
    return {
        "schema_version": SCHEMA_VERSION,
        "baseline_revision": LEGACY_REVISION,
        "verifier_source": {"path": "scripts/oph_observer_contract.py",
                            "sha256": _sha(Path(__file__).read_bytes())},
        "source_pin_semantics": "sha256 fields identify inspected working-source bytes; baseline is historical context",
        "access_policy": {"simulator_specs": "allowed", "observer_implementation": "allowed",
                          "scheduler_implementation": "allowed", "repair_law": "allowed", "memory_law": "allowed"},
        "sources": sources,
        "source_introspection_status": "PASS" if all(s["status"] == "PASS" for s in sources) else "UNRESOLVED",
        "finite_flux_geometry": geometry,
        "implementation_inventory": [
            {"component": "finite_simulator_spec", "status": "IMPLEMENTED_AUTHORED_MODEL", "source": SAMPLER,
             "description": "Complex matter, U(1) links, Gamma conductances on a periodic four-coordinate lattice."},
            {"component": "measurement_observer", "status": "IMPLEMENTED_AUTHORED_READOUT", "source": SAMPLER,
             "description": "Direct and conditional F01 flux slices; readout function is not a biological observer model."},
            {"component": "scheduler", "status": "IMPLEMENTED_SAMPLER_SCHEDULE", "source": SAMPLER,
             "description": "Red/black site updates followed by link and conductance updates, warmup and thinning; sweeps are sampler time."},
            {"component": "repair_law", "status": "IMPLEMENTED_SUBSTITUTE_CONDITIONAL_KERNELS", "source": SAMPLER,
             "description": "The authored Gibbs updates do not instantiate a source-selected canonical OPH accepted-repair law."},
            {"component": "measurement_storage", "status": "IMPLEMENTED_TRANSIENT_RECORDS", "source": SAMPLER,
             "description": "obs/rb_obs append slice arrays; CLI serializes a run. This does not prove protected microscopic memory."},
            {"component": "canonical_memory_law", "status": "UNRESOLVED",
             "description": "No canonical OPH memory-law implementation is instantiated in this audited source set."},
            {"component": "reversible_wave_law", "status": "IMPLEMENTED_AUTHORED_MODEL", "source": WAVE,
             "description": "A supplied leapfrog wave rule retains two field layers and uses a manufactured source; not derived from OPH repairs."},
        ],
        "finite_observer_counterexample": memory_counterexample(),
        "completeness": {
            "status": "UNRESOLVED", "all_natures_observables_explained": False,
            "unresolved": ["source-selected microscopic repair and protected-memory laws",
                           "canonical simulator/observer implementation correspondence",
                           "physical clock and dimensional calibration",
                           "physical particle identity and observed mass attachment",
                           "interacting quantum continuum and gravity bridge premises",
                           "a justified exhaustive physical observable inventory and independent empirical tests"],
            "reason": "Source accessibility and finite observer closure are scoped evidence; neither entails universal physical completeness."},
        "legacy_readout": {
            "revision": LEGACY_REVISION, "status": "QUARANTINED_FOR_INTENDED_F01_AXIS3_CLAIMS",
            "actual_slice_axis": 0, "actual_roll_axes": [1, 2], "intended_slice_axis": 3,
            "intended_roll_axes": [0, 1],
            "reason": "Indexing theta[mu] removed the direction axis before coordinate rolls; averaging axes 1,2,3 left coordinate 0.",
            "historical_summary": "docs/data/oph_n2_flux_stage3_summary.csv",
            "historical_summary_relabelled": False},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path, help="check a frozen receipt against current source bytes")
    args = parser.parse_args()
    contract = build_contract(args.repo)
    serialized = json.dumps(contract, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.check:
        try:
            recorded = json.loads(args.check.read_text())
            recorded_canonical = _canonical(recorded)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            parser.exit(2, f"receipt cannot be read: {exc}\n")
        if recorded_canonical != _canonical(contract):
            parser.exit(1, "receipt differs from current source or contract; review and regenerate explicitly\n")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    elif not args.check:
        print(serialized, end="")
    if contract["source_introspection_status"] != "PASS" or contract["finite_flux_geometry"]["status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
