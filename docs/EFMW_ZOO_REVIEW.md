# EFMW Zoo Review of Observer Patch Holography (OPH Lab)

**Review date:** 2026-10-07  
**Reviewed fork:** [enuminous/oph-lab](https://github.com/enuminous/oph-lab)  
**Reviewed revision:** [78f95b7b058414f6313f6db18cf67efcf7c7c4f1](https://github.com/enuminous/oph-lab/commit/78f95b7b058414f6313f6db18cf67efcf7c7c4f1), 2026-09-30  
**Original lab repository:** [muellerberndt/oph-lab](https://github.com/muellerberndt/oph-lab)  
**Canonical research repository:** [FloatingPragma/observer-patch-holography](https://github.com/FloatingPragma/observer-patch-holography)  
**Zoo reference:** [enuminous/Monolithic-Zoo-Lean4](https://github.com/enuminous/Monolithic-Zoo-Lean4)  
**Review status:** Independent, exploratory source review with two illustrative counterexample calculations; **not** a completed 46-animal execution, formal proof audit, or independent physical validation.

> **Independence and provenance.** This review is added to the enuminous fork; it is not part of the original OPH research record and does not imply endorsement by Bernhard Mueller, OPH authors, or upstream maintainers. The controlling research claims are in the canonical OPH papers, proof sources, claim registry, premise register, and reproducibility receipts. Any disagreement between this review and a dated controlling artifact should be resolved by inspecting that artifact.

## Executive finding

Observer Patch Holography (OPH) and the proposed EFMW recursive coherence program have a notable **structural overlap**: local observers or components carry partial information, exchange records, compare overlaps, and participate in correction or repair procedures. OPH models accepted repairs with an overlap-inconsistency potential and studies normal forms and holonomy under explicit hypotheses. EFMW's Zoo provides a collection of audit operators and empirical/proof obligations for coherence monitoring, leakage control, generalization, causality, residual diagnostics, recovery, and provenance.

The overlap merits a controlled comparison but **does not prove equivalence**, derivation of one theory from the other, or either theory's physical realization. In particular:

- OPH Lab is an *interactive explanatory surface*, not the proof repository; its README explicitly delegates truth and evidence status to the canonical research artifacts.
- The [OPH synthesis page](../src/pages/Synthesis.tsx) distinguishes finite/analytic constructions, physical bridge requirements, and target-exposed comparison coordinates.
- The [OPH prediction page](../src/pages/Predictions.tsx) distinguishes frozen prospective targets from calibration and continuation-only templates. Its primitive-port claim is described as **unarmed** without the required source selection, laboratory attachment, and eligible comparison dataset.
- The [Zoo Lean reference](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/README.md) explicitly describes itself as an **uncompiled formalization draft** with selected operational kernels and contracts, not a complete verified 46-animal implementation.

**Overall assessment:** substantive conditional mathematical architecture; relatively careful source/claim-tier labeling; external physical validation not established by this inspection; EFMW–OPH equivalence unproved.

## Audit method and limits

**Inspected directly** in the OPH Lab fork: README.md, PLAN.md, package.json, the route/content/source listings, src/content/paperSurface.ts, src/core/ophMath.ts, the Axioms, Consensus Protocol, Synthesis, Predictions, and Quantum Mechanics pages. Also inspected the canonical OPH research README, axiom reference, selected premise-register entries, falsification program, and frozen-prediction ladder, plus selected Lean modules and notes from the EFMW Zoo reference.

**Not performed:** building or deploying the OPH frontend; compiling OPH Lean; executing OPH's simulator or complete science/evidence pipeline; running the original full Zoo Python harness; compiling all Zoo Lean modules; quantitative baseline comparisons; external dataset testing; checking every mathematical theorem or each of the 46 animals. Absence of a test result here is **not** a negative test outcome.

The evidence classifications below are **analyst judgments applying named Zoo audit questions to inspected repository text**, rather than instrument-produced measurements. A “strong” provenance assessment is about documentation discipline; it is not a scientific truth certificate.

## Sampled EFMW Zoo findings

| Zoo animal | Review classification | Observed support and remaining obligation |
| --- | --- | --- |
| **TORTOISE** — prospective evaluation | **Conditional** | OPH separates prospective freezes, postdictions, and calibration. Verify timestamped custody, eligible comparison data, predeclared controls and unchanged kill rules before treating a physical comparison as prospective evidence. |
| **OWL** — warning/temporal monitoring | **Untested** | No OPH-specific sequential warning experiment with matched false-positive rate and independent outcomes was executed in this review. |
| **OCTOPUS** — distributed partial observability | **Conceptual match** | Finite patches, overlaps, protected records, and missing/global information are natural representations for a distributed-observer benchmark. No numerical Octopus score computed. |
| **RAVEN** — residual structure | **Open** | No matched comparison shows OPH or EFMW residual features outperforming conventional baselines on unseen data. |
| **HEDGEHOG** — habitat transfer | **Untested** | Generalization outside declared mathematical/simulation habitats needs frozen independent environments and measurement definitions. |
| **CROCODILE** — causal identification | **Open** | Inferring physical causal structure from simulations, repairs or comparison coordinates needs justified identification assumptions; an internally consistent model is insufficient. |
| **DRAGON** — transition/convergence | **Conditional** | Finite normal forms are discussed under repair-completeness, gluing and normalization assumptions; potential descent by itself does not establish a unique endpoint. |
| **WEASEL** — counterexample pressure | **Scope boundary survives** | OPH explicitly recognizes countermodels, non-evaluable branches, and distinctions among same-source confluence, cross-source identification, and liveness. |
| **MAGPIE** — provenance/groundedness | **Strong documentation practice** | The repo tracks structural, conditional, calibration, continuation and open claims, and links to source/receipts. A numerical Magpie groundedness score was **not** calculated. |
| **BEAVER** — bounded repair/rollback | **Conditional** | A declared rollback/checkpoint contract does not independently prove an external reversal happened or retained system-level invariants. |
| **PHOENIX** — restoration | **Open** | Independent disturbance-and-recovery experiments with real hold windows and invariant checks remain to be performed. |
| **TURTLE** — synthesis/veto | **Insufficient evidence for physical synthesis** | There is material mathematical infrastructure, but this inspection supplies neither independent empirical confirmation nor a complete 46-animal verdict. |

The selected Zoo reference formalizations specify important constraints: [TORTOISE](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/Tortoise.lean) requires an explicit prospective split; [HEDGEHOG](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/Hedgehog.lean) takes habitat metrics as inputs; [CROCODILE](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/Crocodile.lean) makes causal-identification assumptions explicit; [MAGPIE](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/Magpie.lean) takes provenance metrics and previous groundedness as inputs; [TURTLE](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/Turtle.lean) gates support on applicability, vetoes and independent evidence groups. Those inputs were **not measured** in this inspection and must not be invented.

## Two illustrative counterexamples (logical stress tests)

These examples test shortcuts that a careless review might infer; they are **not counterexamples to OPH's full conditional theorems**, which already acknowledge the missing conditions.

### Test A — descending inconsistency does not imply a unique normal form

Take a finite state set {A, B, C} with potential values Phi(A)=2, Phi(B)=1, Phi(C)=1 and permitted transitions A→B and A→C, with B and C terminal. Every transition strictly reduces Phi, so there is no infinite descending transition sequence. Yet A has two different normal forms, B and C. Additional confluence/diamond and quotient assumptions are required for uniqueness.

**Expected result:** all transitions descend = true; unique normal form from A = false.

### Test B — local edge assignments do not force trivial cycle holonomy

Assign transport signs +1, +1, -1 to the three oriented edges of a closed loop. Each sign is an admissible element of the multiplicative group {+1,-1}, yet the loop product is -1, not the identity. Locally assigned edge transports are not sufficient to certify globally trivial holonomy.

**Expected result:** edge values valid = true; cycle product = -1; globally trivial holonomy = false.

The following dependency-free script reproduces the two logical examples. This code tests only the toy examples, not OPH implementations.

~~~python
potential = {"A": 2, "B": 1, "C": 1}
transitions = {"A": ("B", "C"), "B": (), "C": ()}

assert all(
    potential[target] < potential[source]
    for source, targets in transitions.items()
    for target in targets
)

def normal_forms(state):
    if not transitions[state]:
        return {state}
    return set().union(*(normal_forms(t) for t in transitions[state]))

assert normal_forms("A") == {"B", "C"}
print("A: strict descent yes; unique normal form no")

edge_transports = (1, 1, -1)
assert all(x in (-1, 1) for x in edge_transports)
cycle = 1
for x in edge_transports:
    cycle *= x
assert cycle == -1
print("B: local group elements yes; trivial cycle holonomy no")
~~~

**Connection to OPH's own scope:** [ConsensusProtocol.tsx](../src/pages/ConsensusProtocol.tsx) explicitly differentiates (i) same-source confluence, (ii) cross-source observation-based identification, (iii) termination/liveness, and (iv) local repairability, and it recognizes cycle/holonomy obstructions. These are good boundaries to preserve, not newly discovered defects.

## OPH-specific claims and stress points

### Fixed points and physical constants

The public [synthesis](../src/pages/Synthesis.tsx) presents certified roots of *declared maps*, measured-endpoint comparisons, and source-forward diagnostic branches. The site expressly says that direct cosmic capacity is not evaluable without source-selected carrier and physical bridge assumptions. Its target-exposed percent residuals are **not predictions**. The Zoo audit should preserve that status rather than score agreement with preexisting measurements as out-of-sample predictive gain.

### Quantum and gauge reconstruction

The [Quantum Mechanics page](../src/pages/QuantumMechanics.tsx) starts with quantum-algebraic patch machinery; it does **not** claim that the full quantum formalism has been derived from classical records alone. The [Axioms page](../src/pages/Axioms.tsx) states a three-axiom basis and explicitly separates compact Lie-algebra recognition from physical current, matter and global-group realization. A valid comparison must inspect which hypotheses enter each branch and whether the same physical object is derived, not merely named.

### Repair and observer consensus

The local-fit/inconsistency-potential construction is the **strongest candidate for an EFMW-style benchmark**, because both frameworks can be supplied identical finite graphs and observable mismatch functions. A fair experiment must separate: (a) purely algebraic statements about accepted updates, (b) termination and confluence under identified assumptions, (c) actual implementability of repairs, and (d) external physical measurements. None implies the next automatically.

### Prediction and possible falsification

The [primitive-port prediction](../src/pages/Predictions.tsx) reports the branch-specific ratios

- B6 / C4² = 32/315
- B0 / C4² = 10/21
- B6 / B0 = 16/75

Its own public text says the physical comparison is **unarmed** for lack of source selection, physical-sector bridge, coherent frame transport and eligible dataset contract. It also warns that Lorentz-violating models and environmental anisotropy may mimic an observed signal. Before forecasting success or failure, define the actual observable and experimental protocol and consult the canonical [frozen ladder](https://github.com/FloatingPragma/observer-patch-holography/blob/main/docs/FROZEN_PREDICTION_LADDER.md). A failed branch test is not automatically a falsification of unrelated OPH claims.

### Historical planning language

The fork's [PLAN.md](../PLAN.md) describes an ambitious early linear derivation with claims about interactive demos reaching “all known physics” without gaps. The current README and research pages are more tightly qualified. **Recommendation:** label PLAN.md as historical design documentation if it remains discoverable, so planned links are not mistaken for a completed deduction.

## EFMW–OPH cross-framework boundary

EFMW's proposed scalar expression is conventionally written here as

\[
\nabla^2\phi-\frac{1}{c^2}\frac{\partial^2\phi}{\partial t^2}
=\frac{4\pi}{c^2}(E+Pc).
\]

OPH's finite patch mismatch functional is denoted Phi in the site. **These are not currently shown to be the same object or to be related by a valid scaling limit.** Similar terminology, fixed-point structures or consistency themes cannot supply the missing map.

An actual correspondence would require explicit definitions of the state spaces and fields; a dimensional analysis; an update-to-continuum or renormalization map; boundary conditions; hypotheses guaranteeing convergence; quantified approximation errors; and discriminating predictions that do not use comparison targets as inputs.

## Prioritized next experiment: frozen same-graph comparison

1. **Fix a finite common testbed.** Specify observer/patch graph, observables, initial distributions, corruption processes, update rules, missing-record masks, and target-independent random seeds before evaluation.
2. **Define comparable outputs.** Record mismatch potential, terminal quotient class, time-to-settle, normal-form disagreement, holonomy defects, hidden-inconsistency detection delay, false-positive rate, recovery under patch failure, memory and compute cost.
3. **Control information and baselines.** Compare OPH-inspired update operators and EFMW-inspired residual/coherence estimators with fixed conventional graph-consensus, residual EWMA and other appropriate baselines. Distinguish retrospective full-column ranks from online scores.
4. **Run minimal ablations.** Remove overlap feedback, protected-record enforcement, holonomy tracking, repair-completeness assumptions, residual memory and provenance tracking one component at a time. Preserve negative results.
5. **Hold out environments and label evidence.** Test disjoint graph families and noise regimes; report intervals, failure examples, complete raw outputs and reproducible execution versions. Require genuine source/physical bridging before interpreting software findings as physics.
6. **Prove only what is actually proved.** Add Lean statements for finite contracts and audit dependency assumptions; compile and inspect axioms/sorries. Keep theorem verification separate from empirical validation.

**Success criterion for the first study:** a reproducible, preregistered improvement on at least one independent operational metric at a matched error or cost budget, with consistent negative-result reporting. It would support the narrowly measured operational advantage, **not** automatically establish a new law of nature or equivalence between theories.

## Review verdict

| Dimension | Assessment |
| --- | --- |
| Mathematical architecture | Substantive, expressly conditional |
| Provenance and boundary discipline | Strong documentation practice in inspected surfaces |
| Reproducible demonstrations | Existence of source/receipt infrastructure confirmed; no full independent rerun here |
| Independent physical validation | Not established by this review |
| EFMW–OPH identity or derivability | Unproved |
| Next best action | Frozen, same-graph, independent comparative experiment |

**Bottom line:** OPH demonstrates a research design attentive to exact hypotheses and failure boundaries. It is a useful candidate for a rigorous EFMW Zoo *comparison*. The appropriate next result is a controlled experiment or checked mapping—not a declaration of scientific equivalence.

## Primary links

- [Fork README](../README.md)
- [OPH Lab consensus page source](../src/pages/ConsensusProtocol.tsx)
- [OPH Lab synthesis page source](../src/pages/Synthesis.tsx)
- [OPH Lab prediction page source](../src/pages/Predictions.tsx)
- [OPH claim and evidence model](https://github.com/FloatingPragma/observer-patch-holography)
- [OPH axiom reference](https://github.com/FloatingPragma/observer-patch-holography/blob/main/docs/AXIOM_REFERENCE.md)
- [OPH falsification program](https://github.com/FloatingPragma/observer-patch-holography/blob/main/docs/OPH_FALSIFICATION_PROGRAM.md)
- [OPH frozen prediction ladder](https://github.com/FloatingPragma/observer-patch-holography/blob/main/docs/FROZEN_PREDICTION_LADDER.md)
- [Zoo coverage notes](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/COVERAGE.md)
- [Zoo formalization limitations](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/FORMALIZATION_NOTES.md)

*Prepared as an independent comparative audit for the enuminous fork, 2026-10-07. No upstream code, theory claims, or test data were altered by this review.*
