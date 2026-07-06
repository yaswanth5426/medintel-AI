import './Navbar.css';

import { NavLink } from 'react-router-dom';

const links = [
  { to: "/", label: "Home" },
  { to: "/chat", label: "Chat" },
  { to: "/upload", label: "Upload" },
  { to: "/dashboard", label: "Dashboard" },
];

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-brand">
        <span className="signal" />
        <span>MedIntel</span>
      </div>
      <nav className="navbar-links">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.to === "/"}
            className={({ isActive }) =>
              isActive ? "navbar-link active" : "navbar-link"
            }
          >
            {l.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}