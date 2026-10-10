#!/usr/bin/env python3
"""Summarize independent OPH flux-MC JSON runs with chain/block bootstrap CIs."""
import argparse, csv, json
from pathlib import Path
import numpy as np


def estimate(chains, lag):
    means=[x.mean() for x in chains]
    q=[np.mean(x*np.roll(x,-lag,axis=1),axis=1) for x in chains]
    return float(np.mean(np.concatenate(q))-np.mean(means)**2)


def block_bootstrap(chains, lag, block, reps, seed):
    q=[np.mean(x*np.roll(x,-lag,axis=1),axis=1) for x in chains]
    rng=np.random.default_rng(seed); out=[]; nc=len(chains)
    for _ in range(reps):
        picks=rng.integers(0,nc,nc); means=[]; products=[]
        for ix in picks:
            x=chains[ix]; v=q[ix]; n=len(v); k=int(np.ceil(n/block))
            starts=rng.integers(0,n,k)
            ind=np.concatenate([(s+np.arange(block))%n for s in starts])[:n]
            means.append(x[ind].mean()); products.append(v[ind].mean())
        out.append(np.mean(products)-np.mean(means)**2)
    return np.quantile(out,[.025,.975])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('directory',type=Path)
    p.add_argument('--output',type=Path,default=Path('oph_flux_summary.csv'))
    p.add_argument('--reps',type=int,default=500)
    a=p.parse_args()
    groups={}
    for path in a.directory.glob('L*_N*_seed*.json'):
        r=json.loads(path.read_text()); m=r['model']
        groups.setdefault((m['N'],m['L']),[]).append(r)
    rows=[]
    for (N,L), runs in sorted(groups.items()):
        runs.sort(key=lambda r:r['sampler']['seed'])
        for estimator,field in [('direct','sampled_slice_series'),('rao_blackwell','rao_blackwell_slice_series')]:
            chains=[np.asarray(r[field],float) for r in runs]
            for d in range(1,L//2+1):
                point=estimate(chains,d)
                intervals=[block_bootstrap(chains,d,b,a.reps,20261010+N*100000+L*1000+d*10+b)
                           for b in (50,100,200)]
                rows.append({'N':N,'L':L,'separation':d,'estimator':estimator,
                    'estimate':point,'ci_low_block_envelope':min(float(x[0]) for x in intervals),
                    'ci_high_block_envelope':max(float(x[1]) for x in intervals),
                    'chains':len(chains),'measurements_per_chain':len(chains[0]),
                    'bootstrap_replicates_per_block':a.reps,'block_lengths_measurements':'50;100;200'})
    with a.output.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(f'Wrote {len(rows)} rows to {a.output}')

if __name__=='__main__': main()
