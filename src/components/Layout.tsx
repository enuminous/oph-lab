import { useState, useEffect } from 'react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import './Layout.css';
import { WALKTHROUGH_STEPS, PART_LABELS, PART_COLORS, type PartId } from '../routes/walkthrough';
import { WalkthroughNav } from './WalkthroughNav';
import { installLinkTracking, trackPageView } from '../lib/analytics';
import { SeoManager } from './SeoManager';
import { getSeoMeta } from '../seo';
import { BLOG_URL, CHALLENGE_URL, FLAGSHIP_PHILPAPERS_URL, MINI_UNIVERSE_SIMULATION_URL, OVERVIEW_URL, PHYSICS_UNIFICATION_URL, RESEARCH_LICENSE_URL, RESEARCH_PATENT_POLICY_URL, RESEARCH_RELEASE_DATE, RESEARCH_RELEASE_ID, RESEARCH_REPO_URL, SIMULATION_URL, TEXTBOOKS_URL, THEORY_URL } from '../content/paperSurface';

export function Layout() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const location = useLocation();
    const normalizedPath = location.pathname.replace(/\/$/, '') || '/';
    const isLandingSurface = normalizedPath === '/';

    useEffect(() => {
        const title = getSeoMeta(normalizedPath).title;
        trackPageView(normalizedPath, title);
    }, [normalizedPath]);

    useEffect(() => installLinkTracking('oph_lab'), []);

    // Group steps by part
    const parts = new Map<PartId, typeof WALKTHROUGH_STEPS>();
    for (const step of WALKTHROUGH_STEPS) {
        const list = parts.get(step.part) ?? [];
        list.push(step);
        parts.set(step.part, list);
    }

    return (
        <div className="layout">
            <SeoManager />
            <aside className={`sidebar ${isMobileMenuOpen ? 'open' : ''}`}>
                <div className="sidebar-header">
                    <a href="https://floatingpragma.io/" className="back-link">&larr;</a>
                    <span className="logo">OPH Lab</span>
                    <button
                        className="close-btn mobile-only"
                        onClick={() => setIsMobileMenuOpen(false)}
                    >
                        <X size={24} />
                    </button>
                </div>

                <nav className="nav">
                    {Array.from(parts.entries()).map(([partId, steps]) => (
                        <div key={partId} className="nav-group">
                            <div
                                className="nav-group-label"
                                style={{ color: PART_COLORS[partId] }}
                            >
                                {PART_LABELS[partId]}
                            </div>
                            {steps.map((item) => (
                                <NavLink
                                    key={item.to}
                                    to={item.to}
                                    end={item.to === '/'}
                                    className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                                    onClick={() => setIsMobileMenuOpen(false)}
                                >
                                    <item.icon size={16} />
                                    <span>{item.label}</span>
                                </NavLink>
                            ))}
                        </div>
                    ))}
                </nav>

                <div className="sidebar-snapshot">
                    <span>Research snapshot</span>
                    <strong>{RESEARCH_RELEASE_ID}</strong>
                    <small>{RESEARCH_RELEASE_DATE}</small>
                </div>
            </aside>

            <div className="main-content">
                <header className="mobile-header">
                    <button
                        className="menu-btn"
                        onClick={() => setIsMobileMenuOpen(true)}
                    >
                        <Menu size={24} />
                    </button>
                    <span className="logo" style={{ marginLeft: '16px' }}>OPH Lab</span>
                </header>

                <main className="content-scroll">
                    <div className={`content-container ${isLandingSurface ? 'content-container-wide' : ''}`}>
                        <Outlet />
                        <WalkthroughNav />

                        <footer style={{
                            marginTop: '64px',
                            paddingTop: '32px',
                            borderTop: '1px solid var(--border-color)',
                            textAlign: 'center',
                            color: 'var(--text-muted)',
                            fontSize: '0.85em'
                        }}>
                            <p>
                                <a href="https://floatingpragma.io/" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Floating Pragma</a>
                                {' \u2022 '}
                                <a href={OVERVIEW_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>OPH Overview</a>
                                {' \u2022 '}
                                <a href={BLOG_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Blog</a>
                                {' \u2022 '}
                                <a href={THEORY_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Theory of Everything</a>
                                {' \u2022 '}
                                <a href={PHYSICS_UNIFICATION_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Physics Unification</a>
                                {' \u2022 '}
                                <a href={SIMULATION_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Simulation Theory</a>
                                {' \u2022 '}
                                <a href={MINI_UNIVERSE_SIMULATION_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Mini-Universe Simulation</a>
                                {' \u2022 '}
                                <a href={TEXTBOOKS_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Textbooks</a>
                                {' \u2022 '}
                                <a href={CHALLENGE_URL} style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Challenge</a>
                                {' \u2022 '}
                                <a href={RESEARCH_LICENSE_URL} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>License</a>
                                {' \u2022 '}
                                <a href={RESEARCH_PATENT_POLICY_URL} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Anti-Patent</a>
                                {' \u2022 '}
                                <a href="https://floatingpragma.io/starklab/" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>STARK Lab</a>
                                {' \u2022 '}
                                <a href="https://floatingpragma.io/selected-works/" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Selected Works</a>
                                {' \u2022 '}
                                <a href="https://floatingpragma.io/awesome-zk-proofs/" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>ZK Proofs</a>
                                {' \u2022 '}
                                <a href="https://floatingpragma.io/awesome-ai-security/" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>AI Security</a>
                            </p>
                            <p style={{ marginTop: '8px' }}>
                                Bernhard Mueller
                                {' \u2022 '}
                                <a href={RESEARCH_REPO_URL} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Research Repo</a>
                                {' \u2022 '}
                                <a href={FLAGSHIP_PHILPAPERS_URL} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-gold)', textDecoration: 'none' }}>Paper (PhilPapers)</a>
                            </p>
                        </footer>
                    </div>
                </main>
            </div>
        </div>
    );
}
