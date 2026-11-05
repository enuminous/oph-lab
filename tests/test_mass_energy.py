import json
import math
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oph_mass_energy import (  # noqa: E402
    ClockCalibration, HBAR_J_S, JOULES_PER_GEV, LIGHT_SPEED_M_S,
    benchmark_receipt, conditional_physical_readout, finite_mode_covariance,
    gaussian_readout, lattice_omega, periodic_effective_gaps, transfer_gap,
    transfer_precision,
)


class MassEnergyTests(unittest.TestCase):
    def test_direct_precision_reconstructs_gaussian_gaps(self):
        receipt = benchmark_receipt()
        self.assertTrue(receipt["passed"])
        self.assertEqual(len(receipt["cases"]), 15)
        json.dumps(receipt, allow_nan=False)

    def test_precision_matches_action_and_is_positive(self):
        q = np.array([0.2, -1.3, 0.8, 1.2, -0.6])
        precision = transfer_precision(0.3, 1.7, len(q))
        action = (0.3 * (q @ q) + 1.7 * np.sum((np.roll(q, -1) - q) ** 2)) / 2
        self.assertAlmostEqual(float(q @ precision @ q / 2), float(action), places=13)
        self.assertGreater(float(np.linalg.eigvalsh(precision).min()), 0)
        covariance = finite_mode_covariance(0.3, 1.7, len(q))
        source = np.array([1, 0, 0, 0, 0])
        np.testing.assert_allclose(precision @ covariance, source, atol=1e-14)

    def test_gap_is_not_bare_mass(self):
        gap = transfer_gap(1.0, 1.0, (1, 1, 1), (0, 0, 0))
        self.assertAlmostEqual(gap, 2 * math.asinh(0.5))
        self.assertNotAlmostEqual(gap, 1.0)
        self.assertAlmostEqual(4 * math.sinh(gap / 2) ** 2, 1.0)

    def test_tiny_positive_anchor_does_not_cancel_to_zero(self):
        gap = transfer_gap(1e-24, 1.0, (1, 1, 1), (0, 0, 0))
        self.assertGreater(gap, 0)
        self.assertAlmostEqual(gap / 1e-12, 1.0)

    def test_positive_momentum_raises_gap(self):
        base = transfer_gap(0.2, 1.0, (1, 1, 1), (0, 0, 0))
        moving = transfer_gap(0.2, 1.0, (1, 1, 1), (math.pi / 2, 0, 0))
        self.assertGreater(moving, base)

    def test_invalid_parameters_fail_closed(self):
        for value in (-1, 0, float("nan"), float("inf"), True, np.bool_(True), "1", None, 1j):
            with self.subTest(value=value), self.assertRaises(ValueError):
                transfer_gap(value, 1, (1, 1, 1), (0, 0, 0))
        with self.assertRaises(ValueError):
            transfer_gap(1, 0, (1, 1, 1), (0, 0, 0))
        with self.assertRaises(ValueError):
            lattice_omega(1, (1, 1), (0, 0))
        with self.assertRaises(ValueError):
            lattice_omega(1, (1, -1, 1), (0, 0, 0))
        with self.assertRaises(ValueError):
            transfer_precision(0.2, 1, 2)

    def test_bad_correlator_is_not_clipped_into_mass(self):
        self.assertIsNone(periodic_effective_gaps([2, -1, 1, 0.5])[1])
        self.assertIsNone(periodic_effective_gaps([1, 3, 1, 0.5])[1])
        self.assertIsNone(periodic_effective_gaps([1, 1, 1])[0])
        with self.assertRaises(ValueError):
            periodic_effective_gaps([1, float("nan"), 1])

    def calibration(self, **overrides):
        values = dict(seconds_per_transfer_step=2e-20,
                      clock_reference="test fixture: supplied clock",
                      spectral_bridge_reference="test fixture: supplied transfer/Hamiltonian bridge",
                      independent_of_mass_target=True)
        values.update(overrides)
        return ClockCalibration(**values)

    def test_no_calibration_emits_no_physical_mass(self):
        result = gaussian_readout()["physical"]
        self.assertEqual(result["status"], "unresolved")
        self.assertIsNone(result["energy_J"])
        self.assertIsNone(result["rest_mass_kg"])

    def test_conditional_units_and_target_independence(self):
        calibration = self.calibration()
        result = conditional_physical_readout(0.7, calibration, zero_momentum=True)
        expected = HBAR_J_S * 0.7 / 2e-20
        self.assertAlmostEqual(result["energy_J"] / expected, 1.0)
        self.assertAlmostEqual(result["energy_GeV"] / (expected / JOULES_PER_GEV), 1.0)
        self.assertAlmostEqual(result["rest_mass_kg"] / (expected / LIGHT_SPEED_M_S ** 2), 1.0)
        self.assertEqual(result["status"], "conditional_unit_conversion")
        self.assertFalse(result["evidence_verified_by_code"])
        self.assertEqual(result["physical_particle_identification"], "unresolved")

    def test_nonzero_momentum_energy_is_not_rest_mass(self):
        result = gaussian_readout(momentum_angles=(0.1, 0, 0), calibration=self.calibration())
        self.assertFalse(result["zero_momentum"])
        self.assertIsNotNone(result["physical"]["energy_J"])
        self.assertIsNone(result["physical"]["rest_mass_kg"])

    def test_calibration_rejects_sweeps_missing_refs_and_mass_fits(self):
        invalid = [dict(coordinate_kind="sampler_sweeps"),
                   dict(clock_reference=""), dict(spectral_bridge_reference=" "),
                   dict(independent_of_mass_target=False),
                   dict(independent_of_mass_target=1),
                   dict(seconds_per_transfer_step="1"),
                   dict(seconds_per_transfer_step=True),
                   dict(seconds_per_transfer_step=float("nan")),
                   dict(seconds_per_transfer_step=0)]
        for overrides in invalid:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                conditional_physical_readout(0.7, self.calibration(**overrides), zero_momentum=True)


if __name__ == "__main__":
    unittest.main()
