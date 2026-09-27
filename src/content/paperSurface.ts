export type ClaimTier =
    | 'structural'
    | 'branch-conditional'
    | 'frozen-prospective'
    | 'calibration'
    | 'continuation-only'
    | 'compare-only'
    | 'open'
    | 'exploratory';

export type PaperSummary = {
    slug: string;
    title: string;
    href: string;
    htmlHref?: string;
    surface: string;
    summary: string;
};

export type PublicRow = {
    label: string;
    value: string;
    tier: ClaimTier;
    note: string;
};

export const RESEARCH_REPO_URL = 'https://github.com/FloatingPragma/observer-patch-holography';
export const RESEARCH_PAPER_DIR_URL = `${RESEARCH_REPO_URL}/tree/main/paper`;
export const RESEARCH_LICENSE_URL = `${RESEARCH_REPO_URL}/blob/main/LICENSE`;
export const RESEARCH_PATENT_POLICY_URL = `${RESEARCH_REPO_URL}/blob/main/PATENTS.md`;
export const LAB_REPO_URL = 'https://github.com/muellerberndt/oph-lab';
export const SIMULATOR_REPO_URL = 'https://github.com/muellerberndt/oph-physics-sim';
export const OVERVIEW_URL = 'https://floatingpragma.io/oph/';
export const THEORY_URL = 'https://floatingpragma.io/oph/theory-of-everything/';
export const SIMULATION_URL = 'https://floatingpragma.io/oph/simulation-theory/';
export const PHYSICS_UNIFICATION_URL = 'https://floatingpragma.io/oph/physics-unification/';
export const BLOG_URL = 'https://blog.floatingpragma.io/';
export const TEXTBOOKS_URL = 'https://learn.floatingpragma.io/';
export const TEXTBOOK_MACHINE_URL = 'https://learn.floatingpragma.io/book/machine/chapter/0';
export const TEXTBOOK_OUTPUTS_URL = 'https://learn.floatingpragma.io/book/outputs/chapter/0';
export const MINI_UNIVERSE_SIMULATION_URL = 'https://simulation.floatingpragma.io/';
export const CHALLENGE_URL = 'https://challenge.floatingpragma.io/';
export const RESEARCH_RELEASE_ID = 'r2042';
export const RESEARCH_RELEASE_DATE = '10 September 2026';

const GITHUB_PDF_BASE = `${RESEARCH_REPO_URL}/blob/main/paper`;
const GITHUB_EXTRA_PDF_BASE = `${RESEARCH_REPO_URL}/blob/main/extra`;
export const FLAGSHIP_PAPER_TITLE = 'Finite Observer Consensus as a Reconstruction Principle';
export const FLAGSHIP_PHILPAPERS_URL = 'https://philpapers.org/rec/MUEFOC';
export const FLAGSHIP_PAPER_HTML_URL = 'https://floatingpragma.io/oph/papers/from-observer-consensus-to-standard-physics/';

