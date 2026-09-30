import {
    BookOpen,
    Lightbulb,
    Eye,
    Globe,
    Shield,
    Flame,
    Link,
    Orbit,
    Clock,
    Apple,
    Telescope,
    Moon,
    Atom,
    Zap,
    Lock,
    Layers,
    Box,
    Scale,
    Merge,
    GitBranch,
    Cpu,
    Target,
    Infinity as InfinityIcon,
    Search,
    Library,
    type LucideIcon,
} from 'lucide-react';

export type PartId = 'foundation' | 'chain1-gr' | 'chain2-qft' | 'observer-machinery' | 'predictions' | 'reference';

export type WalkthroughStep = {
    to: string;
    label: string;
    icon: LucideIcon;
    part: PartId;
};

export const PART_LABELS: Record<PartId, string> = {
    'foundation': 'Foundation',
    'chain1-gr': 'Chain 1: Axioms \u2192 General Relativity',
    'chain2-qft': 'Chain 2: Axioms \u2192 Quantum Field Theory',
    'observer-machinery': 'Consensus & Observers',
    'predictions': 'Predictions & Synthesis',
    'reference': 'Reference',
};

export const PART_COLORS: Record<PartId, string> = {
    'foundation': 'var(--accent-gold)',
    'chain1-gr': 'var(--accent-rose)',
    'chain2-qft': 'var(--accent-blue)',
    'observer-machinery': 'var(--accent-purple)',
    'predictions': 'var(--accent-green)',
    'reference': 'var(--text-muted)',
};

export const WALKTHROUGH_STEPS: WalkthroughStep[] = [
    // Foundation
    { to: '/', icon: BookOpen, label: 'Research Status', part: 'foundation' },
    { to: '/hints/', icon: Lightbulb, label: 'Five Hints', part: 'foundation' },
    { to: '/no-objective-reality/', icon: Eye, label: 'Observer-Local Reality', part: 'foundation' },
    { to: '/the-screen/', icon: Globe, label: 'The Holographic Screen', part: 'foundation' },
    { to: '/axioms/', icon: Shield, label: 'The Three Axioms', part: 'foundation' },

    // Chain 1: Axioms -> General Relativity
    { to: '/entropy/', icon: Flame, label: 'Entropy & Area Bound', part: 'chain1-gr' },
    { to: '/entanglement-geometry/', icon: Link, label: 'Entanglement \u2192 Geometry', part: 'chain1-gr' },
    { to: '/lorentz/', icon: Orbit, label: 'Lorentz from the Screen', part: 'chain1-gr' },
    { to: '/modular-flow/', icon: Clock, label: 'Time from Modular Flow', part: 'chain1-gr' },
    { to: '/gravity/', icon: Apple, label: 'Gravity from Entanglement', part: 'chain1-gr' },
    { to: '/de-sitter/', icon: Telescope, label: 'The de Sitter Universe', part: 'chain1-gr' },
    { to: '/dark-matter/', icon: Moon, label: 'Dark-Sector Benchmark', part: 'chain1-gr' },
    { to: '/classical-physics/', icon: Orbit, label: 'Classical Limits', part: 'chain1-gr' },

    // Chain 2: Axioms -> QFT
    { to: '/quantum-mechanics/', icon: Atom, label: 'QM in OPH', part: 'chain2-qft' },
    { to: '/entanglement/', icon: Zap, label: 'Bell & Entanglement', part: 'chain2-qft' },
    { to: '/error-correction/', icon: Lock, label: 'Quantum Error Correction', part: 'chain2-qft' },
    { to: '/gauge-symmetry/', icon: Layers, label: 'Gauge from Gluing', part: 'chain2-qft' },
    { to: '/standard-model/', icon: Box, label: 'Standard Model Structure', part: 'chain2-qft' },
    { to: '/masses/', icon: Scale, label: 'Matter Continuations', part: 'chain2-qft' },
    { to: '/neutrinos/', icon: Atom, label: 'Neutrino Audit', part: 'chain2-qft' },
    { to: '/unification/', icon: Merge, label: 'Coupling Unification', part: 'chain2-qft' },
    { to: '/qft-emerges/', icon: Atom, label: 'QFT Boundary', part: 'chain2-qft' },

    // Consensus & observer machinery
    { to: '/consensus-protocol/', icon: GitBranch, label: 'Consensus Protocol', part: 'observer-machinery' },
    { to: '/screen-microphysics/', icon: Cpu, label: 'Screen Microphysics', part: 'observer-machinery' },

    // Predictions & Synthesis
    { to: '/predictions/', icon: Target, label: 'Prediction Registry', part: 'predictions' },
    { to: '/synthesis/', icon: InfinityIcon, label: 'OPH Synthesis', part: 'predictions' },

    // Reference
    { to: '/glossary/', icon: Search, label: 'Glossary', part: 'reference' },
    { to: '/resources/', icon: Library, label: 'Further Reading', part: 'reference' },
];
