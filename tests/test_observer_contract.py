"""Source/provenance failures and independent finite-observability controls."""
from itertools import combinations, product
import hashlib
from pathlib import Path
import random
import tempfile
import unittest

from scripts.oph_observer_contract import (
    SAMPLER, audit_finite_observable_closure, audit_flux_geometry,
    build_contract, inspect_source, memory_counterexample,
)


ROOT = Path(__file__).resolve().parents[1]


class SourceContractTests(unittest.TestCase):
    def test_corrected_geometry_and_shared_direct_conditional_readout(self):
        result = audit_flux_geometry((ROOT / SAMPLER).read_text())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["observed"]["default_mu_nu_transfer_axis"], [0, 1, 3])

    def test_changed_roll_axis_is_rejected(self):
        source = (ROOT / SAMPLER).read_text()
        self.assertIn("axis=mu", source)
        result = audit_flux_geometry(source.replace("axis=mu", "axis=1"))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["checks"]["oriented_product"])

    def test_wrong_retained_axis_is_rejected(self):
        source = (ROOT / SAMPLER).read_text()
        result = audit_flux_geometry(source.replace("transfer_axis=3", "transfer_axis=0"))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["checks"]["default_plane_and_separation"])

    def test_bypass_of_shared_readout_is_rejected(self):
        source = (ROOT / SAMPLER).read_text()
        result = audit_flux_geometry(source.replace("return spatial_flux_slices(r)", "return r"))
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["checks"]["conditional_delegate"])

    def test_missing_or_malformed_source_cannot_pass(self):
        for source in ("", "def run(:", "def run():\n    return {}\n"):
            self.assertEqual(audit_flux_geometry(source)["status"], "FAIL")

    def test_exact_hash_and_symbol_span_without_importing_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "source.py"
            raw = b"raise RuntimeError('must never run')\n\ndef observable():\n    return 7\n"
            path.write_bytes(raw)
            result = inspect_source(root, "source.py", ["observable"])
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(result["symbols"][0]["line_start"], 3)
            self.assertEqual(result["symbols"][0]["line_end"], 4)
            original = result["sha256"]
            path.write_bytes(raw.replace(b"return 7", b"return 8"))
            self.assertNotEqual(inspect_source(root, "source.py", ["observable"])["sha256"], original)
            self.assertEqual(inspect_source(root, "source.py", ["missing"])["status"], "UNRESOLVED")
            self.assertEqual(inspect_source(root, "absent.py", ["observable"])["status"], "UNRESOLVED")
            with self.assertRaises(ValueError):
                inspect_source(root, "../outside.py", [])

    def test_contract_distinguishes_specs_storage_and_physical_completeness(self):
        result = build_contract(ROOT)
        self.assertEqual(result["source_introspection_status"], "PASS")
        self.assertTrue(all(permission == "allowed" for permission in result["access_policy"].values()))
        inventory = {row["component"]: row for row in result["implementation_inventory"]}
        self.assertEqual(inventory["canonical_memory_law"]["status"], "UNRESOLVED")
        self.assertEqual(inventory["measurement_storage"]["status"], "IMPLEMENTED_TRANSIENT_RECORDS")
        self.assertEqual(result["completeness"]["status"], "UNRESOLVED")
        self.assertFalse(result["completeness"]["all_natures_observables_explained"])
        self.assertFalse(result["legacy_readout"]["historical_summary_relabelled"])


class FiniteObserverTests(unittest.TestCase):
    def test_known_law_without_hidden_state_access_does_not_predict_next_observable(self):
        result = memory_counterexample()
        self.assertTrue(result["specification_is_known_in_both_cases"])
        visible = result["visible_only"]
        self.assertEqual(visible["status"], "FAIL")
        self.assertEqual(visible["counterexamples"][0]["scheduler_word"], ["tick"])
        self.assertEqual(visible["counterexamples"][0]["values"]["visible_bit"], [0, 1])
        full = result["declared_full_state_readback"]
        self.assertEqual(full["status"], "PASS")
        self.assertEqual(full["physical_completeness"], "UNRESOLVED")

    def test_longer_horizon_alias_is_detected(self):
        states = ["a", "b", "c", "d", "e"]
        readback = {s: s for s in states}
        readback["b"] = "a"
        observable = {s: int(s == "e") for s in states}
        transition = {"a": "c", "b": "d", "c": "c", "d": "e", "e": "e"}
        result = audit_finite_observable_closure(states, readback, {"signal": observable}, {"step": transition})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["counterexamples"][0]["scheduler_word"], ["step", "step"])

    def test_unequal_microstates_may_be_observationally_equivalent(self):
        states = ["a", "b"]
        result = audit_finite_observable_closure(
            states, {s: 0 for s in states}, {"public_bit": {s: 1 for s in states}},
            {"swap": {"a": "b", "b": "a"}})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["behavior_classes"], 1)
        self.assertEqual(result["physical_completeness"], "UNRESOLVED")

    def test_zero_horizon_and_second_scheduler_are_checked(self):
        states = ["a", "b", "c"]
        readback = {"a": 0, "b": 0, "c": 1}
        obs = {"signal": {"a": 0, "b": 0, "c": 1}}
        schedules = {"stay": {s: s for s in states}, "reveal": {"a": "a", "b": "c", "c": "c"}}
        result = audit_finite_observable_closure(states, readback, obs, schedules)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["counterexamples"][0]["scheduler_word"], ["reveal"])
        obs["signal"]["b"] = 1
        result = audit_finite_observable_closure(states, readback, obs, schedules)
        self.assertEqual(result["counterexamples"][0]["scheduler_word"], [])

    def test_partial_state_or_schedule_tables_and_nonfinite_values_fail_closed(self):
        states = ["a", "b"]
        readback = {"a": 0, "b": 1}
        obs = {"bit": {"a": 0, "b": 1}}
        transitions = {"stay": {"a": "a", "b": "b"}}
        invalid = [
            ([], readback, obs, transitions),
            (["a", "a"], readback, obs, transitions),
            (states, {"a": 0}, obs, transitions),
            (states, readback, {}, transitions),
            (states, readback, {"bit": {"a": 0}}, transitions),
            (states, readback, obs, {}),
            (states, readback, obs, {"stay": {"a": "a"}}),
            (states, readback, obs, {"stay": {"a": "c", "b": "b"}}),
            (states, {"a": float("nan"), "b": 1}, obs, transitions),
            (states, readback, {"bit": {"a": 0, "b": float("inf")}}, transitions),
            (states, {"a": {1: "ambiguous JSON key"}, "b": 1}, obs, transitions),
        ]
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                audit_finite_observable_closure(*args)

    def test_partition_refinement_matches_independent_word_enumeration(self):
        rng = random.Random(5112026)
        states = ["a", "b", "c", "d"]
        for _ in range(40):
            readback = {s: rng.randrange(2) for s in states}
            observable = {s: rng.randrange(2) for s in states}
            transitions = {label: {s: rng.choice(states) for s in states} for label in ("x", "y")}
            result = audit_finite_observable_closure(states, readback, {"signal": observable}, transitions)
            distinguishable = False
            # A finite deterministic n-state model stabilizes in at most n-1 refinements.
            for left, right in combinations(states, 2):
                if readback[left] != readback[right]:
                    continue
                for length in range(len(states)):
                    for word in product(transitions, repeat=length):
                        x, y = left, right
                        for label in word:
                            x, y = transitions[label][x], transitions[label][y]
                        if observable[x] != observable[y]:
                            distinguishable = True
            self.assertEqual(result["status"] == "FAIL", distinguishable)


if __name__ == "__main__":
    unittest.main()
