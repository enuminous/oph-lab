# OPH Lab

Interactive explainer app for Observer Patch Holography.

Production URL: `https://oph-lab.floatingpragma.io/`

The lab is a reader-facing guide to the OPH paper stack. Its job is to explain the derivation routes, show where the recovered core stops, and keep public copy aligned with the paper surface. It is not a substitute for the papers, and it should not silently upgrade conditional or continuation results into unconditional theorem claims.

## Independent EFMW Zoo review (fork only)

This fork includes an [independent EFMW Zoo review of OPH Lab](docs/EFMW_ZOO_REVIEW.md),
covering selected audit criteria, two illustrative counterexamples, and proposed
comparative experiments. It is not endorsed by the OPH authors, is not a
completed 46-animal execution or Lean proof audit, and does not establish
physical validation or equivalence between OPH and EFMW.

The related [conditional OPH-to-EFMW continuum-limit study](docs/OPH_EFMW_CONTINUUM_LIMIT.md)
includes an explicitly augmented reversible patch-wave model, dimensional and
boundary assumptions, a finite-horizon error bound, [reproducible numerical
code](scripts/oph_efmw_continuum_demo.py), and [frozen test results](docs/data/oph_efmw_continuum_results.csv).
It does **not** derive EFMW physics from canonical OPH accepted repairs.

The [EFMW analysis of *Agreement and Surprise*](docs/AGREEMENT_AND_SURPRISE_EFMW_ANALYSIS.md)
compares Mueller's local-repair thesis with recursive coherence, attractor dynamics
and conditional gluing. It distinguishes agreement from stillness, shrinking
updates from convergence, and structural correspondence from physical derivation.

The [Cadence–OPH–EFMW common-core proposal](docs/CADENCE_OPH_EFMW_COMMON_CORE_PROPOSAL.md)
sets out a typed correspondence, a continuing-brain transfer experiment, and
ablations to distinguish shared mechanisms from useful additions. Prepared for
discussion with Bernhard Mueller, it is an independent research proposal; the
hybrid and proposed experiments have not been implemented or executed.

## Source Of Truth

Research status is controlled from the sibling `reverse-engineering-reality/` repo, especially:

- `paper/recovering_observer_spacetime_and_einstein_dynamics_from_overlap_consistency.tex`
- `paper/deriving_standard_model_gauge_structure_from_observer_overlap_consistency.tex`
- `paper/deriving_the_particle_zoo_from_observer_consistency.tex`
- `paper/reality_as_consensus_protocol.tex`
- `paper/screen_microphysics_and_observer_synchronization.tex`
- `paper/tex_fragments/PAPER.tex`
- `paper/tex_fragments/THREE_AXIOM_BASIS.tex`
- `paper/tex_fragments/UNIFIED_OBSERVER_PHYSICS_SPINE.tex`
- `code/particles/RESULTS_STATUS.md`
- `claims/claim_registry.yaml`
- `tracking/premise_register.json`
- `README.md`

The finite-simulation boundary is controlled by the sibling `oph-physics-sim/` repo, especially its `README.md`,
lane design documents, receipts, and `docs/RUN_OUTPUTS_AND_VISUALIZATION.md`. The Learn site is a guided
exposition surface; when its prose differs from a controlling paper or receipt, the research artifact controls the
claim. Research changes originate in those sources before the OPH Lab copy is synchronized.

## Paper Surface Summary

This section is the lab-maintainer summary of the public paper surface.

### Fixed-point and scale surface

- The landing page is a fixed-point dashboard, not a universe configurator.
- The measured-endpoint comparison branch uses
  `P_C = 1.630968209403959` and
  `alpha_U(P_C) = 0.041124336195630495`. Measured `Lambda` locates
  `N_Lambda = 3.31292709806038e122`.
- The closure principle stands beside A1–A3. It forces equality when the
  construction-side and readback-side quantities have been proved to be the
  same typed invariant. It does not construct the readings, their physical
  bridge, a return map, or proofs of existence, uniqueness, and stability.
- An exact bounded all-rung generation-register counterfamily has incompatible
  slack zero sets. Its source-contract checks cover declared finite audit
  rungs. Universal all-rung membership in the complete A1–A3 source contract
  and the executable-to-Lean membership bridge are unproved. Direct `N` is not
  evaluable and emits no cosmic value.
- The same algebraic bridge evaluated on the comparison endpoint gives
  `N_EW(P_C) = 3.5323546226929907e122`. This is distinct from the
  source-forward branch
  `P_fwd = 1.630972095858897`,
  `alpha_U(P_fwd) = 0.041124247441816685`, and
  `N0(P_fwd) = 3.532131543418936e122`.
- On the declared finite branch, total reserve expectation `P_fwd/4` and
  six-class equidistribution give one-class presence probability `P_fwd/24`.
  Physical selection of one blocked class, its scalar-weighted presence
  receipt, and a reserve-to-global-capacity survival theorem would give
  `N_presence = N0(1-P_fwd/24) = 3.292097877326465e122`.
