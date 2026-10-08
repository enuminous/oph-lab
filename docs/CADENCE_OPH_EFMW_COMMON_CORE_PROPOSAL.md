# Local Repair, Retained Experience, and a Common Core

## A research proposal for Cadence, OPH, and EFMW

**Date:** 8 October 2026

**Status:** Independent proposal from the [enuminous OPH Lab fork](https://github.com/enuminous/oph-lab), prepared for discussion with Bernhard Mueller. No upstream endorsement or coauthorship is implied.

**Research stage:** Source-grounded design. The proposed hybrid, formal correspondence, and factorial experiment have **not been implemented or executed**. Existing measurements are identified separately below.

### Abstract

We propose a small research programme around a testable question: can the local-repair structures in Cadence, Observer Patch Holography (OPH), and selected EFMW formulations be translated into one explicit computational contract, and does anything distinctive survive when their additional mechanisms are removed? Cadence supplies an executable continuing brain and demanding preservation contracts. OPH supplies questions about local consistency, admissible repair, and global identification. EFMW supplies candidate relations among state, observation, memory, and feedback, together with fixed Zoo audit operations. The first deliverable is a typed correspondence that preserves information access, update rules, and observable behaviour. The second is a bounded experiment on history-dependent transfer, interference, and recovery in the same acquired brain. We propose a factorial comparison only after identifying distinct executable mechanisms, followed by component ablations and conventional substitutions. A useful outcome could be a smaller common mechanism, a demonstrably useful extension, or a precise obstruction to the proposed identification. Each would sharpen the local-repair thesis. None would, by itself, establish a universal physical theory.

## 1. Start with a capable continuing system

The practical opportunity is to connect a formal account of agreement with a system that must keep functioning while its evidence changes. The experimental object should be one acquired brain: it learns useful relations, acts with them, encounters interference, receives the consequences of its actual actions, and resumes after repair or a saved continuation.

In this first programme, OPH supplies the formal repair-and-observation contract, Cadence supplies the runtime, and EFMW supplies candidate constraints and mechanisms to translate and test. Any further OPH-derived runtime mechanism would need its own adapter and ablation. The central challenge is concrete: a brain can settle on a wrong answer; can local evidence-driven correction revise that answer while preserving other acquired abilities?

This choice follows Cadence's [contribution contract][cadence-contributing]. Begin with the simplest existing System 1 composition. Investigate missing information, experience, state, memory, wiring, and implementation before adding machinery. Any addition must enter the local repair process and its coupled equilibrium; it must identify a demonstrated limitation and preserve required capabilities. Optional recursive observation becomes relevant only if the experiment identifies a reason to test it.

The proposal has two separable hypotheses:

- **H1 — computational correspondence:** a specified restriction of each framework implements a common local transition system, under explicit state maps and assumptions.
- **H2 — useful additional mechanism:** a precisely specified EFMW-motivated mechanism improves a declared continuing-learning limitation beyond existing Cadence mechanisms and matched simpler controls.

H1 can hold while H2 fails because the supposed addition is already present. H2 can hold on a task without establishing H1 for the full frameworks. Keeping these outcomes separate makes the investigation productive even when a merger is unnecessary.

## 2. Define the common contract before naming the common core

For a numerical candidate, let patch $i$ carry state $x_i$, read its declared closed neighbourhood $N(i)$, and receive evidence $e_{i,t}$ and retained memory $m_{i,t}$. During a fast repair phase, hold the event-level evidence, memory, and parameters fixed:

$$
r_i^k=x_i^k-F_i(x_{N(i)}^k,e_{i,t},m_{i,t};\theta_t),
\qquad
x_i^{k+1}=x_i^k-\eta_i r_i^k.
$$

Here $F_i$ returns the same type and units as $x_i$; $\eta_i$ is dimensionless in this discrete convention. A separate event transition updates memory and parameters from admissible observations and witnessed outcomes. Its clock, ownership of feedback, and write permissions are part of the model.

This expression alone proves little: an arbitrary update can often be rewritten as a residual. The substantive restrictions must be supplied independently: which information a patch can read, which variables it can change, which discrepancies count, which updates are admissible, and which observations would contradict the model. A core extracted by choosing these definitions after seeing successful trajectories would be circular.

| Contract element | Cadence source interpretation | OPH finite-repair interpretation | EFMW candidate obligation |
| --- | --- | --- | --- |
| Local state and interface | Neural activity, adaptation, directed wiring and evidence ports | Finite patch states and overlap projections, with declared gauge equivalence | Give types to state, observer and memory variables |
| Agreement | Satisfaction of the complete selected API's equations | Compatible overlap observations on the chosen finite branch | Specify a residual or compatibility predicate independently of success |
| Repair | A specified solver and budget; acceptance/refusal depends on API | Admissible local moves with protected boundaries and descent conditions | Give an executable update and its permitted information |
| Retention | Live state, trace, records and learned parameters have distinct roles | Preservation of specified observations or boundary data | Identify what persists, its update clock and its error signal |
| Global claim | Qualified numerical answer, separately assessed for correctness | Existence, reachability and identification require separate hypotheses | Prove the actual correspondence, then test external predictions |

The table records candidate relationships, not established equivalences. The [Cadence contracts][cadence-contracts] specifically distinguish graph settlement, finite learning phases, qualified learning, record scans and temporal repair. In the composed `Brain`, trace and associative memory are held inputs during settlement and updated separately. Their presence does not make every stored variable part of one simultaneous equilibrium. Default reward eligibility also has a finite-phase contract; it does not inherit a convergence guarantee from qualified action selection.

Likewise, numerical agreement need not make all neurons equal. It means that each satisfies its own equation. A local update law may still use a global software reduction to qualify an answer; this proposal makes no hardware-decentralization claim.

### A meaningful translation

For a source system $A$ and proposed kernel $K$, define state and evidence maps $R_A$ and $\rho_A$. On a declared domain, a strong target is

$$
R_A\bigl(U_A(s;e)\bigr)
=U_K\bigl(R_A(s);\rho_A(e)\bigr).
$$

Require observable-output preservation as well. State whether a transition is one primitive move, a complete sweep, or a feedback transaction. If one source step corresponds to several target steps, specify that simulation relation. If the correspondence is approximate, give a norm and an error bound over a stated horizon. A one-way simulation establishes only that direction; an equivalence claim needs inverse-compatible maps up to the declared quotient, or an appropriate bisimulation.

The maps must preserve local information restrictions and distinguish state from memory, parameters, optimizer state, random state and accounting. OPH's finite or quotient states cannot silently become Cadence's real-valued arrays. Establishing an abstraction, discretization or restricted realization is a result to prove.

## 3. The formal programme: consistency, reachability, and perturbation

The useful bridge is between *a consistent configuration exists* and *this local process can reach it*. The fork's [earlier analysis](AGREEMENT_AND_SURPRISE_EFMW_ANALYSIS.md), the [OPH consensus exposition][oph-consensus], and the EFMW [projected-gluing work][efmw-gluing] motivate four distinct obligations:

1. **Static compatibility.** Define the overlaps, protected observations and quotient. Prove the applicable existence or gluing statement in those types.
2. **Constructible local repair.** Show that a permitted write can repair the required boundary while preserving protected data. Existence of a global completion alone does not provide this procedure.
3. **Progress and schedule.** Prove termination or convergence under the actual acceptance rule and scheduler. On a finite state space, strict decrease rules out infinitely many accepted decreasing moves. Reaching zero inconsistency additionally needs the absence of incompatible terminal states and appropriate execution progress; an execution can otherwise stall or reject forever.
4. **Identification and learning.** Same-source confluence concerns different repair orders from one source. Identifying endpoints from different sources needs additional observation/quotient conditions. Learning introduces a changing transition system and needs its own hypotheses.

### A first bridge with a complete, modest proof

Use a restricted real-valued model as an adapter exercise. On a finite connected undirected graph, take positive edge weights $w_{ij}$, nonnegative anchors $\kappa_i$, at least one positive anchor, and fixed real evidence $y_i$. Set

$$
V(z;y)=\frac12\sum_{\{i,j\}}w_{ij}(z_i-z_j)^2
+\frac12\sum_i\kappa_i(z_i-y_i)^2.
$$

With graph Laplacian $L_w$, $D=\operatorname{diag}(\kappa_i)$, and $A=L_w+D$, the local flow is

$$
\dot z=-\nabla V=-Az+Dy.
$$

**Proposition, under these assumptions.** There is a unique equilibrium $z^*=A^{-1}Dy$. Continuous repair converges exponentially to it. Synchronous discrete repair $z^{k+1}=z^k-\eta(Az^k-Dy)$ converges for $0<\eta<2/\lambda_{\max}(A)$.

**Proof.** For nonzero $v$, $v^TAv$ is the sum of weighted squared edge differences and anchored squared values. Its vanishing would force a constant vector by connectivity and then the zero vector by the positive anchor. Thus $A$ is positive definite. The error satisfies $\dot e=-Ae$ in continuous time and $e^{k+1}=(I-\eta A)e^k$ in discrete time. Diagonalizing the symmetric matrix gives the claims. For an evidence change with weights and anchors fixed,

$$
\|\Delta z^*\|_2
\leq \|A^{-1}D\|_2\,\|\Delta y\|_2.
$$

This is a standard special case, included to make the proposed correspondence checkable. It offers a candidate instance of EFMW ME-069 with zero additional feedback and noise, and a target for a restricted reciprocal neural realization. Conflicting anchors can leave nonzero edge disagreements at equilibrium: stationary balance is not automatically OPH's zero-overlap compatibility. That difference must survive the translation.

The proof supplies neither a finite-OPH adapter nor a theorem for arbitrary directed Cadence graphs. Those are open obligations. A Lean formalization should reuse established results and state exactly which runtime configuration meets its assumptions.

For more general fixed-point models, a contraction would give the familiar bound $\|x-x^*\|\leq\|x-F(x)\|/(1-q)$ for contraction constant $q<1$. Without such a condition or another stability argument, a small defect establishes neither uniqueness nor attraction. Shrinking increments alone establish even less. Perfect synchronization can also coexist with motion; stillness follows only when agreement is defined as a zero of the complete dynamical generator.

## 4. What, exactly, would EFMW add?

The first task is a mechanism inventory. The [frozen EFMW catalogue][efmw-equations] labels ME-064 as a symbolic construct, ME-069 and ME-072 as working constructs, and ME-048 as a working metric. Those distinctions should remain visible.

| EFMW item | Initial use in this programme | Test before adding machinery |
| --- | --- | --- |
| ME-064: state–observation–memory recursion | A schema for retained local computation | Can its operators be instantiated by the existing continuing brain? |
| ME-065: observer–observed closure | A candidate contract for coupled observation and feedback | Do existing reciprocal observers already implement the proposed relation? |
| ME-069: cognitive attractor dynamics | A restricted potential-based correspondence | Do the actual weights, activation and update rule admit the claimed potential? |
| ME-072: recursive memory validation | First candidate for an additional learning mechanism | Is its instantiated rule distinct from existing witnessed-outcome memory updates? |
| ME-024 / ME-048: coherence and integrity | Possible measured state or diagnostic | Does the quantity add information beyond a conventional mismatch measure? |

The first executable candidate should therefore be a **local memory-validation mechanism**, if the inventory finds a missing one. The catalogue's ME-072 has the form

$$
m_i^{t+1}=m_i^t+\alpha\,[\mathcal C(m_i^t,x_t)-\lambda\epsilon_i^t].
$$

It becomes an experiment only after specifying what a memory entry contains, the functions $\mathcal C$ and $\epsilon_i$, their units, bounds, locality, and their dependence on actual outcomes. A discrepancy between a state and its own recalled prediction is not independent evidence that either is wrong. The environment must supply the relevant outcome through the existing action-feedback transaction.

If a new observer state $q_i$ is necessary, its state-dependent readback and feedback must enter the same coupled residual:

$$
r_i^x=x_i-F_i(x_{N(i)},q_{N(i)},e_i,m_i;\theta),
\qquad
r_i^q=q_i-H_i(q_{N(i)},x_{N(i)},e_i,m_i;\psi).
$$

Both defects must be checked during qualification, using declared scales and tolerances for their respective units. These equations are an **interface specification**, not an implemented mechanism: the functions, wiring, clocks and coefficients remain to be frozen. A controller that reads a completed solve and changes learning afterwards has a different contract and must be evaluated as such. An EFMW score that only records a trajectory is a diagnostic, not the experimental extension $E$.

Two early exits are scientifically valuable. If the instantiated EFMW rule is the existing Cadence rule under a change of variables, publish the correspondence and remove the duplicate mechanism. If the missing capability is repaired by existing state or experience, preserve that simpler solution. A new label earns no extra experimental factor.

## 5. A bounded experiment that can discriminate

### Existing evidence motivates a harder task

The [published Cadence Zoo audit][cadence-audit] examined Cadence 0.78.0 at one explicitly configured operating point, with three seeds and five arms in an odour reversal chamber. The means of final 100-action accuracy were:

| Arm | First A | Reversal B | Returned A |
| --- | ---: | ---: | ---: |
| Full continuing `live` brain | 100.0% | 100.0% | 100.0% |
| Associative memory disabled (`graph-only`) | 65.3% | 61.0% | 73.3% |
| Actor policy learning frozen (`memory-only`) | 100.0% | 91.3% | 90.0% |

The last arm retains the graph, critic and memory; its instrument name does not mean it contains only memory. All three full-system lives retained the stable skill at the measured probes. Selected tests produced 159 passes and 28 optional-backend skips. These are bounded audit results, not a complete local release-suite run or a hybrid evaluation. The full system's saturated endpoints and the task's sensory-key structure motivate the next test.

### Task: retained history, new combinations, changed consequences

Use an ordered-cue environment in which the same observation at the decision point requires different actions after different histories. Primitive cues occur in training; selected combinations and distractor sequences are withheld. An independently specified generator supplies the correct action and actual-action outcomes. Include:

1. acquisition of a history-dependent relation and an unrelated stable skill;
2. tests on held-out combinations;
3. interfering traffic and reversal of one relation, while the stable relation remains valid;
4. return of the earlier rule and further transfer tests;
5. a save/reload boundary with a real action awaiting feedback.

The generator must prevent a current-cue lookup from solving the history-dependent part and ensure that the histories contain enough information to solve it. A simple full-history reference and an information-limited lookup control can check those properties during development. Privileged task labels must never enter a candidate through hidden state, a teacher or an external answer head.

Freeze the held-out split at the level of cue combinations or task families. New random seeds in a familiar lookup chamber are insufficient. Score held-out choices before revealing their outcomes; specify how probes use and restore state, prevent teaching leakage, and charge their work. Keep the acquired brain through the main life rather than constructing a fresh trained model for each row.

### Factorial comparison, conditional on a valid decomposition

After the mechanism inventory, freeze $K$, the shared executable kernel; $C$, the distinct Cadence mechanisms under examination; and $E$, one distinct executable EFMW-motivated addition.

| Arm | Shared kernel $K$ | Additional Cadence mechanism $C$ | Defined EFMW mechanism $E$ |
| --- | --- | --- | --- |
| $K$ | On | Off | Off |
| $K+C$ | On | On | Off |
| $K+E$ | On | Off | On |
| $K+C+E$ | On | On | On |

These letters denote frozen implementations, not whole theories. Put any genuinely shared trace or learning mechanism in $K$ so it is not counted twice. Preserve common ports and specify the neutral replacement for each disabled component. If $C$ and $E$ cannot be separated without changing the meaning of the task or the shared mechanism, abandon this factorial and report nested ablations of the full system instead. A deliberately incapable $K$ would not establish useful complementarity.

For higher-is-better held-out accuracy $S$, report both incremental benefit and interaction:

$$
\Delta_E=S_{K+C+E}-S_{K+C},
\qquad
I=S_{K+C+E}-S_{K+C}-S_{K+E}+S_K.
$$

Positive $\Delta_E$ means benefit over the Cadence comparator on this score. Positive $I$ indicates complementarity on this particular additive scale; bounded-score ceilings can affect it. Neither implies a new universal mechanism. Report per-founder values and uncertainty, not just an aggregate winning arm.

### Proposed confirmation contract

Use **20 new founders** with paired exogenous streams and initialization for shared components. All arms receive the same allowed information and opportunities; each receives outcomes for its own executed actions. Different actions can produce different experiences, so the comparison estimates the effect on a whole continuing life. Use a separately labelled fixed-record diagnostic when isolating a single update law.

The proposed primary score is held-out history-task accuracy immediately after interference/reversal. Proposed acceptance requires at least a five-percentage-point mean improvement of $K+C+E$ over $K+C$, a paired 95% interval excluding zero, and all preservation gates. As an absolute capability gate, propose that at least 18 of 20 complete lives each achieve both 90% history-task accuracy and 95% stable-skill performance at every specified phase endpoint. Count refusals as unsuccessful decisions in the accuracy denominator and report them separately. These are **proposed thresholds**, not executed results, upstream requirements, or an already registered protocol.

Freeze the interval method, endpoint panels, budgets, initialization, tuning allowance, family split, failure handling and stopping rule before confirmation. Resample complete founders, not correlated actions, for a founder-level interval. Twenty founders define a bounded initial study; a development variance estimate should determine whether a larger confirmatory sample is needed before any confirmation results are examined. Retain every founder and failed phase.

Compare fixed opportunity budgets and disclose actual work. Include all repair and qualification sweeps, nudged phases, memory access and writes, observer computations, failed attempts, probes, checkpoint costs, wall time and storage. A reduced learning-sweep count is not a proportional reduction in total computation or energy. Retain source-bound per-action and feedback records sufficient for independent replay.

Preservation covers acquisition, trace, associative recall, reward reversal, correct action-credit ownership, private imagination, refusal rollback and exact saved continuation under the selected API's contract. Any required regression blocks promotion. Existing release gates stay in place even if the new primary score improves.

## 6. Ablate the claimed core, then substitute ordinary mechanisms

Once a capable reference exists, intervene separately on neighbour feedback, retained history, parameter learning, and informative outcome feedback. Freeze the precise cut and its neutral replacement before looking at the result. A no-history control must remove every route carrying the relevant past, including neural activity, traces and records; disabling associative memory alone is insufficient. A learning-frozen arm can still retain working state. A feedback-shuffled control must preserve timing and marginal reward statistics while breaking the specified action-outcome information.

Also replace any EFMW-specific quantity with a conventional mismatch signal using the same accessible evidence. Compare an equally sized recurrent or observer module, with matched information, tuning opportunity and measured work. If this substitute explains the improvement, the supported result is a useful generic mechanism; the specifically EFMW interpretation remains unestablished.

Define the empirical common core as the **smallest subset in the preregistered candidate set that meets all frozen capability and preservation requirements**. Enumerate that small set where feasible. Single deletions establish at most local irreducibility; compensating components and removal order can conceal smaller successful subsets. A minimal successful subset on this task is not a universally minimal brain.

## 7. Use the Zoo as an audit, with fixed operations

Start with the two operations already executed in the earlier audit. Their meanings come from the pinned [CAT][zoo-cat] and [RHINO][zoo-rhino] sources. This paper proposes their use on new data; it does not report a fresh Zoo run.

| Operation | Purpose and frozen inputs | Transformation and output | Criterion and current status |
| --- | --- | --- | --- |
| CAT ablation penalty | Assess a specified removal; paired loss $1-S$ for full and ablated lives | Ablated loss minus full loss; signed penalty | Positive means removal hurt on that endpoint. New hybrid values: **unresolved / not run**. Statistical adequacy is a separate test. |
| RHINO retention | Assess the stable skill; raw acquired baseline and post-interference score | Canonical clipped ratio, retaining its defined zero-baseline branch | Interpret alongside both raw scores and the absolute 95% floor. New hybrid values: **unresolved / not run**. |

For a zero baseline, the canonical RHINO branch returns 1 when the later score is also zero and 0 otherwise. For positive baselines it clips the ratio to $[0,1]$. Consequently, a ratio of 1 can accompany an inadequate skill. The previous audit exposed this concretely: 0.125 improving to 0.375 produced a clipped ratio of 1. The absolute gate prevents that case from being called successful retention.

Do not convert the remaining animal names into review metaphors or claim a completed 46-operation audit. Additional operators require their own frozen schemas, suitable inputs and acceptance criteria. Scores derived from the same trajectories also remain dependent evidence.

## 8. Novelty, failure conditions, and deliverables

Consensus dynamics already have established convergence analyses, including explicit topology and delay conditions [Olfati-Saber and Murray, 2004][consensus]. Local free/nudged learning has a direct precedent in [Equilibrium Propagation][eqprop]. [Deep Equilibrium Models][deq] compute fixed-point representations with implicit differentiation; that does not identify their learning rule with every Cadence API. The quadratic proposition above is standard mathematics. The proposed contribution is a checked correspondence plus a capability-preserving comparison that identifies which retained mechanisms matter.

The present assessment is **adjacent structural overlap**. Exact equivalence or reparameterization remains to be proved for chosen restrictions. A useful distinct mechanism is a hypothesis. No exhaustive novelty claim is made.

| Possible finding | Evidence status it would justify | Consequence |
| --- | --- | --- |
| The state maps preserve restricted transitions and observations | Demonstrated correspondence for that restriction | Publish the adapters, assumptions and proof scope |
| EFMW's instantiated update equals an existing Cadence rule | Demonstrated equivalence/reparameterization for that rule | Remove duplicate machinery; retain the explanatory translation |
| The addition beats matched simpler controls and preserves required capabilities | Supported, bounded mechanistic benefit | Retain the opt-in implementation; expand independent tests |
| The gain disappears against a conventional substitute | EFMW-specific advantage unsupported on this test | Keep the simpler explanation and the negative comparison |
| A promised improvement misses its frozen gate | Promotion claim rejected under this protocol; an uncertain effect can remain unresolved | Preserve the failure; do not tune on confirmation outcomes |
| Local state or observation maps cannot satisfy the proposed relation | Proposed correspondence rejected on that domain | Publish the obstruction and state any smaller surviving domain |

Physical claims form a separate research branch. The existing [conditional continuum study](OPH_EFMW_CONTINUUM_LIMIT.md) adds a carrier, clock, inertial update and source identification to construct a scalar-wave limit. Those additions are not forced by canonical accepted repairs. Neither a neural benchmark nor the present quadratic lemma validates EFMW's physical field equation, OPH's broader physical programme, or universality across reality. The discussion of *Agreement and Surprise* in this fork used the supplied abstract; its full proofs and fly-brain simulations were not independently verified here.

### A small collaboration with useful stopping points

| Stage | Reviewable deliverable | Proceed when |
| --- | --- | --- |
| 1. Translation | State/interface dictionary, mechanism inventory, explicit counterexamples, restricted adapter specification | The common claim has independent constraints and preserves the relevant observations |
| 2. Formal bridge | Small proof development and executable checks for the selected restriction | Every numerical or finite-model assumption is accounted for; unsupported directions stay open |
| 3. Development | Simplest continuing System 1 baseline, one demonstrated limitation, one fully specified candidate and simpler substitute | The limitation survives information, experience and implementation checks |
| 4. Frozen experiment | Protocol, source commits, generator and split hashes, budgets, paired founder list, full logs and checkpoint receipts | Acceptance conditions are fixed before confirmation outcomes are opened |
| 5. Reduction | Factorial or nested comparison, core ablations, preserved failures and a minimal-subset claim with exact scope | Required capabilities survive and the claimed benefit exceeds its matched control |

The invitation to Bernhard is to review the canonical Cadence/OPH contracts and select the smallest limitation worth testing. The EFMW side can take responsibility for typing its selected relations, freezing its mechanism and Zoo operations, and documenting where the translation fails. These are proposed roles, not agreed commitments.

The first decision is deliberately small: **does a distinct EFMW mechanism remain after translating what Cadence already does?** If it does, the continuing-brain experiment gives it a fair test. If it does not, a proved common core is already a worthwhile result.

## Source and evidence ledger

Repository claims in this proposal refer to the following snapshots, not to moving default branches. The proposed implementation and experiment need their own later pins.

| Source | Frozen revision | Use and limit |
| --- | --- | --- |
| Cadence | `750c8ef45b17ba052279584e49c685ff3d169a82` | Version 0.78.0 contracts and contribution rules; no claim about later changes |
| OPH Lab fork, before this proposal | `a1b8eb3dfb9b5a4cbf549d74cf33af3d3dbc3aea` | Exposition and prior independent analyses; controlling physical papers remain authoritative |
| Cadence Zoo evidence | `e71387449cf0b3f616f990184505b55ffb78c0ec` | Prior three-seed chamber results and selected test logs; no hybrid data |
| EFMW audit/catalogue snapshot | `93c80ff4710e7fc61a84f21943149db550d4ee71` | Selected equation definitions and projected-gluing scope |
| Monolithic Zoo Lean4 | `94e0a9e2550a8fe62b03dc8213e3e3942c30899b` | CAT/RHINO operation definitions; no new Lean build or whole-Zoo execution in this paper |

Related documents: [Agreement and Surprise analysis](AGREEMENT_AND_SURPRISE_EFMW_ANALYSIS.md), [conditional continuum construction](OPH_EFMW_CONTINUUM_LIMIT.md), and [independent OPH Zoo review](EFMW_ZOO_REVIEW.md).

[cadence-contributing]: https://github.com/muellerberndt/cadence/blob/750c8ef45b17ba052279584e49c685ff3d169a82/CONTRIBUTING.md
[cadence-contracts]: https://github.com/muellerberndt/cadence/blob/750c8ef45b17ba052279584e49c685ff3d169a82/docs/contracts.md
[oph-consensus]: https://github.com/enuminous/oph-lab/blob/a1b8eb3dfb9b5a4cbf549d74cf33af3d3dbc3aea/src/pages/ConsensusProtocol.tsx
[efmw-gluing]: https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/93c80ff4710e7fc61a84f21943149db550d4ee71/docs/PROJECTED_GLUING_REPAIR.md
[efmw-equations]: https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/93c80ff4710e7fc61a84f21943149db550d4ee71/research_engine/data/equations.json
[cadence-audit]: https://github.com/enuminous/Cadence-Zoo-Evidence/blob/e71387449cf0b3f616f990184505b55ffb78c0ec/CADENCE_ZOO_REVIEW.md
[zoo-cat]: https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/94e0a9e2550a8fe62b03dc8213e3e3942c30899b/Cat.lean
[zoo-rhino]: https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/94e0a9e2550a8fe62b03dc8213e3e3942c30899b/Rhino.lean
[consensus]: https://authors.library.caltech.edu/records/t2gnt-vd720
[eqprop]: https://arxiv.org/abs/1602.05179v5
[deq]: https://arxiv.org/abs/1909.01377v2
