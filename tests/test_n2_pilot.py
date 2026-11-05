"""Pilot diagnostics controls; synthetic data test algorithms, never particles."""
from copy import deepcopy
import json
import importlib.util
from pathlib import Path
import tempfile
import unittest
import shutil
import numpy as np
from scripts.oph_n2_flux_mc import run
from scripts.oph_particle_readouts import periodic_cosh_values, screen_channel
from scripts.run_oph_n2_pilot import DEFAULT_CONFIG, ROOT, execute, sha, validate_config, write_json
from scripts.analyze_oph_n2_pilot import (
    autocorrelation, connected, diagnostic, features, paired_bootstrap,
    rank_folded_split_rhat, load_pilot, replay_differences,
)


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(DEFAULT_CONFIG.read_text())

    def test_transfer_extent_boundary_is_ten_not_eight(self):
        for period in (8, 10, 12):
            curve = periodic_cosh_values(period, [(1, .4)])
            result = screen_channel({k: (v, v, v) for k, v in curve.items()}, period=period)
            self.assertEqual(result['candidate_gap'] is not None, period >= 10)
            if period == 8:
                self.assertIn('transfer_extent_too_small_for_frozen_window', result['reasons'])

    def test_replay_allows_roundoff_but_rejects_small_signal_changes(self):
        expected = {'signal': [1e-11, -1e-16], 'covariance': 2e-24}
        rounded = {'signal': [1e-11*(1+1e-13), -1e-16*(1-1e-13)], 'covariance': 2e-24*(1+1e-13)}
        self.assertEqual(replay_differences(expected, rounded), [])
        changed = deepcopy(expected); changed['signal'][0] += 1e-18
        self.assertTrue(replay_differences(expected, changed))
        changed = deepcopy(expected); changed['covariance'] = 0.0
        self.assertTrue(replay_differences(expected, changed))
        self.assertTrue(replay_differences(float('nan'), float('nan')))

    def test_replay_requires_exact_decisions_provenance_and_structure(self):
        expected = {'status': 'unresolved', 'sha256': 'abc', 'count': 4, 'gap': None, 'lags': [1, 2]}
        for key, value in [('status', 'candidate'), ('sha256', 'abd'), ('count', 4.0),
                           ('gap', 0.0), ('lags', [1])]:
            changed = deepcopy(expected); changed[key] = value
            self.assertTrue(replay_differences(expected, changed))
        changed = deepcopy(expected); changed['extra'] = 0
        self.assertTrue(replay_differences(expected, changed))

    def test_frozen_plan_rejects_geometry_protocol_budget_and_seed_mutants(self):
        self.assertEqual(validate_config(self.config)['total_sweeps'], 6144)
        mutants = []
        c = deepcopy(self.config); c['model']['L'] = 8; mutants.append(c)
        c = deepcopy(self.config); c['chains'][1]['seed'] = c['chains'][0]['seed']; mutants.append(c)
        c = deepcopy(self.config); c['sampling']['samples'] = 512; mutants.append(c)
        c = deepcopy(self.config); c['limits']['max_total_sweeps'] = 1; mutants.append(c)
        c = deepcopy(self.config); c['analysis']['centers'] = [1, 2, 3]; mutants.append(c)
        c = deepcopy(self.config); c['analysis']['max_relative_gap_spread'] = .5; mutants.append(c)
        c = deepcopy(self.config); c['analysis']['block_lengths'] = [0, 16, 64]; mutants.append(c)
        c = deepcopy(self.config); c['chains'][1]['start'] = 'hot'; mutants.append(c)
        for c in mutants:
            with self.assertRaises(ValueError):
                validate_config(c)

    def test_runner_will_not_replace_an_existing_directory(self):
        with tempfile.TemporaryDirectory() as d:
            sentinel = Path(d)/'unchanged'; sentinel.write_text('keep')
            with self.assertRaises(FileExistsError):
                execute(DEFAULT_CONFIG, Path(d))
            self.assertEqual(sentinel.read_text(), 'keep')

    def test_sampler_diagnostics_replay_and_start_are_recorded(self):
        kwargs = dict(L=4, N=2, seed=10, warmup=2, samples=16, thin=1, diagnostics=True)
        hot, cold, replay = run(**kwargs), run(**kwargs, start='cold'), run(**kwargs)
        self.assertEqual(hot['measurement_diagnostics'], replay['measurement_diagnostics'])
        self.assertEqual(hot['sampled_slice_series'], replay['sampled_slice_series'])
        self.assertNotEqual(hot['sampled_slice_series'], cold['sampled_slice_series'])
        self.assertEqual([x['sweep'] for x in hot['warmup_diagnostics']], [0, 2])
        self.assertEqual(cold['warmup_diagnostics'][0]['psi_norm2_per_site'], 0)
        self.assertEqual(cold['raw_schema_version'], 'oph-flux-chain-v3')
        self.assertIsNone(cold['rao_blackwell_correlator'][0])

    def test_diagnostic_instrumentation_preserves_archived_corrected_chain(self):
        path = ROOT/'experiments/oph_n2/sources/oph_n2_flux_mc_smoke_20261105.py'
        spec = importlib.util.spec_from_file_location('archived_corrected_sampler', path)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        kwargs = dict(L=4, N=2, seed=71, warmup=4, samples=8, thin=2)
        baseline, instrumented = old.run(**kwargs), run(**kwargs, diagnostics=True)
        for field in ('sampled_slice_series', 'rao_blackwell_slice_series',
                      'correlator', 'rao_blackwell_correlator'):
            self.assertEqual(baseline[field], instrumented[field])

    def test_iid_and_ar1_autocorrelation_have_known_scale(self):
        rng = np.random.default_rng(11)
        iid = autocorrelation(rng.normal(size=65536))
        self.assertAlmostEqual(iid['tau_int_measurements'], .5, delta=.06)
        noise = rng.normal(size=66536)
        ar = np.zeros_like(noise)
        for t in range(1, len(ar)):
            ar[t] = .8*ar[t-1] + noise[t]
        result = autocorrelation(ar[1000:])
        # Exact stationary AR(1): tau_int=(1+phi)/(2*(1-phi))=4.5.
        self.assertAlmostEqual(result['tau_int_measurements'], 4.5, delta=.8)
        self.assertLess(result['ess'], iid['ess']/5)
        self.assertEqual(autocorrelation(np.ones(1024))['status'], 'unresolved')

    def test_rhat_detects_location_and_scale_failures(self):
        rng = np.random.default_rng(19)
        iid = rng.normal(size=(4, 4096))
        self.assertLess(rank_folded_split_rhat(iid), 1.01)
        shifted = iid.copy(); shifted[0] += 3
        scaled = iid.copy(); scaled[0] *= 5
        self.assertGreater(rank_folded_split_rhat(shifted), 1.1)
        self.assertGreater(rank_folded_split_rhat(scaled), 1.1)
        self.assertIsNone(rank_folded_split_rhat(np.ones((4, 1024))))
        report = diagnostic(shifted, self.config['analysis'], 1)
        self.assertIn('rank_folded_split_rhat', report['reasons'])

    def test_connected_estimator_is_invariant_to_constant_flux_offset(self):
        rng = np.random.default_rng(24)
        x = rng.normal(size=(4, 64, 12))
        def make(offset):
            return [{'sampled_slice_series': row+offset, 'rao_blackwell_slice_series': row+offset} for row in x]
        a = connected(features(make(0)).mean(axis=(0, 1)))
        b = connected(features(make(10)).mean(axis=(0, 1)))
        np.testing.assert_allclose(a, b, atol=5e-14)

    def test_bootstrap_preserves_direct_rb_pairing_and_replays(self):
        rng = np.random.default_rng(51)
        one = rng.normal(size=(4, 64, 6))
        f = np.concatenate((one, one), axis=2)
        a = paired_bootstrap(f, 8, 100, 40)
        np.testing.assert_array_equal(a, paired_bootstrap(f, 8, 100, 40))
        np.testing.assert_array_equal(a[:, 0], a[:, 1])
        self.assertGreater(np.std(a[:, 0, 0]), 0)
        for block in (0, 3, 64):
            with self.assertRaises(ValueError):
                paired_bootstrap(f, block, 100, 40)

    def test_archived_pilot_loads_but_changed_or_incomplete_evidence_fails(self):
        source = ROOT/'docs/data/oph_n2_pilot_v1'
        c, m, runs = load_pilot(source)
        self.assertEqual(len(runs), 4)
        self.assertEqual(c['model']['L'], 12)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'pilot'
            shutil.copytree(source, target)
            manifest = deepcopy(m); manifest['status'] = 'incomplete'
            write_json(target/'manifest.json', manifest)
            with self.assertRaisesRegex(ValueError, 'Incomplete'):
                load_pilot(target)
            write_json(target/'manifest.json', m)
            raw_path = target/m['runs'][0]['path']
            raw_path.write_text(raw_path.read_text() + '\n')
            with self.assertRaisesRegex(ValueError, 'changed raw'):
                load_pilot(target)
            # Even if someone refreshes a content digest, protocol/schema checks
            # independently reject a legacy observable, lost diagnostics or contact.
            for mutation in ('legacy', 'short', 'nan', 'contact', 'model', 'warmup'):
                raw = deepcopy(runs[0])
                if mutation == 'legacy': raw.pop('readout_version')
                if mutation == 'short': raw['sampled_slice_series'].pop()
                if mutation == 'nan': raw['measurement_diagnostics'][0]['mean_conductance'] = float('nan')
                if mutation == 'contact': raw['rao_blackwell_correlator'][0] = 0.0
                if mutation == 'model': raw['model']['m2'] = 2.0
                if mutation == 'warmup': raw['warmup_diagnostics'].pop()
                raw_path.write_text(json.dumps(raw))
                manifest = deepcopy(m); manifest['runs'][0]['sha256'] = sha(raw_path)
                write_json(target/'manifest.json', manifest)
                with self.assertRaises(ValueError):
                    load_pilot(target)


if __name__ == '__main__':
    unittest.main()
