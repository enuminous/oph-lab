import importlib.util
import math
from pathlib import Path
import sys
import unittest

MODULE = Path(__file__).resolve().parents[1]/"scripts/oph_particle_readouts.py"
SPEC = importlib.util.spec_from_file_location("oph_particle_readouts", MODULE)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)


class ParticleReadoutTests(unittest.TestCase):
    def exact(self, energy=0.4, period=16):
        return {t: (v, v, v) for t, v in m.periodic_cosh_values(period, [(1.0, energy)]).items()}

    def test_recovers_declared_cosh_gap_without_identifying_species(self):
        result = m.screen_channel(self.exact(), period=16)
        self.assertEqual(result["finite_channel_status"], "single_cosh_shape_candidate")
        self.assertAlmostEqual(result["candidate_gap"], 0.4, places=13)
        self.assertIsNone(result["physical_particle_name"])
        self.assertEqual(result["physical_particle_identification"], "unresolved")

    def test_contact_contamination_cannot_select_gap(self):
        data = self.exact()
        data[0] = (-1e10, -1e10, -1e10)
        result = m.screen_channel(data, period=16)
        self.assertFalse(result["contact_lag_used"])
        self.assertAlmostEqual(result["candidate_gap"], 0.4, places=13)

    def test_positive_but_curved_mixture_fails_fixed_plateau(self):
        data = {t: (v, v, v) for t, v in m.periodic_cosh_values(16, [(1.0, 0.15), (8.0, 1.2)]).items()}
        result = m.screen_channel(data, period=16)
        self.assertIn("effective_gap_not_stable_in_frozen_window", result["reasons"])
        self.assertIsNone(result["candidate_gap"])

    def test_no_signal_is_not_evidence_for_no_pole(self):
        data = {t: (0.0, -1.0, 1.0) for t in range(9)}
        result = m.screen_channel(data, period=16)
        self.assertEqual(result["finite_channel_status"], "unresolved")
        self.assertFalse(result["no_pole_exclusion"])
        self.assertEqual(result["effective_gaps"], [])

    def test_wide_intervals_do_not_make_stable_point_estimates_pass(self):
        data = {t: (v[0], 0.5*v[0], 1.5*v[0]) for t, v in self.exact().items()}
        result = m.screen_channel(data, period=16)
        self.assertEqual(result["finite_channel_status"], "unresolved")
        self.assertIn("gap_not_separated_from_zero", result["reasons"])

    def test_constant_correlator_does_not_identify_massless_particle(self):
        result = m.screen_channel(self.exact(energy=0), period=16)
        self.assertIn("gap_not_separated_from_zero", result["reasons"])

    def test_extreme_constant_values_do_not_create_a_false_gap(self):
        for value in (1e308, 1e-320, 5e-324):
            with self.subTest(value=value):
                data = {t: (value, value, value) for t in range(9)}
                result = m.screen_channel(data, period=16)
                self.assertEqual(result["finite_channel_status"], "unresolved")
                self.assertIsNone(result["candidate_gap"])
                self.assertFalse(result["no_pole_exclusion"])

    def test_missing_neighbor_fails_closed(self):
        data = self.exact()
        del data[3]
        result = m.screen_channel(data, period=16)
        self.assertEqual(result["missing_lags"], [3])
        self.assertIsNone(result["candidate_gap"])

    def test_invalid_interval_and_nan_rejected(self):
        for triple in [(1, 2, 3), (math.nan, 0, 1), (1, 0, math.inf)]:
            with self.subTest(triple=triple), self.assertRaises(ValueError):
                m.screen_channel({1: triple}, period=16)

    def test_policies_cannot_touch_contact_or_postselect_disjoint_centers(self):
        for centers in [(1, 2, 3), (2, 4, 6), (2, 3)]:
            with self.subTest(centers=centers), self.assertRaises(ValueError):
                m.screen_channel(self.exact(), period=16, policy=m.ScreenPolicy(centers=centers))

    def test_envelope_contains_independent_perturbed_cosh_gaps(self):
        exact = self.exact()
        data = {t: (v[0], 0.999*v[0], 1.001*v[0]) for t, v in exact.items()}
        result = m.screen_channel(data, period=16)
        for row in result["effective_gaps"]:
            t = row["lag"]
            for a in (-1, 1):
                for b in (-1, 1):
                    for c in (-1, 1):
                        left = exact[t-1][0]*(1+a*0.001)
                        middle = exact[t][0]*(1+b*0.001)
                        right = exact[t+1][0]*(1+c*0.001)
                        gap = math.acosh((left+right)/(2*middle))
                        self.assertLessEqual(row["lower_envelope"], gap+1e-14)
                        self.assertGreaterEqual(row["upper_envelope"], gap-1e-14)

    def test_published_stage3_stays_unresolved(self):
        path = MODULE.parents[1]/"docs/data/oph_n2_flux_stage3_summary.csv"
        results = m.summarize_stage3(path)
        self.assertEqual(len(results), 12)
        for result in results:
            self.assertEqual(result["finite_channel_status"], "unresolved")
            self.assertFalse(result["no_pole_exclusion"])
            self.assertIsNone(result["candidate_gap"])
            self.assertEqual(result["provenance_status"], "quarantined_axis_mismatch")
            self.assertIn("legacy_operator_provenance_mismatch", result["reasons"])


if __name__ == "__main__":
    unittest.main()
