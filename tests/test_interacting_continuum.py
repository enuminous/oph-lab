"""Independent identities and failure controls for the supplied scalar model."""
import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oph_interacting_continuum import (build_receipt, energy_components, evolve,
                                        laplacian, manufactured_case)


class InteractingContinuumTests(unittest.TestCase):
    def test_periodic_eigenmode_uses_all_three_axes(self):
        n, h = 12, 2 * math.pi / 12
        x = np.arange(n) * h
        field = np.cos(x[:, None, None]) + np.sin(2*x[None, :, None]) + np.cos(3*x[None, None, :])
        expected = sum(-4 * math.sin(k*h/2)**2 / h**2 * term for k, term in [
            (1, np.cos(x[:, None, None])), (2, np.sin(2*x[None, :, None])),
            (3, np.cos(3*x[None, None, :]))])
        np.testing.assert_allclose(laplacian(field, h), expected, atol=5e-14)

    def test_force_is_negative_energy_gradient(self):
        rng = np.random.default_rng(20261105)
        field, direction = rng.normal(scale=.1, size=(6, 6, 6)), rng.normal(size=(6, 6, 6))
        velocity, h, m2, coupling = np.zeros_like(field), .3, .7, 2.
        epsilon = 1e-6
        plus = energy_components(field + epsilon*direction, velocity, h, 1., m2, coupling)["total"]
        minus = energy_components(field - epsilon*direction, velocity, h, 1., m2, coupling)["total"]
        gradient = -laplacian(field, h) + m2*field + coupling*field**3
        expected = h**3 * float(np.sum(gradient * direction))
        self.assertAlmostEqual((plus-minus)/(2*epsilon), expected, places=8)

    def test_free_uniform_mode_matches_analytic_oscillator(self):
        field = np.full((4, 4, 4), .4)
        result = evolve(field, np.zeros_like(field), spacing=1., final_time=.6,
                        time_step=.001, mass_squared=4., coupling=0.)
        np.testing.assert_allclose(result["field"], .4*math.cos(1.2), atol=1e-7)
        np.testing.assert_allclose(result["velocity"], -.8*math.sin(1.2), atol=4e-7)

    def test_constant_external_force_work_balance(self):
        zero = np.zeros((4, 4, 4))
        result = evolve(zero, zero, spacing=1., final_time=.5, time_step=.025,
                        mass_squared=0., coupling=0., source=lambda t: np.ones_like(zero)*.3)
        np.testing.assert_allclose(result["field"], .3*.5**2/2, atol=1e-15)
        np.testing.assert_allclose(result["velocity"], .3*.5, atol=1e-15)
        self.assertAlmostEqual(result["records"][-1]["total"],
                               result["records"][-1]["source_work"], places=12)

    def test_nonlinearity_affects_uniform_motion(self):
        field = np.full((4, 4, 4), .6)
        kw = dict(spacing=1., final_time=.3, time_step=.002, mass_squared=.7)
        linear = evolve(field, np.zeros_like(field), coupling=0., **kw)["field"]
        nonlinear = evolve(field, np.zeros_like(field), coupling=2., **kw)["field"]
        self.assertGreater(float(np.max(np.abs(linear-nonlinear))), .01)

    def test_reject_invalid_inputs_and_unstable_time_step(self):
        field = np.zeros((4, 4, 4))
        for changes in [{"time_step": float("nan")}, {"time_step": 1.},
                        {"coupling": -1.}, {"mass_squared": -1.}, {"spacing": 0.}]:
            kwargs = dict(spacing=.1, final_time=1., time_step=.001)
            kwargs.update(changes)
            with self.assertRaises(ValueError):
                evolve(field, field, **kwargs)
        with self.assertRaises(ValueError):
            laplacian(np.ones((4, 4)), 1.)
        with self.assertRaises(ValueError):
            laplacian(np.full((4, 4, 4), np.nan), 1.)
        with self.assertRaises(ValueError):
            laplacian(np.ones((4, 4, 4), dtype=complex), 1.)
        with self.assertRaises(ValueError):
            manufactured_case(4.5)

    def test_frozen_refinement_energy_and_omission_controls(self):
        receipt = build_receipt()
        self.assertTrue(all(receipt["checks"].values()), receipt["checks"])
        self.assertEqual(receipt["status"], "demonstrated")
        self.assertEqual(receipt["model"]["time_kind"], "supplied_model_time")
        self.assertIn("interacting quantum continuum and renormalization", receipt["unresolved"])


if __name__ == "__main__":
    unittest.main()
