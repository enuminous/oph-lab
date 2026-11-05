"""Independent controls for finite tomography and gravity evidence boundaries."""
from fractions import Fraction as F
import json
import random
import unittest

from scripts.oph_gravity_requirements import (
    METRIC, NULL_DIRECTIONS, REQUIREMENTS, add_metric, conservation_diagnostic,
    demo_receipt, evaluate_requirements, null_contractions, null_design,
    reconstruct_modulo_metric, tomography_rank,
)


class GravityTomographyTests(unittest.TestCase):
    def test_nine_directions_have_exactly_metric_ambiguity(self):
        self.assertEqual(tomography_rank()["rank"], 9)
        self.assertEqual(tomography_rank()["nullity"], 1)
        self.assertEqual(null_contractions(METRIC), [0] * 9)
        self.assertFalse(tomography_rank()["identifies_full_tensor"])

    def test_axes_do_not_measure_spatial_shear(self):
        shear = [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(tomography_rank(NULL_DIRECTIONS[:6])["rank"], 6)
        self.assertEqual(null_contractions(shear, NULL_DIRECTIONS[:6]), [0] * 6)
        self.assertNotEqual(null_contractions(shear), [0] * 9)

    def test_arbitrary_rational_tensors_reconstruct_modulo_metric(self):
        rng = random.Random(20261105)
        for _ in range(25):
            tensor = [[F(0)] * 4 for _ in range(4)]
            for i in range(4):
                for j in range(i, 4):
                    tensor[i][j] = tensor[j][i] = F(rng.randrange(-20, 21), rng.randrange(1, 8))
            readings = null_contractions(tensor)
            result = reconstruct_modulo_metric(readings)
            # Independent expected gauge fixing: H + H00*eta has H00=0.
            self.assertEqual(result, add_metric(tensor, tensor[0][0]))
            self.assertEqual(readings, null_contractions(add_metric(tensor, F(13, 7))))
            self.assertEqual(result[0][0], 0)

    def test_not_every_ten_component_input_is_symmetric_tensor(self):
        invalid = [[0] * 4 for _ in range(4)]
        invalid[0][1] = 1
        with self.assertRaises(ValueError):
            null_contractions(invalid)

    def test_nullness_not_assumed_by_label(self):
        for invalid in [((1, 1, 1, 0),), ((0, 0, 0, 0),), ((1, 1, 0),)]:
            with self.assertRaises(ValueError):
                null_design(invalid)

    def test_invalid_numbers_rejected(self):
        for invalid in [float("nan"), float("inf"), True]:
            tensor = [[0] * 4 for _ in range(4)]
            tensor[0][0] = invalid
            with self.assertRaises(ValueError):
                null_contractions(tensor)
        with self.assertRaises(ValueError):
            reconstruct_modulo_metric([0] * 8)


class GravityConservationTests(unittest.TestCase):
    def test_conservation_does_not_select_constant(self):
        edges = [(0, 1), (1, 2)]
        for constant in [F(-17, 2), 0, 31]:
            result = conservation_diagnostic([constant] * 3, edges)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["undetermined_constants"], 1)
            self.assertFalse(result["determines_constant_value"])

    def test_varying_scalar_fails(self):
        result = conservation_diagnostic([1, 2, 1], [(0, 1), (1, 2)])
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["edge_residuals"], ["1", "-1"])

    def test_disconnected_domain_retains_extra_freedom(self):
        result = conservation_diagnostic([1, 1, 8], [(0, 1)])
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["connected"])
        self.assertEqual(result["undetermined_constants"], 2)

    def test_invalid_domain_rejected(self):
        for values, edges in [([], []), ([1], [(0, 1)]), ([1], [(True, 0)])]:
            with self.assertRaises(ValueError):
                conservation_diagnostic(values, edges)


class GravityEvidenceTests(unittest.TestCase):
    def records(self):
        return {name: {"status": "demonstrated", "artifact": "example://unverified-test-fixture",
                       "same_family": True, "target_independent": True} for name in REQUIREMENTS}

    def test_missing_evidence_fails_closed(self):
        result = evaluate_requirements()
        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertFalse(result["manifest_complete"])
        self.assertFalse(result["physical_gravity_established"])
        self.assertIsNone(result["G_SI"])
        self.assertIsNone(result["Lambda_m_minus_2"])

    def test_complete_attestations_are_only_ready_for_review(self):
        result = evaluate_requirements(self.records())
        self.assertEqual(result["status"], "READY_FOR_REVIEW")
        self.assertFalse(result["physical_gravity_established"])

    def test_missing_lineage_or_target_leak_blocks(self):
        for key, bad in [("artifact", ""), ("same_family", False), ("target_independent", False)]:
            records = self.records()
            records["stress_vacuum"][key] = bad
            self.assertIn("stress_vacuum", evaluate_requirements(records)["blockers"])

    def test_rejected_selected_premise_rejects_branch(self):
        records = self.records()
        records["nine_direction_balances"]["status"] = "rejected"
        self.assertEqual(evaluate_requirements(records)["status"], "REJECTED")

    def test_routes_do_not_silently_substitute(self):
        records = self.records()
        del records["tensor_curvature_limit"]
        self.assertEqual(evaluate_requirements(records, route="tensor_limit")["status"], "UNRESOLVED")
        self.assertEqual(evaluate_requirements(records, route="null_balance")["status"], "READY_FOR_REVIEW")
        del records["bounded_interval_transport"]
        self.assertEqual(evaluate_requirements(records, route="bw_null_balance")["status"], "UNRESOLVED")

    def test_no_numeric_certificates_or_unrecognized_premises(self):
        for bad in [{"stress_vacuum": True}, {"made_up_premise": {"status": "demonstrated"}}]:
            with self.assertRaises(ValueError):
                evaluate_requirements(bad)

    def test_receipt_is_finite_json(self):
        receipt = demo_receipt()
        self.assertTrue(receipt["tomography"]["shifted_readings_identical"])
        self.assertRegex(receipt["implementation_sha256"], r"^[0-9a-f]{64}$")
        json.dumps(receipt, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
