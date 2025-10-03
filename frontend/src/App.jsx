import { Route, Routes } from "react-router-dom";
import "./App.css";
import AuthenticationPage from "./auth/AuthenticationPage";
import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes.jsx";
import {ChallengeGenerator} from "./challenge/ChallengeGenerator.jsx";
import HistoryPanel from "./history/HistoryPanel.jsx";
import Layout from "./layout/Layout.jsx";

function App() {
  return (
    <ClerkProviderWithRoutes>
      <Routes>
        <Route path="/sign-in/*" element={<AuthenticationPage />} />
        <Route path="/sign-up" element={<AuthenticationPage />} />

        <Route element={<Layout />}>
          <Route path="/" element={<ChallengeGenerator />} />
          <Route path="/history" element={<HistoryPanel />} />
        </Route>
      </Routes>
    </ClerkProviderWithRoutes>
  );
}

export default App;
