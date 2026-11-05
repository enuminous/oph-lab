#!/usr/bin/env python3
"""Frozen, bounded, serial pilot runner. Never replaces an existing directory."""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import time

if __package__:
    from .oph_n2_flux_mc import run
    from .oph_particle_readouts import DEFAULT_POLICY
else:
    from oph_n2_flux_mc import run
    from oph_particle_readouts import DEFAULT_POLICY

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / 'experiments/oph_n2/pilot_v1.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def validate_config(c):
    if c.get('schema_version') != 'oph-n2-pilot-v1':
        raise ValueError('Unsupported pilot configuration')
    m, s, a = c['model'], c['sampling'], c['analysis']
    if (type(m['L']) is not int or m['L'] < 10 or m['L'] % 2 or m['N'] != 2
            or any(type(m[k]) not in (int, float) or not 0 < m[k] < float('inf')
                   for k in ('alpha', 'beta', 'm2'))):
        raise ValueError('N2 with even L>=10 and finite positive model parameters required')
    if any(type(s[k]) is not int or s[k] < 1 for k in ('warmup', 'samples', 'thin')):
        raise ValueError('Positive integer sampling counts required')
    chains = c['chains']
    if (len(chains) < 4 or len({x['seed'] for x in chains}) != len(chains)
            or any(type(x['seed']) is not int or x['seed'] < 0 for x in chains)
            or any(x['start'] not in ('hot', 'cold') for x in chains)
            or sum(x['start'] == 'hot' for x in chains) < 2
            or sum(x['start'] == 'cold' for x in chains) < 2):
        raise ValueError('At least four distinct seeds and two of each hot/cold start required')
    policy = asdict(DEFAULT_POLICY)
    if (a['required_lags'] != [1, 2, 3, 4, 5] or a['centers'] != list(policy['centers'])
            or any(a[k] != policy[k] for k in ('max_relative_gap_spread', 'max_relative_envelope_width'))
            or a['primary_estimator'] != 'rao_blackwell'):
        raise ValueError('Frozen particle policy/primary estimator may not silently change')
    blocks = a['block_lengths']
    if (not isinstance(blocks, list) or len(blocks) < 3
            or any(type(b) is not int or b < 1 for b in blocks)
            or blocks != sorted(set(blocks))
            or type(a['minimum_blocks_per_chain']) is not int or a['minimum_blocks_per_chain'] < 16
            or s['samples'] < max(blocks) * a['minimum_blocks_per_chain']
            or any(s['samples'] % b for b in blocks)
            or type(a['bootstrap_replicates']) is not int or a['bootstrap_replicates'] < 1000
            or type(a['bootstrap_seed']) is not int or a['bootstrap_seed'] < 0):
        raise ValueError('Need >=16 complete blocks per chain at each of >=3 block sizes and >=1000 replicates')
    for key in ('max_rank_folded_split_rhat', 'minimum_ess_per_chain', 'minimum_total_ess',
                'minimum_chain_length_tau_int', 'minimum_largest_block_tau_int',
                'max_block_standard_error_ratio', 'max_half_chain_drift_standard_errors',
                'max_direct_rb_difference_standard_errors'):
        if type(a[key]) not in (int, float) or not 0 < a[key] < float('inf'):
            raise ValueError(f'Invalid diagnostic threshold: {key}')
    sweeps = len(chains) * (s['warmup'] + s['samples'] * s['thin'])
    updates = sweeps * 4 * m['L']**4
    if any(type(c['limits'][k]) is not int or c['limits'][k] < 1
           for k in ('max_total_sweeps', 'max_link_updates')):
        raise ValueError('Positive explicit compute caps required')
    if sweeps > c['limits']['max_total_sweeps'] or updates > c['limits']['max_link_updates']:
        raise ValueError('Plan exceeds frozen compute caps')
    return {'chains': len(chains), 'total_sweeps': sweeps, 'total_link_updates': updates,
            'volume': m['L']**4, 'transfer_extent': m['L'],
            'raw_slice_values': 2 * len(chains) * s['samples'] * m['L'],
            'scientific_scope': c['purpose']}


def execute(config_path, output):
    c = json.loads(config_path.read_text())
    budget = validate_config(c)
    # exist_ok=False protects all historical, smoke, and previous pilot directories.
    output.mkdir(parents=True, exist_ok=False)
    (output / 'config.json').write_bytes(config_path.read_bytes())
    source_paths = ['scripts/oph_n2_flux_mc.py', 'scripts/oph_particle_readouts.py',
                    'scripts/run_oph_n2_pilot.py', 'requirements-research.txt']
    manifest = {'schema_version': 'oph-n2-pilot-manifest-v1', 'status': 'running',
                'experiment_id': c['experiment_id'], 'config_sha256': sha(config_path),
                'source_sha256': {p: sha(ROOT / p) for p in source_paths},
                'git_parent_revision': subprocess.check_output(
                    ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'git_tree_dirty_at_start': bool(subprocess.check_output(
                    ['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()),
                'platform': platform.platform(), 'python_version': platform.python_version(),
                'budget': budget, 'runs': []}
    write_json(output / 'manifest.json', manifest)
    started = time.perf_counter()
    try:
        for chain in c['chains']:
            r = run(**c['model'], **c['sampling'], **chain, diagnostics=True)
            name = f"L{c['model']['L']}_N2_seed{chain['seed']}.json"
            write_json(output / name, r)
            manifest['runs'].append({'path': name, 'sha256': sha(output / name),
                                     'seed': chain['seed'], 'start': chain['start'],
                                     'elapsed_seconds': r['sampler']['total_elapsed_seconds']})
            write_json(output / 'manifest.json', manifest)
            print(f"Saved {name}: {r['sampler']['total_elapsed_seconds']:.2f}s", flush=True)
        if any(sha(ROOT / p) != h for p, h in manifest['source_sha256'].items()):
            raise ValueError('Source changed during sampling; incomplete evidence')
        manifest['status'] = 'complete'
    except BaseException:
        manifest['status'] = 'incomplete'
        raise
    finally:
        manifest['total_wall_seconds'] = time.perf_counter() - started
        write_json(output / 'manifest.json', manifest)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    p.add_argument('--output', type=Path)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    c = json.loads(args.config.read_text())
    budget = validate_config(c)
    if args.dry_run:
        print(json.dumps(budget, indent=2))
    elif args.output is None:
        p.error('--output required; use a new directory for every execution')
    else:
        execute(args.config, args.output)


if __name__ == '__main__':
    main()