export const OPH_PAPERS: PaperSummary[] = [
    {
        slug: 'flagship',
        title: FLAGSHIP_PAPER_TITLE,
        href: FLAGSHIP_PHILPAPERS_URL,
        htmlHref: FLAGSHIP_PAPER_HTML_URL,
        surface: 'Flagship synthesis',
        summary: 'The primary OPH paper: finite self-reading patches, public quantum records, Lorentz-frame algebra, and conditional geometry, Einstein, and Standard Model branches.',
    },
    {
        slug: 'einstein',
        title: 'Recovering Observer Spacetime and Einstein Dynamics from Overlap Consistency',
        href: `${GITHUB_PDF_BASE}/recovering_observer_spacetime_and_einstein_dynamics_from_overlap_consistency.pdf`,
        surface: 'Spacetime and Gravity',
        summary: 'The source metric, declared causal/count limit, reconstructed action clock and joint spatial/time scalar detector limit, with physical inputs stated for the Einstein route.',
    },
    {
        slug: 'gauge',
        title: 'Deriving Standard Model Gauge Structure from Observer Overlap Consistency',
        href: `${GITHUB_PDF_BASE}/deriving_standard_model_gauge_structure_from_observer_overlap_consistency.pdf`,
        surface: 'Gauge Structure',
        summary: 'The categorical and finite-carrier gauge routes, conditional Standard Model matter image, and physical global-form boundary.',
    },
    {
        slug: 'particles',
        title: 'Deriving the Particle Zoo from Observer Consistency',
        href: `${GITHUB_PDF_BASE}/deriving_the_particle_zoo_from_observer_consistency.pdf`,
        surface: 'Particles',
        summary: 'The particle-status paper. It separates structural outputs, running-chart diagnostics, the conditional capacity-electroweak bridge, compare-only sidecars, continuation lanes, and theorem surfaces.',
    },
    {
        slug: 'consensus',
        title: 'Reality as a Consensus Protocol',
        href: `${GITHUB_PDF_BASE}/reality_as_consensus_protocol.pdf`,
        surface: 'Consensus',
        summary: 'The fixed-point and repair paper. It formalizes overlap reconciliation, schedule-independent normal form, refinement/coarse-graining compatibility, gauge-quotient uniqueness, and stable records.',
    },
    {
        slug: 'microphysics',
        title: 'Federated Echosahedral Screen Microphysics',
        href: `${GITHUB_PDF_BASE}/screen_microphysics_and_observer_synchronization.pdf`,
        surface: 'Observer Machinery',
        summary: 'The concrete federated patch-carrier architecture. It turns patches, overlaps, records, public hardware-evidence rules, checkpoint/restoration, and observer synchronization into one fixed-cutoff surface.',
    },
    {
        slug: 'paradise',
        title: 'Paradise as Fixed-Point Consensus',
        href: `${GITHUB_PDF_BASE}/paradise_as_fixed_point_consensus.pdf`,
        surface: 'Meaning Layer',
        summary: 'The final manifest paper. It carries the OPH account of existence, observer continuation, justice, paradise, hell, resurrection, and memetic evolution.',
    },
];

export const MATH_FOUNDATIONS_PAPER: PaperSummary = {
    slug: 'observation-determined-normal-forms',
    title: 'Observation-Determined Normal Forms',
    href: `${GITHUB_EXTRA_PDF_BASE}/observable_normal_forms.pdf`,
    surface: 'Mathematical Foundations',
    summary: 'A standalone, application-neutral companion separating same-source confluence, cross-source observation-based identification, liveness, and local repairability. It also develops quantitative stability and refinement receipts, with a machine-checked finite core.',
};

export const CLAIM_TIER_LEGEND: Array<{ tier: ClaimTier; label: string; description: string }> = [
    {
        tier: 'structural',
        label: 'Structural',
        description: 'Recovered theorem-grade output that does not depend on a compare-only sidecar.',
    },
    {
        tier: 'branch-conditional',
        label: 'Branch-Conditional',
        description: 'Recovered only on a stated theorem-local premise stack such as the BW or null-stress branch.',
    },
    {
        tier: 'frozen-prospective',
        label: 'Frozen Prospective',
        description: 'Registered before eligible comparison with a fixed source snapshot, public commit custody, a named physical branch, and a fixed decision rule.',
    },
    {
        tier: 'calibration',
        label: 'Calibration',
        description: 'Closed public numeric output on the declared calibration surface.',
    },
    {
        tier: 'continuation-only',
        label: 'Continuation-Only',
        description: 'A downstream lane that sharpens an object not established by the theorem surface.',
    },
    {
        tier: 'compare-only',
        label: 'Compare-Only',
        description: 'A validation sidecar or exact-fit slice that does not replace the public theorem object.',
    },
    {
        tier: 'open',
        label: 'Not derived',
        description: 'The declared corpus supplies no theorem object, physical bridge, or required simulator evidence.',
    },
    {
        tier: 'exploratory',
        label: 'Exploratory',
        description: 'A simulator or diagnostic result that is reproducible but explicitly non-evidential and does not promote a physical claim.',
    },
];

