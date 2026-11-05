#!/usr/bin/env python3
"""Structural integrity and release-policy checks, not scientific evidence verification.

File existence and declared premise statuses do not prove the referenced claims.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'demonstrated', 'supported but incomplete', 'hypothesis/postulate', 'unresolved', 'rejected'}
PREMISE_STATUSES = {'proved_finite', 'verified_numerically', 'supplied', 'unresolved', 'rejected'}
DOMAINS = {'implementation', 'finite_mathematics', 'numerical_model', 'physical'}


def validate(ledger, register, root=ROOT):
    errors = []
    premises = {p['id']: p for p in register['premises']}
    if len(premises) != len(register['premises']):
        errors.append('Duplicate premise IDs')
    ids = set()
    for p in register['premises']:
        if p['status'] not in PREMISE_STATUSES:
            errors.append(f"Invalid premise status: {p['id']}")
        for path in p['evidence']:
            if not (root / path).is_file():
                errors.append(f'Missing premise evidence: {path}')
    for claim in ledger['claims']:
        cid = claim['id']
        if cid in ids:
            errors.append(f'Duplicate claim: {cid}')
        ids.add(cid)
        if claim['status'] not in STATUSES or not claim['scope'].strip():
            errors.append(f'Invalid status/scope: {cid}')
        if claim['domain'] not in DOMAINS:
            errors.append(f'Invalid domain: {cid}')
        dependencies = []
        for pid in claim['premises']:
            if pid not in premises:
                errors.append(f'Unknown premise {pid}: {cid}')
            else:
                dependencies.append(premises[pid])
        for path in claim['evidence'] + claim['checks']:
            if not (root / path).is_file():
                errors.append(f'Missing claim evidence: {path}')
        if claim['status'] == 'demonstrated':
            if not claim['evidence']:
                errors.append(f'Demonstrated claim lacks evidence: {cid}')
            if any(p['status'] in {'unresolved', 'rejected'} for p in dependencies):
                errors.append(f'Demonstrated claim has open premise: {cid}')
            if claim['domain'] == 'physical' and any(p['status'] != 'proved_finite' for p in dependencies):
                errors.append(f'Physical claim depends on supplied/numerical premises: {cid}')
    # This release has no independently validated physical-attachment evidence.
    # Changing this policy requires a reviewed schema/evidence upgrade, not a status edit.
    if any(c['domain'] == 'physical' and c['status'] == 'demonstrated' for c in ledger['claims']):
        errors.append('This release has no physical-validation certificate')
    if ledger['physical_completion_status'] != 'unresolved':
        errors.append('Physical completion must remain unresolved in this release')
    return errors


def main():
    ledger = json.loads((ROOT/'claims/claim_registry.json').read_text())
    register = json.loads((ROOT/'tracking/premise_register.json').read_text())
    errors = validate(ledger, register)
    for stem in ('oph_interacting_continuum', 'oph_mass_energy', 'oph_gravity_requirements', 'oph_particle_readouts'):
        receipt = json.loads((ROOT/f'docs/data/{stem}.json').read_text())
        digest = receipt.get('implementation_sha256') or receipt.get('provenance', {}).get('implementation_sha256')
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            errors.append(f'Missing/invalid source digest: {stem}')
        elif digest != hashlib.sha256((ROOT/f'scripts/{stem}.py').read_bytes()).hexdigest():
            errors.append(f'Stale implementation receipt: {stem}')
    particle = json.loads((ROOT/'docs/data/oph_particle_readouts.json').read_text())
    if particle['input_sha256'] != hashlib.sha256((ROOT/'docs/data/oph_n2_flux_stage3_summary.csv').read_bytes()).hexdigest():
        errors.append('Legacy data hash changed without reviewed particle receipt')
    # Historical evidence binds to its exact archived source, not today's code.
    # Do not rewrite old measurements merely to make a current hash check green.
    archive = json.loads((ROOT/'experiments/oph_n2/preserved_evidence.json').read_text())
    source_hash = hashlib.sha256((ROOT/archive['corrected_smoke_source_path']).read_bytes()).hexdigest()
    if source_hash != archive['corrected_smoke_source_sha256']:
        errors.append('Archived smoke sampler changed')
    preserved_files = dict(archive['files'])
    preserved_files.update(archive.get('portable_replay_archive', {}).get('files', {}))
    for name, digest in preserved_files.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
            errors.append(f'Preserved evidence changed: {name}')
    for path in (ROOT/'docs/data/oph_flux_v2').glob('L*_N*_seed*.json'):
        run = json.loads(path.read_text())
        if run['provenance']['implementation_sha256'] != source_hash:
            errors.append(f'Stale raw-run implementation: {path.name}')
    if __package__:
        from .analyze_oph_n2_pilot import load_pilot
    else:
        from analyze_oph_n2_pilot import load_pilot
    try:
        directory = ROOT/'docs/data/oph_n2_pilot_v1'
        _, manifest, _ = load_pilot(directory)
        for name, digest in manifest['source_sha256'].items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
                errors.append(f'Pilot source changed: {name}; preserve/review source before rerunning')
        if hashlib.sha256((ROOT/'experiments/oph_n2/pilot_v1.json').read_bytes()).hexdigest() != manifest['config_sha256']:
            errors.append('Frozen pilot configuration changed')
        analysis = json.loads((directory/'analysis.json').read_text())
        if analysis['analysis_sha256'] != hashlib.sha256((ROOT/'scripts/analyze_oph_n2_pilot.py').read_bytes()).hexdigest():
            errors.append('Pilot analysis receipt stale')
    except (ValueError, KeyError, OSError) as exc:
        errors.append(f'Pilot evidence invalid: {exc}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f"Research contracts PASS (structural integrity only): {len(ledger['claims'])} scoped claims, {len(register['premises'])} premises; physical completion UNRESOLVED")


if __name__ == '__main__':
    main()
