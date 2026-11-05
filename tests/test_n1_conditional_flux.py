"""Independent finite one-species identities; no source or Lean claim."""
import unittest

import numpy as np
from scipy.special import i0e, i1e

from scripts.oph_n2_flux_mc import plaquette_product, run, spatial_flux_slices


def conditional_link_means(fields, weights):
    """Construct link moments from site fields; fields includes a species axis."""
    means, radii = [], []
    for mu in range(4):
        q = np.sum(np.conj(fields) * np.roll(fields, -1, axis=mu + 1), axis=0)
        kappa = 2 * weights[mu] * np.abs(q)
        radius = i1e(kappa) / i0e(kappa)
        means.append(radius * np.exp(-1j * np.angle(q)))
        radii.append(radius)
    return np.asarray(means), np.asarray(radii)


class OneSpeciesFluxTests(unittest.TestCase):
    def test_link_mean_matches_direct_original_boltzmann_integral(self):
        theta = -np.pi + 2*np.pi*np.arange(8192)/8192
        u = np.exp(1j*theta)
        for left, right, weight in [(0.7+0.2j, -0.3+0.9j, 1.2),
                                     (1.1-0.8j, .4+.5j, .2), (0j, 1+2j, 3.)]:
            with self.subTest(left=left, right=right):
                cost = weight * np.abs(left-u*right)**2
                density = np.exp(-(cost-cost.min()))
                direct = np.sum(density*u)/np.sum(density)
                q = np.conj(left)*right
                kappa = 2*weight*abs(q)
                formula = i1e(kappa)/i0e(kappa)*np.exp(-1j*np.angle(q))
                self.assertLess(abs(direct-formula), 5e-15)

    def test_every_conditional_plaquette_is_real_including_zero_corners(self):
        rng = np.random.default_rng(20261105)
        fields = rng.normal(size=(1, 4, 4, 4, 4)) + 1j*rng.normal(size=(1, 4, 4, 4, 4))
        fields[0, 0, 1, 2, 3] = 0
        fields[0, 3, 0, 1, 2] = 0
        weights = rng.uniform(.1, 2., size=(4, 4, 4, 4, 4))
        means, radii = conditional_link_means(fields, weights)
        actual = plaquette_product(means)
        expected = (radii[0]*np.roll(radii[1], -1, axis=0)
                    *np.roll(radii[0], -1, axis=1)*radii[1])
        np.testing.assert_allclose(actual.real, expected, atol=4e-16, rtol=2e-15)
        self.assertLess(float(np.max(np.abs(actual.imag))), 4e-16)
        self.assertLess(float(np.max(np.abs(spatial_flux_slices(means)))), 1e-16)
        self.assertEqual(actual[0, 1, 2, 3], 0)

    def test_distinct_axis3_slices_use_disjoint_conditional_link_variables(self):
        extent = 4
        link_sets = []
        for t in range(extent):
            links = set()
            for x0, x1, x2 in np.ndindex((extent,)*3):
                links.update([(0, x0, x1, x2, t),
                              (1, (x0+1) % extent, x1, x2, t),
                              (0, x0, (x1+1) % extent, x2, t),
                              (1, x0, x1, x2, t)])
            self.assertEqual(len(links), 2*extent**3)
            link_sets.append(links)
        for t in range(extent):
            for s in range(t+1, extent):
                self.assertTrue(link_sets[t].isdisjoint(link_sets[s]))

    def test_raw_flux_configuration_can_be_maximal(self):
        links = np.ones((4, 4, 4, 4, 4), dtype=complex)
        links[1] = np.exp(1j*np.pi*np.arange(4)[:, None, None, None]/2)
        np.testing.assert_allclose(plaquette_product(links), 1j, atol=4e-16)
        np.testing.assert_allclose(spatial_flux_slices(links), 1., atol=1e-15)

    def test_actual_n1_sampler_has_zero_conditional_flux_but_fluctuating_raw_flux(self):
        result = run(L=4, N=1, warmup=4, samples=8, thin=1, seed=20261105)
        conditional = np.asarray(result['rao_blackwell_slice_series'])
        raw = np.asarray(result['sampled_slice_series'])
        self.assertLess(float(np.max(np.abs(conditional))), 1e-14)
        self.assertGreater(float(np.max(np.abs(raw))), 1e-3)
        self.assertIsNone(result['rao_blackwell_correlator'][0])
        self.assertTrue(all(abs(value) < 1e-27
                            for value in result['rao_blackwell_correlator'][1:]))

    def test_one_species_phase_argument_does_not_extend_to_two_species(self):
        fields = np.zeros((2, 4, 4, 4, 4), dtype=complex)
        fields[0] = 1
        fields[:, 0, 0, 0, 0] = (1, 0)
        fields[:, 1, 0, 0, 0] = (1, 1)
        fields[:, 1, 1, 0, 0] = (1, 1j)
        fields[:, 0, 1, 0, 0] = (1, 0)
        means, _ = conditional_link_means(fields, np.ones((4, 4, 4, 4, 4)))
        product = plaquette_product(means)[0, 0, 0, 0]
        self.assertLess(product.imag, -.1)


if __name__ == '__main__':
    unittest.main()
