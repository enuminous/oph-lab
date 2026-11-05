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