export const CURRENT_RESEARCH_STATUS = [
    {
        "tier": "structural",
        "label": "Exact source structure",
        "summary": "More than 10,800 machine-checked theorem and lemma declarations support the finite theory. Protected records, the continuous rank-three metric carrier and conditional gauge classification have explicit assumptions and independently inspectable proofs."
    },
    {
        "tier": "branch-conditional",
        "label": "Controlled continuum comparisons",
        "summary": "A declared source-record family approaches flat causal order and volume. A specified free scalar action on prepared addresses has a joint spatial/time detector limit and a resolved finite error bound. A separate 64-site execution supports an inferred action clock and quantum comparisons over its time intervals."
    },
    {
        "tier": "branch-conditional",
        "label": "Physical interpretation",
        "summary": "Population, reading law, action and relative time scale are stated inputs. Physical preparation, calibrated clocks, regional interpretation and interacting continuum require separate arguments. The inferred action clock is conditional on the supplied stationary action."
    }
];

export const SPACETIME_PUBLIC_ROWS: PublicRow[] = [
    {
        "label": "Authenticated event order",
        "value": "exact finite order",
        "tier": "structural",
        "note": "Actual read-from dependencies define a finite partial order. Its height is the attained longest authenticated-parent-chain length. This combinatorial coordinate alone does not identify physical duration."
    },
    {
        "label": "Continuous source metric",
        "value": "rank three; ambient dimension four",
        "tier": "structural",
        "note": "Under the stated conservative-record and metric inputs, the source Gram quotient completes to a continuous three-dimensional Euclidean carrier. Adjoining a time coordinate gives Lorentz signature (1,3). This finite-dimensional carrier is not a finite point set or a physical event population."
    },
    {
        "label": "Source-record causal/count limit",
        "value": "declared-family continuum theorem",
        "tier": "branch-conditional",
        "note": "Golden source records form finite populations in a specified window. Complete reads within a shrinking radius, waiting and a specified layer clock produce causal order and normalized event counts approaching flat spacetime when site gaps shrink faster than that radius. Physical source selection and signal identification are additional conditions."
    },
    {
        "label": "Count clock",
        "value": "proper-duration ratios",
        "tier": "branch-conditional",
        "note": "For intervals approaching fixed interior timelike diamonds, fourth roots of record-count ratios recover proper-duration ratios. A reference interval fixes the unit. Finite root enclosures are exact arithmetic; retrospective interval access and the declared count law are required."
    },
    {
        "label": "Common free scalar field",
        "value": "resolved continuum detector response",
        "tier": "branch-conditional",
        "note": "On prepared golden addresses, a specified tensor action defines classical waves and Fock states. At q=233 and step 2^-17, the nearest update inside [0.95,1] has reference-time probability error below 0.050078 and selected split response above 0.137746 throughout that window. These bounds include spatial and temporal errors; the large tensor history is unexecuted. Action, boundary, quantization and time refinement are supplied."
    },
    {
        "label": "Action clock from field records",
        "value": "64 sites; 21 interval comparisons",
        "tier": "branch-conditional",
        "note": "A separate 64-site execution retains 5,888 writes and 34,944 reads. Its configuration records and supplied stationary action identify one duration per whole layer. With a declared error budget and a hidden common stationary-history hypothesis, 15 of 21 quantum comparisons resolve a response throughout the inferred time intervals. Physical seconds, observed outcomes and the q=233 preparation are separate."
    },
    {
        "label": "Einstein relation",
        "value": "conditional tensor theorem",
        "tier": "branch-conditional",
        "note": "Nine supplied directional balances, tensor symmetry, Ward/Bianchi conservation and connectedness imply an Einstein-form identity. Physical stress, coupling and either controlled tensor-curvature convergence or the independent continuum null-balance identification are additional premises."
    }
];

