// client/src/pages/Team.jsx
import React from "react";

/*
 Team page: short bios / photos of team members.
 Replace placeholder names and descriptions with real ones.
*/
export default function Team() {
  return (
    <section className="page">
      <h2>Meet the Team</h2>
      <p>We are group 5 — building better flight comfort tools.</p>

      <div className="team-grid">
        <div className="team-card">
          <h4>Member 1</h4>
          <p>Frontend lead — UI, UX, visual design.</p>
        </div>

        <div className="team-card">
          <h4>Member 2</h4>
          <p>Backend & model integration.</p>
        </div>

        <div className="team-card">
          <h4>Member 3</h4>
          <p>Data scientist — dataset & modelling.</p>
        </div>

        <div className="team-card">
          <h4>Member 4</h4>
          <p>Project manager & testing.</p>
        </div>
      </div>
    </section>
  );
}
