import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Layout } from './components/Layout';

// Foundation
import { Home } from './pages/Home';
import { HintsPage } from './pages/Hints';
import { NoObjectiveRealityPage } from './pages/NoObjectiveReality';
import { TheScreenPage } from './pages/TheScreen';
import { AxiomsPage } from './pages/Axioms';

// Chain 1: GR
import { EntropyPage } from './pages/Entropy';
import { EntanglementGeometryPage } from './pages/EntanglementGeometry';
import { LorentzPage } from './pages/Lorentz';
import { ModularFlowPage } from './pages/ModularFlow';
import { GravityPage } from './pages/Gravity';
import { DeSitterPage } from './pages/DeSitter';
import { DarkMatterPage } from './pages/DarkMatter';
import { ClassicalPhysicsPage } from './pages/ClassicalPhysics';

// Chain 2: QFT
import { QuantumMechanicsPage } from './pages/QuantumMechanics';
import { EntanglementPage } from './pages/Entanglement';
import { ErrorCorrectionPage } from './pages/ErrorCorrection';
import { GaugeSymmetryPage } from './pages/GaugeSymmetry';
import { StandardModelPage } from './pages/StandardModel';
import { MassesPage } from './pages/Masses';
import { NeutrinosPage } from './pages/Neutrinos';
import { UnificationPage } from './pages/Unification';
import { QftEmergesPage } from './pages/QftEmerges';
import { ConsensusProtocolPage } from './pages/ConsensusProtocol';
import { ScreenMicrophysicsPage } from './pages/ScreenMicrophysics';

// Predictions & Reference
import { PredictionsPage } from './pages/Predictions';
import { SynthesisPage } from './pages/Synthesis';
import { GlossaryPage } from './pages/Glossary';
import { ResourcesPage } from './pages/Resources';

function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="hints" element={<HintsPage />} />
          <Route path="no-objective-reality" element={<NoObjectiveRealityPage />} />
          <Route path="the-screen" element={<TheScreenPage />} />
          <Route path="axioms" element={<AxiomsPage />} />

          <Route path="entropy" element={<EntropyPage />} />
          <Route path="entanglement-geometry" element={<EntanglementGeometryPage />} />
          <Route path="lorentz" element={<LorentzPage />} />
          <Route path="modular-flow" element={<ModularFlowPage />} />
          <Route path="gravity" element={<GravityPage />} />
          <Route path="de-sitter" element={<DeSitterPage />} />
          <Route path="dark-matter" element={<DarkMatterPage />} />
          <Route path="classical-physics" element={<ClassicalPhysicsPage />} />

          <Route path="quantum-mechanics" element={<QuantumMechanicsPage />} />
          <Route path="entanglement" element={<EntanglementPage />} />
          <Route path="error-correction" element={<ErrorCorrectionPage />} />
          <Route path="gauge-symmetry" element={<GaugeSymmetryPage />} />
          <Route path="standard-model" element={<StandardModelPage />} />
          <Route path="masses" element={<MassesPage />} />
          <Route path="neutrinos" element={<NeutrinosPage />} />
          <Route path="unification" element={<UnificationPage />} />
          <Route path="qft-emerges" element={<QftEmergesPage />} />
          <Route path="consensus-protocol" element={<ConsensusProtocolPage />} />
          <Route path="screen-microphysics" element={<ScreenMicrophysicsPage />} />

          <Route path="predictions" element={<PredictionsPage />} />
          <Route path="synthesis" element={<SynthesisPage />} />
          <Route path="glossary" element={<GlossaryPage />} />
          <Route path="resources" element={<ResourcesPage />} />
          <Route path="*" element={
            <section aria-labelledby="not-found-title">
              <h1 id="not-found-title">Page not found</h1>
              <p>The requested lesson does not exist. Choose a lesson from the navigation or return to the overview.</p>
              <Link to="/" className="btn btn-primary">Back to OPH Lab</Link>
            </section>
          } />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
