// client/src/components/Footer.jsx
import React from "react";

/*
 Footer: small footer with copyright and subtle background.
*/
export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <p>© {new Date().getFullYear()} You &amp; Airveryone — Creating calmer flights</p>
      </div>
    </footer>
  );
}
