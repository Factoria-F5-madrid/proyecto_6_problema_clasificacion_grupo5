// client/src/components/Nav.jsx
import React from "react";
import { NavLink } from "react-router-dom";


/*
 Nav component: shows brand + navigation links.
 Uses a distinct logo font for the brand (see index.css for font import).
*/
export default function Nav() {
  return (
    <header className="nav">
      <div className="nav-inner">
        {/* Brand: stylized font for identity */}
        <div className="brand">
          <span className="brand-logo">You &amp; Airveryone</span>
          <span className="brand-slogan">For a better flight for you &amp; Airveryone</span>
        </div>

        {/* Navigation links */}
        <nav className="nav-links">
          <NavLink to="/" end className={({isActive}) => isActive ? "active" : ""}>Home</NavLink>
          <NavLink to="/database" className={({isActive}) => isActive ? "active" : ""}>Database</NavLink>
          <NavLink to="/predict" className={({isActive}) => isActive ? "active" : ""}>Predict</NavLink>
          <NavLink to="/team" className={({isActive}) => isActive ? "active" : ""}>Team</NavLink>
        </nav>
      </div>
    </header>
  );
}
