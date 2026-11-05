# Observer access, source contracts, and finite observable closure

**Date:** 2026-11-05  
**Scope:** the independent `enuminous/oph-lab` fork.  
**Result:** implemented source inspection and a finite observable-closure checker; physical completeness remains **unresolved**.

Observers may inspect simulator specifications, observer/readout code, scheduling,
repair rules, and memory rules. This permission makes those objects admissible
inputs to reverse engineering. Their provenance still matters: a supplied update
law is an input to a finite model, and a claim that nature implements that law
needs its own evidence.

The executable contract is
[`scripts/oph_observer_contract.py`](../scripts/oph_observer_contract.py). Its
[receipt](data/oph_observer_contract.json) pins exact source and verifier bytes by
SHA-256 and locates inspected functions by name, line span, and source hash.
Inspection parses source; it does not import or execute the inspected modules.
The historical baseline is commit
`d498af3926c98889531bca425565867409103a99`. The receipt's source hashes identify
the corrected working sources; they do not claim those bytes existed at the
historical commit.

## What can actually be read in this checkout

| Object | Inspected implementation | What it supplies | Remaining boundary |
|---|---|---|---|
| Finite simulator specification | `scripts/oph_n2_flux_mc.py:run` | Complex matter, link phases, positive conductances, supplied parameters, four periodic coordinates, RNG seed | Source selection of this model as physical OPH is unproved |
| Measurement/readout observer | `plaquette_product`, `spatial_flux_slices`, `run.flux_slice`, `run.rb_flux_slice` | Explicit operator orientation, coordinate averaging, direct and conditional readbacks | These functions are measurement operators, not a complete implementation of a human observer |
| Scheduler | `run.sweep` and the warmup/measurement loops | Red/black matter updates, then links and conductances; thinning and warmup | Sampler time is not identified with physical time |
| Repair rule | The same conditional kernels | An authored heat-bath update law for the declared finite model | Canonical OPH accepted-repair correspondence is not established |
| Measurement storage | `obs` and `rb_obs`, followed by run JSON serialization | Retained slice arrays for one run | Appending arrays is not a protected microscopic memory law |
| Wave update and retained layers | `scripts/oph_efmw_continuum_demo.py:test_resolution` | Two retained field layers, declared leapfrog rule, manufactured source | This is the supplied augmented wave model, not a source-derived repair/memory law |
| Canonical microscopic memory law | Not instantiated in the inspected source set | No positive implementation claim | The upstream architecture must be supplied, instantiated, and joined to these readouts |

The upstream research and simulator repositories named by the README are separate
artifacts. This receipt audits the listed local sources; it makes no claim to
have executed, copied, or completed those upstream implementations. The new
interacting field, mass, particle, and gravity lanes have their own receipts and
scope notes.

## A source audit exposed a material readout error

The historical direct and conditional routines selected a link component
(`theta[mu]` or `r[mu]`), which removes the link-direction axis. They then rolled
the selected arrays on coordinate axes 1 and 2. The declared oriented `F01`
plaquette requires the corresponding shifts on axes 0 and 1:

\[
P_{01}(x)=U_0(x)U_1(x+\hat 0)\overline{U_0(x+\hat 1)}\overline{U_1(x)}.
\]

They also averaged axes `(1,2,3)`, leaving coordinate 0, while the documentation
said the retained/separation coordinate was 3. The corrected default averages
`(0,1,2)` and leaves coordinate 3. Both estimators now use the same geometry
helpers. Independent index-loop and local-gauge-transformation tests are in
[`tests/test_flux_readout.py`](../tests/test_flux_readout.py).

**The old summary is quarantined for the intended `F01`/axis-3 claim.** Its
historical bytes are retained. Relabelling that summary cannot reconstruct the
intended observable or a valid gauge-invariant flux channel. A corrected run
needs a new version/hash and raw records. This finding also weakens any earlier
interpretation that treated the old summary as evidence about the intended
channel; it does not prove a no-pole theorem.

`audit_flux_geometry` checks a deliberately restricted AST contract: the oriented
product, default `(mu,nu)=(0,1)`, default separation axis 3, averaging expression,
and both delegates to the shared slice routine. Missing helpers, malformed
source, or a changed checked expression fail closed. This source-shape check
does not prove arbitrary Python semantics or the complete conditional-estimator
derivation. An algebraically equivalent rewrite outside the contract requires
review and a contract update.

## An exact finite observable question that can be decided

`audit_finite_observable_closure` accepts:

