// client/src/pages/Home.jsx
import React from "react";

/*
 Home page: hero area + short intro + quick links to pages.
 This uses the hero image on the left (or top on small screens).
*/
export default function Home() {
  return (
    <section className="home">
      <div className="hero">
        {/* Bloque de texto */}
        <div className="hero-text">
          <h1 className="hero-title">
            <span className="script">You &amp; Airveryone</span>
            <br />
            <span className="bold">TRAVEL</span>
          </h1>

           <div className="cta-combined">
            <a href="/predict" className="btn start-btn">Try your predict</a>
            <span className="cta-url">www.youandairveryone.com</span>
           </div>
        </div>

        {/* Imagen del avión */}
        {/* <div className="hero-image" aria-hidden>
          <img
            src={hero}
            alt="Airplane wing flying over the clouds"
            className="hero-img"
          />
        </div> */}
      </div>
    </section>
  );
}