export const SIMULATION_FRONTIER = [
    {
        "label": "Source records and causal geometry",
        "status": "declared law / authenticated records",
        "summary": "Finite golden source populations carry exact read/write histories. Their continuum theorem controls causal order and counts under its window, radius and clock assumptions; finite fixture statistics are separate from that analytic limit."
    },
    {
        "label": "Classical and quantum scalar detectors",
        "status": "specified common action / certified comparison",
        "summary": "A compact preparation and separated detector share one free scalar action. The q=233 packet bounds spatial and temporal errors below its signal without executing a large history. A separate 64-site record history supports an action-clock comparison; its preparation and clock bounds do not transfer to q=233."
    },
    {
        "label": "Observer-frame quantum statistics",
        "status": "declared instruments / finite replay",
        "summary": "Exact finite contexts reproduce their committed Born weights and conditioned repeatability. The operation and weights are supplied; the receipt verifies the readout and conditioning."
    },
    {
        "label": "Self-reading visualization data",
        "status": "separate evidence scopes",
        "summary": "The visualization handoff groups local port states, records, repairs, field preparations and detectors by actual shared data. Display references and independent model clocks retain their own labels."
    }
];

export const CORE_PARAMETERS = [
    {
        label: 'Local pixel-map closure',
        value: 'a_cell ~ 1.63 l_P^2',
        equation: 'P* = phi + sqrt(pi) / A_T(P*)',
        note: 'Each declared map has one certified root. Physical calibration also requires target-independent map selection, a same-quantity bridge, and endpoint transport.',
    },
    {
        label: 'Global capacity closure boundary',
        value: 'no source-selected N',
        equation: 'N = log M0(U_N)',
        note: 'Self-reference forces equality after both sides are identified as the same typed invariant. An exact bounded generation-register counterfamily is non-identifying, while universal A1–A3 membership is unproved. Direct N is not evaluable and emits no cosmic value. Conditional finite-presence and Poisson reserve formulas are target-exposed retrospective comparisons.',
    },
];

export const BOSON_PUBLIC_ROWS: PublicRow[] = [
    {
        label: 'W calibration coordinate',
        value: '80.377 GeV',
        tier: 'compare-only',
        note: 'The displayed calibration coordinate consumes the comparison pair. The strict-one-loop map from complete renormalized inputs to a complex pole is checked, but the separate source chart near 80.330 GeV lacks the OPH/FJ identity, tadpole conversion, matching, independent gauge/BRST engine, covariance, amplitudes, and clock required for a physical comparison.',
    },
    {
        label: 'Z calibration coordinate',
        value: '91.1879781 GeV',
        tier: 'compare-only',
        note: 'The displayed calibration coordinate consumes the comparison pair. A separate source chart near 91.119 GeV gives a running-chart coordinate. Its physical pole interpretation requires the OPH-native renormalized inputs and evidence receipts used by the checked strict map kernel.',
    },
    {
        label: 'H',
        value: '125.199530 GeV',
        tier: 'calibration',
        note: 'Public row carried by the source-only Higgs/top split surface. The exact inverse adapter is a check.',
    },
    {
        label: 't',
        value: '172.352355 GeV',
        tier: 'calibration',
        note: 'Public row carried by the same source-only Higgs/top split surface, not by the inverse check surface.',
    },
];

export const PARTICLE_LANE_STATUS = [
    {
        label: 'Structural carriers',
        summary: 'Photon, gluons, and graviton have exact structural zero on the public surface.',
    },
    {
        label: 'Quarks',
        summary: 'The source equations leave a free (R>0)^2 spread fiber, so no numeric quark prediction is emitted. No physical flavor-orbit selector, quark-Higgs carrier, or common-scheme transport is derived.',
    },
    {
        label: 'Charged leptons',
        summary: 'The icosahedral screen supplies an exact A5/C3 face-corner carrier. The finite CFQ model proves its stipulated schema is nonempty but authors the registers, automaton, clock, and response. It derives no physical source selection, family/Yukawa attachment, determinant descent, interacting refinement, or pole scheme; no nonzero source-only mass is emitted.',
    },
    {
        label: 'Neutrinos',
        summary: 'The isotropic ansatz has an exact no-go. The target-informed weighted-cycle point is a rejected comparison candidate; no source-closed physical PMNS matrix, ordering, absolute mass family, or Majorana pair is emitted.',
    },
    {
        label: 'Hadrons',
        summary: 'Hadron masses sit outside the closed public scope until a working OPH backend and production systematics exist.',
    },
    {
        label: 'Capacity-electroweak bridge',
        summary: 'The measured-endpoint coordinate N_EW(P_C)=3.5323546226929907e122 and source-forward N0(P_fwd)=3.532131543418936e122 are distinct. The finite-presence and Poisson rows give 3.292097877326465e122 and 3.300072225377652e122, with retrospective residuals of -0.6287% and -0.3880%. Exact neutral and multiplicative completions share the local survival datum and the declared positive composition rules but have different global effects. The declared finite-cut attachment class selects neither action nor a blocked-event semantics. The named-law branch is not evaluable on this class, its horizon branch has no source-selected positive capacity carrier, and neither value is predictive. A positive branch requires a stronger target-independent source law.',
    },
];