- A nonempty, exhaustive finite state table \(S\).
- A current readback \(R:S\to\mathcal R\).
- A nonempty declared list of observables \(O_i:S\to\mathcal V_i\).
- A nonempty list of total deterministic transitions \(T_a:S\to S\), indexed by
  known scheduler labels \(a\).

It decides whether, for every finite scheduler word \(w\),

\[
R(s)=R(t)\quad\Longrightarrow\quad
O_i(T_w(s))=O_i(T_w(t))\quad\text{for every declared }i.
\]

The empty word is included, so current observables must also be determined.
Values are compared as canonical, finite JSON values. All state tables must
match exactly; partial transitions, unknown destination states, absent
observables, and NaN/Infinity inputs are rejected. A known sequence of scheduler
labels is an assumption. The result is not a theorem about an unobserved or
arbitrary stochastic scheduler.

The algorithm starts by partitioning states by their observable tuples, then
repeatedly refines classes by their labelled successor classes. Classes can
split but cannot merge, so finite termination follows. At a fixed partition,
equal-class states have equal observables and equal-class successors for every
label. Induction on word length gives equality for every finite word. Conversely,
each split records either a present observable difference or a successor
difference, hence a finite distinguishing word. A `PASS` means each readback
class is contained in one final class. A `FAIL` includes explicit initial
states, a shortest distinguishing scheduler word, and differing terminal
observables. This is a finite-model determinacy claim under the listed premises.

Knowing a law and knowing a realized state are distinct. The receipt includes
an **authored four-state counterexample**, not a proposed physical memory law:

\[
s=(x,m)\in\{0,1\}^2,\qquad T(x,m)=(m,m),\qquad O(x,m)=x.
\]

The law is available in both cases. Readback of only \(x\) cannot distinguish
`00` and `01`, but one `tick` produces visible values 0 and 1, so the finite
criterion fails. Declared access to both \((x,m)\) resolves the ambiguity for
this supplied model and passes. Access to the scheduler or memory-law source
alone does not provide the missing realized memory bit. Different microscopic
states may also remain equivalent for all declared observables; the checker
does not require raw-state injectivity.

The Monte Carlo simulator is not certified by this finite table example. It has
stochastic draws, floating state, and RNG state; no exhaustive state/transition
table for that simulator has been supplied to this checker.

## Claim ledger for this lane

| Claim | Evidence status | Evidence and limit |
|---|---|---|
| `OBS-SOURCE`: the listed simulator/readout/scheduler sources are inspectable and content-pinned | **Demonstrated** for the listed files | Exact bytes, AST locations and reproducible receipt |
| `OBS-GEOMETRY`: corrected direct and conditional readbacks share the declared default `F01`/axis-3 geometry | **Demonstrated** within the restricted contract and tested arrays | AST regression checks plus independent index/gauge tests; no physical-time claim |
| `OBS-LEGACY`: the historical implementation does not implement its stated flux geometry | **Demonstrated** source defect | Original axes conflict with the documented operator; legacy formula fails the gauge control |
| `OBS-FINITE`: declared finite readbacks determine all declared observables at all finite known schedule histories | **Conditional, decidable per supplied table** | Partition refinement and explicit counterexamples; no claim that the table describes nature |
| `OBS-MEMORY`: canonical source-selected microscopic memory is implemented here | **Unresolved** | Run-array retention and two-layer wave state do not discharge this premise |
| `OBS-COMPLETE`: all of nature's observables are explained | **Unresolved** | No exhaustive physical inventory, source identification, interacting quantum/gravity bridge, or independent empirical attachment is supplied by introspection |

The physical-completeness output remains `UNRESOLVED` even when a finite table
passes. Permitting source access removes an artificial access restriction; it
does not remove the distinction between a supplied specification, a theorem
conditional on that specification, and a physical law supported by measurement.

## Reproduction and tests

From the repository root:

```bash
python -m unittest discover -s tests -p test_observer_contract.py -v
python scripts/oph_observer_contract.py --output docs/data/oph_observer_contract.json
python scripts/oph_observer_contract.py --check docs/data/oph_observer_contract.json
```

The 13 tests cover malformed/absent sources, content-hash changes, symbol spans,
no-import inspection, deliberate axis/delegate corruption, incomplete transition
tables, nonfinite evidence, zero- and longer-horizon distinguishing histories,
multiple scheduler labels, observationally silent states, and the memory
counterexample. The refinement result is also compared with an independent
enumeration of finite scheduler words for 40 seeded four-state models.

The receipt has no wall-clock timestamp or mutable `HEAD` dependency. Changes
to inspected source bytes or the verifier change the receipt; `--check` rejects
a stale receipt. Exit zero certifies successful source/geometry inspection and
receipt equality when requested. It never means physical completeness.
