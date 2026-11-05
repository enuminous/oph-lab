# OPH parallel work queue — 2026-11-05

Baseline: `d498af3926c98889531bca425565867409103a99` in `enuminous/oph-lab`.
Six workers ran independently, with a seventh performing integration, source
corrections, ledger maintenance, paper updates and CI. Follow-up cross-review
used the same workers. GitHub Issues is disabled on this fork: the API returned
410 to issue creation. These are repository work items, **not invented GitHub
issue numbers**. Scientific closure and implementation completion are separate.

| ID | Independent lane | Deliverable | Scientific work remaining |
|---|---|---|---|
| OPH-W1 | Particle identification | Fixed-window shape screen, negative controls, legacy-data quarantine | Source-selected physical particles, spin/statistics, charges, independent experiments |
| OPH-W2 | Interacting 3+1D readouts | Classical nonlinear scalar integrator, refinement and energy receipts | Source-selected action/clock, interacting quantum continuum |
| OPH-W3 | Mass and energy | Transfer gaps, independent covariance inversion, gated calibration | Physical spectral/clock/calibration bridge, pole and common-scheme masses |
| OPH-W4 | Gravity requirements | Exact rational null tomography and finite conservation controls | Metric ambiguity, continuum/BW/stress and empirical scale premises |
| OPH-W5 | Finite theorem premises | Lean operator and graph-action theorems plus axiom audit | Product Haar/incidence specialization, Mehler spectrum and physical bridges |
| OPH-W6 | Observer specifications | Hashed implementation inventory and finite observable-closure audit | Source-derived memory/repair selection and physical completeness |

Integration discovered and corrected the N2 flux-readout axis error. The
historical data are retained as a rejected readout of the intended observable;
the corrected smoke chains are separately versioned and archived. Completion
of these deliverables does not close the scientific column. The machine-readable
[premise register](premise_register.json) is the open-obligation list.

## Follow-up: OPH-N2-PILOT-1

The [corrected N2 pilot](../docs/OPH_N2_PARTICLE_PILOT.md) is implemented and
executed after the parallel integration. Its four L=12 chains use distinct
hot/cold seeds, 512 warmup sweeps and 1,024 retained measurements. Source,
configuration and raw-output hashes, paired block-bootstrap analysis,
autocorrelation/ESS/R-hat checks and timing probes are archived separately.

Implementation/provenance checks are complete. Numerical convergence and the
finite gap remain **unresolved**: all required lag envelopes include zero and
one chain has a direct mean-flux half-chain drift alarm. Fresh longer chains,
larger volumes, operator/transfer reconstruction and physical attachment remain
open under `P-N2-SAMPLING`, `P-N2-SPECTRUM` and the existing physical premises.
No GitHub issue was created; this is a repository work-item ID.
