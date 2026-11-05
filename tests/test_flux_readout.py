"""Geometry and gauge regressions independent of Monte Carlo sampling."""
import unittest
from copy import deepcopy
import numpy as np
from scripts.oph_n2_flux_mc import plaquette_product, spatial_flux_slices, run
from scripts.summarize_oph_flux import validate_runs, block_bootstrap


class FluxReadoutTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(105)
        self.shape = (4, 5, 6, 7)
        self.links = np.exp(1j * self.rng.normal(size=(4,) + self.shape))

    def test_wilson_loop_is_invariant_under_local_gauge_transformation(self):
        phase = np.exp(1j * self.rng.normal(size=self.shape))
        transformed = np.stack([
            phase * self.links[mu] * np.conj(np.roll(phase, -1, axis=mu))
            for mu in range(4)])
        np.testing.assert_allclose(plaquette_product(self.links),
                                   plaquette_product(transformed), atol=2e-15)

    def test_independent_index_loop_and_correct_slice_axis(self):
        expected = np.zeros(self.shape, dtype=complex)
        for x in np.ndindex(self.shape):
            xp0 = list(x); xp0[0] = (x[0] + 1) % self.shape[0]
            xp1 = list(x); xp1[1] = (x[1] + 1) % self.shape[1]
            expected[x] = (self.links[(0,) + x] * self.links[(1,) + tuple(xp0)]
                           * np.conj(self.links[(0,) + tuple(xp1)])
                           * np.conj(self.links[(1,) + x]))
        np.testing.assert_allclose(plaquette_product(self.links), expected)
        slices = spatial_flux_slices(self.links)
        self.assertEqual(slices.shape, (7,))
        np.testing.assert_allclose(slices, expected.imag.mean(axis=(0, 1, 2)))

    def test_orientation_reversal_conjugates_loop(self):
        np.testing.assert_allclose(plaquette_product(self.links, 1, 0),
                                   np.conj(plaquette_product(self.links)), atol=2e-15)

    def test_legacy_formula_fails_gauge_control(self):
        phase = np.exp(1j * self.rng.normal(size=self.shape))
        changed = np.stack([phase * self.links[mu] *
                            np.conj(np.roll(phase, -1, axis=mu)) for mu in range(4)])
        def legacy(u):
            return u[0] * np.roll(u[1], -1, axis=1) * np.conj(
                np.roll(u[0], -1, axis=2)) * np.conj(u[1])
        self.assertGreater(float(np.max(np.abs(legacy(changed) - legacy(self.links)))), 0.1)

    def test_small_run_replays_with_separate_sampler_and_transfer_coordinates(self):
        kwargs = dict(L=4, N=1, warmup=2, samples=3, thin=1, seed=42)
        first, second = run(**kwargs), run(**kwargs)
        self.assertEqual(first['sampled_slice_series'], second['sampled_slice_series'])
        self.assertEqual(first['readout_version'], 'F01-axis3-v2')
        self.assertFalse(first['provenance']['physical_time_identified'])
        self.assertIsNone(first['rao_blackwell_correlator'][0])
        self.assertEqual(np.asarray(first['sampled_slice_series']).shape, (3, 4))

    def test_invalid_run_parameters_rejected(self):
        for kw in ({'samples': 0}, {'thin': 0}, {'warmup': -1}, {'alpha': np.nan}, {'L': 4.0}):
            with self.assertRaises(ValueError):
                run(**kw)

    def test_summary_rejects_legacy_mixed_models_and_duplicate_seeds(self):
        a = run(L=4, N=1, warmup=0, samples=3, thin=1, seed=2)
        b = run(L=4, N=1, warmup=0, samples=3, thin=1, seed=3)
        validate_runs([a, b])
        legacy = deepcopy(b); legacy.pop('readout_version')
        other_model = deepcopy(b); other_model['model']['m2'] = 2
        other_axis = deepcopy(b); other_axis['provenance']['transfer_axis'] = 0
        for candidate in (legacy, other_model, other_axis, a):
            with self.assertRaises(ValueError):
                validate_runs([a, candidate])

    def test_bootstrap_rejects_short_single_chain_and_contact(self):
        short = np.ones((3, 4))
        adequate = np.ones((400, 4))
        for chains, lag, block, reps in (([short, short], 1, 50, 20),
                ([adequate], 1, 50, 20), ([adequate, adequate], 0, 50, 20),
                ([adequate, adequate], 1, 0, 20), ([adequate, adequate], 1, 50, 1)):
            with self.assertRaises(ValueError):
                block_bootstrap(chains, lag, block, reps, 1)


if __name__ == '__main__':
    unittest.main()
