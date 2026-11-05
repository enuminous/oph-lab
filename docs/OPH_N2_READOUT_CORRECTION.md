# N2 readout correction and historical-data quarantine

**2026-11-05 — demonstrated implementation defect; physical channel unresolved**

The source audit of baseline `d498af3926c98889531bca425565867409103a99`
found that the historical implementation did not measure its documented
observable. The array `theta` has shape `(4,L,L,L,L)`. Selecting `theta[mu]`
removes the direction axis, so its coordinate axes are then `0,1,2,3`.

For links directed from x to x+mu, the intended Wilson plaquette is

\[
W_{01}(x)=U_0(x)U_1(x+\hat0)\overline{U_0(x+\hat1)}\overline{U_1(x)}.
\]

| Operation | Historical implementation | Correct F01 / axis-3 readout |
|---|---|---|
| Shift U1 in plaquette | axis 1 | axis 0 |
| Shift U0 in plaquette | axis 2 | axis 1 |
| Spatial average | axes 1,2,3 (leaves axis 0) | axes 0,1,2 (leaves axis 3) |

The historical product is generally not gauge invariant under
`U_mu(x) -> g(x) U_mu(x) conjugate(g(x+mu))`. The new direct-index loop,
random local gauge transformation and reversed-orientation tests independently
check the corrected product. The old expression fails the same gauge control.
Both direct and conditional link-mean readouts use the corrected shared helper.

## Consequence for the October result

The CSV and its original numbers are preserved. Their interpretation as the
specified gauge-invariant F01 correlator separated along axis 3 is **rejected**.
The negative midpoint is not evidence of a reflection-positivity obstruction
for the intended physical operator. The old numbers cannot be repaired by
renaming axes; the link directions and shifts disagree. Raw historical chains
are unavailable, so no corrected reanalysis is claimed. The physical N2
pole/no-pole question remains **unresolved**.

## New raw data and uncertainty boundary

`scripts/oph_n2_flux_mc.py` emits `readout_version=F01-axis3-v2`, its SHA-256,
library versions, coordinate/observable specification, seed, sweep protocol and
raw direct/conditional slice arrays. The four smoke runs under
[`data/oph_flux_v2`](data/oph_flux_v2) use L=4, N=1 or 2, seeds 20261105 and
20261106, 200 warmup sweeps, 512 measurements and two sweeps per measurement.
They exercise the corrected readout; mixing, volume stability and sensitivity
are not certified. They are too short in the transfer direction for the frozen
particle-screen window. No mass or named particle is inferred.

At nonzero axis-3 separation, the two F01 slices contain disjoint links.
Conditional link independence therefore permits the product of conditional
means used in the Rao–Blackwell correlator. At contact the links are shared;
the square of the conditional mean is not the conditional second moment. The
RB contact correlator is now `null`, with the reason in provenance.

The summarizer refuses legacy versions, mixed models/source hashes, duplicate
seeds, incompatible sampling protocols and malformed arrays. Uncertainty
calculation needs at least two independent-seed chains and two full blocks per
chain for every requested block length (50,100,200); these are minimum software
guards, **not a mixing certificate**. Reported envelopes are exploratory and
do not assert simultaneous coverage or independent direct/RB replications.

```bash
python -m unittest discover -s tests -p 'test_flux_readout.py' -v
python scripts/summarize_oph_flux.py docs/data/oph_flux_v2 \
  --output docs/data/oph_flux_v2_summary.csv --reps 200
```

The scope of this correction is the independent fork sampler. It does not
assert that upstream OPH sources contain the same defect.

## Subsequent bounded experiment

The [N2 particle-channel pilot](OPH_N2_PARTICLE_PILOT.md) adds chain diagnostics
and executes four new L=12 runs using the same corrected F01/axis-3 operator.
The observable remains `F01-axis3-v2`; diagnostic records use the expanded raw
schema `oph-flux-chain-v3`. All five required lag envelopes include zero for
both estimators and one direct mean-flux drift alarm remains. No stable gap or
particle is established. Its longer-run/volume proposal is not executed here.

The four L=4 smoke files and their summary above remain byte-for-byte intact.
The [preservation manifest](../experiments/oph_n2/preserved_evidence.json) and
exact archived smoke-sampler source bind them to the implementation that
actually generated them; later instrumentation does not invalidate or rewrite
that historical provenance.
