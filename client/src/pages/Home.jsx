// client/src/pages/Home.jsx
import React from "react";
import hero from "../assets/hero.png";

/*
 Home page: hero area + short intro + quick links to pages.
 This uses the hero image on the left (or top on small screens).
*/
export default function Home() {
  return (
    <section className="home">
      <div className="hero">
        <div className="hero-text">
          <h1 className="hero-title">You &amp; Airveryone</h1>
          <p className="hero-sub">For a better flight for you &amp; Airveryone.</p>
          <p className="lead">
            We measure passenger comfort and predict how to improve a flight experience.
            Try our demo or explore the dataset.
          </p>

          <div className="hero-ctas">
            <a href="/predict" className="btn">Try the Predictor</a>
            <a href="/database" className="btn btn-ghost">View Database</a>
          </div>
        </div>

        <div className="hero-image" aria-hidden>
          <img src={hero} alt="Passengers relaxing on a calm flight (illustration)" />
        </div>
      </div>
    </section>
  );
}
