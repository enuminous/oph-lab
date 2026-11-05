#!/usr/bin/env python3
"""Exploratory, autocorrelation-aware finite-channel pilot receipt; fail closed.

Sampler time is used only for Monte Carlo diagnostics. Transfer lag is a
different coordinate. No diagnostic or cosh screen certifies physical particles.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import json
import math
from pathlib import Path
import numpy as np
from scipy.special import ndtri
from scipy.stats import rankdata

if __package__:
    from .oph_particle_readouts import DEFAULT_POLICY, screen_channel
    from .run_oph_n2_pilot import ROOT, sha, validate_config, write_json
    from .summarize_oph_flux import validate_runs
else:
    from oph_particle_readouts import DEFAULT_POLICY, screen_channel
    from run_oph_n2_pilot import ROOT, sha, validate_config, write_json
    from summarize_oph_flux import validate_runs

SCALARS = ('psi_norm2_per_site', 'mean_conductance', 'matter_link_action_per_site',
           'real_plaquette_mean')
ESTIMATORS = ('direct', 'rao_blackwell')
FIELDS = ('sampled_slice_series', 'rao_blackwell_slice_series')
REPLAY_REL_TOL = 1e-10
REPLAY_ABS_TOL = 1e-30


def replay_differences(expected, actual, path='$'):
    """Exact structure/categories/hashes; bounded floating-point roundoff only.

    The tiny absolute floor cannot swallow the ~1e-11 RB correlator signal.
    This tolerance never changes a sampler or classifier decision threshold.
    """
    if type(expected) is not type(actual):
        return [f'{path}: type mismatch']
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            return [f'{path}: key mismatch']
        return [d for key in expected for d in replay_differences(expected[key], actual[key], f'{path}.{key}')]
    if isinstance(expected, list):
        if len(expected) != len(actual):
            return [f'{path}: length mismatch']
        return [d for i, (left, right) in enumerate(zip(expected, actual))
                for d in replay_differences(left, right, f'{path}[{i}]')]
    if isinstance(expected, float):
        equal = (math.isfinite(expected) and math.isfinite(actual)
                 and math.isclose(expected, actual, rel_tol=REPLAY_REL_TOL, abs_tol=REPLAY_ABS_TOL))
    else:
        equal = expected == actual
    return [] if equal else [f'{path}: {expected!r} != {actual!r}']


def autocorrelation(x):
    """FFT autocovariance, biased 1/n normalization, self-consistent W>=6 tau.

    tau_int = 1/2 + sum_{k=1}^W rho(k); ESS = n/(2 tau_int).
    Clipping tau_int>=1/2 conservatively caps ESS at n. Unfound windows and
    zero variance fail closed. Short-chain estimates can miss slow modes.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or len(x) < 16 or not np.isfinite(x).all():
        raise ValueError('Need a finite scalar chain of length >=16')
    n = len(x)
    y = x - x.mean()
    variance = float(np.dot(y, y) / n)
    if variance <= 0:
        return {'status': 'unresolved', 'reason': 'zero_variance', 'tau_int_measurements': None,
                'ess': None, 'window': None, 'acf': []}
    f = np.fft.rfft(y, n=1 << (2*n-1).bit_length())
    acov = np.fft.irfft(f * f.conj())[:n] / n
    rho = acov / acov[0]
    tau = 0.5
    window = None
    for w in range(1, n//4 + 1):
        tau = max(0.5, float(0.5 + rho[1:w+1].sum()))
        if w >= 6*tau:
            window = w
            break
    return {'status': 'estimated' if window is not None else 'unresolved',
            'reason': None if window is not None else 'autocorrelation_window_unresolved',
            'tau_int_measurements': tau, 'ess': n/(2*tau), 'window': window,
            'mean': float(x.mean()), 'standard_deviation': float(np.sqrt(variance)),
            'acf': rho[:min(65, n)].tolist()}


def rank_folded_split_rhat(chains):
    """Maximum of rank-normalized split Rhat and folded split Rhat."""
    x = np.asarray(chains, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 16 or not np.isfinite(x).all():
        raise ValueError('Need >=2 finite chains and >=16 samples')
    half = x.shape[1]//2
    split = np.concatenate((x[:, :half], x[:, -half:]), axis=0)

    def one(v):
        ranks = rankdata(v.ravel(), method='average').reshape(v.shape)
        z = ndtri((ranks - 3/8) / (v.size + 1/4))
        within = float(np.var(z, axis=1, ddof=1).mean())
        if within <= 0:
            return None
        between = half * float(np.var(z.mean(axis=1), ddof=1))
        return float(np.sqrt(((half-1)/half * within + between/half) / within))

    rank = one(split)
    folded = one(np.abs(split - np.median(split)))
    return None if rank is None or folded is None else max(rank, folded)


def diagnostic(chains, a, thin):
    x = np.asarray(chains, float)
    ac = [autocorrelation(row) for row in x]
    rhat = rank_folded_split_rhat(x)
    reasons = []
    if rhat is None or rhat > a['max_rank_folded_split_rhat']:
        reasons.append('rank_folded_split_rhat')
    if any(r['status'] != 'estimated' for r in ac):
        reasons.append('autocorrelation_unresolved')
    taus = [r['tau_int_measurements'] for r in ac]
    ess = [r['ess'] for r in ac]
    if any(t is None or len(x[0]) < a['minimum_chain_length_tau_int']*t for t in taus):
        reasons.append('chain_too_short_relative_to_tau')
    if any(e is None or e < a['minimum_ess_per_chain'] for e in ess):
        reasons.append('per_chain_ess')
    total_ess = None if any(e is None for e in ess) else sum(ess)
    if total_ess is None or total_ess < a['minimum_total_ess']:
        reasons.append('total_ess')
    if any(t is None or max(a['block_lengths']) < a['minimum_largest_block_tau_int']*t for t in taus):
        reasons.append('largest_block_too_short_relative_to_tau')
    half_drift = []
    for row in x:
        half = len(row)//2
        left, right = row[:half], row[-half:]
        da, db = autocorrelation(left), autocorrelation(right)
        if da['status'] != 'estimated' or db['status'] != 'estimated':
            half_drift.append(None)
            continue
        error = np.sqrt(np.var(left, ddof=1)/da['ess'] + np.var(right, ddof=1)/db['ess'])
        half_drift.append(float(abs(left.mean()-right.mean())/error) if error > 0 else None)
    if any(z is None or z > a['max_half_chain_drift_standard_errors'] for z in half_drift):
        reasons.append('half_chain_drift')
    for row in ac:
        row['tau_int_sweeps'] = (None if row['tau_int_measurements'] is None
                                  else row['tau_int_measurements']*thin)
    return {'status': 'diagnostics_pass_only' if not reasons else 'unresolved',
            'reasons': reasons, 'rank_folded_split_rhat': rhat,
            'estimated_total_ess': total_ess,
            'half_chain_drift_standard_errors': half_drift, 'chains': ac}


def features(runs):
    """Paired mean flux and noncontact products, retaining all lag covariances."""
    out = []
    for run in runs:
        columns = []
        for field in FIELDS:
            x = np.asarray(run[field], float)
            columns.append(x.mean(axis=1))
            columns.extend(np.mean(x*np.roll(x, -lag, axis=1), axis=1) for lag in range(1, 6))
        out.append(np.stack(columns, axis=1))
    return np.asarray(out)


def connected(feature_mean):
    v = np.asarray(feature_mean)
    return np.stack((v[..., 1:6] - v[..., 0, None]**2,
                     v[..., 7:12] - v[..., 6, None]**2), axis=-2)


def paired_bootstrap(f, block, reps, seed):
    """Resample chains and circular moving blocks; recompute pooled mean².

    Identical resampling indices for both estimators and all lags preserve their
    covariance. Bootstrap replicates are not independent simulations.
    """
    f = np.asarray(f, float)
    if (f.ndim != 3 or f.shape[0] < 2 or f.shape[2] != 12 or not np.isfinite(f).all()
            or type(block) is not int or block < 1 or f.shape[1] < 2*block
            or f.shape[1] % block or type(reps) is not int or reps < 2):
        raise ValueError('Need paired finite features and >=2 full blocks/chains/replicates')
    nc, n, _ = f.shape
    extended = np.concatenate((f, f[:, :block-1]), axis=1)
    sums = np.concatenate((np.zeros((nc, 1, 12)), np.cumsum(extended, axis=1)), axis=1)
    block_means = (sums[:, block:] - sums[:, :-block])/block
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(reps):
        picks = rng.integers(nc, size=nc)
        starts = rng.integers(n, size=(nc, n//block))
        means = block_means[picks[:, None], starts].mean(axis=(0, 1))
        out.append(connected(means))
    return np.asarray(out)


def load_pilot(directory):
    c = json.loads((directory / 'config.json').read_text())
    validate_config(c)
    manifest = json.loads((directory / 'manifest.json').read_text())
    if (manifest.get('status') != 'complete'
            or manifest.get('schema_version') != 'oph-n2-pilot-manifest-v1'
            or manifest['config_sha256'] != sha(directory / 'config.json')
            or manifest['experiment_id'] != c['experiment_id']
            or len(manifest['runs']) != len(c['chains'])):
        raise ValueError('Incomplete pilot or changed configuration')
    runs = []
    if len({r['path'] for r in manifest['runs']}) != len(c['chains']):
        raise ValueError('Duplicate raw paths')
    for entry, expected in zip(manifest['runs'], c['chains']):
        path = directory / entry['path']
        if path.parent != directory or sha(path) != entry['sha256']:
            raise ValueError('Invalid path or changed raw data')
        r = json.loads(path.read_text())
        m, s = r['model'], r['sampler']
        if (r.get('raw_schema_version') != 'oph-flux-chain-v3'
                or r['provenance']['implementation_sha256'] != manifest['source_sha256']['scripts/oph_n2_flux_mc.py']
                or m != {'L': c['model']['L'], 'dimension': 4, 'N': c['model']['N'],
                         'alpha_gamma_shape': c['model']['alpha'], 'beta_gamma_rate': c['model']['beta'],
                         'm2': c['model']['m2'], 'volume': c['model']['L']**4}
                or s['seed'] != expected['seed'] or s['initialization'] != expected['start']
                or entry['seed'] != expected['seed'] or entry['start'] != expected['start']
                or s['warmup_sweeps'] != c['sampling']['warmup']
                or s['measurements'] != c['sampling']['samples']
                or s['sweeps_between_measurements'] != c['sampling']['thin']
                or not s['diagnostics_recorded']
                or r['rao_blackwell_correlator'][0] is not None):
            raise ValueError('Raw run does not match frozen plan/schema/source/contact rule')
        if len(r['measurement_diagnostics']) != s['measurements']:
            raise ValueError('Missing measurement diagnostics')
        monitors = np.asarray([[row[k] for k in SCALARS] for row in r['measurement_diagnostics']])
        if not np.isfinite(monitors).all():
            raise ValueError('Nonfinite diagnostics')
        trace = r['warmup_diagnostics']
        expected_steps = [0] + list(range(16, s['warmup_sweeps']+1, 16))
        if expected_steps[-1] != s['warmup_sweeps']:
            expected_steps.append(s['warmup_sweeps'])
        if ([row['sweep'] for row in trace] != expected_steps
                or not np.isfinite([[row[k] for k in SCALARS] for row in trace]).all()):
            raise ValueError('Missing or malformed warmup trace')
        runs.append(r)
    validate_runs(runs)
    return c, manifest, runs


def analyze(c, manifest, runs):
    a = c['analysis']
    f = features(runs)
    mean = f.mean(axis=(0, 1))
    point = connected(mean)
    monitored = {k: np.asarray([[row[k] for row in r['measurement_diagnostics']]
                                for r in runs]) for k in SCALARS}
    for ei, estimator in enumerate(ESTIMATORS):
        start = ei*6
        monitored[f'{estimator}.mean_flux'] = f[..., start]
        for lag in range(1, 6):
            monitored[f'{estimator}.product_lag{lag}'] = f[..., start+lag]
            # Linearized connected-correlator fluctuations; mean subtraction
            # must not hide slow modes or correlations with the mean flux.
            monitored[f'{estimator}.connected_influence_lag{lag}'] = (
                f[..., start+lag] - 2*mean[start]*f[..., start])
    diagnostics = {name: diagnostic(x, a, c['sampling']['thin']) for name, x in monitored.items()}
    blocks = []
    bootstrap_draws = []
    for block in a['block_lengths']:
        draws = paired_bootstrap(f, block, a['bootstrap_replicates'], a['bootstrap_seed']+block)
        bootstrap_draws.append(draws)
        blocks.append({'block_length_measurements': block,
                       'full_blocks_per_chain': f.shape[1]//block,
                       'pointwise_95_percentiles': np.quantile(draws, [.025, .975], axis=0).tolist(),
                       'standard_errors': np.std(draws, axis=0, ddof=1).tolist(),
                       'covariance_direct_then_rb_lags1to5': np.cov(draws.reshape(len(draws), 10), rowvar=False).tolist()})
    ses = np.asarray([b['standard_errors'] for b in blocks])
    se_ratio = np.divide(ses.max(axis=0), ses.min(axis=0),
                         out=np.full((2, 5), np.inf), where=ses.min(axis=0)>0)
    intervals = np.asarray([b['pointwise_95_percentiles'] for b in blocks])
    # Expanding to include the point avoids invalid triples under bootstrap bias;
    # preserve original quantiles above. No simultaneous coverage is asserted.
    lower = np.minimum(intervals[:, 0].min(axis=0), point)
    upper = np.maximum(intervals[:, 1].max(axis=0), point)
    reasons = [f'diagnostic:{k}' for k, v in diagnostics.items() if v['reasons']]
    if not np.isfinite(se_ratio).all() or (se_ratio > a['max_block_standard_error_ratio']).any():
        reasons.append('block_standard_errors_unstable')
    differences = point[0] - point[1]
    difference_se = np.max([np.std(d[:, 0]-d[:, 1], axis=0, ddof=1) for d in bootstrap_draws], axis=0)
    paired_z = np.divide(abs(differences), difference_se, out=np.full(5, np.inf), where=difference_se>0)
    if (paired_z > a['max_direct_rb_difference_standard_errors']).any():
        reasons.append('direct_rb_paired_disagreement')
    channels = {}
    for ei, name in enumerate(ESTIMATORS):
        triples = {lag: (point[ei, lag-1], lower[ei, lag-1], upper[ei, lag-1]) for lag in range(1, 6)}
        screen = screen_channel(triples, period=c['model']['L'], source=c['experiment_id']+':'+name)
        channels[name] = {'correlator': {str(lag): list(row) for lag, row in triples.items()},
                          'shape_screen_only': screen,
                          'per_chain_connected_correlators': connected(f.mean(axis=1))[:, ei].tolist(),
                          'numerically_eligible_shape_candidate': not reasons and screen['candidate_gap'] is not None}
    return {'schema_version': 'oph-n2-pilot-analysis-v2', 'experiment_id': c['experiment_id'],
            'replay_comparison': {'float_relative_tolerance': REPLAY_REL_TOL,
                                  'float_absolute_tolerance': REPLAY_ABS_TOL,
                                  'nonfloat_fields': 'exact',
                                  'scope': 'platform_roundoff_only_not_statistical_tolerance'},
            'scope': 'exploratory_sampling_and_shape_screen_not_spectral_or_physical_identification',
            'config_sha256': manifest['config_sha256'], 'raw_runs': manifest['runs'],
            'analysis_sha256': sha(Path(__file__)),
            'classifier_sha256': sha(ROOT/'scripts/oph_particle_readouts.py'),
            'summary_validator_sha256': sha(ROOT/'scripts/summarize_oph_flux.py'),
            'policy': asdict(DEFAULT_POLICY), 'diagnostic_thresholds': a,
            'numerical_diagnostics_status': 'diagnostics_pass_only' if not reasons else 'unresolved',
            'numerical_reasons': reasons, 'diagnostics': diagnostics, 'block_bootstrap': blocks,
            'block_standard_error_ratios': [[None if not np.isfinite(v) else float(v) for v in row] for row in se_ratio],
            'paired_direct_rb_difference': differences.tolist(),
            'paired_direct_rb_difference_standard_errors': difference_se.tolist(),
            'paired_direct_rb_z': [None if not np.isfinite(v) else float(v) for v in paired_z],
            'channels': channels, 'primary_estimator': a['primary_estimator'],
            'uncertainty': 'Exploratory pointwise 95% block-bootstrap percentiles, enveloped across block lengths and expanded to contain point. No simultaneous coverage; direct/RB are paired, not independent replications.',
            'stable_transfer_gap': 'unresolved', 'volume_stability': 'unresolved',
            'spectral_reconstruction': 'unresolved', 'physical_particle_identification': 'unresolved',
            'physical_mass': None, 'no_pole_exclusion': False,
            'remaining': ['independent longer-chain replication and thermalization assessment',
                          'second and larger volumes; finite-volume and transfer-extent control',
                          'reflection positivity/operator parity and transfer reconstruction',
                          'multi-operator/threshold/dispersion evidence',
                          'interacting continuum, calibrated physical clock and empirical identification']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--check', type=Path, help='Recompute and compare a stored deterministic receipt')
    args = p.parse_args()
    c, manifest, runs = load_pilot(args.directory)
    receipt = analyze(c, manifest, runs)
    if args.check:
        differences = replay_differences(json.loads(args.check.read_text()),
                                        json.loads(json.dumps(receipt, allow_nan=False)))
        if differences:
            p.error('Analysis receipt differs beyond roundoff; preserve/review evidence: '
                    + '; '.join(differences[:8]))
    if args.output:
        if args.output.exists():
            p.error('Refusing to replace existing analysis; choose a new path')
        write_json(args.output, receipt)
    print(json.dumps({'experiment_id': receipt['experiment_id'],
                      'numerical_diagnostics_status': receipt['numerical_diagnostics_status'],
                      'numerical_reasons': receipt['numerical_reasons'],
                      'channels': {k: v['shape_screen_only']['finite_channel_status'] for k, v in receipt['channels'].items()},
                      'physical_particle_identification': 'unresolved'}, indent=2))


if __name__ == '__main__':
    main()