export const GRAVITY_SURFACE = [
    'Authenticated dependencies give an exact finite order and longest-chain height. Conservative source records and their metric complete to a continuous rank-three carrier; its Lorentz extension is a space of possible event coordinates.',
    'On a specified golden source population, complete local reads and a model layer clock approach flat causal order and volume when the read radius shrinks more slowly than the site gaps. Fourth roots of counts in fixed interior timelike intervals recover duration ratios.',
    'An exact order embedding is one reconstruction route. A deterministic controlled limit with vanishing order error and a count-to-volume law is another; it does not require a Poisson law by definition. Physical population selection, signal propagation, clock and volume identification remain distinct hypotheses.',
    'A specified free scalar action on prepared addresses has a joint spatial/time detector limit. Compact preparations have vanishing induced detector response before continuum arrival in that limit. A separate finite field history admits an action clock; neither result identifies field-read ancestry with the causal-count law or supplies physical clock calibration.',
    'A separate exact finite theorem reduces nine supplied source-direction balances in a supplied 3+1 tensor interface to an Einstein-form shape after Ward/Bianchi conservation and connectedness. Smooth Einstein promotion needs stress and coupling plus either same-family tensor-curvature convergence or the independent continuum small-ball/null-balance identification; scalar-curvature convergence alone is diagnostic.',
    'Lorentz kinematics is recovered on the explicit BW scaling branch from the screen identity Conf+(S^2) = SO+(3,1).',
    'The Jacobson-type Einstein relation is local and branch-conditional. It uses the null-modular bridge, the separate bounded-interval projective branch, and fixed-cap generalized-entropy stationarity.',
    'Collar recovery has two routes: exact zero CMI on the declared central-interface branch, or a conditional finite-range Gibbs theorem requiring uniform strong conditional matrix mixing.',
    'On the conditional route, I(A_delta:D_delta|B_delta) <= c |partial C|_UV exp(-delta/xi), and vanishing requires delta/xi - log|partial C|_UV -> +infinity. The ratio delta/l_UV -> infinity and ordinary two-point clustering are both insufficient.',
    'Finite CMI and matrix-defect receipts are finite proxies for the collar branch. Scalar CMI is not the rank-two stress tensor or a dark-sector source.',
    'Null data fix the tensor only up to the null-invisible metric term. An exact bounded generation-register counterfamily is non-identifying, while universal A1–A3 membership is unproved. Direct N is not evaluable and emits no cosmic value. Closing the metric term requires a source-selected positive capacity carrier, a same-invariant bridge, and horizon-record saturation.',
    'The UV/BW scaffold is the realized cap-pair extraction plus ordered cut-pair rigidity on the extracted prime geometric subnet.',
];

export const STANDARD_MODEL_SURFACE = [
    'The complete compact response clause and endogenous carrier transport force the abstract Lie type u(1) + su(2) + su(3). No source reconstruction of the complete current is derived.',
    'Inside the declared fifteen-state representation fixture, the hypercharges, anomalies, Nc = 3, and common Z6 kernel are exact. No physical matter selection or same-source global quotient is derived.',
    'The CP-capability and weak-sector clauses give the window 3 <= Ng <= 5; they do not select a count inside it, and Ng = 3 enters as a declared completion. Physical three-family status requires the rank-45 attachment, source-selected matter action, and quantum-field-theory construction.',
    'The product adjoint excludes the ordinary simple-GUT X/Y channel, not every proton-decay mechanism.',
    'Coupling unification is geometric on the published edge-running surface. The published surface uses no simple-group GUT embedding or superpartners.',
    'The committed charged-current dictionary derives the W-direction shift algebra and g/sqrt(2) normalization inside the declared carrier. It supplies no physical current operator, W propagator, decay amplitude, Fermi limit, flavor, or mixing matrix.',
    'A declared local Standard Model action on flat spacetime includes gauge fields, anticommuting fermions, the Higgs field and all three Yukawa couplings. Exact first- and second-jet Ward identities and analytic currents are checked. Spacetime, Spin convention, coefficients and field content are supplied; source production and interacting quantization are separate.',
];