- `N_Poisson = N0 exp(-P_fwd/24) = 3.300072225377652e122` is a separate branch.
  It requires a mean-count or projective-limit carrier that the finite theorem
  does not provide.
- Exact neutral and multiplicative global-capacity completions share the same
  local survival datum, are positive, compose across disconnected cuts and
  finite cut-count regrouping, and disagree after one cut. The finite source
  also selects no blocked-event semantics. The named-law branch is therefore
  not evaluable on the declared finite-cut attachment class. Its horizon branch
  has no source-selected positive capacity carrier. A positive branch requires
  a stronger target-independent source law.
- The finite-presence and Poisson values sit `-0.6287%` and `-0.3880%` below
  the Planck base-`Lambda`CDM comparison coordinate. The target was exposed
  and the tested formula menu was dense, so neither comparison is a
  prediction or a source-selected cosmic capacity.
- `G_SI` comes from the selected no-G scale certificate. The Newton row is
  separate from variable P-slider diagnostics.
- Off-point controls in the app are formula-sensitivity diagnostics. They are
  separate from certified branch claims.

### Source geometry and scalar fields

- Conservative source records and their metric complete to a continuous
  three-dimensional carrier. A declared golden population, complete local
  reading law and model clock have a controlled flat causal/count limit.
  Fourth roots of counts in fixed interior timelike intervals recover
  proper-duration ratios relative to a reference interval.
- A specified free scalar action on prepared golden addresses supports
  classical waves and Fock detectors, with certified comparison to the
  massive Dirichlet continuum field. The q=233 separated response exceeds
  its total error throughout model time [0.95,1]. Population, boundary,
  action and time are supplied; the field-to-recorded-clock join and an
  interacting continuum are separate requirements.
- The local Standard Model action has exact jet Ward identities under
  supplied spacetime, Spin, matter and coefficient conventions. It does
  not establish source-produced physical matter or its quantization.

### Gravity / Lorentz branch

- Lorentz kinematics is recovered on the explicit BW geometric branch.
- The BW theorem surface is sharpened and stable at the automorphism level.
- The formal surface does not derive broader UV/BW internalization.
- The remaining UV/BW scaffold is:
  - `canonical_scaling_cap_pair_realization_from_transported_cap_marginals`
  - `independent_bw_rigidity_on_realized_limit`
- The smallest lower blocker beneath the first object is:
  - `eventual_fixed_local_collar_common_floor_on_modular_transport_marginals`
- The OPH half-line generator is identified with the effective local null-stress charge on that same half-line family.
- The null/stress result does not supply:
  - bounded-interval transport / projective branch
  - tensor reconstruction beyond the null-invisible metric ambiguity

### Gauge / Standard Model structural branch

- On the twelve-port branch, the first axiom supplies a faithful compact
  commutator-closed port response. The second makes every proper carrier
  symmetry endogenous to that response. Compact Lie classification forces
  the abstract type `u(1) + su(2) + su(3)`.
- Target-blind readback derives the inverse-port response `R = -J`.
  Reconstructing the complete response map and bracket from source histories
  is not derived. The charged-double-triplet matrices are a declared exact witness.
- The declared fifteen-state representation fixture has exact hypercharges,
  anomaly cancellation, `N_c = 3`, and a common `Z_6` kernel. This does not
  select physical matter. The quotient
  `SU(3) x SU(2) x U(1) / Z_6` additionally requires a complete matter
  character lattice and a same-source loop-to-kernel identification.
  Physical global-form and three-family attachment require separate source identifications.
- The sharp exclusion is the ordinary simple-GUT `X/Y` gauge channel, not every proton-decay mechanism.

### Particle branch

- Symmetry-protected classical carrier zeros:
  - photon
  - gluons
  - graviton
- Electroweak:
  - `W/Z` values form a declared running/chart surface, not physical pole-mass predictions
- Higgs/top:
  - public rows are carried by the source-only Higgs/top split surface
  - the exact inverse pair is a check sidecar
  - the selected algebraic branch has `epsilon_H = 0`; its physical hierarchy
    interpretation requires `HIERARCHY-SCREEN-READOUT`
- Charged leptons:
  - the icosahedral screen supplies an exact `A5/C3` face-corner carrier
  - an engineered digital CFQ model proves the stipulated packet is nonempty
    and supplies a fixed-cutoff central accepted/rejected record dilation
  - the model authors its registers, automaton, clock, and response
  - physical source selection, family/Yukawa attachment, phase and determinant
    descent, interacting refinement, and pole-mass scheme are not derived
  - no nonzero source-only charged-lepton mass is emitted
- Quarks:
  - the source equations leave an exact free `(R_{>0})^2` spread fiber, so
    selected-frame descent does not emit either physical spread modulus
  - numeric quark rows are withheld from the public surface
  - the physical flavor-orbit selector, quark-Higgs carrier, and common-scheme
    source transport are not derived
