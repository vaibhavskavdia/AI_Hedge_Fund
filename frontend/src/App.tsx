import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";

import PortfolioPage from "./features/portfolio/PortfolioPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<PortfolioPage />} />

          <Route path="/research" element={<div>Research</div>} />

          <Route path="/stocks" element={<div>Stock Intelligence</div>} />

          <Route path="/sectors" element={<div>Sector Intelligence</div>} />

          <Route path="/risk" element={<div>Risk</div>} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;