export const CONSENSUS_HIGHLIGHTS = [
    'Accepted local repairs strictly lower the inconsistency potential Phi on the overlaps they touch.',
    'On the finite patch net, that local-fit contract makes Phi a Lyapunov functional for the repair dynamics.',
    'The fixed-cutoff union-collar gluing theorem makes overlapping accepted repairs quotient-locally compatible.',
    'Under repair completeness, each fixed initial quotient state has a unique schedule-independent normal form.',
    'Cross-source agreement for states with the same protected observation is a separate obligation: the observation map must identify the consistent quotient modulo the declared silent or gauge equivalence.',
    'Weak normalization supplies endpoint existence; settlement under every allowed schedule requires fairness, strong normalization, or another liveness argument.',
    'Global inconsistency is a holonomy problem. Pairwise agreement can leave a nontrivial cycle obstruction.',
    'Separated refinement systems carry normal-form and holonomy classes through coarse-graining when the square defects are controlled.',
    'Stable records live on the fixed-cutoff record algebra, with exact central projectors or explicitly controlled approximately commuting surrogates.',
    'Law-space selection is presented as a meta-model over reconciliation laws. The stated claim is narrower than a literal cosmological evolution story.',
    'At the committed operator/record interface, diagonal records embed by a star homomorphism, while the declared projection is a positive unital trace-preserving expectation and is not multiplicative. Stronger categorical grades are not classified.',
    'Exact finite universality precursors exist, but no fixed-federation, all-schedule repair-universality theorem with immutable inputs and overhead/stability bounds is claimed.',
];

export const MICROPHYSICS_HIGHLIGHTS = [
    'A spherical screen is a regulator chart for observer-facing cuts, not a literal spherical quantum computer.',
    'Federated echosahedral patch carriers expose multi-port overlap data, records, repair instruments, and synchronization interfaces.',
    'Measurement, stable records, checkpoint/restoration, and observer synchronization live inside one shared microscopic model.',
    'Toroidal subchannels supply local recurrence and winding-sensitive dynamics inside bounded patches.',
    'Hardware evidence counts only through public bundles with stable hashes, calibration records, controls, and verifier receipts.',
    'The committed finite Maxwell update proves conditional identities, continuity, and a conserved staggered quadratic form, but the form is not proved positive and exact modes exceed the unit-step stability threshold. No stable calibrated propagation theorem is supplied.',
];

