#!/usr/bin/env python3
"""Small timing-only probes, isolated processes; no spectral measurements."""
import argparse
import json
import os
from pathlib import Path
import platform
import resource
import statistics
import subprocess
import sys

if __package__:
    from .oph_n2_flux_mc import run
    from .run_oph_n2_pilot import ROOT, sha, write_json
else:
    from oph_n2_flux_mc import run
    from run_oph_n2_pilot import ROOT, sha, write_json


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path)
    p.add_argument('--worker-L', type=int)
    p.add_argument('--seed', type=int)
    args = p.parse_args()
    if args.worker_L:
        r = run(L=args.worker_L, N=2, seed=args.seed, warmup=16, samples=32, thin=1,
                diagnostics=True)
        s = r['sampler']
        print(json.dumps({'L': args.worker_L, 'seed': args.seed,
                          'warmup_sweeps': 16, 'measurements': 32,
                          'warmup_seconds_per_sweep_including_initialization': s['warmup_elapsed_seconds']/16,
                          'measurement_seconds_per_sweep_including_readouts': s['elapsed_seconds']/32,
                          'total_seconds': s['total_elapsed_seconds'],
                          'peak_process_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
        return
    if args.output is None or args.output.exists():
        p.error('--output must be a new file')
    rows = []
    for size in (10, 12, 16):
        probes = [json.loads(subprocess.check_output(
            [sys.executable, str(Path(__file__)), '--worker-L', str(size),
             '--seed', str(20261105800+size*10+j)], text=True)) for j in range(3)]
        warm = [x['warmup_seconds_per_sweep_including_initialization'] for x in probes]
        measure = [x['measurement_seconds_per_sweep_including_readouts'] for x in probes]
        row = {'L': size, 'volume': size**4, 'probes': probes,
               'warmup_seconds_per_sweep_median': statistics.median(warm),
               'measurement_seconds_per_sweep_median': statistics.median(measure),
               'measurement_seconds_per_sweep_range': [min(measure), max(measure)],
               'projected_four_chain_pilot_seconds': 4*(512*statistics.median(warm)+1024*statistics.median(measure)),
               'projected_four_chain_long_run_seconds': 4*(2048*statistics.median(warm)+8192*statistics.median(measure)),
               'raw_state_bytes_lower_bound': (16*2+8*4+8*4)*size**4}
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'probes'}), flush=True)
    write_json(args.output, {'schema_version': 'oph-n2-timing-v1',
                             'scope': 'timing_only_no_spectral_evidence',
                             'platform': platform.platform(), 'machine': platform.machine(),
                             'python_version': platform.python_version(), 'visible_cpus': os.cpu_count(),
                             'source_sha256': sha(ROOT/'scripts/oph_n2_flux_mc.py'),
                             'benchmark_sha256': sha(Path(__file__)), 'rows': rows,
                             'limits': 'Short timings include readout/diagnostic cost and cold-start process effects. No scaling, mixing, effective-sample or hardware guarantee; reserve 2x wall-time margin. RSS is peak per isolated process on Linux, not an extrapolated full-run bound.'})


if __name__ == '__main__':
    main()
