import { useMemo } from 'react';
import { ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';
import {
    CURRENT_RESEARCH_STATUS,
    FLAGSHIP_PHILPAPERS_URL,
    MINI_UNIVERSE_SIMULATION_URL,
    OPH_PAPERS,
    RESEARCH_RELEASE_DATE,
    RESEARCH_RELEASE_ID,
    SIMULATION_FRONTIER,
    TEXTBOOKS_URL,
} from '../content/paperSurface';
import {
    ALPHA_U_COMPARISON_REFERENCE_DISPLAY,
    ALPHA_U_FORWARD_REFERENCE_DISPLAY,
    BETA_COEFFICIENTS_MSSM_LIKE,
    COMMON_LOAD_CAPACITY_DISPLAY,
    ELECTROWEAK_BRIDGE_CAPACITY_DISPLAY,
    FINITE_PRESENCE_CAPACITY_DISPLAY,
    GRAVITATIONAL_CONSTANT_REFERENCE_SI,
    PIXEL_COMPARISON_REFERENCE_DISPLAY,
    PIXEL_FORWARD_REFERENCE_DISPLAY,
    PIXEL_REFERENCE,
    POISSON_CAPACITY_DISPLAY,
    SCREEN_CAPACITY_REFERENCE_DISPLAY,
    SCREEN_CAPACITY_REFERENCE_EXACT_DISPLAY,
    SCREEN_CAPACITY_REFERENCE_LOG10,
    deriveD11ForwardSeed,
    deriveTargetFreeElectroweakRepair,
    formatPixelConstant,
    hubbleFromLambda,
    lambdaFromScreen,
    newtonConstantFromScaleCertificate,
    solveGaugeClosure,
} from '../core/ophMath';

type CoreLockRow = {
    label: string;
    value: string;
    equation: string;
    note: string;
};

type SurfaceBoardRow = {
    label: string;
    family: string;
    familyClass: 'gr' | 'qft' | 'exact' | 'candidate';
    primaryLabel: string;
    primaryValue: string;
    secondaryLabel: string;
    secondaryValue: string;
};

const CANONICAL_GAUGE_OPTIONS = {
    betaCoefficients: BETA_COEFFICIENTS_MSSM_LIKE,
    su2MaxJ: 30,
    su3MaxIndex: 14,
    alphaRange: { min: 0.015, max: 0.09, step: 0.0005 },
} as const;

// Interval-certified unique root of the declared incomplete source map.
// Physical promotion also requires target-independent map selection,
// a same-quantity bridge, and same-scheme endpoint transport.
const ALPHA_ROOT_INV = 136.994835177413;
// Root of the declared gauge-width map. This is another incomplete-map diagnostic,
// not a physical fine-structure prediction.
const ALPHA_GAUGE_WIDTH_FP_INV = 137.0356601369466;

function formatFixed(value: number, digits = 6): string {
    if (!Number.isFinite(value)) {
        return 'n/a';
    }
    return value.toFixed(digits);
}

function formatScientific(value: number, digits = 3): string {
    if (!Number.isFinite(value)) {
        return 'n/a';
    }
    return value.toExponential(digits);
}

function renderCoreLocks(rows: CoreLockRow[]) {
    return (
        <div className="landing-controls-grid">
            {rows.map((row) => (
                <article key={row.label} className="input-control-card">
                    <div className="input-control-header">
                        <div>
                            <div className="input-control-label">{row.label}</div>
                            <div className="input-control-value">{row.value}</div>
                        </div>
                    </div>
                    <div className="input-control-caption">{row.equation}</div>
                    <p style={{ margin: '12px 0 0', fontSize: '0.82em', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                        {row.note}
                    </p>
                </article>
            ))}
        </div>
    );
}

function renderCompactSurfaceBoard(rows: SurfaceBoardRow[]) {
    return (
        <section className="card compact-live-board">
            <div className="metric-section-header">
                <div>
                    <h3 style={{ margin: 0, fontSize: '0.95em' }}>Closure and comparison readouts</h3>
                    <p className="compact-live-board-copy">
                        Each tile shows a paper-surface coordinate with its claim status.
                        Target-anchored quark diagnostics are excluded.
                    </p>
                </div>
                <span style={{ fontSize: '0.72em', color: 'var(--accent-gold)', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                    {rows.length} rows
                </span>
            </div>
            <div className="compact-live-grid">
                {rows.map((row) => (
                    <article key={`${row.family}-${row.label}`} className="compact-live-card">
                        <div className="compact-live-card-header">
                            <strong className="compact-live-label">{row.label}</strong>
                            <span className={`compact-live-family compact-live-family-${row.familyClass}`}>{row.family}</span>
                        </div>
                        <div>
                            <span className="metric-card-caption">{row.primaryLabel}</span>
                            <div className="compact-live-value">{row.primaryValue}</div>
                        </div>
                        <div className="compact-live-baseline">
                            <span className="metric-card-caption">{row.secondaryLabel}</span>
                            <div className="compact-live-baseline-value">{row.secondaryValue}</div>
                        </div>
                    </article>
                ))}
            </div>
        </section>
    );
}

export function Home() {
    const canonicalSurface = useMemo(() => {
        const closure = solveGaugeClosure(PIXEL_REFERENCE, CANONICAL_GAUGE_OPTIONS);
        const electroweakRepair = deriveTargetFreeElectroweakRepair(closure);
        const higgsTop = deriveD11ForwardSeed(electroweakRepair);
        const newtonConstant = newtonConstantFromScaleCertificate();
        const lambda = lambdaFromScreen(PIXEL_REFERENCE, SCREEN_CAPACITY_REFERENCE_LOG10);
        const hubble = hubbleFromLambda(lambda);

        return {
            closure,
            electroweakRepair,
            higgsTop,
            newtonConstant,
            lambda,
            hubble,
        };
    }, []);

    const coreLocks = useMemo<CoreLockRow[]>(() => [
        {
            label: 'Measured-endpoint comparison P_C',
            value: formatPixelConstant(PIXEL_REFERENCE),
            equation: 'P_C = phi + sqrt(pi) / A_T(P_C)',
            note: `The comparison branch uses P_C=${PIXEL_COMPARISON_REFERENCE_DISPLAY} and alpha_U(P_C)=${ALPHA_U_COMPARISON_REFERENCE_DISPLAY}. A physical Thomson value requires target-independent map selection, a same-quantity bridge, and source-derived same-scheme transport.`,
        },
        {
            label: 'Global N closure boundary',
            value: 'no source-selected N',
            equation: 'N = log M0(U_N)',
            note: `Self-reference forces equality after supplied and read-back values are typed as the same invariant. An exact bounded generation-register counterfamily is non-identifying, while universal A1–A3 membership is unproved. Direct N is not evaluable and emits no cosmic value. Exact compositional completions select neither the finite-presence value ${FINITE_PRESENCE_CAPACITY_DISPLAY} nor the Poisson value ${POISSON_CAPACITY_DISPLAY}; both are target-exposed retrospective comparisons.`,
        },
        {
            label: 'Comparison-endpoint hierarchy coordinate',
            value: ELECTROWEAK_BRIDGE_CAPACITY_DISPLAY,
            equation: 'N_EW(P_C) = pi exp(6pi/(P_C alpha_U(P_C)))',
            note: 'This measured-endpoint bridge coordinate is distinct from the source-forward common-load coordinate.',
        },
        {
            label: 'Source-forward common-load coordinate',
            value: COMMON_LOAD_CAPACITY_DISPLAY,
            equation: 'N0(P_fwd) = pi exp(6pi/(P_fwd alpha_U(P_fwd)))',
            note: `P_fwd=${PIXEL_FORWARD_REFERENCE_DISPLAY} and alpha_U(P_fwd)=${ALPHA_U_FORWARD_REFERENCE_DISPLAY}. This value is 6.6166% above the Planck base-LambdaCDM coordinate ${SCREEN_CAPACITY_REFERENCE_EXACT_DISPLAY}.`,
        },
        {
            label: 'Repair tick lock',
            value: '24',
            equation: 'm_rep = 2(8 + 3 + 1)',
            note: 'This product-adjoint round count is independent of the screen register; its hierarchy use requires the separate screen-readout receipt.',
        },
        {
            label: 'Newton scale certificate',
            value: formatScientific(GRAVITATIONAL_CONSTANT_REFERENCE_SI, 10),
            equation: 'G_SI = c^3 ell_*^2 / hbar',
            note: 'G is read from the selected no-G scale certificate. The local P factor cancels in the Newton row.',
        },
    ], []);

    const surfaceBoardRows = useMemo<SurfaceBoardRow[]>(() => [
            {
                label: "Newton's gravitational constant",
                family: 'GRAVITY',
                familyClass: 'gr' as const,
                primaryLabel: 'OPH',
                primaryValue: `${formatScientific(canonicalSurface.newtonConstant, 6)} m^3 kg^-1 s^-2`,
                secondaryLabel: 'source',
                secondaryValue: 'no-G scale certificate',
            },
            {
                label: 'Cosmological constant',
                family: 'GRAVITY',
                familyClass: 'gr' as const,
                primaryLabel: 'input-based display',
                primaryValue: `${formatScientific(canonicalSurface.lambda, 3)} m^-2`,
                secondaryLabel: 'source',
                secondaryValue: 'Lambda-located capacity',
            },
            {
                label: 'Hubble rate',
                family: 'GRAVITY',
                familyClass: 'gr' as const,
                primaryLabel: 'input-based display',
                primaryValue: `${formatScientific(canonicalSurface.hubble, 3)} s^-1`,
                secondaryLabel: 'source',
                secondaryValue: 'measured Lambda',
            },
            {
                label: 'Hierarchy naturality',
                family: 'EXACT',
                familyClass: 'exact' as const,
                primaryLabel: 'selected branch',
                primaryValue: '0',
                secondaryLabel: 'bridge',
                secondaryValue: '24 ticks',
            },
            {
                label: 'Fine-structure map roots',
                family: 'COUPLINGS',
                familyClass: 'qft' as const,
                primaryLabel: 'incomplete gauge-width map',
                primaryValue: formatFixed(ALPHA_GAUGE_WIDTH_FP_INV, 9),
                secondaryLabel: 'incomplete source map; hadronic payload required',
                secondaryValue: formatFixed(ALPHA_ROOT_INV, 9),
            },
            {
                label: 'W running-chart coordinate',
                family: 'BOSONS',
                familyClass: 'qft' as const,
                primaryLabel: 'non-pole chart',
                primaryValue: `${formatFixed(canonicalSurface.electroweakRepair.mWGeV, 9)} GeV`,
                secondaryLabel: 'surface',
                secondaryValue: 'scheme map absent',
            },
            {
                label: 'Z running-chart coordinate',
                family: 'BOSONS',
                familyClass: 'qft' as const,
                primaryLabel: 'non-pole chart',
                primaryValue: `${formatFixed(canonicalSurface.electroweakRepair.mZGeV, 9)} GeV`,
                secondaryLabel: 'surface',
                secondaryValue: 'scheme map absent',
            },
            {
                label: 'Higgs boson mass',
                family: 'BOSONS',
                familyClass: 'qft' as const,
                primaryLabel: 'OPH',
                primaryValue: `${formatFixed(canonicalSurface.higgsTop.mHGeV, 9)} GeV`,
                secondaryLabel: 'surface',
                secondaryValue: 'Higgs/top split',
            },
            {
                label: 'Top mass',
                family: 'BOSONS',
                familyClass: 'qft' as const,
                primaryLabel: 'OPH',
                primaryValue: `${formatFixed(canonicalSurface.higgsTop.mtPoleGeV, 9)} GeV`,
                secondaryLabel: 'surface',
                secondaryValue: 'Higgs/top split',
            },
        ], [canonicalSurface]);

    return (
        <div className="landing-surface-page">
            <section className="research-hero">
                <p className="research-hero-kicker">Research companion · {RESEARCH_RELEASE_ID} · {RESEARCH_RELEASE_DATE}</p>
                <h1>See what OPH proves, assumes, tests, and does not derive.</h1>
                <p className="research-hero-copy">
                    Observer Patch Holography studies bounded, self-reading systems with local state, ports,
                    records, readback, and repair. This Lab connects the formal paper stack to finite simulator
                    receipts without flattening branch conditions or exploratory diagnostics into physical claims.
                </p>
                <div className="research-hero-actions">
                    <a className="btn btn-primary" href={TEXTBOOKS_URL}>Start with the textbooks</a>
                    <a className="btn btn-ghost" href={FLAGSHIP_PHILPAPERS_URL}>Read the technical paper</a>
                    <a className="btn btn-ghost" href={MINI_UNIVERSE_SIMULATION_URL}>Open the simulation</a>
                </div>
            </section>

            <section className="status-grid" aria-label="Research results and boundaries">
                {CURRENT_RESEARCH_STATUS.map((item) => (
                    <article key={item.label} className="status-card">
                        <span className="status-card-kicker" style={{ color: item.tier === 'structural' ? 'var(--accent-green)' : item.tier === 'branch-conditional' ? 'var(--accent-gold)' : 'var(--accent-cyan)' }}>
                            {item.tier}
                        </span>
                        <h3>{item.label}</h3>
                        <p>{item.summary}</p>
                    </article>
                ))}
            </section>

            <div className="demo-container landing-controls-shell" style={{ marginTop: 0 }}>
                <div className="landing-controls-header">
                    <h2 className="landing-controls-title">Closure and comparison surface</h2>
                    <div className="landing-actions landing-actions-top">
                        <Link className="btn btn-ghost" to="/de-sitter">
                            Capacity sensitivity
                        </Link>
                        <Link className="btn btn-ghost" to="/masses">
                            Particle surface
                        </Link>
                    </div>
                </div>
                <p className="landing-controls-intro">
                    These coordinates are kept beside their epistemic status. Algebraic roots, calibration rows,
                    target-exposed comparisons, and physical readouts are not interchangeable.
                </p>

                {renderCoreLocks(coreLocks)}
            </div>

            {renderCompactSurfaceBoard(surfaceBoardRows)}
            <p className="landing-surface-note">
                The first screen separates algebraic roots from physical readouts. P<sub>C</sub> belongs to an incomplete
                electromagnetic map. The Planck base-LambdaCDM chain supplies the retrospective coordinate
                {SCREEN_CAPACITY_REFERENCE_DISPLAY}. The measured-endpoint P<sub>C</sub> bridge and source-forward
                P<sub>fwd</sub> bridge are separate coordinates. The latter is 6.6166% higher than the Planck
                comparison. Its finite-presence candidate is 0.6287% lower, and the extra-premise Poisson candidate is
                0.3880% lower. Exact same-source compositional completions disagree on the global action, so neither
                row is selected and the exposed comparison has no predictive weight. Physical use requires a stronger
                source law, common-load and seam identifications, and the horizon-record bridge.
                Numeric quark rows are absent because the source equations leave
                a free (R<sub>&gt;0</sub>)<sup>2</sup> spread fiber. The retained target audit also mixes mass schemes,
                and its GeV-valued matrices are not physical dimensionless Yukawas.
            </p>

            <section className="card landing-links-card">
                <div className="landing-links-header">
                    <h3 style={{ margin: 0, fontSize: '0.95em' }}>Inspect The Proof Surfaces</h3>
                    <p className="landing-links-copy">
                        The lab summarizes the paper stack. The PDFs and code are the source surface for theorem details.
                    </p>
                </div>
                <div className="landing-links-grid">
                    <a
                        className="landing-link-tile"
                        href="https://github.com/FloatingPragma/observer-patch-holography/blob/main/paper/deriving_the_particle_zoo_from_observer_consistency.pdf"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <span className="landing-link-kicker">Paper</span>
                        <strong className="landing-link-title">Deriving the Particle Zoo</strong>
                        <span className="landing-link-body">Particle derivations, hierarchy branch, and quantitative rows.</span>
                        <span className="landing-link-cta">
                            <ExternalLink size={14} />
                            Open paper
                        </span>
                    </a>
                    <a
                        className="landing-link-tile"
                        href="https://github.com/FloatingPragma/observer-patch-holography/tree/main/code/particles"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        <span className="landing-link-kicker">Code</span>
                        <strong className="landing-link-title">Particles Code</strong>
                        <span className="landing-link-body">Browse the derivation artifacts and particle-status code in GitHub.</span>
                        <span className="landing-link-cta">
                            <ExternalLink size={14} />
                            Open code
                        </span>
                    </a>
                </div>
            </section>

            <section className="card landing-links-card">
                <div className="landing-links-header">
                    <h3 style={{ margin: 0, fontSize: '0.95em' }}>Finite-simulator evidence</h3>
                    <p className="landing-links-copy">
                        The source packages describe bounded self-reading systems with local state, ports, records and
                        feedback. Each calculation states its actual shared data, action and clock.
                    </p>
                </div>
                <div className="landing-links-grid">
                    {SIMULATION_FRONTIER.map((item) => (
                        <article key={item.label} className="landing-link-tile">
                            <span className="landing-link-kicker">{item.status}</span>
                            <strong className="landing-link-title">{item.label}</strong>
                            <span className="landing-link-body">{item.summary}</span>
                        </article>
                    ))}
                </div>
                <a className="landing-link-cta" href={MINI_UNIVERSE_SIMULATION_URL}>
                    <ExternalLink size={14} />
                    Explore the visual simulator
                </a>
            </section>

            <div className="card" style={{ marginBottom: '24px' }}>
                <h3 style={{ marginTop: 0, fontSize: '0.95em' }}>OPH Paper Stack</h3>
                <div style={{ display: 'grid', gap: '12px' }}>
                    {OPH_PAPERS.map((paper) => (
                        <a
                            key={paper.slug}
                            href={paper.href}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                                display: 'block',
                                padding: '14px',
                                background: 'rgba(0,0,0,0.18)',
                                border: '1px solid var(--border-color)',
                                textDecoration: 'none',
                            }}
                        >
                            <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', marginBottom: '6px' }}>
                                <strong style={{ color: 'var(--text-primary)' }}>{paper.title}</strong>
                                <span style={{ color: 'var(--accent-gold)', fontSize: '0.78em' }}>{paper.surface}</span>
                            </div>
                            <div style={{ fontSize: '0.82em', color: 'var(--text-secondary)' }}>{paper.summary}</div>
                        </a>
                    ))}
                </div>
            </div>
        </div>
    );
}
