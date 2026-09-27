import { Explainer } from '../components/Explainer';
import {
    BLOG_URL,
    CHALLENGE_URL,
    CLAIM_TIER_LEGEND,
    FLAGSHIP_PAPER_HTML_URL,
    FLAGSHIP_PAPER_TITLE,
    FLAGSHIP_PHILPAPERS_URL,
    LAB_REPO_URL,
    MINI_UNIVERSE_SIMULATION_URL,
    MATH_FOUNDATIONS_PAPER,
    OPH_PAPERS,
    OVERVIEW_URL,
    PHYSICS_UNIFICATION_URL,
    RESEARCH_LICENSE_URL,
    RESEARCH_PAPER_DIR_URL,
    RESEARCH_PATENT_POLICY_URL,
    RESEARCH_RELEASE_DATE,
    RESEARCH_RELEASE_ID,
    RESEARCH_REPO_URL,
    SIMULATOR_REPO_URL,
    SIMULATION_URL,
    TEXTBOOK_MACHINE_URL,
    TEXTBOOK_OUTPUTS_URL,
    TEXTBOOKS_URL,
    THEORY_URL,
} from '../content/paperSurface';

const BACKGROUND_READING = [
    {
        category: 'Holographic Principle',
        items: [
            { author: "G. 't Hooft", title: 'Dimensional Reduction in Quantum Gravity', year: '1993', ref: 'gr-qc/9310026' },
            { author: 'L. Susskind', title: 'The World as a Hologram', year: '1995', ref: 'hep-th/9409089' },
            { author: 'R. Bousso', title: 'The Holographic Principle', year: '2002', ref: 'hep-th/0203101' },
        ],
    },
    {
        category: 'Thermodynamic Gravity',
        items: [
            { author: 'T. Jacobson', title: 'Thermodynamics of Spacetime: The Einstein Equation of State', year: '1995', ref: 'gr-qc/9504004' },
            { author: 'T. Jacobson', title: 'Entanglement Equilibrium and the Einstein Equation', year: '2015', ref: '1505.04753' },
            { author: 'E. Verlinde', title: 'On the Origin of Gravity and the Laws of Newton', year: '2010', ref: '1001.0785' },
        ],
    },
    {
        category: 'Quantum Information and Modular Theory',
        items: [
            { author: 'A. Almheiri, X. Dong, D. Harlow', title: 'Bulk Locality and Quantum Error Correction in AdS/CFT', year: '2014', ref: '1411.7041' },
            { author: 'J. Bisognano, E. Wichmann', title: 'On the Duality Condition for Quantum Fields', year: '1976', ref: 'JMP 17:303' },
            { author: 'A. Connes, C. Rovelli', title: 'Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation', year: '1994', ref: 'gr-qc/9406019' },
        ],
    },
];