export const PREDICTION_SURFACE = {
    primitivePortPrediction: {
        title: 'Primitive twelve-port degree-six propagation test',
        tier: 'frozen-prospective' as ClaimTier,
        summary: 'The named physical branch uses a real, reciprocal, finite-range cosine kinetic operator whose complete primitive twelve-port orbit is the sole hop support, with no independent kinetic term through the displayed order. Proper-carrier covariance fixes equal weights. Intrinsic anisotropic ranks j = 1 through 5 vanish. Rank j = 6 has the unique icosahedral shape up to SO(3)/A5 orientation, where A5 is the sixty-element proper icosahedral rotation group.',
        coefficients: 'C4 = -a^2/20, B0 = a^4/840, B6 = 2a^4/7875; B6/C4^2 = 32/315, B0/C4^2 = 10/21, B6/B0 = 16/75.',
        boundary: 'The certified repair operator acts on internal seams. It does not define spatial hops, a physical readout, or a laboratory frame. Exact propagation calculations also admit distinct vertex, face, and edge orbit rays, so symmetry equalizes weights inside each orbit without selecting the primitive-port ray. No scalar or polarization-independent sector bridge, coherent frame transport, or exclusivity theorem is derived. A photon test also requires equal action on both transverse polarizations. The excluded exposure class is the 17 July 2026 WMAP ILC template campaign, its CMB likelihood class, and every inspected data product; its template-only null has no role in this comparison. The linked coefficient relation has no qualifying physical comparison. The comparison is unarmed until its own versioned eligible contract fixes the source operator, readout, frame, covariance, nuisance model, sensitivity, and thresholds. Failure rejects this branch and reaches the full framework only if the bridge derivation proves the branch forced and exclusive.',
    },
    distinctiveTemplates: [
        {
            title: 'GW horizon spectroscopy comb',
            tier: 'continuation-only' as ClaimTier,
            summary: 'A continuation-level horizon-area template with line positions x_k = ln(k)/(8pi). The alpha = 4 or one-nat headline belongs to a rejected uniform-offset branch.',
        },
        {
            title: 'Discrete Hawking spectrum',
            tier: 'continuation-only' as ClaimTier,
            summary: 'The discrete-line Hawking picture is carried only if the extra integer-transition selection rule is realized. The paper labels it a continuation-level template.',
        },
        {
            title: 'Deep-IR MOND/RAR response',
            tier: 'open' as ClaimTier,
            summary: 'The benchmark a0 scale is numerically suggestive. The paper does not derive a galaxy-dynamics law or promote a MOND/RAR response functional.',
        },
    ],
    nullExpectations: [
        {
            title: 'No primitive-port anisotropy at angular ranks one through five',
            summary: 'The named equal-weight physical propagation branch puts its first intrinsic directional term at rank six. Spin six is angular rank, unrelated to particle spin.',
        },
        {
            title: 'No ordinary simple-GUT X/Y channel',
            summary: 'The product adjoint blocks the classic X/Y leptoquark route; other baryon-violating mechanisms are separate.',
        },
        {
            title: 'No simple-group GUT is needed for the published unification surface',
            summary: 'The coupling story is geometric on the published edge-running lane. The lab should not imply a hidden SU(5)-style embedding.',
        },
        {
            title: 'No supersymmetry is required by the public edge-shift derivation',
            summary: 'The published beta-shift surface reproduces MSSM-like running behavior without introducing a superpartner sector.',
        },
        {
            title: 'Source-derived ambient 1+3 Lorentz precursor',
            summary: 'The exact rank-three source quotient independently defines the four-dimensional (+---) ambient target carrier R ⊕ V_src. Exact longest-chain height is not part of that carrier construction. Every finite log has an auxiliary injective forward-causal placement; it is enumeration-dependent and does not reflect the order. The carrier is not an intrinsic poset-dimension estimate, and the physical manifold limit is conditional.',
        },
    ],
    falsificationPressure: [
        'Under an eligible contract, a positive intrinsic C4, a nonzero intrinsic coefficient at angular rank one through five, or exclusion of the linked B0/B6 ratios or rigid rotated degree-six shape at five or more standard deviations, after the fixed SO(3)/A5 orientation profile and with calibrated joint coverage, rejects the primitive-port physical propagation branch. Null and underpowered outcomes are inconclusive.',
        'Support requires exclusion of the zero-coefficient minimal Standard Model plus General Relativity baseline at five or more standard deviations, agreement with the linked branch within two standard deviations, rejection of named systematic alternatives, and replication in an independent eligible release.',
        'Observation of the ordinary simple-GUT X/Y channel or a different realized gauge quotient would pressure the corresponding declared branch.',
        'W/Z data become a physical pressure test only after OPH supplies the inputs to the checked strict-one-loop pole kernel: an FJ renormalized vev and tadpole conversion, thresholds and matching, independent gauge/BRST evidence, source covariance, amplitudes, and a clock.',
        'A fully derived dark-sector particle explanation would conflict with the gravity-side interpretation; the galaxy-response hypothesis requires its physical source and attachment.',
        'Ringdown data can test and pressure the conditional horizon-comb template.',
    ],
};