- Neutrinos:
  - the isotropic neutrino-only ansatz has an exact no-go
  - the target-informed weighted-cycle point is rejected by the NuFIT 6.1
    correlated profile and is a comparison record only
  - physical PMNS, ordering, absolute masses, and Majorana phases require
    source, basis, Takagi, ordering, and no-target-leak certificates
- Hadrons:
  - production masses require a working OPH hadron backend and systematics

### Consensus branch

- Accepted local repairs lower the touched-overlap inconsistency potential `Phi`.
- On the finite patch net, that local-fit contract makes `Phi` a Lyapunov functional for accepted repair moves.
- Under repair completeness and quotient-compatible union-collar gluing, each fixed initial quotient state has a unique schedule-independent normal form.
- Same-source confluence does not by itself identify endpoints from different sources with the same boundary. That stronger statement requires the protected observation to identify the consistent quotient modulo the declared silent or gauge equivalence.
- Weak normalization supplies an endpoint; settlement under every allowed schedule requires fairness, strong normalization, or another liveness argument.
- A unique extension need not be constructible by the declared local write support. Local repairability is a separate proof obligation.
- Cycle and holonomy defects obstruct global consistency. Pairwise overlap agreement alone is insufficient.
- Gauge-invariant uniqueness belongs on the quotient, not on raw microscopic representatives.
- The standalone mathematical companion
  [Observation-Determined Normal Forms](https://github.com/FloatingPragma/observer-patch-holography/blob/main/extra/observable_normal_forms.pdf)
  develops these distinctions without importing OPH-specific assumptions into the paper.

### Screen microphysics branch

- The lab should treat the federated patch-carrier architecture as a first-class public surface, not a side note.
- The microphysics paper carries:
  - echosahedral multi-port patch carriers
  - toroidal local recurrence channels
  - \(A_5\)-icosahedral and \(E_8\)-type symmetry framing
  - explicit patch and overlap observables
  - record registers
  - public hardware-evidence rules
  - checkpoint / restoration machinery
  - observer synchronization as an operational protocol
- This is a fixed-cutoff reference architecture and simulator target. It does not claim unique final UV completion.
- The simulator must never be presented as an actual sphere. Sphere language names regulator geometry; the public carrier is a federated patch system.

## Lab Copy Rules

- Keep recovered, conditional, continuation, compare-only and unproved results distinct.
  Exact-hit diagnostics and phenomenological templates are not theorem predictions.
- Keep the explicit Bisognano–Wichmann branch qualifier on modular-flow and Lorentz
  claims. Neither unconditional boost identity nor Einstein recovery follows from
  the local axioms alone; gravity needs the stated null/stress and continuum inputs.
- Separate local axioms, bridge assumptions and unproved scaffold objects on the
  axioms and synthesis pages. Public summaries give the scientific state, without
  release-note narration.
- The landing page is a fixed-point dashboard. Avoid free-constant language, keep
  Newton's constant tied to the no-G scale certificate, and label sliders as
  sensitivity diagnostics.
- Keep W/Z on their running-chart surface and Higgs/top on the source-only split
  plus inverse check sidecar. Their physical hierarchy interpretation requires
  `HIERARCHY-SCREEN-READOUT`.
- Preserve charged, quark and neutrino classifications. The quark two-modulus
  source-spread obstruction is distinct from the mixed-scheme target audit and
  physical-Yukawa normalization. Never publish the six target-anchored quark
  coordinates as OPH mass predictions; hadrons need a working backend and systematics.
- Keep gravitational-wave combs, discrete Hawking templates and galaxy-response
  hypotheses at their declared tiers.
- Preserve the consensus and microphysics account of bounded self-reading patches:
  local state, ports, readback, protected records, feedback and public evidence.
  Fixed points, holonomy, synchronization and fixed-cutoff architecture are
  substantive parts of the model.

## Development

Install:

```bash
npm ci
```

Local dev server:

```bash
npm run dev
```

Production build:

```bash
npm run build
```

Deploy:

```bash
npm run deploy
```

The app uses `gh-pages -d dist` for deployment.
Build and check `dist` before deploying; `npm run deploy` publishes that
directory and does not rebuild it. The repository remote is
`https://github.com/muellerberndt/oph-lab` and the public domain is set by
`public/CNAME`.

Route titles and descriptions live in `src/seo-data.json`. The browser and
postbuild use the same functions in `src/seo.ts`; `npm run check:seo` verifies
all generated route metadata, canonical URLs, structured data and preview
dimensions. The build generates `dist/sitemap.xml` from the route inventory.
Optional `lastmod` dates are omitted because no verified per-page publication
history is maintained; rebuilding an unchanged page does not imply a content
update. The root metadata in `index.html` is checked against the same source.

## License And Patent Policy

OPH Lab is a public OPH surface and links back to the canonical OPH repository
license and anti-patent covenant:

- https://github.com/FloatingPragma/observer-patch-holography/blob/main/LICENSE
- https://github.com/FloatingPragma/observer-patch-holography/blob/main/PATENTS.md
