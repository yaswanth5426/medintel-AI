import './Navbar.css';

import { NavLink } from 'react-router-dom';
import {
  HiOutlineChartBar,
  HiOutlineChatBubbleLeftRight,
  HiOutlineDocumentArrowUp,
  HiOutlineHome,
} from 'react-icons/hi2';

const links = [
  { to: "/", label: "Home", icon: HiOutlineHome },
  { to: "/chat", label: "Chat", icon: HiOutlineChatBubbleLeftRight },
  { to: "/upload", label: "Upload", icon: HiOutlineDocumentArrowUp },
  { to: "/dashboard", label: "Dashboard", icon: HiOutlineChartBar },
];

export default function Navbar() {
  return (
    <header className="navbar glass">
      <div className="navbar-brand">
        <span className="navbar-mark">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M2 12h4l2-7 4 14 2-7h8"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
        <span className="navbar-brand-text">
          MedIntel<span className="gradient-text">AI</span>
        </span>
      </div>
      <nav className="navbar-links">
        {links.map((l) => {
          const Icon = l.icon;
          return (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === "/"}
              className={({ isActive }) =>
                isActive ? "navbar-link active" : "navbar-link"
              }
            >
              <Icon className="navbar-link-icon" />
              <span>{l.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </header>
  );
}
