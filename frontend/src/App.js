// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HRPageOne from './Components/HRPageOne';
import HRPageTwo from './Components/HRPageTwo';
import HRPageThree from './Components/ApplierPage';

const App = () => {
  return (
    <Router>
      <div >
        <nav >
          <Link to="/page1" className="mr-4 text-blue-600 font-semibold">HR Dashboard - Page 1</Link>
          <Link to="/page2" className="text-blue-600 font-semibold">HR Dashboard - Page 2</Link>
          <Link to="/page4" className="text-blue-600 font-semibold">Candidate Manager</Link>

        </nav>

        <Routes>
          <Route path="/page1" element={<HRPageOne />} />
          <Route path="/page2" element={<HRPageTwo />} />
          <Route path="/page4" element={<HRPageThree />} /> {/* 👈 New route for HRPageThree */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;