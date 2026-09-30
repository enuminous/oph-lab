import { Explainer } from '../components/Explainer';
import { BOSON_PUBLIC_ROWS, PARTICLE_LANE_STATUS, RESEARCH_REPO_URL, SPACETIME_PUBLIC_ROWS, STANDARD_MODEL_SURFACE } from '../content/paperSurface';
import { SCREEN_CAPACITY_REFERENCE_DISPLAY } from '../core/ophMath';

export function QftEmergesPage() {
    return (
        <div>
            <div className="section-header">
                <span className="section-tag qft">Chain 2: QFT</span>
                <h1 style={{ fontSize: '1.5rem', margin: 0 }}>QFT Reconstruction Boundary</h1>
            </div>

            <p style={{ marginBottom: '16px' }}>
                The finite quantum record algebra and conditional gauge classification supply distinct mathematical
                ingredients. A specified free scalar action on prepared source addresses supports a common classical
                and Fock-space detector comparison with controlled spatial and temporal errors. The full physical interacting
                Standard Model requires further source, locality, state and continuum identifications.
            </p>

            <div className="math-block" style={{ fontSize: '0.95em', lineHeight: '2.2' }}>
                complete compact port response plus endogenous carrier transport &rarr;
                u(1)&oplus;su(2)&oplus;su(3) &rarr; declared fifteen-state fixture with
                N_c=3 and a common Z6 kernel &rarr; matter and global-form selection not derived
            </div>

            <div className="card" style={{ marginTop: '24px', marginBottom: '24px', borderLeft: '3px solid var(--accent-cyan)' }}>
                <h3 style={{ margin: '0 0 10px 0', fontSize: '0.95em' }}>Paper-surface summary</h3>
                <div style={{ display: 'grid', gap: '8px', marginBottom: '12px' }}>
                    {STANDARD_MODEL_SURFACE.map((item) => (
                        <div key={item} style={{ fontSize: '0.82em', color: 'var(--text-secondary)' }}>
                            {item}
                        </div>
                    ))}
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '8px' }}>
                    {BOSON_PUBLIC_ROWS.map((row) => (
                        <div key={row.label} style={{ padding: '10px', background: 'rgba(0,0,0,0.18)', border: '1px solid var(--border-color)' }}>
                            <div style={{ fontSize: '0.78em', color: 'var(--text-muted)' }}>{row.label}</div>
                            <div style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>{row.value}</div>
                        </div>
                    ))}
                </div>
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Quantum reconstruction routes</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '24px' }}>
                {[
                    {
                        step: '1',
                        title: 'Quantum mechanics as effective algebraic description',
                        detail: 'Patch algebras, states, trace/Born event probabilities, and record updating belong to the OPH working basis.',
                        color: 'var(--accent-blue)',
                    },
                    {
                        step: '2',
                        title: 'Entanglement structure',
                        detail: 'The Tsirelson upper bound 2\u221a2 and a declared Bell-state witness live in the supplied complex Hilbert-space setting. The declared source counts do not produce a Bell violation; contextual readout requires a separate construction.',
                        color: 'var(--accent-blue)',
                    },
                    {
                        step: '3',
                        title: 'Quantum error correction',
                        detail: 'The declared recovery interface is code-like and supplies recoverability under named hypotheses. It is not a theorem that physical spacetime is literally a quantum code on every branch.',
                        color: 'var(--accent-blue)',
                    },
                    {
                        step: '4',
                        title: 'Gauge symmetry from patch gluing',
                        detail: 'Gauge-as-gluing fixes one common strict transport representative per stage and retains the seed sectors trivial under it. On a cofinal tail carrying the explicit refinement receipt, Tannaka-Krein reconstructs compact G from the tensor category and forgetful fiber.',
                        color: 'var(--accent-cyan)',
                    },
                    {
                        step: '5',
                        title: 'Standard Model gauge group',
                        detail: 'The finite A5 packet forces the abstract Lie type and the declared fixture carries three colors plus a common Z6 kernel. No physical global form or matter selection is derived; N_g=3 is a declared completion inside the 3-to-5 window.',
                        color: 'var(--accent-cyan)',
                    },
                    {
                        step: '6',
                        title: 'Matter-sector continuations',
                        detail: 'The icosahedral screen supplies an exact A5/C3 local three-corner carrier. It derives no physical charged-family attachment or mass-value law.',
                        color: 'var(--accent-gold)',
                    },
                    {
                        step: '7',
                        title: 'Coupling unification',
                        detail: 'Peter-Weyl second-index mechanism \u2192 MSSM-like beta shifts \u0394b \u2248 (2.49, 4.38, 3.97) without superpartners.',
                        color: 'var(--accent-gold)',
                    },
                    {
                        step: '8',
                        title: 'Quantum field theory as effective description',
                        detail: 'A specified massive free scalar field in a Dirichlet cube has a joint spatial/time detector limit, including vanishing response before continuum arrival. Physical source selection and an interacting relativistic field theory require additional construction.',
                        color: 'var(--accent-green)',
                    },
                ].map((item) => (
                    <div key={item.step} className="card" style={{ borderLeft: `3px solid ${item.color}` }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                width: '28px',
                                height: '28px',
                                background: `${item.color}22`,
                                border: `1px solid ${item.color}`,
                                fontSize: '0.75em',
                                fontWeight: 700,
                                color: item.color,
                                flexShrink: 0,
                            }}>
                                {item.step}
                            </span>
                            <div>
                                <h4 style={{ margin: 0, fontSize: '0.9em' }}>{item.title}</h4>
                                <p style={{ margin: '4px 0 0', fontSize: '0.8em', color: 'var(--text-muted)' }}>
                                    {item.detail}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>What Chain 2 Uses and Derives</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '24px' }}>
                <div style={{ padding: '12px', background: 'rgba(122, 184, 212, 0.1)', border: '1px solid rgba(122, 184, 212, 0.3)', fontSize: '0.85em' }}>
                    <div style={{ color: 'var(--accent-blue)', fontWeight: 600, marginBottom: '4px' }}>Structural outputs</div>
                    <ul style={{ paddingLeft: '16px', margin: 0, lineHeight: '1.8' }}>
                        <li>Patch operator algebras and states as the starting language</li>
                        <li>Born/trace event probabilities on declared record algebras</li>
                        <li>Measurement as local record updating</li>
                        <li>Tsirelson bound (2&radic;2) in the supplied operator setting; no source-derived Bell violation</li>
                        <li>Axiom-forced compact Lie type u(1) &oplus; su(2) &oplus; su(3)</li>
                        <li>No source reconstruction of the complete current is derived</li>
                        <li>Rank-three candidate family band; declared completion N<sub>g</sub> = 3</li>
                        <li>Three colors and hypercharges inside the declared matter fixture</li>
                        <li>Common Z6 kernel inside that fixture; no physical global form is derived</li>
                        <li>Gauge-calibration and unification surfaces</li>
                        <li>No minimal simple-GUT X/Y exchange channel in the product adjoint</li>
                        <li>Conditional classical massless photon and graviton carrier modes</li>
                    </ul>
                </div>
                <div style={{ padding: '12px', background: 'rgba(201, 169, 110, 0.1)', border: '1px solid rgba(201, 169, 110, 0.3)', fontSize: '0.85em' }}>
                    <div style={{ color: 'var(--accent-gold)', fontWeight: 600, marginBottom: '4px' }}>Input Ledger</div>
                    <ul style={{ paddingLeft: '16px', margin: 0, lineHeight: '1.8' }}>
                        <li>Oriented twelve-port observer screen</li>
                        <li>Observer agreement</li>
                        <li>Conditional maximum randomness</li>
                        <li>Recovery and generalized-entropy interfaces (declared premises, not axioms)</li>
                        <li>Finite-dimensional regulator premise</li>
                        <li>Boundary gauge fixed-point premise</li>
                        <li>Central or higher-associator strictification plus at least one allowed strict representative with trivial represented loop holonomy where global transportability is invoked</li>
                        <li>Declared sector completions (three generations, one Higgs, no extra light sectors) without derived physical selection</li>
                        <li>Symmetric braiding in the 3+1D EFT branch</li>
                        <li>Compact-gauge refinement receipt: finite extendability, explicit center-compatible block-multiplicity embeddings, common stagewise strict representatives, and coherent surjective boundary-group maps that intertwine them</li>
                        <li>Finite tensor realizations and compatible objectwise finite-dimensional forgetful fibers, or an explicit super-Tannakian fork</li>
                    </ul>
                    <div style={{ marginTop: '12px', padding: '8px', background: 'rgba(0,0,0,0.2)', fontSize: '0.9em' }}>
                        <strong>Quantitative closure coordinates</strong>
                        <div style={{ color: 'var(--text-muted)', marginTop: '4px' }}>
                            P is a certified root of a declared incomplete local map. The direct global proposal is
                            N = log M<sub>0</sub>(𝔘<sub>N</sub>). Self-reference forces equality only after the
                            supplied and read-back quantities are proved to describe the same invariant. An exact bounded
                            all-rung generation-register counterfamily is non-identifying. Universal membership in the
                            complete A1–A3 source contract is unproved, so direct N is not evaluable and emits no cosmic value.
                        </div>
                    </div>
                </div>
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Shared causal-spacetime substrate</h3>
            <p style={{ marginBottom: '16px' }}>
                A physical relativistic field theory needs a common event, metric and clock interpretation. The
                source-record causal/count limit and the supplied free scalar comparison give concrete mathematical
                models. Their shared source addresses do not identify the field history with the recorded event order.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px', marginBottom: '16px' }}>
                {SPACETIME_PUBLIC_ROWS.map((row) => (
                    <div key={row.label} className="card" style={{ borderLeft: `3px solid ${row.tier === 'structural' ? 'var(--accent-cyan)' : 'var(--accent-rose)'}` }}>
                        <div style={{ fontSize: '0.75em', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{row.tier}</div>
                        <h4 style={{ margin: '4px 0', fontSize: '0.9em' }}>{row.label}</h4>
                        <div style={{ color: 'var(--accent-green)', fontWeight: 700, fontSize: '0.82em' }}>{row.value}</div>
                        <p style={{ margin: '8px 0 0', fontSize: '0.78em', color: 'var(--text-secondary)' }}>{row.note}</p>
                    </div>
                ))}
            </div>
            <p style={{ marginBottom: '24px', fontSize: '0.84em', color: 'var(--text-secondary)' }}>
                The declared golden record family has an analytic causal/count limit. Complete local reads use a
                radius that shrinks more slowly than the population gaps. Interior interval counts recover volume
                and proper-duration ratios. The field action uses the same prepared address family with different
                finite mass weights; its model evolution and count clock are not identified by that fact.
            </p>
            <p style={{ marginBottom: '24px', fontSize: '0.84em', color: 'var(--text-secondary)' }}>
                The <a href={`${RESEARCH_REPO_URL}/tree/main/code/source_scalar_time_refinement`} target="_blank" rel="noreferrer">scalar refinement certificate</a>
                compares a compact coherent preparation and separated compact detector with the massive Dirichlet
                continuum field. At q=233 and step 2<sup>&minus;17</sup>, selecting the nearest update inside
                [0.95,1] gives probability error below 0.050078 and selected split response above 0.137746 at every
                reference time in that window. The bound includes full operator leakage, localization tails,
                time stepping and the original vacuum covariance change. The large tensor history is unexecuted;
                boundary, action, quantum convention and refinement are declared.
            </p>
            <p style={{ marginBottom: '24px', fontSize: '0.84em', color: 'var(--text-secondary)' }}>
                The separate <a href={`${RESEARCH_REPO_URL}/tree/main/code/source_scalar_clock_quantum`} target="_blank" rel="noreferrer">64-site clock comparison</a>
                uses actual configuration records and a supplied stationary action, with one duration per whole layer.
                Under its hidden-history and error-budget assumptions, 15 of 21 original-vacuum detector comparisons
                resolve a signed response throughout the inferred time intervals. At update 16, error is at most
                0.000811258283 and the continuous response is negative with magnitude at least 0.008694950984.
                This preparation differs from q=233; neither spatial errors nor clock bounds transfer between them.
                These are effect expectations, with physical calibration and outcome recording requiring separate inputs.
            </p>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Physical interacting continuum</h3>
            <p style={{ marginBottom: '16px' }}>
                A cosmological application of the proposed interacting field theory would additionally relate the model to these physical scales:
            </p>
            <ul style={{ paddingLeft: '20px', lineHeight: '1.8', marginBottom: '16px' }}>
                <li>The Lambda-located horizon count is large (N<sub>&Lambda;</sub> &asymp; {SCREEN_CAPACITY_REFERENCE_DISPLAY})</li>
                <li>The curvature scale is much larger than the Planck length (L &gt;&gt; l<sub>P</sub>)</li>
                <li>The observables are "coarse-grained" over many pixels</li>
            </ul>
            <p style={{ marginBottom: '16px' }}>
                The free Dirichlet comparison does not require this cosmological scale identification. A physical
                interacting field theory on reconstructed spacetime additionally needs a nonperturbative observable
                construction with locality, covariance, positivity, a spectral condition and controlled refinement.
            </p>

            <Explainer title="Why QFT breaks down at the Planck scale">
                <p>
                    In the intended physical interpretation, QFT is an effective description at energies
                    E &lt;&lt; M<sub>P</sub>. OPH motivates a finite-carrier completion, but does not prove that the
                    continuum approximation fails by exactly this mechanism. The candidate picture is:
                </p>
                <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
                    <li>Individual pixels become resolved (the "lattice spacing" of the screen)</li>
                    <li>The finite carrier capacity of the screen (Axiom A1) limits the number of degrees of freedom</li>
                    <li>A physical event geometry, if constructed, may require a finite-scale correction model</li>
                </ul>
                <p>
                    This is the programmatic reason OPH uses a finite screen algebra at the fundamental level. It is
                    not a completed theorem that this mechanism alone explains perturbative non-renormalizability.
                </p>
            </Explainer>

            <Explainer title="Chain 1 and Chain 2: same axioms, different paths">
                <p>
                    Both chains share the same three core axioms; the realized matter sector enters through the
                    declared completions:
                </p>
                <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
                    <li><strong>Chain 1 (GR):</strong> Three typed branches coexist rather than forming one linear chain: the exact source poset and ambient 1+3 carrier, the conditional BW/null/entropy branch, and the exact typed finite Einstein-shape implication. A smooth physical Einstein description follows only after their same-family causal, continuum, field, stress, and curvature certificates are supplied.</li>
                    <li><strong>Chain 2 (QFT):</strong> Emphasizes observer agreement on overlaps, gauge-as-gluing, transportability, the explicit compact-gauge refinement receipt, and the declared sector completions. Result: receipt-conditional compact gauge reconstruction, the structural Standard Model branch, and downstream conditional extensions.</li>
                </ul>
                <p>
                    The two chains share the same screen and foundational structure. In Chain 2 the admissibility
                    filters cut the candidate class, and the realized sector enters through the declared completions.
                </p>
                <p>
                    Synthesis page shows how they combine into a unified picture.
                </p>
            </Explainer>

            <Explainer title="Matter-Lane Boundaries In Chain 2">
                <p>
                    Chain 2 separates a strong structural core from several matter-sector boundaries:
                </p>
                <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
                    <li>Quark source equations leave a free (R<sub>&gt;0</sub>)<sup>2</sup> spread fiber, so numeric rows are withheld; the mixed-scheme target packet and GeV mass textures do not define physical dimensionless Yukawas.</li>
                    <li>Charged leptons have an exact A<sub>5</sub>/C<sub>3</sub> face-corner carrier and a conditional fixed-point theorem for one declared map. An engineered digital CFQ model closes schema nonemptiness and gives a central record dilation, but its registers, automaton, grading, clock, and response are authored inputs, and historical no-target ancestry fails audit. A conditional nature/pole theorem gives the correct transport implications after the physical Yukawa response and CFQ-to-Dyson singularity readout are assumed; its zero-self-energy kernel is only a free witness. Its 0.000300 ppm headline uses rounded fields; the tau residual is -1.387289 ppm against the packet's higher-precision central value. No physical source selection, attachment, determinant, coherent branch, cofinal refinement, interacting kernel, or infrared completion is derived.</li>
                    <li>Neutrino isotropic no-go retained; the target-informed weighted-cycle point is a rejected comparison candidate without source, basis, Takagi, or ordering certificates</li>
                    <li>Higgs/top proof structure and scope discipline around the closed source-only split theorem</li>
                    <li>Hadron backend / compute-bound closure</li>
                </ul>
                <p>
                    The foundation (axioms &rarr; gauge branch &rarr; particle-structure ledger) is stronger than the
                    detailed matter continuations. The QFT landing is a typed dependency graph: QFT-Q2 and QFT-Q3
                    are parallel descendants of QFT-Q1, strict finite-order W/Z algebra belongs to QFT-Q3, and
                    QFT-Q4 separately requires a nonperturbative observable tower and resonance continuation.
                    These conditional implications are checked. W/Z carry no physical pole prediction status because
                    the OPH-native action, quantum construction, matching and identity transcripts, physical-current
                    amplitudes, numerical freeze, observable tower, analytic sheet, and clock are not supplied. The
                    weighted-cycle neutrino candidate is rejected, while the charged lane and the quark source-spread,
                    scheme-coordinate and physical-Yukawa boundaries are stated explicitly.
                </p>
                <div style={{ display: 'grid', gap: '8px', marginTop: '12px' }}>
                    {PARTICLE_LANE_STATUS.map((lane) => (
                        <div key={lane.label} style={{ fontSize: '0.82em', color: 'var(--text-secondary)' }}>
                            <strong>{lane.label}:</strong> {lane.summary}
                        </div>
                    ))}
                </div>
            </Explainer>
        </div>
    );
}