export function ResourcesPage() {
    return (
        <div>
            <div className="section-header">
                <span className="section-tag foundation">Reference</span>
                <h1 style={{ fontSize: '1.5rem', margin: 0 }}>Resources</h1>
            </div>

            <p style={{ marginBottom: '24px' }}>
                Primary sources, mirrors, and entry points for the OPH public stack. This Lab is aligned to paper
                snapshot <strong>{RESEARCH_RELEASE_ID}</strong> ({RESEARCH_RELEASE_DATE}) and the finite
                simulator boundary recorded with that snapshot.
            </p>

            <div className="card" style={{ marginBottom: '24px', borderLeft: '3px solid var(--accent-gold)' }}>
                <h4 style={{ margin: '0 0 8px', fontSize: '0.9em', color: 'var(--accent-gold)' }}>How the public surfaces fit together</h4>
                <p style={{ margin: 0, fontSize: '0.84em' }}>
                    Use the textbooks for guided exposition, this Lab for interactive status-aware exploration, the
                    papers and Lean/code for technical claims, and simulator receipts for finite computational tests.
                    If explanatory wording conflicts with a controlling paper or receipt, the paper plus its formal or
                    executable evidence controls the research status.
                </p>
            </div>

            <div className="card" style={{ marginBottom: '24px', borderLeft: '3px solid var(--accent-cyan)' }}>
                <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-cyan)' }}>
                    Search Entry Pages
                </h4>
                <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                    For readers arriving via high-intent public queries, OPH maintains dedicated entry pages for
                    <strong> theory of everything</strong>, <strong> physics unification</strong>, and <strong> simulation theory</strong>.
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                    <a href={THEORY_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        theory of everything &rarr;
                    </a>
                    <a href={PHYSICS_UNIFICATION_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        physics unification &rarr;
                    </a>
                    <a href={SIMULATION_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        simulation theory &rarr;
                    </a>
                    <a href={OVERVIEW_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        OPH overview &rarr;
                    </a>
                    <a href={BLOG_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        OPH blog &rarr;
                    </a>
                </div>
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Seven-Paper Release Stack</h3>
            <p style={{ marginBottom: '16px', fontSize: '0.85em', color: 'var(--text-muted)' }}>
                The Lab lists the flagship synthesis plus six focused papers. Use the individual paper that matches
                the surface you are discussing.
            </p>

            <div style={{ display: 'grid', gap: '12px', marginBottom: '24px' }}>
                {OPH_PAPERS.map((paper) => (
                    <div key={paper.slug} className="card" style={{ borderLeft: '3px solid var(--accent-gold)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', marginBottom: '8px' }}>
                            <h4 style={{ margin: 0, fontSize: '0.9em', color: 'var(--accent-gold)' }}>{paper.title}</h4>
                            <span style={{ fontSize: '0.75em', color: 'var(--accent-cyan)' }}>{paper.surface}</span>
                        </div>
                        <p style={{ margin: '0 0 10px 0', fontSize: '0.85em', color: 'var(--text-secondary)' }}>
                            {paper.summary}
                        </p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                            <a href={paper.href} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                                Open paper &rarr;
                            </a>
                            {paper.htmlHref && (
                                <a href={paper.htmlHref} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                                    HTML version &rarr;
                                </a>
                            )}
                            <a href={RESEARCH_PAPER_DIR_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                                Paper directory &rarr;
                            </a>
                        </div>
                    </div>
                ))}
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Mathematical Companion</h3>
            <p style={{ marginBottom: '16px', fontSize: '0.85em', color: 'var(--text-muted)' }}>
                This standalone paper supplies the application-neutral theorem layer used to distinguish repair-order
                independence from reconstruction across different states with the same observable boundary. It is not a
                seventh core OPH paper and does not select a physical boundary map or repair law.
            </p>

            <div className="card" style={{ marginBottom: '24px', borderLeft: '3px solid var(--accent-purple)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', marginBottom: '8px' }}>
                    <h4 style={{ margin: 0, fontSize: '0.9em', color: 'var(--accent-purple)' }}>
                        {MATH_FOUNDATIONS_PAPER.title}
                    </h4>
                    <span style={{ fontSize: '0.75em', color: 'var(--accent-cyan)' }}>
                        {MATH_FOUNDATIONS_PAPER.surface}
                    </span>
                </div>
                <p style={{ margin: '0 0 10px 0', fontSize: '0.85em', color: 'var(--text-secondary)' }}>
                    {MATH_FOUNDATIONS_PAPER.summary}
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                    <a
                        href={MATH_FOUNDATIONS_PAPER.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ fontSize: '0.85em' }}
                    >
                        Open companion paper &rarr;
                    </a>
                    <a
                        href={`${RESEARCH_REPO_URL}/tree/main/Lean/ObserverPatchHolography/Proofs/ObservableNormalForms`}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ fontSize: '0.85em' }}
                    >
                        Inspect Lean artifact &rarr;
                    </a>
                </div>
            </div>

            <div className="card" style={{ marginBottom: '24px', borderLeft: '3px solid var(--accent-blue)' }}>
                <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-blue)' }}>
                    How To Read The Status Language
                </h4>
                <div style={{ display: 'grid', gap: '8px' }}>
                    {CLAIM_TIER_LEGEND.map((item) => (
                        <div key={item.tier} style={{ fontSize: '0.82em' }}>
                            <strong>{item.label}:</strong>{' '}
                            <span style={{ color: 'var(--text-secondary)' }}>{item.description}</span>
                        </div>
                    ))}
                </div>
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Other OPH Surfaces</h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px', marginBottom: '24px' }}>
                <div className="card" style={{ borderLeft: '3px solid var(--accent-blue)' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-blue)' }}>
                        Technical paper
                    </h4>
                    <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                        {FLAGSHIP_PAPER_TITLE}. Primary technical account of the observer-first reconstruction and its
                        stated boundaries.
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                        <a href={FLAGSHIP_PHILPAPERS_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                            philpapers.org/rec/MUEFOC &rarr;
                        </a>
                        <a href={FLAGSHIP_PAPER_HTML_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                            HTML version &rarr;
                        </a>
                    </div>
                </div>

                <div className="card" style={{ borderLeft: '3px solid var(--accent-green)' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-green)' }}>
                        Floating Pragma Blog
                    </h4>
                    <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                        Public essays and entry points connecting OPH to meaning, computation, semiotics, and interpretation.
                    </p>
                    <a href={BLOG_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        blog.floatingpragma.io &rarr;
                    </a>
                </div>

                <div className="card" style={{ borderLeft: '3px solid var(--accent-cyan)' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-cyan)' }}>
                        OPH Textbooks
                    </h4>
                    <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                        Guided study surface for readers who want a structured path. The newer Machine and Outputs
                        books use the same observer, record, repair, and readback vocabulary as this Lab.
                    </p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
                        <a href={TEXTBOOKS_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>Textbooks &rarr;</a>
                        <a href={TEXTBOOK_MACHINE_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>The OPH Machine &rarr;</a>
                        <a href={TEXTBOOK_OUTPUTS_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>The Outputs &rarr;</a>
                    </div>
                </div>

                <div className="card" style={{ borderLeft: '3px solid var(--accent-gold)' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-gold)' }}>
                        Mini-Universe Simulation
                    </h4>
                    <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                        Visual explorer for observer patches, overlap readback, repair pressure, records, and the conditional geometry branch.
                    </p>
                    <a href={MINI_UNIVERSE_SIMULATION_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        simulation.floatingpragma.io &rarr;
                    </a>
                    {' · '}
                    <a href={SIMULATOR_REPO_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        receipt source &rarr;
                    </a>
                </div>

                <div className="card" style={{ borderLeft: '3px solid var(--accent-green)' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-green)' }}>
                        OPH Challenge
                    </h4>
                    <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                        Public objection and review surface for testing the paper corpus.
                    </p>
                    <a href={CHALLENGE_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        challenge.floatingpragma.io &rarr;
                    </a>
                </div>

                <div className="card" style={{ borderLeft: '3px solid var(--accent-purple)' }}>
                    <h4 style={{ margin: '0 0 8px 0', fontSize: '0.9em', color: 'var(--accent-purple)' }}>
                        OPH Lab Repo
                    </h4>
                    <p style={{ margin: '0 0 8px 0', fontSize: '0.85em' }}>
                        The codebase for this interactive lab app.
                    </p>
                    <a href={LAB_REPO_URL} target="_blank" rel="noopener noreferrer" style={{ fontSize: '0.85em' }}>
                        github.com/muellerberndt/oph-lab &rarr;
                    </a>
                </div>
            </div>

            <h3 style={{ fontSize: '1em', marginTop: '32px' }}>Background Reading</h3>
            <p style={{ marginBottom: '16px', fontSize: '0.85em', color: 'var(--text-muted)' }}>
                A small starter set from the broader literature behind holography, thermodynamic gravity, and modular
                structure.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
                {BACKGROUND_READING.map((section) => (
                    <div key={section.category}>
                        <h4 style={{ margin: '0 0 8px 0', fontSize: '0.85em', color: 'var(--accent-gold)' }}>
                            {section.category}
                        </h4>
                        {section.items.map((item) => (
                            <div
                                key={`${section.category}-${item.ref}`}
                                style={{
                                    padding: '8px 12px',
                                    background: 'rgba(0,0,0,0.15)',
                                    border: '1px solid var(--border-color)',
                                    marginBottom: '4px',
                                    fontSize: '0.8em',
                                }}
                            >
                                <span style={{ color: 'var(--text-primary)' }}>{item.author}</span>
                                <span style={{ color: 'var(--text-muted)' }}> ({item.year}). </span>
                                <span style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>{item.title}. </span>
                                <span style={{ color: 'var(--accent-cyan)' }}>{item.ref}</span>
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            <Explainer title="How to cite OPH material">
                <p>
                    Cite the specific paper that matches the claim you are discussing. The public OPH surface spans
                    the flagship synthesis, six focused papers, and maintained extra papers.
                </p>
                <p>
                    For the flagship paper, cite its PhilPapers record:{' '}
                    <a href={FLAGSHIP_PHILPAPERS_URL} target="_blank" rel="noopener noreferrer">
                        {FLAGSHIP_PAPER_TITLE}
                    </a>.
                </p>
                <p>
                    For technical statements, it is better to cite the exact paper and visible release line than to
                    cite the lab or a bundled summary.
                </p>
            </Explainer>

            <Explainer title="Research and code links">
                <p>
                    The main research repo is:
                </p>
                <p>
                    <a href={RESEARCH_REPO_URL} target="_blank" rel="noopener noreferrer">
                        {RESEARCH_REPO_URL}
                    </a>
                </p>
                <p>
                    The paper sources live under the paper directory:
                </p>
                <p>
                    <a href={RESEARCH_PAPER_DIR_URL} target="_blank" rel="noopener noreferrer">
                        {RESEARCH_PAPER_DIR_URL}
                    </a>
                </p>
                <p>
                    License and patent policy:
                </p>
                <p>
                    <a href={RESEARCH_LICENSE_URL} target="_blank" rel="noopener noreferrer">
                        Main license and anti-patent covenant
                    </a>
                    {' | '}
                    <a href={RESEARCH_PATENT_POLICY_URL} target="_blank" rel="noopener noreferrer">
                        PATENTS.md
                    </a>
                </p>
            </Explainer>
        </div>
    );
}
