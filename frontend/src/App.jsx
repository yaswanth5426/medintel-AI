import './index.css';

import {
  BrowserRouter,
  Route,
  Routes,
} from 'react-router-dom';

import Disclaimer from './components/Disclaimer';
import Navbar from './components/Navbar';
import Chat from './pages/Chat';
import Dashboard from './pages/Dashboard';
import Home from './pages/Home';
import UploadReport from './pages/UploadReport';

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/upload" element={<UploadReport />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
      <Disclaimer />
    </BrowserRouter>
  );
}