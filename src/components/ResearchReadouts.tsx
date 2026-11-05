import ledger from '../../claims/claim_registry.json';

const REPO = 'https://github.com/enuminous/oph-lab/blob/main/';

/** Fork evidence only; never overwrites the upstream paper snapshot. */
export function ResearchReadouts() {
    return (
        <section className="card" aria-labelledby="fork-readouts-title" style={{ marginBottom: '24px' }}>
            <h2 id="fork-readouts-title">Independent fork: research readouts</h2>
            <p>
                Updated {ledger.updated}. Physical particle identification, the interacting quantum
                continuum, gravity and explanatory completeness remain <strong>unresolved</strong>.
                The results below describe supplied finite models and explicit proof boundaries.
            </p>
            <p>
                The October flux data are quarantined after an observable-axis defect.
                Corrected code, gauge tests and separate raw replay data are available in the{' '}
                <a href={`${REPO}docs/OPH_N2_READOUT_CORRECTION.md`}>readout correction</a>.
            </p>
            <div style={{ overflowX: 'auto' }}>
                <table>
                    <thead><tr><th>Claim</th><th>Evidence status</th><th>Scope</th></tr></thead>
                    <tbody>{ledger.claims.map(claim => (
                        <tr key={claim.id}>
                            <td><a href={`${REPO}${claim.evidence[0]}`}>{claim.title}</a></td>
                            <td>{claim.status}</td>
                            <td>{claim.scope}</td>
                        </tr>
                    ))}</tbody>
                </table>
            </div>
            <p>
                <a href={`${REPO}docs/OPH_FINITE_LATTICE_PROGRESS_AND_FORMALIZATION.md`}>Fork flagship report</a>
                {' · '}<a href={`${REPO}claims/claim_registry.json`}>Claim ledger</a>
                {' · '}<a href={`${REPO}tracking/premise_register.json`}>Open premises</a>
                {' · '}<a href={`${REPO}tracking/parallel_work_queue.md`}>Parallel work queue</a>
            </p>
        </section>
    );
}
